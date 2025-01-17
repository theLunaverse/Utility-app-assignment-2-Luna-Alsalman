class Product:
    def __init__(self, name: str, price: float, category: str, stock: int = 10):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def reduce_stock(self):
        self.stock -= 1

class VendingMachine:
    LANGUAGES = {
        'english': {
            'welcome': "Welcome to the Vending Machine!",
            'invalid_choice': "Invalid choice. Please select a valid product number.",
            'insufficient_payment': "Insufficient payment. Please try again.",
            'payment_prompt': "Enter payment amount: $",
            'dispensing': "Dispensing",
            'thank_you': "Thank you for using the vending machine. Goodbye!",
            'another_item': "Would you like to buy another item? (yes/no): "
        },
        'arabic': {
            'welcome': "مرحبا بك في جهاز البيع!",
            'invalid_choice': "خيار غير صحيح. يرجى اختيار رقم منتج صحيح.",
            'insufficient_payment': "الدفع غير كافِ. يرجى المحاولة مرة أخرى.",
            'payment_prompt': "أدخل مبلغ الدفع: $",
            'dispensing': "جاري توزيع",
            'thank_you': "شكراً لاستخدامك جهاز البيع. وداعا!",
            'another_item': "هل تود شراء منتج آخر؟ (نعم/لا): "
        }
    }

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
        self.language = 'english'

    def translate(self, key):
        return self.LANGUAGES[self.language].get(key, key)

    def set_language(self):
        choice = input("Select language (english/arabic): ").strip().lower()
        if choice in self.LANGUAGES:
            self.language = choice
        print(self.translate('welcome'))

    def display_products(self):
        for key, product in self.products.items():
            print(f"{key}: {product.name.capitalize()} - ${product.price:.2f} (Stock: {product.stock})")

    def select_product(self):
        self.display_products()
        try:
            choice = input("Enter the number of the product you want: ").strip()
            return self.products[choice]
        except KeyError:
            print(self.translate('invalid_choice'))
            return self.select_product()

    def process_payment(self, product: Product):
        print(f"{product.name.capitalize()} costs ${product.price:.2f}")
        try:
            payment = float(input(self.translate('payment_prompt')))
            if payment < product.price:
                print(self.translate('insufficient_payment'))
                return self.process_payment(product)
            print(f"{self.translate('dispensing')} {product.name.capitalize()}! Change: ${payment - product.price:.2f}")
            product.reduce_stock()
        except ValueError:
            print("Invalid payment input. Please enter a valid number.")
            return self.process_payment(product)

    def run(self):
        self.set_language()
        while True:
            product = self.select_product()
            self.process_payment(product)
            if input(self.translate('another_item')).strip().lower() != 'yes':
                print(self.translate('thank_you'))
                break

if __name__ == "__main__":
    vending_machine = VendingMachine()
    vending_machine.run()
