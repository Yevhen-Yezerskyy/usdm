(() => {
  "use strict";

  const MB = 1024 * 1024;
  const keyFor = (file) => `${file.name}:${file.size}:${file.lastModified}`;
  const formatSize = (bytes) => bytes < MB
    ? `${Math.max(1, Math.round(bytes / 1024))} KB`
    : `${(bytes / MB).toFixed(1).replace(".0", "")} MB`;

  document.querySelectorAll("[data-contact-form]").forEach((form) => {
    const messagesNode = form.querySelector("#contact-client-messages");
    let messages = {};
    try {
      messages = JSON.parse(messagesNode?.textContent || "{}");
    } catch (_error) {
      return;
    }

    const input = form.querySelector('input[type="file"]');
    const dropzone = form.querySelector("[data-contact-dropzone]");
    const list = form.querySelector("[data-contact-file-list]");
    const maxFiles = Number(input.dataset.maxFiles || 10);
    const maxTotalSize = Number(input.dataset.maxTotalSize || 25 * MB);
    const allowedExtensions = new Set(
      input.accept.split(",").map((value) => value.trim().replace(/^\./, "").toLowerCase()).filter(Boolean),
    );
    const errors = new Map();
    let activeControl = null;
    let activePopover = null;
    let files = [];

    const interpolate = (template, values) => Object.entries(values).reduce(
      (result, [key, value]) => result.replace(`{${key}}`, value),
      template,
    );

    const positionPopover = (control, popover) => {
      const anchor = control.type === "file"
        ? dropzone
        : (control.type === "checkbox" ? control.closest(".contact-consent") : control);
      const rect = anchor.getBoundingClientRect();
      const horizontalInset = Math.min(8, rect.width * 0.03);
      popover.style.left = `${window.scrollX + rect.left + horizontalInset}px`;
      popover.style.top = `${window.scrollY + rect.bottom + 7}px`;
      popover.style.maxWidth = `${Math.max(180, rect.width - horizontalInset * 2)}px`;
    };

    const hidePopover = () => {
      activeControl?.removeAttribute("aria-describedby");
      activePopover?.remove();
      activePopover = null;
      activeControl = null;
    };

    const showPopover = (control) => {
      const message = errors.get(control);
      if (!message) return;
      hidePopover();
      const popover = document.createElement("div");
      popover.className = "contact-error-popover";
      popover.id = `contact-error-${control.name}`;
      popover.setAttribute("role", "alert");
      popover.setAttribute("data-contact-error-popover", "");
      popover.textContent = message;
      document.body.append(popover);
      activeControl = control;
      activePopover = popover;
      control.setAttribute("aria-describedby", popover.id);
      positionPopover(control, popover);
    };

    const setError = (control, message = "", reveal = false) => {
      const invalid = Boolean(message);
      control.classList.toggle("is-invalid", invalid);
      if (invalid) {
        errors.set(control, message);
        control.setAttribute("aria-invalid", "true");
        if (reveal) showPopover(control);
      } else {
        errors.delete(control);
        control.removeAttribute("aria-invalid");
        control.removeAttribute("aria-describedby");
        if (activeControl === control) hidePopover();
      }
      return !invalid;
    };

    const syncInput = () => {
      const transfer = new DataTransfer();
      files.forEach((file) => transfer.items.add(file));
      input.files = transfer.files;
    };

    const validateFiles = (reveal = false) => {
      if (files.length > maxFiles) {
        return setError(input, interpolate(messages.fileCount, {maximum: maxFiles}), reveal);
      }
      const total = files.reduce((sum, file) => sum + file.size, 0);
      if (total > maxTotalSize) {
        return setError(
          input,
          interpolate(messages.fileSize, {maximum: Math.round(maxTotalSize / MB)}),
          reveal,
        );
      }
      if (files.some((file) => file.size === 0)) return setError(input, messages.fileEmpty, reveal);
      const unsupported = files.find((file) => {
        const extension = file.name.includes(".") ? file.name.split(".").pop().toLowerCase() : "";
        return !allowedExtensions.has(extension);
      });
      if (unsupported) {
        return setError(input, interpolate(messages.fileType, {name: unsupported.name}), reveal);
      }
      return setError(input);
    };

    const render = () => {
      list.replaceChildren();
      files.forEach((file) => {
        const item = document.createElement("li");
        item.className = "contact-file-item";
        const name = document.createElement("span");
        name.className = "contact-file-name";
        name.textContent = `${file.name} · ${formatSize(file.size)}`;
        const remove = document.createElement("button");
        remove.className = "contact-file-remove";
        remove.type = "button";
        remove.textContent = "×";
        remove.setAttribute("aria-label", interpolate(messages.removeFile, {name: file.name}));
        remove.addEventListener("click", () => {
          files = files.filter((candidate) => keyFor(candidate) !== keyFor(file));
          syncInput();
          validateFiles(true);
          render();
        });
        item.append(name, remove);
        list.append(item);
      });
    };

    const addFiles = (incoming) => {
      const known = new Set(files.map(keyFor));
      Array.from(incoming).forEach((file) => {
        if (!known.has(keyFor(file))) {
          files.push(file);
          known.add(keyFor(file));
        }
      });
      syncInput();
      validateFiles(true);
      render();
    };

    const validateControl = (control, reveal = false) => {
      if (control.type === "checkbox") {
        return setError(control, control.checked ? "" : messages[control.name], reveal);
      }
      if (!control.value.trim()) {
        if (!control.required) return setError(control);
        const requiredMessage = control.name === "email" ? messages.emailRequired : messages[control.name];
        return setError(control, requiredMessage, reveal);
      }
      if (control.name === "email" && !control.checkValidity()) {
        return setError(control, messages.emailInvalid, reveal);
      }
      if (control.name === "phone") {
        const digitCount = (control.value.match(/[0-9]/g) || []).length;
        if (digitCount < 6 || !/^[0-9+()./ -]+$/.test(control.value)) {
          return setError(control, messages.phoneInvalid, reveal);
        }
      }
      return setError(control);
    };

    input.addEventListener("change", () => addFiles(input.files));
    ["dragenter", "dragover"].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.add("is-dragging");
    }));
    ["dragleave", "drop"].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.remove("is-dragging");
    }));
    dropzone.addEventListener("drop", (event) => addFiles(event.dataTransfer.files));
    dropzone.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        input.click();
      }
    });

    const controls = form.querySelectorAll(".contact-control:not([type='file']):not([name='website'])");
    controls.forEach((control) => {
      control.addEventListener("input", () => {
        if (control.classList.contains("is-invalid")) validateControl(control, true);
      });
      control.addEventListener("blur", () => {
        if (control.value || control.classList.contains("is-invalid")) validateControl(control, true);
      });
      control.addEventListener("focus", () => {
        if (errors.has(control)) showPopover(control);
      });
    });

    form.addEventListener("submit", (event) => {
      let valid = validateFiles();
      controls.forEach((control) => { valid = validateControl(control) && valid; });
      if (!valid) {
        event.preventDefault();
        const first = form.querySelector(".is-invalid");
        if (first) showPopover(first);
        (first?.type === "file" ? dropzone : first)?.focus({preventScroll: true});
        first?.scrollIntoView({behavior: "smooth", block: "center"});
      }
    }, true);

    const repositionPopover = () => {
      if (activeControl && activePopover) positionPopover(activeControl, activePopover);
    };
    window.addEventListener("resize", repositionPopover);
    window.addEventListener("scroll", repositionPopover, {passive: true});

    const serverErrorsNode = form.querySelector("#contact-server-errors");
    if (serverErrorsNode) {
      try {
        const serverErrors = JSON.parse(serverErrorsNode.textContent);
        Object.entries(serverErrors).forEach(([name, message]) => {
          const control = form.elements.namedItem(name);
          if (control && message) setError(control, message);
        });
        const first = form.querySelector(".is-invalid");
        if (first) showPopover(first);
      } catch (_error) {
        // Invalid server state must not prevent the form from working.
      }
    }

    const serverStatusNode = form.querySelector("#contact-server-status");
    if (serverStatusNode) {
      try {
        const status = JSON.parse(serverStatusNode.textContent);
        if (status.name && status.message) {
          const grid = form.querySelector(".contact-form-grid");
          const message = document.createElement("p");
          message.className = `contact-status-message contact-status-message--${status.name}`;
          message.setAttribute("role", status.name === "failure" ? "alert" : "status");
          message.setAttribute("data-contact-status-message", "");
          message.textContent = status.message;
          grid.before(message);
        }
      } catch (_error) {
        // Invalid server state must not prevent the form from working.
      }
    }
  });
})();
