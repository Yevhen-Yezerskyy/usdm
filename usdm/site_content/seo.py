import json

from django.conf import settings


GTM_CONTAINER_ID = "GTM-K95Z727"

PUBLIC_PAGE_NAMES = (
    "home",
    "technology",
    "houses",
    "experience",
    "contact",
    "impressum",
    "datenschutz",
)

_CANONICAL_PAGE = {
    "imprint": "impressum",
    "privacy": "datenschutz",
}

_PAGE_PATHS = {
    "home": "/{lang}/",
    "technology": "/{lang}/technology/",
    "houses": "/{lang}/houses/",
    "experience": "/{lang}/experience/",
    "contact": "/{lang}/contact/",
    "impressum": "/{lang}/impressum/",
    "datenschutz": "/{lang}/datenschutz/",
}

_OG_IMAGES = {
    "home": "/static/img/og-home.jpg",
    "technology": "/static/img/og-technology.jpg",
    "houses": "/static/img/og-houses.jpg",
    "experience": "/static/img/og-experience.jpg",
    "contact": "/static/img/og-contact.jpg",
    "impressum": "/static/img/og-home.jpg",
    "datenschutz": "/static/img/og-home.jpg",
}

# Localized SEO copy for every public language.
_COPY = {
    "fr": {
        "home": {
            "title": "USDM | Maisons à ossature bois et maisons modulaires",
            "description": "USDM fabrique des kits de construction à ossature bois et des maisons modulaires : structures en bois, panneaux techniques, production WEINMANN, livraison et montage en Europe.",
        },
        "technology": {
            "title": "Technologie des maisons à ossature bois et modulaires | USDM",
            "description": "Production automatisée WEINMANN de structures et panneaux en bois, construction écoénergétique, conception modulaire, livraison et montage de maisons.",
        },
        "houses": {
            "title": "Maisons modulaires et à ossature bois : projets et prix | USDM",
            "description": "Exemples de maisons modulaires et à ossature bois USDM : plans, équipements, prix indicatifs, livraison et montage.",
        },
        "experience": {
            "title": "Réalisations de maisons modulaires et à ossature bois | USDM",
            "description": "Plus de 10 ans d’expérience USDM : maisons réalisées, intérieurs, fabrication, livraison et montage de constructions modulaires et à ossature bois.",
        },
        "contact": {
            "title": "Contact USDM | Maisons à ossature bois et modulaires",
            "description": "Contactez USDM pour vos projets de maisons à ossature bois, kits de construction et maisons modulaires livrées et montées.",
        },
        "impressum": {
            "title": "Mentions légales | USDM",
            "description": "Informations légales sur TOV USDM, propriétaire du site et fabricant de maisons à ossature bois et de constructions en bois.",
        },
        "datenschutz": {
            "title": "Politique de confidentialité | USDM",
            "description": "Informations de TOV USDM sur le traitement des données personnelles des visiteurs de ce site.",
        },
    },
    "de": {
        "home": {
            "title": "USDM | Holzrahmen-Panelhäuser und Modulhäuser",
            "description": "USDM fertigt Holzrahmen-Panel-Bausätze und Modulhäuser: Holzrahmen, technische Paneele, WEINMANN-Fertigung, Lieferung und Montage in Europa.",
        },
        "technology": {
            "title": "Technologie für Holzrahmen-Panelhäuser | USDM",
            "description": "Automatisierte WEINMANN-Fertigung von Holzrahmen und Paneelen, energieeffiziente Konstruktion, Modulbau, Lieferung und Montage fertiger Häuser.",
        },
        "houses": {
            "title": "Modulhäuser und Holzrahmen-Panelhäuser: Projekte & Preise | USDM",
            "description": "Projektbeispiele für Modulhäuser und Holzrahmen-Panelhäuser von USDM: Grundrisse, Ausstattung, Richtpreise, Lieferung und Montage.",
        },
        "experience": {
            "title": "Referenzen für Modulhäuser und Holzrahmen-Panelhäuser | USDM",
            "description": "Mehr als 10 Jahre Erfahrung von USDM: realisierte Häuser, Innenräume, Fertigung, Lieferung und Montage in Holzrahmen-Panel- und Modulbauweise.",
        },
        "contact": {
            "title": "USDM - Kontakt. Holzrahmen-Panelhäuser, modulare Bautechnologie.",
            "description": "Anfragen für Holzrahmen-Panelhäuser, Bausätze und fertige modulare Häuser mit Lieferung. Kontakt TOV „USDM“.",
        },
        "impressum": {
            "title": "Impressum | USDM",
            "description": "Impressum und Anbieterkennzeichnung von TOV USDM, Hersteller von Holzrahmen-Panelhäusern und Holzbaukonstruktionen.",
        },
        "datenschutz": {
            "title": "Datenschutz | USDM",
            "description": "Datenschutzhinweise von TOV USDM zur Verarbeitung personenbezogener Daten auf der Website.",
        },
    },
    "uk": {
        "home": {
            "title": "USDM | каркасно-панельні та модульні будинки",
            "description": "USDM виробляє каркасно-панельні комплекти та модульні будинки: дерев’яний каркас, технічні панелі, доставка й монтаж в Україні та Європі.",
        },
        "technology": {
            "title": "Технології каркасно-панельного та модульного будівництва | USDM",
            "description": "Автоматизоване виробництво дерев’яних каркасів і панелей WEINMANN, проєктування, енергоефективні рішення, доставка та монтаж модульних будинків.",
        },
        "houses": {
            "title": "Каркасно-панельні та модульні будинки: ціни й проєкти | USDM",
            "description": "Приклади каркасно-панельних і модульних будинків USDM: планування, комплектація, орієнтовна вартість, доставка та монтаж.",
        },
        "experience": {
            "title": "Досвід USDM — реалізовані каркасно-панельні та модульні будинки",
            "description": "Понад 10 років досвіду USDM: реалізовані будинки, інтер’єри, виробництво, доставка та монтаж каркасно-панельних конструкцій.",
        },
        "contact": {
            "title": "Контакти USDM — запит щодо каркасно-панельного або модульного будинку",
            "description": "Звертайтеся до USDM щодо проєктування, виробництва, постачання та монтажу каркасно-панельних комплектів і модульних будинків.",
        },
        "impressum": {
            "title": "Юридична інформація | USDM",
            "description": "Відомості про власника та оператора сайту USDM, виробника каркасно-панельних і модульних будинків.",
        },
        "datenschutz": {
            "title": "Політика конфіденційності | USDM",
            "description": "Інформація про обробку персональних даних відвідувачів сайту USDM.",
        },
    },
}

_PAGE_LABELS = {
    "fr": {
        "home": "Accueil",
        "technology": "Technologies",
        "houses": "Maisons",
        "experience": "Expérience",
        "contact": "Contact",
        "impressum": "Mentions légales",
        "datenschutz": "Politique de confidentialité",
    },
    "uk": {
        "home": "Головна",
        "technology": "Технології",
        "houses": "Будинки",
        "experience": "Досвід",
        "contact": "Контакти",
        "impressum": "Юридична інформація",
        "datenschutz": "Політика конфіденційності",
    },
    "de": {
        "home": "Startseite",
        "technology": "Technologie",
        "houses": "Häuser",
        "experience": "Erfahrung",
        "contact": "Kontakt",
        "impressum": "Impressum",
        "datenschutz": "Datenschutz",
    },
}


def canonical_page_name(page_name):
    return _CANONICAL_PAGE.get(page_name, page_name)


def page_path(language, page_name):
    canonical_name = canonical_page_name(page_name)
    return _PAGE_PATHS[canonical_name].format(lang=language)


def absolute_url(path):
    return f"{settings.SITE_PUBLIC_URL.rstrip('/')}{path}"


def page_seo(language, page_name):
    canonical_name = canonical_page_name(page_name)
    language = language if language in _COPY else "uk"
    copy = _COPY[language][canonical_name]
    canonical_url = absolute_url(page_path(language, canonical_name))
    image_url = absolute_url(_OG_IMAGES[canonical_name])
    language_tag = {"de": "de-DE", "fr": "fr-FR"}.get(language, "uk-UA")
    robots = "noindex, nofollow" if settings.DEBUG or page_name != canonical_name else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{settings.SITE_PUBLIC_URL.rstrip('/')}/#organization",
                "name": "TOV USDM",
                "alternateName": "USDM",
                "url": settings.SITE_PUBLIC_URL,
                "logo": absolute_url("/static/img/apple-touch-icon.gif"),
                "email": "info@usdm.com.ua",
                "telephone": "+380974101430",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "вул. Глибочицька, 72, офіс 320/1",
                    "addressLocality": "Київ",
                    "postalCode": "04655",
                    "addressCountry": "UA",
                },
                "sameAs": [
                    "https://www.facebook.com/usdm.ua",
                    "https://www.instagram.com/usdm.ua/",
                ],
            },
            {
                "@type": "ImageObject",
                "@id": f"{image_url}#primaryimage",
                "url": image_url,
                "contentUrl": image_url,
                "width": 1200,
                "height": 630,
                "caption": copy["title"],
                "inLanguage": language_tag,
            },
            {
                "@type": "WebPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": copy["title"],
                "description": copy["description"],
                "inLanguage": language_tag,
                "isPartOf": {
                    "@id": f"{settings.SITE_PUBLIC_URL.rstrip('/')}/#website",
                },
                "primaryImageOfPage": {"@id": f"{image_url}#primaryimage"},
            },
        ],
    }
    if canonical_name == "home":
        schema["@graph"].append(
            {
                "@type": "WebSite",
                "@id": f"{settings.SITE_PUBLIC_URL.rstrip('/')}/#website",
                "url": settings.SITE_PUBLIC_URL,
                "name": "USDM",
                "inLanguage": ["uk-UA", "de-DE", "fr-FR"],
                "publisher": {"@id": f"{settings.SITE_PUBLIC_URL.rstrip('/')}/#organization"},
            }
        )
    else:
        schema["@graph"].append(
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": _PAGE_LABELS[language]["home"],
                        "item": absolute_url(page_path(language, "home")),
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": _PAGE_LABELS[language][canonical_name],
                        "item": canonical_url,
                    },
                ],
            }
        )

    return {
        "title": copy["title"],
        "description": copy["description"],
        "canonical_url": canonical_url,
        "image_url": image_url,
        "language_tag": language_tag,
        "og_locale": language_tag.replace("-", "_"),
        "og_locale_alternates": [
            tag.replace("-", "_")
            for tag in ("uk-UA", "de-DE", "fr-FR")
            if tag != language_tag
        ],
        "alternates": [
            {"language": "uk-UA", "url": absolute_url(page_path("uk", canonical_name))},
            {"language": "de-DE", "url": absolute_url(page_path("de", canonical_name))},
            {"language": "fr-FR", "url": absolute_url(page_path("fr", canonical_name))},
            {"language": "x-default", "url": absolute_url(page_path("uk", canonical_name))},
        ],
        "robots": robots,
        "structured_data": json.dumps(schema, ensure_ascii=False, separators=(",", ":")),
        "gtm_container_id": GTM_CONTAINER_ID,
        "page_type": canonical_name,
    }


def sitemap_urls():
    for language in ("uk", "de", "fr"):
        for page_name in PUBLIC_PAGE_NAMES:
            yield absolute_url(page_path(language, page_name))


def sitemap_pages():
    for language in ("uk", "de", "fr"):
        for page_name in PUBLIC_PAGE_NAMES:
            yield language, page_name, absolute_url(page_path(language, page_name))
