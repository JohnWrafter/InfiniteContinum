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
const basketPanel = document.querySelector("[data-basket]");
const basketToggle = document.querySelector("[data-basket-toggle]");
const basketCount = document.querySelector("[data-basket-count]");
const basketItems = document.querySelector("[data-basket-items]");
const basketEmpty = document.querySelector("[data-basket-empty]");
const basketTotal = document.querySelector("[data-basket-total]");
const basketClear = document.querySelector("[data-basket-clear]");
const basketNote = document.querySelector(".apparel-basket-note");
const basketStorageKey = "infinite-continuum-apparel-basket";
const formatPrice = (amount) =>
  new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP", maximumFractionDigits: 0 }).format(amount);
let basket = [];
let canPersistBasket = true;

try {
  const savedBasket = window.localStorage.getItem(basketStorageKey);
  if (savedBasket) {
    const parsedBasket = JSON.parse(savedBasket);
    if (Array.isArray(parsedBasket)) {
      basket = parsedBasket.filter(
        (item) =>
          item &&
          typeof item.key === "string" &&
          typeof item.name === "string" &&
          typeof item.color === "string" &&
          typeof item.priceLabel === "string" &&
          Number.isFinite(item.price) &&
          Number.isInteger(item.quantity) &&
          item.quantity > 0 &&
          Array.isArray(item.sizes) &&
          item.sizes.every((size) => typeof size === "string"),
      );
    } else {
      basketNote.textContent = "A saved basket could not be read. New items will be saved in this browser.";
    }
  }
} catch {
  canPersistBasket = false;
  basketNote.textContent = "Browser storage is unavailable; this basket will only last until you leave the page.";
}

const saveBasket = () => {
  if (!canPersistBasket) return;
  try {
    window.localStorage.setItem(basketStorageKey, JSON.stringify(basket));
  } catch {
    canPersistBasket = false;
    basketNote.textContent = "Browser storage is unavailable; this basket will only last until you leave the page.";
  }
};

const renderBasket = () => {
  const itemCount = basket.reduce((total, item) => total + item.quantity, 0);
  basketCount.textContent = String(itemCount);
  basketItems.replaceChildren();
  basketEmpty.hidden = basket.length > 0;
  basketClear.hidden = basket.length === 0;

  basket.forEach((item) => {
    const row = document.createElement("li");
    row.className = "apparel-basket-item";

    const info = document.createElement("div");
    info.className = "apparel-basket-item-info";
    const name = document.createElement("strong");
    name.textContent = `${item.name} · ${item.color}`;
    const details = document.createElement("span");
    details.textContent = `${item.sizes.join(" · ")} — ${item.priceLabel} each`;
    info.append(name, details);

    const controls = document.createElement("div");
    controls.className = "apparel-basket-item-controls";
    const quantity = document.createElement("span");
    quantity.className = "apparel-basket-quantity";
    quantity.textContent = `Qty ${item.quantity}`;
    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "apparel-basket-remove";
    remove.dataset.basketRemove = item.key;
    remove.setAttribute("aria-label", `Remove ${item.name} in ${item.sizes.join(" and ")}`);
    remove.textContent = "Remove";
    controls.append(quantity, remove);

    row.append(info, controls);
    basketItems.append(row);
  });

  const total = basket.reduce((sum, item) => sum + item.price * item.quantity, 0);
  basketTotal.textContent = formatPrice(total);
};

renderBasket();

apparelCards.forEach((card) => {
  card.querySelector("[data-add-to-basket]").addEventListener("click", () => {
    const status = card.querySelector("[data-card-status]");
    const selects = Array.from(card.querySelectorAll(".apparel-size-select"));
    const missingSize = selects.find((select) => !select.value);
    if (missingSize) {
      status.textContent = "Choose a size before adding this item.";
      missingSize.focus();
      return;
    }

    const priceLabel = card.querySelector(".apparel-price").textContent.trim();
    const priceMatch = priceLabel.match(/\d+(?:\.\d{1,2})?/);
    if (!priceMatch) {
      status.textContent = "This item does not have a valid price.";
      return;
    }

    const sizes = selects.map((select) => {
      const component = select.closest(".apparel-size-group");
      const label = component?.querySelector("label")?.textContent.trim();
      const selectedSize = select.options[select.selectedIndex].textContent.trim();
      return label && label !== "Size" ? `${label}: ${selectedSize}` : `Size: ${selectedSize}`;
    });
    const key = JSON.stringify([card.dataset.productId, ...sizes]);
    const item = basket.find((entry) => entry.key === key);

    if (item) {
      item.quantity += 1;
    } else {
      basket.push({
        key,
        name: card.querySelector(".apparel-product-info h3").textContent.trim(),
        color: card.querySelector(".apparel-product-info > div > p").textContent.trim(),
        sizes,
        price: Number(priceMatch[0]),
        priceLabel,
        quantity: 1,
      });
    }

    status.textContent = "Added to basket.";
    basketPanel.hidden = false;
    basketToggle.setAttribute("aria-expanded", "true");
    renderBasket();
    saveBasket();
  });
});

basketItems.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-basket-remove]");
  if (!removeButton) return;

  basket = basket.filter((item) => item.key !== removeButton.dataset.basketRemove);
  renderBasket();
  saveBasket();
});

basketClear.addEventListener("click", () => {
  basket = [];
  renderBasket();
  saveBasket();
});

basketToggle.addEventListener("click", () => {
  const isOpen = basketToggle.getAttribute("aria-expanded") === "true";
  basketToggle.setAttribute("aria-expanded", String(!isOpen));
  basketPanel.hidden = isOpen;
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