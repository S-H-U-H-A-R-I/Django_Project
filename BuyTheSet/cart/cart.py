from store.models import Product


class Cart:
    def __init__(self, request):
        # Initialize the Cart object with the given request.
        # The request object contains the session information.
        self.session = request.session
        
        # Get the cart from the session using the 'session_key' key.
        # If the 'session_key' key is not present in the session,
        # use an empty dictionary as the default value.
        self.cart = self.session.get('session_key', {})
        if not self.cart:  # If the cart is empty, initialize it with an empty dictionary.
            self.session['session_key'] = self.cart
            
    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:     # If the product is not already in the cart, add it with a quantity of 0
            self.cart[product_id] = 0
        self.cart[product_id] += quantity   # Increment the quantity of the product in the cart by the given quantity
        self.session.modified = True        # Indicate that the session has been modified
        
    def __len__(self):
        """
        This method returns the length of the user's cart.
        The `len` method is a special method in Python that is called when the built-in `len` function is used on an instance of this class.
        By implementing this method, we can define the behavior of `len` for instances of this class.
        In this case, we return the length of the `cart` attribute, which is a list of items in the user's cart.
        """
        return len(self.cart)    
    
    def get_products(self):
        # Retrieve the keys (product IDs) from the cart object
        product_ids = self.cart.keys()
        
        # Filter the Product model to only include objects with IDs in the product_ids list
        # The '__in' lookup type is used to filter the queryset based on a list of values
        products = Product.objects.filter(id__in=product_ids)

        # Return the filtered queryset of Product objects
        return products
    
    def get_quantity(self):
        quantities = self.cart
        return quantities

    def cart_total(self):
        # Get the list of products in the cart
        products = self.get_products()
        
        # Initialize the total cost to 0
        total = 0
        
        # Iterate through each product in the cart
        for product in products:
            # Check if the product is on sale
            if product.is_sale:
                # If it is on sale, calculate the cost of each individual product
                # and add it to the total
                total += product.sale_price * self.cart[str(product.id)]
            else:
                # If not on sale, use the regular price
                total += product.price * self.cart[str(product.id)]
        print(total)
        # Return the total cost of all products in the cart
        return total
    
    def update(self, product, quantity):
        """
        Update the quantity of the specified product in the cart.

        :param product: The product instance or identifier.
        :param quantity: The new quantity for the product.
        """
        product_id = str(product)
        product_qty = int(quantity)  
        
        ourcart = self.cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True
            
        thing = self.cart
        return thing
    
    
            
        