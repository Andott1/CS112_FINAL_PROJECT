import pickle


class System:
    def __init__(self):
        self.is_admin = False
        self.is_logged = False
        self.wholesale = False
        self.products = {}
        self.transactions = []

    def login(self, username, password):  # For login functions
        while True:
            # Back to previous display
            if username == '0':
                main()
            # Validate admin login credentials
            if username == "admin" and password == "123":
                print("\nAdmin login successful.")
                print("=====================================================================")
                self.is_logged = True
                self.is_admin = True
                break
            # Validate guest login credentials
            elif username == "guest" and password == "":
                print("\nGuest login successful.")
                print("=====================================================================")
                self.is_logged = True
                self.is_admin = False
                break
            else:
                print("\nInvalid username or password.")
                print("=====================================================================")
                # If invalid credentials, re-attempt login
                username = input("Enter Username [admin|guest|0 Back]: ")
                if username == '0':
                    main()
                password = input("Enter Password: ")
                continue

    def logout(self):  # For logout functions
        self.is_logged = False
        self.is_admin = False
        print("Logged out successfully.")

    def add_product(self):  # For adding product in product list
        # For admin access only
        if not self.is_admin:
            print("Only admin can add products.")
            return

        while True:
            print()
            # Input name for the product, or back to previous display
            name = input("Enter product name [0 back]: ")
            if name == "0":
                return
            if name == '':
                print("Product name can't be blank")
                continue

            while True:
                try:
                    # Input price for product in gallon
                    price_g = float(input("Enter gallon price: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid float value for gallon price.")
            while True:
                try:
                    # Input price for product in liter
                    price_l = float(input("Enter liter price: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid float value for liter price.")

            # Store product name and price in a list
            self.products[name] = (price_g, price_l)
            print(f"Product '{name}' added successfully.\n")

            filename = "products_wholesale.pkl" if self.wholesale else "products_retail.pkl"
            # Autosave list to specific file
            self.save_products(filename)

            while True:
                # Prompt to input another product or back to previous display
                again = input("Add another? [1 continue|0 back]: ")
                if again == '0':
                    return
                elif again == '1':
                    break
                else:
                    print("Invalid option. Please enter '1' or '0'\n")

    def delete_product(self):  # For deleting product in product list
        # For admin access only
        if not self.is_admin:
            print("Only admin can delete products.")
            return

        def delete_product_list():  # Display of product list
            print("=====================================================================")
            print("\nPRODUCT LIST:")
            print("{:<6} {:<25} {:<20} {:<20}".format("Index", "Name", "[1] Gallon Price", "[2] Liter Price"))
            index1 = 1
            for name, prices in self.products.items():
                print("{:<6} {:<29} ₱{:<19.2f} ₱{:<19.2f}".format(str(index1) + '.', name, prices[0], prices[1]))
                index1 += 1
            print("\n=====================================================================")

        delete_product_list()

        while True:
            try:
                # Input index of product to delete or back to previous display
                index = int(input("Enter index to delete [0 back]: "))
                if index == 0:
                    return
                if 1 <= index <= len(self.products):
                    product_name = list(self.products.keys())[index - 1]
                    del self.products[product_name]
                    print(f"Product '{product_name}' deleted successfully.")

                    filename = "products_wholesale.pkl" if self.wholesale else "products_retail.pkl"
                    # Autosave list to specific file
                    self.save_products(filename)
                else:
                    print("Invalid index.")
                    continue

                while True:
                    # Prompt to delete another product or back to previous display
                    again = input("\nDelete another? [1 continue|0 back]: ")
                    if again == '0':
                        return
                    elif again == '1':
                        delete_product_list()
                        break
                    else:
                        print("Invalid option. Please enter '1' or '0'")

            except ValueError:
                print("Invalid input. Please enter a valid option.")

    def display_product_list(self):  # For displaying current product list
        print(f"\n=====================================================================\n"
              f"\nPRODUCT LIST:")
        print("{:<6} {:<25} {:<20} {:<20}".format("Index", "Name", "[1] Gallon Price", "[2] Liter Price"))
        index = 1
        for name, prices in self.products.items():
            print("{:<6} {:<29} ₱{:<19.2f} ₱{:<19.2f}".format(str(index) + '.', name, prices[0], prices[1]))
            index += 1
        print("\n=====================================================================")
        if self.is_admin:
            input("Press enter to continue")

    def save_products(self, filename):  # Save product list  to file function
        with open(filename, 'wb') as file:
            pickle.dump(self.products, file)

    def load_products(self, filename):  # Load product list from file function
        try:
            with open(filename, 'rb') as file:
                self.products = pickle.load(file)
        except FileNotFoundError:
            self.products = {}
        except Exception as e:
            print("Error loading product list:", e)
            self.products = {}

    def display_transaction_history(self):  # For displaying transaction history
        print("=====================================================================")
        print("\nTRANSACTION HISTORY:")
        for index, purchase in enumerate(self.transactions, start=1):
            print(f"\nTRANSACTION {index}:")
            if 'Items' in purchase:
                print("Items:")
                for item in purchase['Items']:
                    print(f" - {item['Name']} ({item['Packaging']}): x {item['Quantity']}")
            print(f"{'Total Amount:':<16}   ₱{purchase.get('Total Amount', 0):.2f}")
            print(f"{'Amount Received:':<16}   ₱{purchase.get('Amount Received', 0):.2f}")
            print(f"{'Change:':<16}   ₱{purchase.get('Change', 0):.2f}")
        print("\n=====================================================================")
        input("Press enter to continue")

    def save_transaction_history(self, filename):  # Save transaction history to file function
        with open(filename, 'wb') as file:
            pickle.dump(self.transactions, file)

    def load_transaction_history(self, filename):  # Load transaction history from file function
        try:
            with open(filename, 'rb') as file:
                self.transactions = pickle.load(file)
        except FileNotFoundError:
            self.transactions = []  # Initialize empty list if file doesn't exist
        except Exception as e:
            print("Error loading transaction history:", e)
            self.transactions = []  # Initialize empty list if error loading

    def clear_transactions(self):  # For clearing current loaded transaction history
        self.transactions = []
        print("Transaction history cleared.")
        if self.wholesale:
            self.save_transaction_history("transactions_wholesale.pkl")
        else:
            self.save_transaction_history("transactions_retail.pkl")
        print("=====================================================================")
        input("Press enter to continue")

    def clear_products(self):  # For clearing current product list
        self.products = {}
        print("Product list cleared.")
        if self.wholesale:
            self.save_products("products_wholesale.pkl")
        else:
            self.save_products("products_retail.pkl")
        print("=====================================================================")
        input("Press enter to continue")

    def new_transaction(self):  # For transactions if guest login
        # For guest access only
        if self.is_admin:
            print("Only guests can buy products.")
            return

        purchase_list = []

        while True:
            # Display current loaded product list
            self.display_product_list()
            # Display selected item/s
            print("\nTRANSACTION ITEMS:")
            for item in purchase_list:
                index = item["Name"]
                packaging = item["Packaging"]
                quantity = item["Quantity"]
                if packaging == "Gallon":
                    price = self.products[index][0]
                elif packaging == "Liter":
                    price = self.products[index][1]
                else:
                    break
                print("{:<29} {:<7} ₱{:<8.2f} x {:<4}".format(index, packaging, price, quantity))

            print("\n=====================================================================")
            # Input selected product index
            index = input("Choose product index ['' pay | '0' back]: ")

            if index == '0':
                return
            if index == '':
                if not purchase_list:
                    print("No Product Selected")
                    break
                else:
                    print("Proceeding to Payment...")
                    break

            try:
                index = int(index)
                if 1 <= index <= len(self.products):
                    product_name = list(self.products.keys())[index - 1]

                    # Input selected product packaging
                    packaging_choice = input("Choose packaging [1|2]: ")
                    if packaging_choice == '1':
                        packaging = 'Gallon'
                    elif packaging_choice == '2':
                        packaging = 'Liter'
                    else:
                        print("Invalid packaging choice.")
                        continue

                    # Input desired product quantity
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("Invalid quantity.")
                        continue

                    # Collect selected product details
                    purchase_list.append({
                        "Name": product_name,
                        "Packaging": packaging,
                        "Quantity": quantity,
                    })
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input. Please enter a valid index or '0'.")

        if purchase_list:
            # Load each product details
            total_amount = 0
            while True:
                print("\n=====================================================================")
                print("\n---------------------------------------------------------------------"
                      "\nTRANSACTION ITEMS:")
                for item in purchase_list:
                    index = item["Name"]
                    packaging = item["Packaging"]
                    quantity = item["Quantity"]
                    if packaging == "Gallon":
                        price = self.products[index][0]
                    elif packaging == "Liter":
                        price = self.products[index][1]
                    else:
                        print("Invalid price type.")
                        return

                    # Calculate and display total amount of product selected
                    item_total = price * quantity
                    total_amount += item_total
                    print("{:<29} {:<7} ₱{:<8.2f} x {:<4}".format(index, packaging, price, quantity))

                print("---------------------------------------------------------------------")
                print("{:<29} {:<7} ₱{:<8.2f}".format("", "TOTAL", total_amount))
                print("\n=====================================================================")

                while True:
                    try:
                        # Input payment amount
                        amount_received = float(input("Payment Amount Received: "))
                        if amount_received < total_amount:
                            print("Insufficient amount received. Please enter a sufficient amount.\n")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Invalid amount. Please enter a valid amount.\n")

                # Calculate and display change
                change = amount_received - total_amount
                print(f"CHANGE: ₱{change:.2f}")
                print("=====================================================================")

                # Collect and save transaction details
                transaction_details = {
                    "Items": purchase_list,
                    "Total Amount": total_amount,
                    "Amount Received": amount_received,
                    "Change": change
                }
                self.transactions.append(transaction_details)

                # Save transaction details to specific file
                if self.wholesale:
                    self.save_transaction_history("transactions_wholesale.pkl")
                else:
                    self.save_transaction_history("transactions_retail.pkl")

                input("Press Enter to continue...")
                break


def main():  # Main program flow
    pos = System()
    # Login page
    header = ("\n====================================================================="
              "\n----------------------- POINT OF SALE SYSTEM ------------------------"
              "\n---------------- ALO KLEEN CHEMICAL PRODUCTS TRADING ----------------"
              "\n=====================================================================\n")
    print(f"{header}\n[1] Login\n[2] Exit")
    print("\n=====================================================================")

    while True:
        choice = input("Enter Option: ")

        if choice == "1":
            print("=====================================================================")
            username = input("Enter Username [admin|guest|0 Back]: ")
            if username == '0':
                main()
            password = input("Enter Password: ")
            pos.login(username, password)
            if pos.is_logged:
                break
        elif choice == "2":
            print("=====================================================================")
            print("Exiting System...")
            exit()
        else:
            print("Invalid option. Please enter 1 to login or 2 to exit.")

    # Selection of sales type page
    while True:
        print(f"{header}\nSALES TYPE: \n[1] Wholesale \n[2] Retail \n[0] Logout")
        print("\n=====================================================================")
        sale_type = input("Choose an Option: ")

        if sale_type == "1":
            # Load wholesale mode, products, and transaction history
            pos.wholesale = True
            pos.load_products("products_wholesale.pkl")
            pos.load_transaction_history("transactions_wholesale.pkl")
            sale_type_reminder = "WHOLESALE"
            break
        elif sale_type == "2":
            # Load retail mode, products, and transaction history
            pos.wholesale = False
            pos.load_products("products_retail.pkl")
            pos.load_transaction_history("transactions_retail.pkl")
            sale_type_reminder = "RETAIL"
            break
        elif sale_type == "0":
            # Logout
            pos.logout()
            main()

        else:
            print("Invalid Option")

    while True:
        if pos.is_logged:
            print(f"{header}\nSALES TYPE: {sale_type_reminder}")
            if pos.is_admin:
                # Option menu for admin access
                print("[1] Logout\n[2] Add Product\n[3] Delete Product\n[4] Display Products"
                      "\n[5] Save Products to File\n[6] Load Products from File\n[7] Display Transaction History"
                      "\n[8] Clear Transaction History\n[9] Clear Products List\n[10] Switch Sales Type")
            else:
                # Option menu for guest access
                print("[1] Logout\n[2] New Transaction\n[3] Switch Sales Type")

            print("\n=====================================================================")

            choice = input("Enter an Option: ")

            # Option functions according to menu
            if pos.is_admin:
                # Option functions for admin access
                if choice == "1":
                    pos.logout()
                    main()
                elif choice == "2":
                    pos.add_product()
                elif choice == "3":
                    pos.delete_product()
                elif choice == "4":
                    pos.display_product_list()
                elif choice == "5":
                    while True:
                        filename = input("Enter filename to save products [0 back]: ")
                        if filename == '0':
                            break
                        elif filename != '':
                            pos.save_products(filename)
                            print("Products loaded from file."
                                  "\n=====================================================================")
                            input("Press enter to continue")
                            break
                        else:
                            print("filename can't be blank\n")
                elif choice == "6":
                    while True:
                        filename = input("Enter filename to load products from [0 back]: ")
                        if filename == '0':
                            break
                        elif filename != '':
                            pos.load_products(filename)
                            print("Products loaded from file."
                                  "\n=====================================================================")
                            input("Press enter to continue")
                            break
                        else:
                            print("filename can't be blank\n")

                elif choice == "7":
                    pos.display_transaction_history()
                elif choice == "8":
                    pos.clear_transactions()
                elif choice == "9":
                    pos.clear_products()
                elif choice == "10":
                    if pos.wholesale:
                        pos.wholesale = False
                        pos.load_products("products_retail.pkl")
                        pos.load_transaction_history("transactions_retail.pkl")
                        sale_type_reminder = "RETAIL"
                    else:
                        pos.wholesale = True
                        pos.load_products("products_wholesale.pkl")
                        pos.load_transaction_history("transactions_wholesale.pkl")
                        sale_type_reminder = "WHOLESALE"
                else:
                    print("Invalid Option.")
            else:
                # Option functions for guest access
                if choice == "1":
                    pos.logout()
                    main()
                elif choice == "2":
                    pos.new_transaction()
                elif choice == "3":
                    if pos.wholesale:
                        pos.wholesale = False
                        pos.load_products("products_retail.pkl")
                        pos.load_transaction_history("transactions_retail.pkl")
                        sale_type_reminder = "RETAIL"
                    else:
                        pos.wholesale = True
                        pos.load_products("products_wholesale.pkl")
                        pos.load_transaction_history("transactions_wholesale.pkl")
                        sale_type_reminder = "WHOLESALE"
                else:
                    print("Invalid Option.")
        else:
            print("Invalid option. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
