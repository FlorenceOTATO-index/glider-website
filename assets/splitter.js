(function () {
  // Re-attach logic whenever Dash re-renders:
  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  function attachSplitter() {
    // Try repeatedly until elements exist (Dash renders asynchronously)
    const MAX_TRIES = 200;
    let tries = 0;

    const tick = () => {
      const container = document.getElementById("split-container");
      const left = document.getElementById("ma-panel");
      const right = document.getElementById("mi-panel");
      const bar = document.getElementById("dragbar");

      if (!container || !left || !right || !bar) {
        if (tries++ < MAX_TRIES) {
          requestAnimationFrame(tick);
        }
        return;
      }

      // Prevent double-binding
      if (bar._splitterAttached) return;
      bar._splitterAttached = true;

      let isDragging = false;

      function onMove(clientX) {
        const rect = container.getBoundingClientRect();
        const x = clientX - rect.left;

        // keep a minimum for each panel
        const min = 150;
        const max = rect.width - min;
        if (x <= min || x >= max) return;

        // lock left width, let right fill the rest
        left.style.flex = "none";
        left.style.width = x - bar.offsetWidth / 2 + "px";
        right.style.flex = "1";
      }

      // Mouse events
      bar.addEventListener("mousedown", (e) => {
        isDragging = true;
        document.body.style.cursor = "col-resize";
        bar.classList.add("dragging");
        e.preventDefault();
      });

      document.addEventListener("mousemove", (e) => {
        if (!isDragging) return;
        onMove(e.clientX);
      });

      document.addEventListener("mouseup", () => {
        if (!isDragging) return;
        isDragging = false;
        document.body.style.cursor = "";
        bar.classList.remove("dragging");
      });

      // Touch events
      bar.addEventListener("touchstart", (e) => {
        isDragging = true;
        bar.classList.add("dragging");
      });

      document.addEventListener("touchmove", (e) => {
        if (!isDragging) return;
        if (e.touches && e.touches[0]) {
          onMove(e.touches[0].clientX);
        }
      }, { passive: true });

      document.addEventListener("touchend", () => {
        if (!isDragging) return;
        isDragging = false;
        bar.classList.remove("dragging");
      });
    };

    tick();
  }

  // Attach on load
  ready(attachSplitter);

  // Re-attach after Dash hot reloads or route changes
  // Observe body mutations (cheap and reliable for Dash multipage)
  const observer = new MutationObserver(() => attachSplitter());
  observer.observe(document.documentElement || document.body, { childList: true, subtree: true });
})();
