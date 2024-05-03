function displayAlert(message, alertType) {
    const alertContainer = document.getElementById('alert-container');
    const alertElement = document.createElement('div');
    alertElement.classList.add('alert', `alert-${alertType}`, 'cart-message', 'pt-2', 'pb-3');
    alertElement.setAttribute('role', 'alert');
    alertElement.setAttribute('data-bs-autohide', 'true');
    alertElement.innerHTML = `
        <p class="mb-0">${message}</p>
        <div class="progress position-absolute bottom-0 start-0 end-0 mx-3 mb-1" style="height: 5px;">
            <div class="progress-bar custom-bg-${alertType}" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
    `;
    alertContainer.appendChild(alertElement);

    // Start the progress bar animation
    const progressBar = alertElement.querySelector('.progress-bar');
    let width = 100;
    const animationDuration = 5000;
    const animationInterval = 30;
    const animationStep = (100 / animationDuration) * animationInterval;

    const animationTimer = setInterval(() => {
        if (width <= 0) {
            clearInterval(animationTimer);
            alertElement.remove();
        } else {
            width -= animationStep;
            progressBar.style.width = width + '%';
        }
    }, animationInterval);

    // Remove the alert when the user navigatest away from the page
    window.addEventListener('beforeunload', () => {
        alertElement.remove();
    });
}


// Mobile Menu
document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.getElementById('menuButton');
    var mobileMenu = document.getElementById('mobileMenu');
    var mobileMenuClose = document.getElementById('mobileMenuClose');
  
    menuButton.addEventListener('click', function(e) {
        e.preventDefault();
        mobileMenu.style.display = 'block';
        setTimeout(function() {
            mobileMenu.classList.add('show');
        }, 10);
        document.body.style.overflow = 'hidden';
    });
  
    mobileMenuClose.addEventListener('click', function() {
        mobileMenu.classList.remove('show');
        document.body.style.overflow = 'auto';
    });
  
    mobileMenu.addEventListener('click', function(e) {
        if (e.target === mobileMenu) {
            mobileMenu.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
    });
  
    mobileMenu.addEventListener('transitionend', function() {
        if (!mobileMenu.classList.contains('show')) {
            mobileMenu.style.display = 'none';
        }
    });
});


// Scroll to top button


// Cart Sidebar
document.addEventListener('DOMContentLoaded', function() {
    var cartLink = document.querySelector('.cart-link');
    var cartOffcanvas = document.getElementById('cartOffcanvas');

    cartLink.addEventListener('click', function(e) {
        e.preventDefault();
        var offcanvasInstance = new bootstrap.Offcanvas(cartOffcanvas);
        offcanvasInstance.show();

        // Load cart items and total
        fetch('/cart/items/', {
            method: 'GET',
            headers: {
                'X-requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            var cartItemsContainer = document.getElementById('cartItems');
            cartItemsContainer.innerHTML = ''; // Clear existing cart items
            data.cart_items.forEach(item => {
                var itemHtml = `
                    <div class="cart-item"> 
                    <img src="${item.product.image_url}" alt="${item.product.name}" class="cart-item-image">
                        <div class="cart-item-details">
                            <h6>${item.product.name}</h6> 
                            <p>Quantity: ${item.quantity}</p> 
                            <p>Price: R${item.product.price}</p> 
                        </div>
                    </div>
                `;
                cartItemsContainer.insertAdjacentHTML('beforeend', itemHtml);
            });
            document.getElementById('cartTotal').textContent = data.cart_total;
        })
        .catch(error => {
            console.error('Error loading cart items:', error);
        });
    });

    // Remove the backdrop when the offcanvas is hidden
    cartOffcanvas.addEventListener('hidden.bs.offcanvas', function() {
        var backdrop = document.querySelector('.offcanvas-backdrop');
        if(backdrop) {
            backdrop.remove();
        }
    });
});


// Reload page if it is loaded from back/forward cache
window.addEventListener('pageshow', function(event) {
    if (event.persisted || (window.performance && window.performance.getEntriesByType('navigation')[0].type === 'back_forward')) {
        location.reload();
    }
});








