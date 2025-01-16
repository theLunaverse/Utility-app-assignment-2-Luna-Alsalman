import random
from typing import Dict, Tuple, List

class Product:
    #Represents a single product in the vending machine.
    def __init__(self, name: str, price: float, category: str, stock: int = 10):
        # Initialize product attributes: name, price, category, and stock.
        self.name = name  # Product name.
        self.price = price  # Product price.
        self.category = category  # Product category (e.g., Drinks, Snacks).
        self.stock = stock  # Initial stock quantity (default is 10).
    
    def is_available(self) -> bool:
        # Check if the product is in stock by verifying if stock > 0.
        return self.stock > 0
    
    def reduce_stock(self):
        # Decrease the product stock by 1 if stock is greater than 0.
        if self.stock > 0:
            self.stock -= 1


class VendingMachine:
    """
    Advanced Vending Machine with multiple features.
    """
    def __init__(self):
        # Initialize the vending machine with predefined products and suggestions.
        self.products: Dict[str, Product] = {
            "1": Product("orange juice", 2.99, "Drinks"),  # Key '1' maps to orange juice in the Drinks category.
            "2": Product("apple juice", 2.99, "Drinks"),   # Key '2' maps to apple juice in the Drinks category.
            "3": Product("salty chips", 1.50, "Snacks"),  # Key '3' maps to salty chips in the Snacks category.
            "4": Product("spicy chips", 1.50, "Snacks"),  # Key '4' maps to spicy chips in the Snacks category.
            "5": Product("kitkat", 2.50, "Chocolate"),    # Key '5' maps to KitKat in the Chocolate category.
            "6": Product("water", 1.25, "Drinks"),        # Key '6' maps to water in the Drinks category.
            "7": Product("energy drink", 3.25, "Drinks"), # Key '7' maps to energy drink in the Drinks category.
            "8": Product("chocolate bar", 2.75, "Chocolate"),  # Key '8' maps to a chocolate bar in the Chocolate category.
            "9": Product("cookies", 1.75, "Snacks")       # Key '9' maps to cookies in the Snacks category.
        }
        
        # Define product category-based suggestions.
        self.purchase_suggestions = {
            "Drinks": ["cookies", "chocolate bar"],  # Suggest Snacks and Chocolate for Drinks purchases.
            "Snacks": ["water", "orange juice"],     # Suggest Drinks for Snacks purchases.
            "Chocolate": ["apple juice", "energy drink"]  # Suggest Drinks for Chocolate purchases.
        }
    
    def display_products(self):
        # Display all products categorized by their type.
        print("\n--- VENDING MACHINE MENU ---")
        categories = {}  # Dictionary to group products by category.
        
        for code, product in self.products.items():
            # Group products under their respective categories.
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append((code, product))
        
        for category, items in categories.items():
            # Display each category and its available products.
            print(f"\n{category.upper()} CATEGORY:")
            for code, product in items:
                if product.is_available():
                    print(f"{code}: {product.name.capitalize()} - ${product.price:.2f} (Stock: {product.stock})")
                else:
                    print(f"{code}: {product.name.capitalize()} - SOLD OUT")
    
    def select_product(self) -> str:
        # Prompt the user to select a product and validate the input.
        while True:
            try:
                self.display_products()  # Show the menu to the user.
                choice = input("\nEnter the number of the product you want: ")
                
                if choice not in self.products:  # Check if the input is valid.
                    print("Invalid product number. Please try again.")
                    continue
                
                if not self.products[choice].is_available():  # Check if the product is in stock.
                    print(f"Sorry, {self.products[choice].name} is SOLD OUT!")
                    continue
                
                return choice  # Return the valid product code.
            
            except ValueError:
                # Handle cases where input is not a valid string.
                print("Please enter a valid product number.")
    
    def suggest_purchase(self, selected_product: Product) -> List[Product]:
        # Suggest additional products based on the selected product's category.
        suggestions = []  # List to store suggested products.
        suggested_names = self.purchase_suggestions.get(selected_product.category, [])
        
        for code, product in self.products.items():
            # Add products to the suggestion list if they match and are in stock.
            if product.name in suggested_names and product.is_available():
                suggestions.append(product)
        
        return suggestions  # Return the list of suggested products.
    
    def process_payment(self, product: Product) -> bool:
        # Process payment for the selected product and check for sufficient funds.
        while True:
            try:
                print(f"\n{product.name.capitalize()} costs ${product.price:.2f}")
                payment = float(input("Enter payment amount: $"))
                
                if payment < product.price:  # Verify if payment is sufficient.
                    print(f"Insufficient payment. You need at least ${product.price:.2f}")
                    continue
                
                change = payment - product.price  # Calculate the change.
                print(f"\nDispensing {product.name.capitalize()}!")
                print(f"Change returned: ${change:.2f}")
                
                product.reduce_stock()  # Reduce the stock of the purchased product.
                
                return True  # Indicate a successful transaction.
            
            except ValueError:
                # Handle cases where the payment input is not a valid number.
                print("Please enter a valid payment amount.")
    
    def get_yes_no_input(self, prompt: str) -> bool:
        # Prompt the user for a yes or no answer and validate the input.
        while True:
            response = input(prompt).lower().strip()  # Get user input.
            if response == 'yes':
                return True  # Return True if the input is 'yes'.
            elif response == 'no':
                return False  # Return False if the input is 'no'.
            else:
                # Handle invalid input by prompting again.
                print("Invalid input. Please enter 'yes' or 'no'.")
    
    def run(self):
        # Run the main loop for the vending machine operations.
        print("Welcome to the Advanced Vending Machine!")
        
        while True:
            selected_code = self.select_product()  # Select a product.
            selected_product = self.products[selected_code]
            
            if self.process_payment(selected_product):  # Process payment for the selected product.
                suggestions = self.suggest_purchase(selected_product)  # Get purchase suggestions.
                if suggestions:
                    print("\nRecommended add-ons:")
                    for suggestion in suggestions:
                        print(f"- {suggestion.name.capitalize()} (${suggestion.price:.2f})")
                    
                    if self.get_yes_no_input("Would you like to buy an add-on? (yes/no): "):
                        additional_code = self.select_product()  # Allow user to select an add-on.
                        additional_product = self.products[additional_code]
                        self.process_payment(additional_product)
            
            if not self.get_yes_no_input("\nWould you like to buy another item? (yes/no): "):
                # Exit the loop if the user does not want another transaction.
                print("Thank you for using the Advanced Vending Machine. Goodbye!")
                break


# Run the vending machine
if __name__ == "__main__":
    vending_machine = VendingMachine()  # Create an instance of VendingMachine.
    vending_machine.run()  # Start the vending machine application.
