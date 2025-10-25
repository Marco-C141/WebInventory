// Get all html elements and create a list to represent the client's cart
const searchInput = document.getElementById('product-search');
const searchResults = document.getElementById('search-results');
const cartItemsContainer = document.getElementById('pos-cart-items-container');
const totalPriceEl = document.getElementById('total-price');

let cart = []

// Search functionality
searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    searchResults.innerHTML = ''; // Clear previous results

    if (query.length === 0) {
        searchResults.style.display = "none";
        return;
    }

    const filteredProducts = allProducts.filter(p => p.name.toLowerCase().includes(query));
    const limitedResults = filteredProducts.slice(0, 5);

    limitedResults.forEach(product => {
        const div = document.createElement('div');
        div.className = 'search-item';
        div.dataset.productId = product.id; // Store the ID for easy access

        const imageUrl = product.img;

        div.innerHTML = `
            <div class="search-item-img-container" >
                <img src="${imageUrl}" class="search-item-img">
            </div>
            <span class="search-item-name">${product.name}</span>
            <span class="search-item-price">\$${product.price}</span>
        `;
        searchResults.appendChild(div);
    });

    searchResults.style.display = "block";
});

// --- LISTENER 1: Handles direct text input ---
cartItemsContainer.addEventListener('change', (e) => {
    if (e.target.classList.contains('quantity-input')) {
        const productId = parseInt(e.target.dataset.id);
        let newQuantity = parseInt(e.target.value);
        const cartItem = cart.find(item => item.id === productId);

        if (isNaN(newQuantity) || newQuantity < 1) {
            newQuantity = 1;
        } else if (newQuantity > cartItem.stock) {
            showAlert("Cantidad insuficiente" ,`Solo hay ${cartItem.stock} unidades disponibles.`);
            newQuantity = cartItem.stock;
        }

        cartItem.quantity = newQuantity;
        renderCart(); // Re-render to ensure UI consistency
    }
});

// --- LISTENER 2: Handles all button clicks (+, -, Remove) ---
cartItemsContainer.addEventListener('click', (e) => {
    const target = e.target;
    const productId = parseInt(target.dataset.id);
    const cartItem = cart.find(item => item.id === productId);

    if (target.classList.contains('increase-btn')) {
        if (cartItem.quantity < cartItem.stock) {
            cartItem.quantity++;
            renderCart();
        } else {
            showAlert("Error", 'No hay suficientes unidades!');
        }
    } else if (target.classList.contains('decrease-btn')) {
        if (cartItem.quantity > 1) {
            cartItem.quantity--;
            renderCart();
        }
    } else if (target.classList.contains('cart-item-rm')) {
        cart = cart.filter(item => item.id !== productId);
        renderCart();
    }
});

function renderCart() {
    cartItemsContainer.innerHTML = '';
    let totalPrice = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        totalPrice += itemTotal;

        const imageUrl = item.img

        const cartItemDiv = document.createElement('div');
        cartItemDiv.className = 'cart-item';
        cartItemDiv.innerHTML = `
            <div class="cart-item-left">
                <div class="cart-item-img-container">
                    <img src="${imageUrl}" alt="${item.name}" class="cart-item-img">
                </div>
                <span class="cart-item-name">${item.name}</span>
            </div>
            <div class="cart-item-right">
                <div class="quantity-controls">
                    <button data-id="${item.id}" class="quantity-btn decrease-btn"><</button>
                    <input
                        type="number"
                        class="quantity-input"
                        value="${item.quantity}"
                        min="1"
                        max="${item.stock}"
                        data-id="${item.id}"
                    >
                    <button data-id="${item.id}" class="quantity-btn increase-btn">></button>
                </div>
                <button data-id="${item.id}" class="cart-item-rm">Quitar</button>
                <span class="cart-item-price">$${itemTotal.toFixed(2)}</span>
            </div>
        `;
        cartItemsContainer.appendChild(cartItemDiv);
    });

    totalPriceEl.textContent = `$${totalPrice.toFixed(2)}`;
}



// Add item to cart when search result is clicked
searchResults.addEventListener('click', (e) => {
    const searchResultItem = e.target.closest('.search-item');

    // If a matching parent was found
    if (searchResultItem) {
        const productId = parseInt(searchResultItem.dataset.productId);
        const product = allProducts.find(p => p.id === productId);

        // Check if item is already in cart
        const cartItem = cart.find(item => item.id === productId);
        if (cartItem) {
            cartItem.quantity++; // Increase quantity
        } else {
            cart.push({ ...product, quantity: 1 }); // Add new item
        }

        renderCart();
    }

    // Hide input and results
    searchInput.value = '';
    searchResults.innerHTML = '';
    searchResults.style.display = "none";
});


// Confirm the sale function

const confirmSaleBtn = document.getElementById('confirm-sale');

confirmSaleBtn.addEventListener('click', async () => {
    if (cart.length === 0) {
        showAlert("Error", '¡El carro está vacío!');
        return;
    }

    const response = await fetch('process-sale/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cart: cart })
    });

    const result = await response.json();

    if (result.status === 'success') {
        showAlert("","Venta realizada exitosamente");

        // Update stock levels in the main 'allProducts' list
        result.updated_products.forEach(updatedProduct => {
            const productInList = allProducts.find(p => p.id === updatedProduct.id);
            if (productInList) {
                productInList.stock = updatedProduct.new_stock;
            }
        });

        // 2. Filter out any products that are now depleted
        allProducts = allProducts.filter(p => p.stock > 0);

        cart = []; // Clear the cart
        renderCart(); // Update the display
    } else {
        showAlert("Error",`Error: ${result.message}`);
    }
});