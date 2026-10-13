const menuToggle = document.querySelector(".menu-toggle");
const mainNav = document.querySelector(".main-nav");

menuToggle?.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  menuToggle.setAttribute("aria-expanded", String(!isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Open navigation" : "Close navigation");
  mainNav.classList.toggle("is-open", !isOpen);
});

mainNav?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuToggle?.setAttribute("aria-expanded", "false");
    menuToggle?.setAttribute("aria-label", "Open navigation");
    mainNav.classList.remove("is-open");
  });
});

const apparelFilters = document.querySelector(".apparel-filters");
const apparelCards = document.querySelectorAll(".apparel-card");

apparelFilters?.addEventListener("click", (event) => {
  const selectedFilter = event.target.closest("[data-filter]");
  if (!selectedFilter) return;

  const category = selectedFilter.dataset.filter;
  apparelFilters.querySelectorAll("[data-filter]").forEach((filter) => {
    const isActive = filter === selectedFilter;
    filter.classList.toggle("is-active", isActive);
    filter.setAttribute("aria-pressed", String(isActive));
  });

  apparelCards.forEach((card) => {
    card.hidden = category !== "all" && card.dataset.category !== category;
  });
});

const revealObserver = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.14 },
);

document.querySelectorAll(".value-item, .session-card, .studio-grid, .apparel-card").forEach((element) => {
  element.classList.add("reveal");
  revealObserver.observe(element);
});