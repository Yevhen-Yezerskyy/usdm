(() => {
  "use strict";

  const parallaxSections = Array.from(document.querySelectorAll("[data-parallax]"));
  if (parallaxSections.length) {
    let frameRequested = false;

    const renderParallax = () => {
      const viewportHeight = window.innerHeight;
      const scrollTop = window.scrollY;

      for (const section of parallaxSections) {
        const velocity = Math.abs(Number(section.dataset.parallaxVelocity) || 0.3);
        const travel = viewportHeight * velocity;
        const sectionTop = section.getBoundingClientRect().top + scrollTop;
        const sectionHeight = section.offsetHeight;
        const scrollMin = Math.max(sectionTop - viewportHeight, 0);
        const scrollMax = sectionTop + sectionHeight;

        section.style.setProperty("--parallax-travel", `${travel}px`);
        if (scrollTop + viewportHeight < sectionTop || scrollTop > scrollMax) {
          continue;
        }

        const progress = Math.min(
          1,
          Math.max(0, (scrollTop - scrollMin) / (scrollMax - scrollMin)),
        );
        section.style.setProperty("--parallax-offset", `${-travel * progress}px`);
      }

      frameRequested = false;
    };

    const requestParallax = () => {
      if (!frameRequested) {
        frameRequested = true;
        window.requestAnimationFrame(renderParallax);
      }
    };

    window.addEventListener("scroll", requestParallax, { passive: true });
    window.addEventListener("resize", requestParallax);
    requestParallax();
  }

  const mobileNavigation = document.querySelector(".mobile-navigation");
  if (mobileNavigation) {
    const summary = mobileNavigation.querySelector("summary");
    const desktopQuery = window.matchMedia("(min-width: 761px)");

    const syncMobileNavigation = () => {
      summary.setAttribute("aria-expanded", mobileNavigation.open ? "true" : "false");
    };

    mobileNavigation.addEventListener("toggle", syncMobileNavigation);
    document.addEventListener("click", (event) => {
      if (mobileNavigation.open && !mobileNavigation.contains(event.target)) {
        mobileNavigation.open = false;
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && mobileNavigation.open) {
        mobileNavigation.open = false;
        summary.focus();
      }
    });
    desktopQuery.addEventListener("change", (event) => {
      if (event.matches) mobileNavigation.open = false;
    });
    syncMobileNavigation();
  }

  if (
    "IntersectionObserver" in window
    && !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    const revealItems = document.querySelectorAll(
      ".site-main > section, .site-main > header, .site-main > article",
    );
    const revealObserver = new IntersectionObserver((entries, observer) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    }, { rootMargin: "0px 0px -4%", threshold: 0.01 });

    for (const item of revealItems) {
      item.classList.add("scroll-reveal");
      revealObserver.observe(item);
    }
  }

  for (const switcher of document.querySelectorAll("[data-language-switch]")) {
    switcher.addEventListener("click", () => {
      const language = switcher.dataset.languageSwitch;
      if (!language) return;
      const secure = window.location.protocol === "https:" ? "; Secure" : "";
      document.cookie = `usdm_language=${encodeURIComponent(language)}; Max-Age=31536000; Path=/; SameSite=Lax${secure}`;
    });
  }

  for (const carousel of document.querySelectorAll("[data-carousel]")) {
    const viewport = carousel.querySelector("[data-carousel-viewport]");
    const track = carousel.querySelector("[data-carousel-track]");
    const slides = Array.from(track.children);
    const previous = carousel.querySelector("[data-carousel-previous]");
    const next = carousel.querySelector("[data-carousel-next]");
    const pagination = carousel.querySelector("[data-carousel-pagination]");
    let index = 0;
    let pageCount = 0;
    let startX = null;

    const perPage = () => (window.matchMedia("(max-width: 760px)").matches ? 1 : 2);

    const renderCarousel = () => {
      const visible = perPage();
      pageCount = Math.max(1, slides.length - visible + 1);
      index = Math.min(index, pageCount - 1);
      const gap = 10;
      const slideWidth = (viewport.clientWidth - gap * (visible - 1)) / visible;
      track.style.transform = `translate3d(${-index * (slideWidth + gap)}px, 0, 0)`;
      previous.disabled = index === 0;
      next.disabled = index === pageCount - 1;

      pagination.replaceChildren();
      for (let dotIndex = 0; dotIndex < pageCount; dotIndex += 1) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = `carousel__dot${dotIndex === index ? " is-active" : ""}`;
        dot.setAttribute("aria-label", `${dotIndex + 1}`);
        dot.addEventListener("click", () => {
          index = dotIndex;
          renderCarousel();
        });
        pagination.append(dot);
      }
    };

    const move = (amount) => {
      index = Math.max(0, Math.min(pageCount - 1, index + amount));
      renderCarousel();
    };

    previous.addEventListener("click", () => move(-1));
    next.addEventListener("click", () => move(1));
    viewport.addEventListener("pointerdown", (event) => {
      startX = event.clientX;
    });
    viewport.addEventListener("pointerup", (event) => {
      if (startX === null) return;
      const distance = event.clientX - startX;
      startX = null;
      if (Math.abs(distance) > 45) move(distance < 0 ? 1 : -1);
    });
    viewport.addEventListener("pointercancel", () => { startX = null; });
    window.addEventListener("resize", renderCarousel);
    renderCarousel();
  }

  const lightboxItems = document.querySelectorAll("[data-lightbox-item]");
  if (!lightboxItems.length) return;

  const lightbox = document.createElement("div");
  lightbox.className = "lightbox";
  lightbox.setAttribute("role", "dialog");
  lightbox.setAttribute("aria-modal", "true");
  lightbox.setAttribute("aria-label", "Image viewer");
  lightbox.innerHTML = `
    <button class="lightbox__close" type="button" aria-label="Close"></button>
    <button class="lightbox__previous" type="button" aria-label="Previous"></button>
    <img class="lightbox__image" alt="">
    <button class="lightbox__next" type="button" aria-label="Next"></button>
    <div class="lightbox__pagination"></div>
    <div class="lightbox__counter" aria-live="polite"></div>
  `;
  document.body.append(lightbox);

  const image = lightbox.querySelector(".lightbox__image");
  const close = lightbox.querySelector(".lightbox__close");
  const previous = lightbox.querySelector(".lightbox__previous");
  const next = lightbox.querySelector(".lightbox__next");
  const pagination = lightbox.querySelector(".lightbox__pagination");
  const counter = lightbox.querySelector(".lightbox__counter");
  let activeItems = [];
  let activeIndex = 0;
  let touchStartX = null;

  const showImage = () => {
    const item = activeItems[activeIndex];
    image.src = item.href;
    image.alt = item.querySelector("img")?.alt || "";
    counter.textContent = `${activeIndex + 1} / ${activeItems.length}`;
    previous.hidden = activeItems.length < 2;
    next.hidden = activeItems.length < 2;

    if (pagination.children.length !== activeItems.length) {
      pagination.replaceChildren();
      for (let dotIndex = 0; dotIndex < activeItems.length; dotIndex += 1) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "lightbox__dot";
        dot.setAttribute("aria-label", `${dotIndex + 1}`);
        dot.addEventListener("click", () => {
          activeIndex = dotIndex;
          showImage();
        });
        pagination.append(dot);
      }
    }

    for (const [dotIndex, dot] of Array.from(pagination.children).entries()) {
      dot.classList.toggle("is-active", dotIndex === activeIndex);
      dot.setAttribute("aria-current", dotIndex === activeIndex ? "true" : "false");
    }
  };

  const moveLightbox = (amount) => {
    activeIndex = (activeIndex + amount + activeItems.length) % activeItems.length;
    showImage();
  };

  const closeLightbox = () => {
    lightbox.classList.remove("is-open");
    document.body.classList.remove("has-open-lightbox");
    image.removeAttribute("src");
  };

  for (const item of lightboxItems) {
    item.addEventListener("click", (event) => {
      event.preventDefault();
      const gallery = item.closest("[data-lightbox-gallery]");
      activeItems = Array.from(gallery.querySelectorAll("[data-lightbox-item]"));
      activeIndex = activeItems.indexOf(item);
      showImage();
      lightbox.classList.add("is-open");
      document.body.classList.add("has-open-lightbox");
      close.focus();
    });
  }

  close.addEventListener("click", closeLightbox);
  previous.addEventListener("click", () => moveLightbox(-1));
  next.addEventListener("click", () => moveLightbox(1));
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  lightbox.addEventListener("pointerdown", (event) => { touchStartX = event.clientX; });
  lightbox.addEventListener("pointerup", (event) => {
    if (touchStartX === null) return;
    const distance = event.clientX - touchStartX;
    touchStartX = null;
    if (Math.abs(distance) > 45) moveLightbox(distance < 0 ? 1 : -1);
  });
  document.addEventListener("keydown", (event) => {
    if (!lightbox.classList.contains("is-open")) return;
    if (event.key === "Escape") closeLightbox();
    if (event.key === "ArrowLeft") moveLightbox(-1);
    if (event.key === "ArrowRight") moveLightbox(1);
  });
})();
