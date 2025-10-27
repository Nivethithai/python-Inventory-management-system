const API_URL = "http://127.0.0.1:8000/products";
let editingId = null;

// 🟢 Handle Add or Update Product
document.getElementById("productForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    name: document.getElementById("name").value,
    sku: document.getElementById("sku").value,
    description: document.getElementById("description").value,
    price: parseFloat(document.getElementById("price").value),
    quantity: parseInt(document.getElementById("quantity").value),
    is_active: true
  };

  try {
    if (editingId) {
      await fetch(`${API_URL}/${editingId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      editingId = null;
      document.querySelector("button[type='submit']").textContent = "Add Product";
    } else {
      await fetch(API_URL + "/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
    }

    e.target.reset();
    loadProducts();
  } catch (err) {
    console.error("Error saving product:", err);
  }
});

// 🧾 Load All Products
async function loadProducts() {
  const res = await fetch(API_URL + "/");
  const products = await res.json();
  const table = document.getElementById("productTable");
  table.innerHTML = "";


        products.forEach((p, index) => {
    const row = `
        <tr>
            <td>${index + 1}</td> <!-- Serial Number -->
        <td>${p.name}</td>
        <td>${p.sku}</td>
        <td>${p.price}</td>
        <td>${p.quantity}</td>
        <td>
          <button class="btn btn-sm btn-info" onclick="viewProduct(${p.id})">View</button>
          <button class="btn btn-sm btn-warning" onclick="editProduct(${p.id})">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="deleteProduct(${p.id})">Delete</button>
        </td>
      </tr>
    `;
    table.innerHTML += row;
  });
}

// 🟣 Delete Product
async function deleteProduct(id) {
  if (!confirm("Are you sure you want to delete this product?")) return;
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  loadProducts();
}

// 🟡 Edit Product
async function editProduct(id) {
  const res = await fetch(`${API_URL}/${id}`);
  const product = await res.json();

  document.getElementById("name").value = product.name;
  document.getElementById("sku").value = product.sku;
  document.getElementById("description").value = product.description;
  document.getElementById("price").value = product.price;
  document.getElementById("quantity").value = product.quantity;

  editingId = id;
  document.querySelector("button[type='submit']").textContent = "Update Product";
}

// 🔵 View Product (Bootstrap Modal)
async function viewProduct(id) {
  const res = await fetch(`${API_URL}/${id}`);
  const product = await res.json();

  document.getElementById("viewName").textContent = product.name;
  document.getElementById("viewSKU").textContent = product.sku;
  document.getElementById("viewDescription").textContent = product.description;
  document.getElementById("viewPrice").textContent = product.price;
  document.getElementById("viewQuantity").textContent = product.quantity;
  document.getElementById("viewStatus").textContent = product.is_active ? "Active" : "Inactive";

  const viewModal = new bootstrap.Modal(document.getElementById("viewModal"));
  viewModal.show();
}

loadProducts();
