// The page's only script: fades elements in as they come into view and lets a light follow the pointer over the
// project cards. Everything works without it; with reduced motion it does nothing.
(() => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("js");

  document.addEventListener("DOMContentLoaded", () => {
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("seen");
        observer.unobserve(entry.target);
      }
    }, { rootMargin: "0px 0px -40px 0px" });
    const pending = new Set(document.querySelectorAll(".reveal"));
    pending.forEach((element) => {
      element.style.transitionDelay = `${[...element.parentElement.children].indexOf(element) % 3 * 70}ms`;
      observer.observe(element);
    });
    // A fast jump (the end key, an anchor) can pass elements without the observer seeing them; anything above the
    // bottom of the window counts as seen.
    let queued = false;
    const sweep = () => {
      queued = false;
      for (const element of pending) {
        if (element.classList.contains("seen") || element.getBoundingClientRect().top < window.innerHeight) {
          element.classList.add("seen");
          pending.delete(element);
        }
      }
      if (!pending.size) window.removeEventListener("scroll", onScroll);
    };
    const onScroll = () => { if (!queued) { queued = true; requestAnimationFrame(sweep); } };
    window.addEventListener("scroll", onScroll, { passive: true });

    document.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("pointermove", (event) => {
        const box = card.getBoundingClientRect();
        card.style.setProperty("--x", `${event.clientX - box.left}px`);
        card.style.setProperty("--y", `${event.clientY - box.top}px`);
      });
    });
  });
})();
