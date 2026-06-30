const typeSelect = document.getElementById("filter_type");
const catSelect = document.getElementById("filter_category");
const subSelect = document.getElementById("filter_subcategory");

async function loadCategories(typeId) {
    const url = new URL("/api/categories/", window.location.origin);
    if (typeId) url.searchParams.append("type_id", typeId);

    const res = await fetch(url);
    const data = await res.json();

    const prev = catSelect.value;

    catSelect.replaceChildren(
        new Option("Все категории", ""),
        ...data.map(c => new Option(c.label, c.id))
    );

    catSelect.value = [...catSelect.options].some(o => o.value === prev)
        ? prev
        : "";
}

async function loadSubcategories(typeId, catId) {
    const url = new URL("/api/subcategories/", window.location.origin);
    if (typeId) url.searchParams.append("type_id", typeId);
    if (catId) url.searchParams.append("category_id", catId);

    const res = await fetch(url);
    const data = await res.json();

    const prev = subSelect.value;

    subSelect.replaceChildren(
        new Option("Все подкатегории", ""),
        ...data.map(s => new Option(s.label, s.id))
    );

    subSelect.value = [...subSelect.options].some(o => o.value === prev)
        ? prev
        : "";
}

typeSelect?.addEventListener("change", async () => {
    const typeId = typeSelect.value;

    await loadCategories(typeId);
    await loadSubcategories(typeId, "");
});

catSelect?.addEventListener("change", async () => {
    await loadSubcategories(typeSelect.value, catSelect.value);
});
subSelect?.addEventListener("change", async () => {
    const subId = subSelect.value;
    if (!subId) return;

    const res = await fetch(`/api/categories/?subcategory_id=${subId}`);
    const data = await res.json();

    if (data.length) {
        catSelect.value = String(data[0].id);
    }
});

(async function init() {
    const initType = typeSelect?.value || "";
    const initCat = catSelect?.value || "";
    const initSub = subSelect?.value || "";

    if (initType) {
        await loadCategories(initType);
    }

    if (initCat) {
        await loadSubcategories(initType, initCat);
    }

    if (initSub) {
        subSelect.value = initSub;
    }
})();