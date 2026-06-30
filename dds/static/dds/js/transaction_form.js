const meta = document.getElementById("tx-meta");

const initCatId = meta.dataset.initCat;
const initSubId = meta.dataset.initSub;
const initTypeId = meta.dataset.initType;

const typeSelect = document.getElementById("id_transaction_type");
const catSelect = document.getElementById("id_category");
const subSelect = document.getElementById("id_subcategory");

async function loadCategories(typeId) {
    const url = new URL("/api/categories/", window.location.origin);
    if (typeId) url.searchParams.append("type_id", typeId);

    const res = await fetch(url);
    const data = await res.json();

    const prev = catSelect.value;

    catSelect.replaceChildren(
        new Option("Выберите категорию", ""),
        ...data.map(c => new Option(c.label, c.id))
    );

    if ([...catSelect.options].some(o => o.value === prev)) {
        catSelect.value = prev;
    } else {
        catSelect.value = "";
    }
}

async function loadSubcategories(typeId, catId) {
    const url = new URL("/api/subcategories/", window.location.origin);
    if (typeId) url.searchParams.append("type_id", typeId);
    if (catId) url.searchParams.append("category_id", catId);

    const res = await fetch(url);
    const data = await res.json();

    const prev = subSelect.value;

    subSelect.replaceChildren(
        new Option("Выберите подкатегорию", ""),
        ...data.map(s => new Option(s.label, s.id))
    );

    if ([...subSelect.options].some(o => o.value === prev)) {
        subSelect.value = prev;
    } else {
        subSelect.value = "";
    }
}

typeSelect.addEventListener("change", async () => {
    const typeId = typeSelect.value;

    await loadCategories(typeId);
    await loadSubcategories(typeId, "");
});

catSelect.addEventListener("change", async () => {
    await loadSubcategories(typeSelect.value, catSelect.value);
});

subSelect.addEventListener("change", async () => {
    const subId = subSelect.value;
    if (!subId) return;

    const res = await fetch(`/api/categories/?subcategory_id=${subId}`);
    const data = await res.json();

    if (data.length) {
        catSelect.value = String(data[0].id);
    }
});

const amountInput = document.querySelector('input[name="amount"]');

amountInput.addEventListener("input", () => {
    amountInput.value = amountInput.value
        .replace(/[^0-9.,]/g, "")
        .replace(/(.*)[.,](.*)[.,]/g, "$1.$2");
});

amountInput.addEventListener("paste", (e) => {
    const text = (e.clipboardData || window.clipboardData).getData("text");

    if (/[^0-9.,]/.test(text)) {
        e.preventDefault();
    }
});

(async function init() {
    await loadCategories(initTypeId);

    if (initCatId) {
        catSelect.value = initCatId;
        await loadSubcategories(initTypeId, initCatId);
    }

    if (initSubId) {
        subSelect.value = initSubId;
    }
})();