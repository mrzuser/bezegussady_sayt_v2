// Favorites Logic
let favorites = JSON.parse(localStorage.getItem('bezeg_ussady_favorites')) || [];

document.addEventListener('DOMContentLoaded', () => {
    updateFavoriteIcons();
    if (window.location.pathname === '/halanlarym') {
        renderFavoritesPage();
    }
});

function toggleFavorite(product) {
    const index = favorites.findIndex(item => item.id === product.id);
    const icon = document.getElementById(`fav-icon-${product.id}`);

    if (index === -1) {
        // Add
        favorites.push(product);
        if (icon) {
            icon.classList.remove('far'); // Empty heart
            icon.classList.add('fas');    // Solid heart
            icon.classList.add('text-red-500');
        }
    } else {
        // Remove
        favorites.splice(index, 1);
        if (icon) {
            icon.classList.remove('fas');
            icon.classList.remove('text-red-500');
            icon.classList.add('far');
        }

        // If on favorites page, re-render
        if (window.location.pathname === '/halanlarym') {
            renderFavoritesPage();
        }
    }

    localStorage.setItem('bezeg_ussady_favorites', JSON.stringify(favorites));
}

function updateFavoriteIcons() {
    favorites.forEach(item => {
        const icon = document.getElementById(`fav-icon-${item.id}`);
        if (icon) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            icon.classList.add('text-red-500');
        }
    });
}

function renderFavoritesPage() {
    const container = document.getElementById('favoritesContainer');
    if (!container) return;

    if (favorites.length === 0) {
        container.innerHTML = `
            <div class="text-center text-gray-400 mt-20">
                <i class="far fa-heart text-6xl mb-4 opacity-20"></i>
                <h3 class="text-xl font-medium text-gray-600">Halanlaryňyz boş</h3>
                <p class="mt-2 text-sm">Haryt sahypalaryndan ýürek belgisine basyp goşup bilersiňiz.</p>
                <a href="/satlyk-harytlar" class="mt-8 inline-block bg-amber-600 text-white px-8 py-3 rounded hover:bg-amber-700 transition uppercase font-bold tracking-widest text-xs">Söwda Başla</a>
            </div>
        `;
        return;
    }

    container.innerHTML = `<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        ${favorites.map(product => `
            <div class="bg-white rounded shadow hover:shadow-lg transition border border-gray-100 relative group">
                <button onclick='toggleFavorite(${JSON.stringify(product)})' class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full bg-white/80 flex items-center justify-center hover:bg-white text-red-500 shadow-sm transition">
                    <i class="fas fa-times"></i>
                </button>
                <div class="h-48 overflow-hidden border-b border-gray-50">
                    <img src="${product.image}" class="w-full h-full object-cover transition duration-500 group-hover:scale-110">
                </div>
                <div class="p-4 text-center">
                    <h4 class="font-bold text-gray-800 mb-2 truncate">${product.name}</h4>
                    <p class="text-amber-600 font-bold mb-4">${product.price} TMT</p>
                    <button onclick='addToCart(${JSON.stringify(product)})' class="w-full bg-gray-900 text-white py-2 text-xs font-bold uppercase tracking-widest hover:bg-amber-600 transition">Sebede Goş</button>
                </div>
            </div>
        `).join('')}
    </div>`;
}
