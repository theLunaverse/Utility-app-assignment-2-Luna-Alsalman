class Product:
    def __init__(self, name: str, price: float, category: str, stock: int = 10):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def reduce_stock(self):
        self.stock -= 1

class VendingMachine:
    def __init__(self):
        self.products = {
            "1": Product("orange juice", 2.99, "Drinks"),
            "2": Product("apple juice", 2.99, "Drinks"),
            "3": Product("salty chips", 1.50, "Snacks"),
            "4": Product("spicy chips", 1.50, "Snacks"),
            "5": Product("kitkat", 2.50, "Chocolate"),
            "6": Product("water", 1.25, "Drinks"),
            "7": Product("energy drink", 3.25, "Drinks"),
            "8": Product("chocolate bar", 2.75, "Chocolate"),
            "9": Product("cookies", 1.75, "Snacks")
        }

    def display_products(self):
        for key, product in self.products.items():
            print(f"{key}: {product.name.capitalize()} - ${product.price:.2f} (Stock: {product.stock})")

    def select_product(self):
        self.display_products()
        choice = input("Enter the number of the product you want: ").strip()
        return self.products[choice]

    def process_payment(self, product: Product):
        print(f"{product.name.capitalize()} costs ${product.price:.2f}")
        payment = float(input("Enter payment amount: $"))
        print(f"Dispensing {product.name.capitalize()}! Change: ${payment - product.price:.2f}")
        product.reduce_stock()

    def run(self):
        while True:
            product = self.select_product()
            self.process_payment(product)
            if input("Would you like to buy another item? (yes/no): ").strip().lower() != 'yes':
                print("Thank you for using the vending machine. Goodbye!")
                break

if __name__ == "__main__":
    vending_machine = VendingMachine()
    vending_machine.run()