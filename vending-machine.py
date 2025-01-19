# Luna Alslaman 588512
# Vending Machine App

# import type hints for better code documentation
from typing import Dict, Tuple, List

class Product:
    def __init__(self, name: str, price: float, category: str, stock: int = 5):
        # initialise a new product with its basic properties
        self.name = name        # the name of the product in the current language
        self.price = price      # the price of the product
        self.category = category # the category the product belongs to (e.g., drinks, snacks)
        self.stock = stock      # the current quantity available, defaults to 5

    def is_available(self) -> bool:
        # check if the product has any units in stock
        return self.stock > 0   # returns True if stock is greater than 0

    def reduce_stock(self):
        # decrease the stock count by 1 after a successful purchase
        if self.stock > 0:      # only reduce if there are items available
            self.stock -= 1     # reduce stock by 1

class VendingMachine:
    # dictionary containing all translatable text in English and Arabic
    LANGUAGES = {
        'english': {
            # english translations for system messages
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
            # english product names
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
            # english category names
            'drinks': "Drinks",
            'snacks': "Snacks",
            'chocolate': "Chocolate"
        },
        'arabic': {
            # arabic translations for system messages
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
            # arabic product names
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
            # arabic category names
            'drinks': "المشروبات",
            'snacks': "الوجبات الخفيفة",
            'chocolate': "الشوكولاتة"
        }
    }

    def __init__(self):
        # initialise the vending machine with default settings
        self.language = 'english'  # set default language to English
        self.initialize_products() # set up the initial product inventory

    def initialize_products(self):
      # initialize products and suggestions with current language
    # create a dictionary of available products
        self.products: Dict[str, Product] = {
        # each product is initialized with a translated name, price, and category
            "1": Product(self.translate('orange_juice'), 2.99, self.translate('drinks')),
            "2": Product(self.translate('apple_juice'), 2.99, self.translate('drinks')),
            "6": Product(self.translate('salty_chips'), 1.50, self.translate('snacks')),
            "7": Product(self.translate('takkis'), 1.50, self.translate('snacks')),
            "9": Product(self.translate('kitkat'), 2.50, self.translate('chocolate')),
            "3": Product(self.translate('water'), 1.25, self.translate('drinks')),
            "4": Product(self.translate('professor_peppy'), 5.75, self.translate('drinks')),
            "10": Product(self.translate('chocolate_bar'), 2.75, self.translate('chocolate')),
            "8": Product(self.translate('cookies'), 1.75, self.translate('snacks')),
            "5": Product(self.translate('dr_pepper'), 10, self.translate('drinks'))
        }

        # define suggested products for each category to guide users in making choices
        self.purchase_suggestions = {
        # map each product category to a list of suggested product names within that category
            self.translate('drinks'): [self.translate('cookies'), self.translate('chocolate_bar')],
            self.translate('snacks'): [self.translate('water'), self.translate('orange_juice')],
            self.translate('chocolate'): [self.translate('apple_juice'), self.translate('dr_pepper')]
        }

    def translate(self, text_key: str, **kwargs) -> str:
    # retrieve the translation for the given text key in the current language
    # access the appropriate language dictionary from LANGUAGES based on the current language setting
        translation = self.LANGUAGES[self.language].get(text_key, text_key)

    # format the translation string with any additional arguments provided (e.g., placeholders in the translation)
        return translation.format(**kwargs) if kwargs else translation

    def set_language(self):
        while True:
        # prompt the user to choose between 'english' or 'arabic' (input is case-insensitive)
            language_choice = input("Select language (english/arabic): ").strip().lower()

            if language_choice in self.LANGUAGES:
            # if the user selects a valid language (present in the LANGUAGES dictionary), set it as the current language
                self.language = language_choice
            # reinitialise the products with the new language settings (translations will be updated)
                self.initialize_products()
                break # exit the loop after a valid language is selected
            else:
            # if the user enters an invalid language choice, display an error message
                print("Invalid language choice. Please select either 'english' or 'arabic'.")

    def display_products(self):
    # display the vending machine menu with product categories and availability
        print(f"\n{self.translate('menu_header')}")  # display the translated header for the menu

        categories = {}  # an empty dictionary to group products by category

        # group products by their categories
        for code, product in self.products.items():
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append((code, product))  # add the product to its category

        # display each category and its products
        for category, items in categories.items():
            print(f"\n{self.translate('category_header', category=category)}") # display the translated category header
            for code, product in items:
                if product.is_available():  # check if the product is available in stock
                    # show available products with price and stock
                    print(f"{code}: {product.name} - ${product.price:.2f} ({self.translate('stock', stock=product.stock)})")
                else:
                    # if the product is sold out, display a "sold out" message
                    print(f"{code}: {product.name} - SOLD OUT")

    def select_product(self) -> str:
    # handle product selection, make sure of valid input and availability
        while True:
            try:
                # show the menu of available products
                self.display_products()
                # prompt the user to select a product by entering its code
                choice = input(self.translate('select_product'))

                # check if the user's choice is valid (i.e., the product exists in the inventory)
                if choice not in self.products:
                    print(self.translate('invalid_choice'))  # inform the user if the choice is invalid
                # ask for a new choice
                    continue

                # check if the product is in stock
                if not self.products[choice].is_available():
                    print(self.translate('sold_out', product=self.products[choice].name))  # notify the user if the product is sold out
                # ask for a new choice
                    continue

                return choice  # return the valid product choice (the loop ends here)

            except ValueError:
            # handle any errors that occur due to invalid input (e.g., non-numeric input)
                print("Please enter a valid product number.")

    def suggest_purchase(self, selected_product: Product) -> List[Product]:
        # generate purchase suggestions based on selected product
        suggestions = [] # initialise an empty list to store suggested products

        # get the names of products that are suggested for the selected product's category
        suggested_names = self.purchase_suggestions.get(selected_product.category, [])

        # iterate through all products to find those that match the suggestions and are available
        for code, product in self.products.items():
            if product.name in suggested_names and product.is_available():
                suggestions.append(product)  # add the product to the suggestions list if it's available

        return suggestions  # return list of suggested products

    def process_payment(self, product: Product) -> bool:
        # handle the payment process for the selected product

        while True:
            try:
                # display the product price and prompt the user to enter payment
                print(self.translate('enter_payment', product=product.name, price=product.price))
                payment = float(input(self.translate('payment_prompt'))) # get the user's payment input as a float

                # check if payment is sufficient
                if payment < product.price:
                    print(self.translate('insufficient_payment', amount=product.price))  # inform the user if the payment is insufficient
                    continue # prompt for payment again if it's insufficient

                # calculate and return change
                change = payment - product.price
                print(f"\n{self.translate('dispensing')} {product.name}!")  # notify the user that the product is being dispensed
                print(f"Change returned: ${change:.2f}") # display the change amount

                # update product stock
                product.reduce_stock()
                return True  # indicate successful payment

            except ValueError:
                # handle invalid payment input
                print("Please enter a valid payment amount.") # prompt the user to enter a valid amount

    def get_yes_no_input(self, prompt: str) -> bool:
    # prompt the user for a yes/no answer and return True for 'yes' or False for 'no'
        while True:
        # get user input, convert to lowercase and remove leading/trailing spaces
            response = input(prompt).lower().strip()

        # accept both English ('yes'/'no') and Arabic ('نعم'/'لا') responses
            if response in ['yes', 'نعم']:
                return True  # return True for 'yes' or 'نعم'
            elif response in ['no', 'لا']:
                return False  # return False for 'no' or 'لا'
            else:
            # if input is invalid, prompt the user to enter a valid response
                print("Invalid input. Please enter 'yes'/'نعم' or 'no'/'لا'.")

    def run(self):
        # main function to run the vending machine
        print(f"{self.translate('welcome')}\n")  # show welcome message
        self.set_language()  # set language preference

        while True:
        # prompt the user to select a product and process the selection
            selected_code = self.select_product()  # get the selected product's code number
            selected_product = self.products[selected_code]  # retrieve the corresponding product

            # process payment and handle purchase
            if self.process_payment(selected_product):
            # generate and display product suggestions based on the selected product
                suggestions = self.suggest_purchase(selected_product)
                if suggestions:
                    print(self.translate('recommended_addons'))
                # display each suggested product with its price
                    for suggestion in suggestions:
                        print(f"- {suggestion.name} (${suggestion.price:.2f})")

                # ask the user if they want to purchase any suggested add-ons
                    if self.get_yes_no_input(self.translate('add_on_prompt')):
                    # if the user agrees, prompt them to select an additional product
                        additional_code = self.select_product()
                        additional_product = self.products[additional_code]
                        # process payment for the additional product
                        self.process_payment(additional_product)

            # check if user wants to make another purchase
            if not self.get_yes_no_input(self.translate('yes_no_prompt')):
                print(self.translate('thank_you'))  # show thank you message when exiting
                break  # exit the main loop and end the program

# entry point of the program, where the execution starts
if __name__ == "__main__":
    vending_machine = VendingMachine()  # create new vending machine instance
    vending_machine.run()  # start the vending machine operation