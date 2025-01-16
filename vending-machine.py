import random  # Importing the random module (not used in this version, but it could be useful in the future)
from typing import Dict, Tuple, List  # Importing typing utilities to define type hints for dictionaries, tuples, and lists

class Product:
    # Represents a single product in the vending machine.
    def __init__(self, name: str, price: float, category: str, stock: int = 10):
        # Initialize the product's attributes: name, price, category, and stock (default to 10).
        self.name = name  # Product name
        self.price = price  # Product price
        self.category = category  # Product category (e.g., Drinks, Snacks, etc.)
        self.stock = stock  # Product stock (default is 10)

    def is_available(self) -> bool:
        # Check if the product is available by verifying if stock > 0
        return self.stock > 0

    def reduce_stock(self):
        # Reduces the stock of the product by 1 if the stock is greater than 0
        if self.stock > 0:
            self.stock -= 1  # Decrease stock by 1


class VendingMachine:
    # Language dictionaries for translation
    LANGUAGES = {
        'english': {  # English language translations
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
        'arabic': {  # Arabic language translations
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
        self.language = 'english'  # Default language is set to English
        # Initializing a dictionary with product codes as keys and Product objects as values
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

        # Suggesting additional products based on the category of the selected product
        self.purchase_suggestions = {
            "Drinks": ["cookies", "chocolate bar"],
            "Snacks": ["water", "orange juice"],
            "Chocolate": ["apple juice", "energy drink"]
        }

    def translate(self, text_key: str, **kwargs) -> str:
        # This method returns the translated text based on the current selected language.
        translation = self.LANGUAGES[self.language].get(text_key, text_key)
        # It also formats any dynamic content (like prices or stock) if there are placeholders
        return translation.format(**kwargs) if kwargs else translation

    def set_language(self):
        # This method asks the user to choose a language at the start.
        while True:
            language_choice = input("Select language (english/arabic): ").strip().lower()  # Prompt the user for language
            if language_choice in self.LANGUAGES:  # Check if the entered language is valid
                self.language = language_choice  # Set the language to the user's choice
                print(self.translate('welcome'))  # Print the welcome message in the selected language
                break
            else:
                print("Invalid language choice. Please select either 'english' or 'arabic'.")  # If invalid, prompt again

    def display_products(self):
        # This method displays the product menu in a categorized format
        print("\n--- VENDING MACHINE MENU ---")
        categories = {}  # Create an empty dictionary to hold products categorized by type

        for code, product in self.products.items():
            if product.category not in categories:  # If the category is not in the dictionary, add it
                categories[product.category] = []
            categories[product.category].append((code, product))  # Group products under their respective categories

        for category, items in categories.items():
            print(f"\n{category.upper()} CATEGORY:")  # Print category header (e.g., DRINKS CATEGORY)
            for code, product in items:
                if product.is_available():
                    # Display product details if the product is available
                    print(f"{code}: {product.name.capitalize()} - ${product.price:.2f} ({self.translate('no_stock', stock=product.stock)})")
                else:
                    # If the product is sold out, show that it's unavailable
                    print(f"{code}: {product.name.capitalize()} - {self.translate('sold_out', product=product.name)}")

    def select_product(self) -> str:
        # This method allows the user to select a product by entering the corresponding code
        while True:
            try:
                self.display_products()  # Display the product menu
                choice = input(self.translate('select_product'))  # Ask the user to enter the product code

                if choice not in self.products:  # If the choice is invalid (not in the products dictionary)
                    print(self.translate('invalid_choice'))  # Show an invalid choice message
                    continue

                if not self.products[choice].is_available():  # If the selected product is out of stock
                    print(self.translate('sold_out', product=self.products[choice].name))  # Show sold out message
                    continue

                return choice  # Return the valid product code if valid and available

            except ValueError:
                print("Please enter a valid product number.")  # Handle invalid inputs

    def suggest_purchase(self, selected_product: Product) -> List[Product]:
        # This method suggests additional products based on the selected product's category
        suggestions = []  # Create an empty list to store suggested products
        suggested_names = self.purchase_suggestions.get(selected_product.category, [])  # Get suggestions for the product's category

        for code, product in self.products.items():
            if product.name in suggested_names and product.is_available():
                suggestions.append(product)  # Add products to the suggestion list if they match and are in stock

        return suggestions  # Return the list of suggested products

    def process_payment(self, product: Product) -> bool:
        # This method handles payment for the selected product
        while True:
            try:
                print(self.translate('enter_payment', product=product.name.capitalize(), price=product.price))  # Show product price
                payment = float(input(self.translate('payment_prompt')))  # Ask the user to input payment amount

                if payment < product.price:  # If payment is less than the product price
                    print(self.translate('insufficient_payment', amount=product.price))  # Show insufficient payment message
                    continue

                change = payment - product.price  # Calculate the change
                print(f"\n{self.translate('dispensing')} {product.name.capitalize()}!")  # Dispense the product
                print(f"Change returned: ${change:.2f}")  # Show the change returned

                product.reduce_stock()  # Reduce the stock of the purchased product

                return True  # Return True indicating the transaction was successful

            except ValueError:
                print("Please enter a valid payment amount.")  # Handle invalid input for payment

    def get_yes_no_input(self, prompt: str) -> bool:
        # This method asks the user for a yes/no answer and validates the input
        while True:
            response = input(prompt).lower().strip()  # Get the response, convert to lowercase, and remove extra spaces
            if response == 'yes':  # If the response is 'yes'
                return True  # Return True
            elif response == 'no':  # If the response is 'no'
                return False  # Return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")  # Handle invalid input

    def run(self):
        # This method runs the main logic of the vending machine
        self.set_language()  # Prompt the user to select a language

        while True:
            selected_code = self.select_product()  # Prompt the user to select a product
            selected_product = self.products[selected_code]  # Get the selected product object

            if self.process_payment(selected_product):  # Process payment for the selected product
                suggestions = self.suggest_purchase(selected_product)  # Get suggested products
                if suggestions:
                    print(self.translate('recommended_addons'))  # Show recommended add-ons
                    for suggestion in suggestions:
                        print(f"- {suggestion.name.capitalize()} (${suggestion.price:.2f})")  # Display each suggestion

                    if self.get_yes_no_input(self.translate('add_on_prompt')):  # Ask if they want to buy an add-on
                        additional_code = self.select_product()  # Let the user select an additional product
                        additional_product = self.products[additional_code]  # Get the additional product
                        self.process_payment(additional_product)  # Process payment for the additional product

            if not self.get_yes_no_input(self.translate('yes_no_prompt')):  # Ask if they want to buy another item
                print(self.translate('thank_you'))  # Thank the user and exit the loop
                break


if __name__ == "__main__":
    vending_machine = VendingMachine()  # Create an instance of the VendingMachine class
    vending_machine.run()  # Start the vending machine application
