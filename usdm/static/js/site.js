(() => {
  "use strict";

  const sections = Array.from(document.querySelectorAll("[data-parallax]"));
  if (!sections.length) {
    return;
  }

  let frameRequested = false;

  const render = () => {
    const viewportHeight = window.innerHeight;
    const scrollTop = window.scrollY;

    for (const section of sections) {
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

  const requestRender = () => {
    if (!frameRequested) {
      frameRequested = true;
      window.requestAnimationFrame(render);
    }
  };

  window.addEventListener("scroll", requestRender, { passive: true });
  window.addEventListener("resize", requestRender);
  requestRender();
})();
