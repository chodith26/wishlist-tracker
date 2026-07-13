function loadWishlist() {
    fetch('/api/wishlist')
        .then(response => response.json())
        .then(items => {
            const grid = document.getElementById('wishlist-grid');
            grid.innerHTML = '';

            if (items.length === 0) {
                grid.innerHTML = '<p class="empty-msg">Your wishlist is empty. Add something above!</p>';
                return;
            }

            items.forEach(item => {
                const card = document.createElement('div');
                card.classList.add('card');
                card.innerHTML = `
                    <p class="item-name">${item.name}</p>
                    <p class="item-price">${item.price}</p>
                    <span class="item-category">${item.category}</span>
                    <p class="item-date">Added: ${item.added_on}</p>
                    <form action="/delete/${item.id}" method="POST">
                        <button type="submit" class="delete-btn">Remove</button>
                    </form>
                `;
                grid.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Fetch error:', error);
            document.getElementById('wishlist-grid').innerHTML =
                '<p class="empty-msg">Failed to load items. Please refresh.</p>';
        });
}

loadWishlist();