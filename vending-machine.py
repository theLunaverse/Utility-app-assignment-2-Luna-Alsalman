import random
from typing import Dict, Tuple, List

class Product:
    def __init__(self, name: str, price: float, category: str, stock: int = 10):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def is_available(self) -> bool:
        return self.stock > 0

    def reduce_stock(self):
        self.stock -= 1

class VendingMachine:
    LANGUAGES = {
        'english': {
            'welcome': "Welcome to the Advanced Vending Machine!",
            'invalid_choice': "Invalid product number. Please try again.",
            'sold_out': "Sorry, {product} is SOLD OUT!",
            'insufficient_payment': "Insufficient payment. You need at least ${amount:.2f}",
            'payment_prompt': "Enter payment amount: $",
            'thank_you': "Thank you for using the Advanced Vending Machine. Goodbye!",
            'yes_no_prompt': "Would you like to buy another item? (yes/no): ",
            'add_on_prompt': "Would you like to buy an add-on? (yes/no): ",
            'recommended_addons': "Recommended add-ons:",
            'no_stock': "Stock: {stock}",
            'select_product': "Enter the number of the product you want: ",
            'enter_payment': "{product} costs ${price:.2f}",
        },
        'arabic': {
            'welcome': "مرحبًا بك في جهاز البيع المتقدم!",
            'invalid_choice': "رقم المنتج غير صالح. يرجى المحاولة مرة أخرى.",
            'sold_out': "عذرًا، {product} نفد من المخزون!",
            'insufficient_payment': "المبلغ غير كافٍ. تحتاج إلى دفع على الأقل ${amount:.2f}",
            'payment_prompt': "أدخل مبلغ الدفع: $",
            'thank_you': "شكرًا لاستخدامك جهاز البيع المتقدم. وداعًا!",
            'yes_no_prompt': "هل ترغب في شراء عنصر آخر؟ (نعم/لا): ",
            'add_on_prompt': "هل ترغب في شراء إضافة؟ (نعم/لا): ",
            'recommended_addons': "الإضافات الموصى بها:",
            'no_stock': "المخزون: {stock}",
            'select_product': "أدخل رقم المنتج الذي ترغب في اختياره: ",
            'enter_payment': "{product} يكلف ${price:.2f}",
        }
    }

    def __init__(self):
        self.language = 'english'
        self.products: Dict[str, Product] = {
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
        self.purchase_suggestions = {
            "Drinks": ["cookies", "chocolate bar"],
            "Snacks": ["water", "orange juice"],
            "Chocolate": ["apple juice", "energy drink"]
        }

    def translate(self, text_key: str, **kwargs) -> str:
        translation = self.LANGUAGES[self.language].get(text_key, text_key)
        return translation.format(**kwargs) if kwargs else translation

    def set_language(self):
        language_choice = input("Select language (english/arabic): ").strip().lower()
        self.language = language_choice
        print(self.translate('welcome'))

    def display_products(self):
        print("\n--- VENDING MACHINE MENU ---")
        for key, product in self.products.items():
            if product.is_available():
                print(f"{key}: {product.name.capitalize()} - ${product.price:.2f} ({self.translate('no_stock', stock=product.stock)})")
            else:
                print(f"{key}: {product.name.capitalize()} - {self.translate('sold_out', product=product.name)}")

    def select_product(self) -> str:
        self.display_products()
        choice = input(self.translate('select_product')).strip()
        return choice

    def suggest_purchase(self, selected_product: Product) -> List[Product]:
        suggestions = []
        suggested_names = self.purchase_suggestions.get(selected_product.category, [])
        for code, product in self.products.items():
            if product.name in suggested_names and product.is_available():
                suggestions.append(product)
        return suggestions

    def process_payment(self, product: Product) -> bool:
        print(self.translate('enter_payment', product=product.name.capitalize(), price=product.price))
        payment = float(input(self.translate('payment_prompt')))
        change = payment - product.price
        print(f"Dispensing {product.name.capitalize()}! Change: ${change:.2f}")
        product.reduce_stock()
        return True

    def get_yes_no_input(self, prompt: str) -> bool:
        response = input(prompt).strip().lower()
        return response == 'yes'

    def run(self):
        self.set_language()
        while True:
            selected_code = self.select_product()
            selected_product = self.products[selected_code]
            if self.process_payment(selected_product):
                suggestions = self.suggest_purchase(selected_product)
                if suggestions:
                    print(self.translate('recommended_addons'))
                    for suggestion in suggestions:
                        print(f"- {suggestion.name.capitalize()} (${suggestion.price:.2f})")
                    if self.get_yes_no_input(self.translate('add_on_prompt')):
                        additional_code = self.select_product()
                        additional_product = self.products[additional_code]
                        self.process_payment(additional_product)
            if not self.get_yes_no_input(self.translate('yes_no_prompt')):
                print(self.translate('thank_you'))
                break

if __name__ == "__main__":
    vending_machine = VendingMachine()
    vending_machine.run()
