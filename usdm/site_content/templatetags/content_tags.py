from django import template
from django.utils.html import conditional_escape, format_html, format_html_join


register = template.Library()


@register.filter
def bold_prefix(value, prefix):
    text = str(value)
    prefix_text = str(prefix)
    if prefix_text and text.startswith(prefix_text):
        return format_html(
            "<strong>{}</strong>{}",
            prefix_text,
            text[len(prefix_text):],
        )
    return conditional_escape(text)


@register.filter
def price_label(value, amount):
    text = str(value)
    amount_text = str(amount)
    if amount_text and text.endswith(amount_text):
        return text[:-len(amount_text)].rstrip()
    return text


@register.filter
def banner_lines(value):
    return format_html_join(
        format_html("<br>"),
        "{}",
        ((line,) for line in str(value).split(" / ")),
    )


@register.filter
def contact_address(value, bold_prefix=""):
    lines = str(value).split(" / ")
    prefix = str(bold_prefix)
    if prefix and lines[0].startswith(prefix):
        lines[0] = format_html(
            "<strong>{}</strong>{}",
            prefix,
            lines[0][len(prefix):],
        )
    return format_html_join(
        format_html("<br>"),
        "{}",
        ((line,) for line in lines),
    )
