from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get['cart']

        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_post_price(self):
        total_post_price = sum(item['quantity'] * item['weight'] for item in self.cart.values())
        if total_post_price < 1000:
            return 100
        if 1000 < total_post_price < 2000:
            return 200
        if total_post_price < 2000:
            return 3000

    def get_total_price(self):
        total_price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return total_price

    def get_final_price(self):
        final_price = self.get_total_price() + self.get_post_price()
        return final_price

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()
        for product in products:
            cart_dict[str(product.id)]['product'] = product

        for item in self.cart.values():
            yield item


    def save(self):
        self.session.modified = True
