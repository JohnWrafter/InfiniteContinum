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
const apparelSizeSelects = document.querySelectorAll(".apparel-size-select");

apparelSizeSelects.forEach((select) => {
  const shopLink = select.closest(".apparel-size-control").querySelector("[data-size-link]");

  select.addEventListener("change", () => {
    const variantId = select.value;
    const productUrl = new URL(select.dataset.productUrl);
    const selectedSize = select.options[select.selectedIndex].textContent;

    shopLink.setAttribute("aria-disabled", String(!variantId));
    if (!variantId) {
      shopLink.href = productUrl.toString();
      shopLink.textContent = "Choose size";
      return;
    }

    if (select.dataset.sizeMode === "collection") {
      productUrl.searchParams.set("filter.v.option.size", selectedSize);
      shopLink.href = productUrl.toString();
      shopLink.textContent = `${shopLink.dataset.shopLabel} size ${selectedSize} ↗`;
      return;
    }

    productUrl.searchParams.set("variant", variantId);
    shopLink.href = productUrl.toString();
    shopLink.textContent = `${shopLink.dataset.shopLabel} · ${selectedSize} ↗`;
  });

  shopLink.addEventListener("click", (event) => {
    if (shopLink.getAttribute("aria-disabled") === "true") {
      event.preventDefault();
    }
  });
});

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