(function () {
  "use strict";

  var root = document.querySelector("[data-site-consent]");
  var textNode = document.querySelector("[data-site-consent-texts]");
  var launcher = document.querySelector(".site-consent-launcher[data-consent-open]");
  if (!root || !textNode) return;

  var texts;
  try {
    texts = JSON.parse(textNode.textContent);
  } catch (error) {
    return;
  }

  var cookieName = root.getAttribute("data-consent-cookie") || "site_cookie_consent_v1";
  var privacyUrl = root.getAttribute("data-consent-privacy-url") || "/datenschutz/";
  var available = (root.getAttribute("data-consent-categories") || "")
    .split(/\s+/)
    .filter(Boolean);
  var maxAge = 31536000;
  var categories = ["statistics", "external_media"];
  var currentConsent = readConsent() || defaultConsent();

  function hasCategory(category) {
    return available.indexOf(category) !== -1;
  }

  function defaultConsent() {
    return { statistics: false, external_media: false };
  }

  function getCookie(name) {
    var prefix = name + "=";
    var parts = document.cookie ? document.cookie.split(";") : [];
    for (var index = 0; index < parts.length; index += 1) {
      var part = parts[index].trim();
      if (part.indexOf(prefix) === 0) {
        return decodeURIComponent(part.slice(prefix.length));
      }
    }
    return "";
  }

  function setCookie(name, value) {
    var secure = window.location.protocol === "https:" ? "; Secure" : "";
    document.cookie = name + "=" + encodeURIComponent(value) + "; Max-Age=" + maxAge + "; Path=/; SameSite=Lax" + secure;
  }

  function readConsent() {
    var raw = getCookie(cookieName);
    if (!raw) return null;
    var params = new URLSearchParams(raw);
    if (params.get("necessary") !== "1") return null;
    return {
      statistics: params.get("statistics") === "1",
      external_media: params.get("external_media") === "1"
    };
  }

  function persistConsent(consent) {
    var value = "necessary=1&statistics=" + (consent.statistics ? "1" : "0") +
      "&external_media=" + (consent.external_media ? "1" : "0");
    setCookie(cookieName, value);
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function optionMarkup(category, title, description, checked, disabled) {
    if (category !== "necessary" && !hasCategory(category)) return "";
    return '<label class="site-consent__option">' +
      '<input type="checkbox" data-site-consent-setting="' + category + '"' +
      (checked ? " checked" : "") + (disabled ? " disabled" : "") + '>' +
      '<span><strong>' + escapeHtml(title) + '</strong><br>' + escapeHtml(description) + '</span>' +
      '</label>';
  }

  function render() {
    var acceptAllButton = available.length ?
      '<button class="site-consent__button site-consent__button--primary" type="button" data-site-consent-accept-all>' + escapeHtml(texts.acceptAll) + '</button>' : "";
    root.innerHTML =
      '<div class="site-consent__dialog" role="dialog" aria-modal="false" aria-labelledby="site-consent-title">' +
        '<div class="site-consent__head">' +
          '<p class="site-consent__title" id="site-consent-title">' + escapeHtml(texts.title) + '</p>' +
          '<div class="site-consent__head-actions">' +
            '<button class="site-consent__toggle" type="button" data-site-consent-toggle aria-expanded="false">' + escapeHtml(texts.settings) + '</button>' +
            '<button class="site-consent__close" type="button" data-site-consent-close aria-label="' + escapeHtml(texts.close) + '" title="' + escapeHtml(texts.close) + '"><span aria-hidden="true"></span></button>' +
          '</div>' +
        '</div>' +
        '<p class="site-consent__intro">' + escapeHtml(texts.intro) + '</p>' +
        '<div class="site-consent__actions">' +
          acceptAllButton +
          '<button class="site-consent__button site-consent__button--neutral" type="button" data-site-consent-necessary>' + escapeHtml(texts.necessaryOnly) + '</button>' +
          '<button class="site-consent__button site-consent__button--ghost" type="button" data-site-consent-close>' + escapeHtml(texts.close) + '</button>' +
          '<a class="site-consent__button site-consent__button--ghost site-consent__privacy-button" href="' + escapeHtml(privacyUrl) + '">' + escapeHtml(texts.privacy) + '</a>' +
        '</div>' +
        '<div class="site-consent__panel" data-site-consent-panel hidden>' +
          optionMarkup("necessary", texts.necessaryTitle, texts.necessaryText, true, true) +
          optionMarkup("statistics", texts.statisticsTitle, texts.statisticsText, currentConsent.statistics, false) +
          optionMarkup("external_media", texts.externalMediaTitle, texts.externalMediaText, currentConsent.external_media, false) +
          '<div class="site-consent__actions">' +
            '<button class="site-consent__button site-consent__button--primary" type="button" data-site-consent-save>' + escapeHtml(texts.save) + '</button>' +
            '<button class="site-consent__button site-consent__button--neutral" type="button" data-site-consent-necessary>' + escapeHtml(texts.necessaryOnly) + '</button>' +
          '</div>' +
        '</div>' +
      '</div>';
  }

  function activateScripts(category) {
    document.querySelectorAll('script[type="text/plain"][data-consent-category="' + category + '"]').forEach(function (source) {
      if (source.getAttribute("data-consent-loaded") === "1") return;
      var script = document.createElement("script");
      Array.prototype.slice.call(source.attributes).forEach(function (attribute) {
        if (["type", "data-consent-category", "data-consent-loaded", "data-consent-src"].indexOf(attribute.name) === -1) {
          script.setAttribute(attribute.name, attribute.value);
        }
      });
      var src = source.getAttribute("data-consent-src");
      if (src) script.src = src;
      if (source.textContent.trim()) script.textContent = source.textContent;
      source.setAttribute("data-consent-loaded", "1");
      source.parentNode.insertBefore(script, source.nextSibling);
    });
  }

  function applyCategory(category, allowed) {
    document.documentElement.setAttribute("data-consent-" + category, allowed ? "1" : "0");

    document.querySelectorAll('[data-consent-category="' + category + '"][data-consent-src]:not(script)').forEach(function (element) {
      if (allowed) {
        if (!element.getAttribute("src")) element.setAttribute("src", element.getAttribute("data-consent-src"));
        element.hidden = false;
      } else {
        element.removeAttribute("src");
        element.hidden = true;
      }
    });

    document.querySelectorAll('[data-consent-embed="' + category + '"]').forEach(function (embed) {
      embed.classList.toggle("is-consent-active", allowed);
      var placeholder = embed.querySelector("[data-consent-placeholder]");
      if (placeholder) placeholder.hidden = allowed;
    });

    if (allowed) activateScripts(category);
  }

  function applyConsent(consent, persist) {
    var previous = currentConsent;
    currentConsent = {
      statistics: hasCategory("statistics") && Boolean(consent.statistics),
      external_media: hasCategory("external_media") && Boolean(consent.external_media)
    };
    if (persist) persistConsent(currentConsent);
    categories.forEach(function (category) {
      applyCategory(category, currentConsent[category]);
    });
    window.dispatchEvent(new CustomEvent("site-consent:change", { detail: currentConsent }));
    if (persist && previous.statistics && !currentConsent.statistics) {
      window.location.reload();
    }
  }

  function selectionFromPanel() {
    var consent = defaultConsent();
    categories.forEach(function (category) {
      var input = root.querySelector('[data-site-consent-setting="' + category + '"]');
      consent[category] = Boolean(input && input.checked);
    });
    return consent;
  }

  function showBanner(show, openPanel) {
    root.hidden = !show;
    if (launcher) launcher.hidden = show;
    var panel = root.querySelector("[data-site-consent-panel]");
    var toggle = root.querySelector("[data-site-consent-toggle]");
    if (panel && openPanel !== undefined) panel.hidden = !openPanel;
    if (toggle && openPanel !== undefined) toggle.setAttribute("aria-expanded", openPanel ? "true" : "false");
  }

  render();
  applyConsent(currentConsent, false);
  showBanner(!readConsent(), false);

  root.addEventListener("click", function (event) {
    var target = event.target.closest("button");
    if (!target) return;
    if (target.matches("[data-site-consent-toggle]")) {
      var panel = root.querySelector("[data-site-consent-panel]");
      showBanner(true, Boolean(panel && panel.hidden));
    } else if (target.matches("[data-site-consent-accept-all]")) {
      applyConsent({ statistics: true, external_media: true }, true);
      showBanner(false);
    } else if (target.matches("[data-site-consent-necessary], [data-site-consent-close]")) {
      applyConsent(defaultConsent(), true);
      showBanner(false);
    } else if (target.matches("[data-site-consent-save]")) {
      applyConsent(selectionFromPanel(), true);
      showBanner(false);
    }
  });

  document.addEventListener("click", function (event) {
    var opener = event.target.closest("[data-consent-open]");
    var categoryButton = event.target.closest("[data-consent-accept-category]");
    if (opener) {
      event.preventDefault();
      render();
      showBanner(true, true);
    }
    if (categoryButton) {
      event.preventDefault();
      var category = categoryButton.getAttribute("data-consent-accept-category");
      var next = Object.assign({}, currentConsent);
      next[category] = true;
      applyConsent(next, true);
      showBanner(false);
    }
  });
}());
