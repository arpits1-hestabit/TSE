let products = [];

async function loadProducts() {
    const res = await fetch("https://dummyjson.com/products");
    const data = await res.json();
    products = data.products;
    displayProducts(products);
}
function displayProducts(list) {
    const container = document.getElementById("product-container");
    container.innerHTML = "";

    list.forEach(p => {
        container.innerHTML += `
                <div class="card">
                    <img src="${p.thumbnail}" alt="${p.title}" />
                    <div class="title">${p.title}</div>
                    <div class="price">$${p.price}</div>
                </div>
            `;
    });
}
document.getElementById("search").addEventListener("input", e => {
    const value = e.target.value.toLowerCase();
    const filtered = products.filter(p =>
        p.title.toLowerCase().includes(value)
    );
    displayProducts(filtered);
});

document.getElementById("sort").addEventListener("change", e => {
    const value = e.target.value;
    let sorted = [...products];

    if (value === "high") {
        sorted.sort((a, b) => b.price - a.price);
    } else if (value === "low") {
        sorted.sort((a, b) => a.price - b.price);
    }

    displayProducts(sorted);
});

document.querySelectorAll(".categories span").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelector(".active").classList.remove("active");
        btn.classList.add("active");

        const cat = btn.dataset.cat;

        if (cat === "all") {
            display(allProducts);
        } else {
            const filtered = allProducts.filter(p => p.category === cat);
            display(filtered);
        }
    });
});

loadProducts();