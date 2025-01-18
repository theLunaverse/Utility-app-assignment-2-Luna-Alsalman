from typing import Dict, Tuple, List

class Product:
    def __init__(self, name: str, price: float, category: str, stock: int = 5):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def is_available(self) -> bool:
        return self.stock > 0

    def reduce_stock(self):
        if self.stock > 0:
            self.stock -= 1

class VendingMachine:
    LANGUAGES = {
        'english': {
            'invalid_choice': "Invalid product number. Please try again.",
            'sold_out': "Sorry, {product} is SOLD OUT!",
            'insufficient_payment': "Insufficient payment. You need at least ${amount:.2f}",
            'payment_prompt': "Enter payment amount: $",
            'thank_you': "Thank you for using Luna's Vending Machine. Goodbye!",
            'yes_no_prompt': "Would you like to buy another item? (yes/no): ",
            'add_on_prompt': "Would you like to buy an add-on? (yes/no): ",
            'recommended_addons': "Recommended add-ons:",
            'stock': "Stock: {stock}",
            'select_product': "Enter the number of the product you want: ",
            'enter_payment': "{product} costs ${price:.2f}",
            'menu_header': "--- VENDING MACHINE MENU ---",
            'category_header': "{category} category:",
            'dispensing': "Dispensing",
            'welcome': "Welcome to Luna's Vending Machine!",
            'orange_juice': "orange juice",
            'apple_juice': "apple juice",
            'salty_chips': "salty chips",
            'takkis': "takkis",
            'kitkat': "kitkat",
            'water': "water",
            'professor_peppy': "professor peppy",
            'chocolate_bar': "chocolate bar",
            'cookies': "cookies",
            'dr_pepper': "dr Pepper",
            'drinks': "Drinks",
            'snacks': "Snacks",
            'chocolate': "Chocolate"
        },
        'arabic': {
            'invalid_choice': "رقم المنتج غير صالح. يرجى المحاولة مرة أخرى.",
            'sold_out': "عذرًا، {product} نفد من المخزون!",
            'insufficient_payment': "المبلغ غير كافٍ. تحتاج إلى دفع على الأقل ${amount:.2f}",
            'payment_prompt': "أدخل مبلغ الدفع: $",
            'thank_you': "شكرًا لاستخدامك جهاز لونا للبيع. وداعًا!",
            'yes_no_prompt': "هل ترغب في شراء عنصر آخر؟ (نعم/لا): ",
            'add_on_prompt': "هل ترغب في شراء إضافة؟ (نعم/لا): ",
            'recommended_addons': "الإضافات الموصى بها:",
            'stock': "المخزون: {stock}",
            'select_product': "أدخل رقم المنتج الذي ترغب في اختياره: ",
            'enter_payment': "{product} يكلف ${price:.2f}",
            'menu_header': "--- قائمة آلة البيع ---",
            'category_header': "فئة {category}:",
            'dispensing': "جاري صرف",
            'welcome': "!مرحباً بكم في آلة لونا للبيع",
            'orange_juice': "عصير برتقال",
            'apple_juice': "عصير تفاح",
            'salty_chips': "شيبس مملح",
            'takkis': "تاكيز",
            'kitkat': "كيت كات",
            'water': "ماء",
            'professor_peppy': "بروفيسور بيبي",
            'chocolate_bar': "لوح شوكولاتة",
            'cookies': "بسكويت",
            'dr_pepper': "دكتور بيبر",
            'drinks': "المشروبات",
            'snacks': "الوجبات الخفيفة",
            'chocolate': "الشوكولاتة"
        }
    }

    def __init__(self):
        self.language = 'english'
        self.initialize_products()

    def initialize_products(self):
        self.products: Dict[str, Product] = {
            "1": Product(self.translate('orange_juice'), 2.99, self.translate('drinks')),
            "2": Product(self.translate('apple_juice'), 2.99, self.translate('drinks')),
            "3": Product(self.translate('salty_chips'), 1.50, self.translate('snacks')),
            "4": Product(self.translate('takkis'), 1.50, self.translate('snacks')),
            "5": Product(self.translate('kitkat'), 2.50, self.translate('chocolate')),
            "6": Product(self.translate('water'), 1.25, self.translate('drinks')),
            "7": Product(self.translate('professor_peppy'), 5.75, self.translate('drinks')),
            "8": Product(self.translate('chocolate_bar'), 2.75, self.translate('chocolate')),
            "9": Product(self.translate('cookies'), 1.75, self.translate('snacks')),
            "10": Product(self.translate('dr_pepper'), 10, self.translate('drinks'))
        }

        self.purchase_suggestions = {
            self.translate('drinks'): [self.translate('cookies'), self.translate('chocolate_bar')],
            self.translate('snacks'): [self.translate('water'), self.translate('orange_juice')],
            self.translate('chocolate'): [self.translate('apple_juice'), self.translate('dr_pepper')]
        }

    def translate(self, text_key: str, **kwargs) -> str:
        translation = self.LANGUAGES[self.language].get(text_key, text_key)
        return translation.format(**kwargs) if kwargs else translation

    def set_language(self):
        while True:
            language_choice = input("Select language (english/arabic): ").strip().lower()
            if language_choice in self.LANGUAGES:
                self.language = language_choice
                self.initialize_products()
                break
            else:
                print("Invalid language choice. Please select either 'english' or 'arabic'.")

    def display_products(self):
        print(f"\n{self.translate('menu_header')}")
        categories = {}

        for code, product in self.products.items():
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append((code, product))

        for category, items in categories.items():
            print(f"\n{self.translate('category_header', category=category)}")
            for code, product in items:
                if product.is_available():
                    print(f"{code}: {product.name} - ${product.price:.2f} ({self.translate('stock', stock=product.stock)})")
                else:
                    print(f"{code}: {product.name} - SOLD OUT")

    def select_product(self) -> str:
        while True:
            try:
                self.display_products()
                choice = input(self.translate('select_product'))

                if choice not in self.products:
                    print(self.translate('invalid_choice'))
                    continue

                if not self.products[choice].is_available():
                    print(self.translate('sold_out', product=self.products[choice].name))
                    continue

                return choice

            except ValueError:
                print("Please enter a valid product number.")

    def suggest_purchase(self, selected_product: Product) -> List[Product]:
        suggestions = []
        suggested_names = self.purchase_suggestions.get(selected_product.category, [])
        
        for code, product in self.products.items():
            if product.name in suggested_names and product.is_available():
                suggestions.append(product)

        return suggestions

    def process_payment(self, product: Product) -> bool:
        while True:
            try:
                print(self.translate('enter_payment', product=product.name, price=product.price))
                payment = float(input(self.translate('payment_prompt')))

                if payment < product.price:
                    print(self.translate('insufficient_payment', amount=product.price))
                    continue

                change = payment - product.price
                print(f"\n{self.translate('dispensing')} {product.name}!")
                print(f"Change returned: ${change:.2f}")

                product.reduce_stock()
                return True

            except ValueError:
                print("Please enter a valid payment amount.")

    def get_yes_no_input(self, prompt: str) -> bool:
        while True:
            response = input(prompt).lower().strip()
            if response in ['yes', 'نعم']:
                return True
            elif response in ['no', 'لا']:
                return False
            else:
                print("Invalid input. Please enter 'yes'/'نعم' or 'no'/'لا'.")

    def run(self):
        print(f"{self.translate('welcome')}\n")
        self.set_language()

        while True:
            selected_code = self.select_product()
            selected_product = self.products[selected_code]

            if self.process_payment(selected_product):
                suggestions = self.suggest_purchase(selected_product)
                if suggestions:
                    print(self.translate('recommended_addons'))
                    for suggestion in suggestions:
                        print(f"- {suggestion.name} (${suggestion.price:.2f})")

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