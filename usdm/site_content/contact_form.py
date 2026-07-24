import logging
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .models import ContactAttachment, ContactRequest


FORM_ANCHOR = "contact-form"
STATE_KEY = "contact_form_state"
MAX_FILES = 10
MAX_TOTAL_UPLOAD_BYTES = 25 * 1024 * 1024
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "xls", "xlsx", "jpg", "jpeg", "png", "webp",
    "zip", "dwg", "dxf", "ifc",
}
logger = logging.getLogger(__name__)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        uploads = data if isinstance(data, (list, tuple)) else ([data] if data else [])
        return [forms.FileField.clean(self, upload, initial) for upload in uploads]


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=80)
    message = forms.CharField(max_length=2000, widget=forms.Textarea)
    files = MultipleFileField(required=False)
    privacy = forms.BooleanField(required=True)
    website = forms.CharField(required=False)

    def __init__(self, *args, invalid_fields=(), **kwargs):
        super().__init__(*args, **kwargs)
        invalid_fields = set(invalid_fields)
        field_settings = {
            "first_name": (_("Ваше ім’я *"), "given-name"),
            "last_name": (_("Ваше прізвище"), "family-name"),
            "email": (_("Ваш email *"), "email"),
            "phone": (_("Ваш телефон *"), "tel"),
            "message": (_("Ваше повідомлення або запит *"), "off"),
        }
        for name, (placeholder, autocomplete) in field_settings.items():
            field = self.fields[name]
            field.widget.attrs.update({
                "placeholder": placeholder,
                "aria-label": str(placeholder).rstrip(" *"),
                "autocomplete": autocomplete,
            })
        self.fields["message"].widget.attrs["rows"] = 4
        self.fields["files"].widget.attrs.update({
            "multiple": True,
            "accept": ".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.webp,.zip,.dwg,.dxf,.ifc",
            "aria-label": _("Вибрати файли проєкту"),
            "data-max-files": str(MAX_FILES),
            "data-max-total-size": str(MAX_TOTAL_UPLOAD_BYTES),
        })
        self.fields["website"].widget.attrs.update({
            "tabindex": "-1",
            "autocomplete": "off",
            "aria-hidden": "true",
        })
        for name, field in self.fields.items():
            classes = ["contact-control"]
            if name in invalid_fields:
                classes.append("is-invalid")
                field.widget.attrs["aria-invalid"] = "true"
            field.widget.attrs["class"] = " ".join(classes)

        self.fields["first_name"].error_messages.update({
            "required": _("Будь ласка, вкажіть ваше ім’я."),
            "max_length": _("Вказане ім’я надто довге."),
        })
        self.fields["last_name"].error_messages["max_length"] = _("Вказане прізвище надто довге.")
        self.fields["email"].error_messages.update({
            "required": _("Будь ласка, вкажіть адресу електронної пошти."),
            "invalid": _("Будь ласка, вкажіть дійсну адресу електронної пошти."),
            "max_length": _("Вказана адреса електронної пошти надто довга."),
        })
        self.fields["phone"].error_messages.update({
            "required": _("Будь ласка, вкажіть номер телефону."),
            "max_length": _("Вказаний номер телефону надто довгий."),
        })
        self.fields["message"].error_messages.update({
            "required": _("Будь ласка, напишіть повідомлення або запит."),
            "max_length": _("Повідомлення надто довге."),
        })
        self.fields["files"].error_messages.update({
            "empty": _("Один із вибраних файлів порожній."),
            "invalid": _("Один із вибраних файлів не вдалося прочитати."),
            "max_length": _("Назва одного з вибраних файлів надто довга."),
        })
        self.fields["privacy"].error_messages["required"] = _(
            "Підтвердьте згоду на обробку персональних даних."
        )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        allowed_characters = set("0123456789+()-./ ")
        digit_count = sum(character.isascii() and character.isdigit() for character in phone)
        if digit_count < 6 or any(character not in allowed_characters for character in phone):
            raise ValidationError(_("Будь ласка, вкажіть дійсний номер телефону."))
        return phone

    def clean(self):
        cleaned = super().clean()
        uploads = cleaned.get("files") or []
        if len(uploads) > MAX_FILES:
            self.add_error("files", ValidationError(_("Можна додати щонайбільше 10 файлів.")))
        if sum(upload.size for upload in uploads) > MAX_TOTAL_UPLOAD_BYTES:
            self.add_error(
                "files",
                ValidationError(_("Загальний розмір файлів не повинен перевищувати 25 МБ.")),
            )
        unsupported = next(
            (
                upload for upload in uploads
                if Path(upload.name).suffix.lower().lstrip(".") not in ALLOWED_EXTENSIONS
            ),
            None,
        )
        if unsupported:
            self.add_error(
                "files",
                ValidationError(
                    _("Формат файлу «%(name)s» не підтримується."),
                    params={"name": Path(unsupported.name).name},
                ),
            )
        return cleaned


def _client_messages():
    return {
        "first_name": str(_("Будь ласка, вкажіть ваше ім’я.")),
        "emailRequired": str(_("Будь ласка, вкажіть адресу електронної пошти.")),
        "emailInvalid": str(_("Будь ласка, вкажіть дійсну адресу електронної пошти.")),
        "phone": str(_("Будь ласка, вкажіть номер телефону.")),
        "phoneInvalid": str(_("Будь ласка, вкажіть дійсний номер телефону.")),
        "message": str(_("Будь ласка, напишіть повідомлення або запит.")),
        "privacy": str(_("Підтвердьте згоду на обробку персональних даних.")),
        "fileCount": str(_("Можна додати щонайбільше {maximum} файлів.")),
        "fileSize": str(_("Загальний розмір файлів не повинен перевищувати {maximum} МБ.")),
        "fileEmpty": str(_("Один із вибраних файлів порожній.")),
        "fileType": str(_("Формат файлу «{name}» не підтримується.")),
        "removeFile": str(_("Видалити файл {name}")),
    }


def contact_context(request):
    state = request.session.pop(STATE_KEY, {}) if hasattr(request, "session") else {}
    form = ContactForm(
        initial=state.get("values", {}),
        invalid_fields=state.get("invalid_fields", ()),
    )
    status = state.get("status", "")
    message = ""
    if status == "success":
        message = str(_("Ваш запит прийнято. Ми зв’яжемося з вами найближчим часом."))
    elif status == "failure":
        message = str(_("Не вдалося прийняти запит. Будь ласка, напишіть нам на вказану електронну адресу."))
    return {
        "contact_form": form,
        "contact_errors": state.get("field_errors", {}),
        "contact_status": {"name": status, "message": message},
        "contact_messages": _client_messages(),
    }


def _target(request, lang):
    candidate = request.POST.get("next", f"/{lang}/contact/")
    if not url_has_allowed_host_and_scheme(candidate, allowed_hosts={request.get_host()}):
        candidate = f"/{lang}/contact/"
    parts = urlsplit(candidate)
    return urlunsplit((parts.scheme, parts.netloc, parts.path or "/", parts.query, FORM_ANCHOR))


def _remember(request, status, values=None, invalid_fields=(), field_errors=None):
    request.session[STATE_KEY] = {
        "status": status,
        "values": values or {},
        "invalid_fields": list(invalid_fields),
        "field_errors": field_errors or {},
    }


def _save_request(cleaned, lang):
    with transaction.atomic():
        contact_request = ContactRequest.objects.create(
            first_name=cleaned["first_name"],
            last_name=cleaned.get("last_name", ""),
            email=cleaned["email"],
            phone=cleaned["phone"],
            message=cleaned["message"],
            language=lang,
        )
        for upload in cleaned.get("files") or []:
            attachment = ContactAttachment(
                request=contact_request,
                original_name=Path(upload.name).name,
                content_type=upload.content_type or "",
                size=upload.size,
            )
            attachment.file.save(Path(upload.name).name, upload, save=False)
            attachment.save()
    return contact_request


def _send_notification(cleaned, request):
    if not settings.EMAIL_HOST:
        return
    email = EmailMessage(
        subject=f"USDM: {cleaned['first_name']} {cleaned.get('last_name', '')}".strip(),
        body="\n".join((
            "New request from usdm.com.ua",
            "",
            f"Name: {cleaned['first_name']} {cleaned.get('last_name', '')}".strip(),
            f"Email: {cleaned['email']}",
            f"Phone: {cleaned['phone']}",
            f"Page: {request.build_absolute_uri(request.POST.get('next') or '/')}",
            "",
            "Message:",
            cleaned["message"],
        )),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECIPIENT_EMAIL],
        reply_to=[cleaned["email"]],
    )
    for upload in cleaned.get("files") or []:
        upload.seek(0)
        email.attach(Path(upload.name).name, upload.read(), upload.content_type)
    email.send(fail_silently=False)


@require_POST
def submit_contact(request, lang):
    target = _target(request, lang)
    if request.POST.get("website", "").strip():
        _remember(request, "success")
        return redirect(target)

    form = ContactForm(request.POST, request.FILES)
    if not form.is_valid():
        values = {
            name: request.POST.get(name, "").strip()
            for name in ("first_name", "last_name", "email", "phone", "message")
        }
        values["privacy"] = request.POST.get("privacy") == "on"
        field_errors = {
            name: " ".join(str(error) for error in errors)
            for name, errors in form.errors.items()
            if name in form.fields
        }
        _remember(request, "invalid", values, form.errors.keys(), field_errors)
        return redirect(target)

    try:
        _save_request(form.cleaned_data, lang)
    except Exception:
        logger.exception("USDM contact request storage failed")
        values = {
            name: form.cleaned_data.get(name, "")
            for name in ("first_name", "last_name", "email", "phone", "message")
        }
        values["privacy"] = bool(form.cleaned_data.get("privacy"))
        _remember(request, "failure", values)
        return redirect(target)

    try:
        _send_notification(form.cleaned_data, request)
    except Exception:
        logger.exception("USDM contact email notification failed")
    _remember(request, "success")
    return redirect(target)
