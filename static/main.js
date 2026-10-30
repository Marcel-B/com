// The page's only script, apart from the line in every page's head that applies a stored colour scheme before anything
// is drawn. It offers the colour scheme switch, fades elements in as they come into view and lets a light follow the
// pointer over the project cards. Everything works without it; with reduced motion only the switch remains.
(() => {
  const root = document.documentElement;
  const motion = !window.matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window;
  if (motion) root.classList.add("js");

  document.addEventListener("DOMContentLoaded", () => {
    setUpTheme();
    if (motion) setUpMotion();
  });

  // System, light or dark. "System" removes the choice, so the stylesheet follows prefers-color-scheme again.
  function setUpTheme() {
    const group = document.querySelector(".theme");
    if (!group) return;
    const colours = { light: "#f6f6f3", dark: "#0e1014" };
    const metas = document.querySelectorAll('meta[name="theme-color"]');
    const show = (choice) => {
      group.querySelectorAll("button").forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.themeChoice === choice));
      });
      metas.forEach((meta) => {
        meta.content = colours[choice] || (meta.media.includes("dark") ? colours.dark : colours.light);
      });
    };
    let stored = null;
    try { stored = localStorage.getItem("theme"); } catch { /* storage blocked: the choice lasts for this page only */ }
    show(stored === "light" || stored === "dark" ? stored : "system");
    group.hidden = false;
    group.addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button) return;
      const choice = button.dataset.themeChoice;
      if (choice === "system") delete root.dataset.theme;
      else root.dataset.theme = choice;
      try {
        if (choice === "system") localStorage.removeItem("theme");
        else localStorage.setItem("theme", choice);
      } catch { /* see above */ }
      show(choice);
    });
  }

  function setUpMotion() {
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
  }
})();
