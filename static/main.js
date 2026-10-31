// The page's only script, apart from the line in every page's head that applies a stored colour scheme before anything
// is drawn. It offers the colour scheme switch, puts a copy button on every code block, fades elements in as they come
// into view and lets a light follow the pointer over the project cards. Everything works without it; with reduced motion
// the switch and the copy buttons remain.
(() => {
  const root = document.documentElement;
  const motion = !window.matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window;
  if (motion) root.classList.add("js");

  document.addEventListener("DOMContentLoaded", () => {
    setUpTheme();
    setUpCopy();
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

  // A button on every code block that puts its text on the clipboard, ready for a terminal or an editor. Only where the
  // browser offers the clipboard (https or localhost); otherwise the text can still be selected by hand.
  function setUpCopy() {
    if (!navigator.clipboard || !window.isSecureContext) return;
    const english = root.lang === "en";
    const words = english
      ? { copy: "Copy", copied: "Copied", failed: "Not copied", label: "Copy code to the clipboard" }
      : { copy: "Kopieren", copied: "Kopiert", failed: "Nicht kopiert", label: "Code in die Zwischenablage kopieren" };
    const icon = '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5">' +
      '<rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 5.5v-2a1.5 1.5 0 0 0-1.5-1.5H4a1.5 1.5 0 0 0-1.5 1.5v5A1.5 1.5 0 0 0 4 10h1.5"/></svg>';
    document.querySelectorAll(".prose pre").forEach((pre) => {
      const code = pre.querySelector("code") || pre;
      const box = document.createElement("div");
      box.className = "code";
      pre.replaceWith(box);
      box.append(pre);
      const button = document.createElement("button");
      button.type = "button";
      button.className = "copy";
      button.setAttribute("aria-label", words.label);
      const text = document.createElement("span");
      text.setAttribute("aria-live", "polite");
      text.textContent = words.copy;
      button.innerHTML = icon;
      button.append(text);
      box.append(button);
      let timer;
      button.addEventListener("click", async () => {
        let state = "copied";
        try {
          await navigator.clipboard.writeText(code.textContent.replace(/\n+$/, ""));
        } catch {
          state = "failed";
        }
        button.dataset.state = state;
        text.textContent = words[state];
        clearTimeout(timer);
        timer = setTimeout(() => {
          delete button.dataset.state;
          text.textContent = words.copy;
        }, 2000);
      });
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
