// Cart Logic
// Initialize cart from localStorage
let cart = JSON.parse(localStorage.getItem('bezeg_ussady_cart')) || [];

// Update UI on load
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
});

function addToCart(product) {
    // Check if product already exists
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    
    saveCart();
    updateCartUI();
    openCartModal(); // Optional: open cart when added
    
    // Show feedback (could be a toast, but using simple alert for now or just the modal opening)
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartUI();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            saveCart();
            updateCartUI();
        }
    }
}

function saveCart() {
    localStorage.setItem('bezeg_ussady_cart', JSON.stringify(cart));
}

function updateCartUI() {
    // Update Badge
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountEl = document.getElementById('cartCount');
    if (cartCountEl) {
        cartCountEl.innerText = totalItems;
        cartCountEl.style.display = totalItems > 0 ? 'flex' : 'none';
    }

    // Update Modal Content
    const container = document.getElementById('cartItemsContainer');
    const totalEl = document.getElementById('cartTotal');
    
    if (container && totalEl) {
        let totalStats = 0;
        
        if (cart.length === 0) {
            container.innerHTML = `
                <div class="text-center text-gray-400 mt-20 flex flex-col items-center">
                    <i class="fas fa-shopping-cart text-6xl mb-4 opacity-20"></i>
                    <p class="font-medium">Sebet boş</p>
                    <button onclick="closeCartModal()" class="mt-4 text-amber-600 hover:underline text-sm uppercase font-bold">Söwdany dowam et</button>
                </div>
            `;
            totalEl.innerText = '0 TMT';
        } else {
            container.innerHTML = cart.map(item => {
                totalStats += item.price * item.quantity;
                return `
                    <div class="flex gap-4 mb-6 pb-6 border-b border-dashed border-gray-200 last:border-0 animation-fade-in">
                        <div class="w-20 h-20 flex-shrink-0 bg-gray-100 rounded-md overflow-hidden border border-gray-200">
                            <img src="${item.image}" class="w-full h-full object-cover">
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-gray-800 text-sm mb-1 line-clamp-2">${item.name}</h4>
                            <p class="text-amber-600 font-bold mb-2">${item.price} TMT</p>
                            
                            <div class="flex items-center justify-between">
                                <div class="flex items-center border border-gray-300 rounded-md">
                                    <button onclick="updateQuantity('${item.id}', -1)" class="px-2 py-1 text-gray-600 hover:bg-gray-100">-</button>
                                    <span class="px-2 text-xs font-bold text-gray-800 min-w-[20px] text-center">${item.quantity}</span>
                                    <button onclick="updateQuantity('${item.id}', 1)" class="px-2 py-1 text-gray-600 hover:bg-gray-100">+</button>
                                </div>
                                <button onclick="removeFromCart('${item.id}')" class="text-xs text-red-400 hover:text-red-600 uppercase font-bold tracking-wider">Poz</button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            totalEl.innerText = `${totalStats} TMT`;
        }
    }
}

// Modal Functions
function openCartModal() {
    const modal = document.getElementById('cartModal');
    const sidebar = document.getElementById('cartSidebar');
    modal.classList.remove('hidden');
    // Small delay to allow display:block to apply before transition
    setTimeout(() => {
        sidebar.classList.remove('translate-x-full');
    }, 10);
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

function closeCartModal() {
    const modal = document.getElementById('cartModal');
    const sidebar = document.getElementById('cartSidebar');
    sidebar.classList.add('translate-x-full');
    setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }, 300);
}

// Checkout Function - Called from checkout page
function loadCheckoutItems() {
    const container = document.getElementById('checkoutItems');
    const totalEl = document.getElementById('checkoutTotal');
    const inputField = document.getElementById('cartDataInput');
    
    if (container && totalEl && inputField) {
        if (cart.length === 0) {
            window.location.href = '/satlyk-harytlar'; // Redirect if empty
            return;
        }

        let totalStats = 0;
        container.innerHTML = cart.map(item => {
            const subtotal = item.price * item.quantity;
            totalStats += subtotal;
            return `
                <div class="flex justify-between items-center py-4 border-b border-gray-100 text-sm">
                    <div class="flex items-center gap-4">
                        <div class="relative">
                            <img src="${item.image}" class="w-12 h-12 rounded object-cover border">
                            <span class="absolute -top-2 -right-2 bg-amber-600 text-white text-[10px] w-5 h-5 flex items-center justify-center rounded-full font-bold">${item.quantity}</span>
                        </div>
                        <span class="font-medium text-gray-700">${item.name}</span>
                    </div>
                    <span class="font-bold text-gray-900">${subtotal} TMT</span>
                </div>
            `;
        }).join('');
        
        // Add total row
        container.innerHTML += `
             <div class="flex justify-between items-center py-4 text-base font-bold text-gray-900 mt-2">
                <span>Jemi Töleg</span>
                <span class="text-amber-600 text-xl">${totalStats} TMT</span>
             </div>
        `;

        // Set form data
        inputField.value = JSON.stringify(cart);
    }
}

// Clear cart after successful order
if (window.location.pathname.includes('/order-success')) {
    localStorage.removeItem('bezeg_ussady_cart');
}
