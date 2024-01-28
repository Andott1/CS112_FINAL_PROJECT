import pickle


class System:
    def __init__(self):
        self.is_admin = False
        self.is_logged = False
        self.wholesale = False
        self.products = {}
        self.transactions = []

    def login(self, username, password):
        while True:
            if username == '0':
                main()
            if username == "admin" and password == "123":
                print("\nAdmin login successful.")
                self.is_logged = True
                self.is_admin = True
                break
            elif username == "guest" and password == "":
                print("\nGuest login successful.")
                self.is_logged = True
                self.is_admin = False
                break
            else:
                print("Invalid username or password.\n")
                username = input("Enter Username [admin|guest|0 Back]: ")
                if username == '0':
                    main()
                password = input("Enter Password: ")
                continue

    def logout(self):
        self.is_logged = False
        self.is_admin = False
        print("Logged out successfully.")

    def add_product(self):
        if not self.is_admin:
            print("Only admin can add products.")
            return

        while True:
            name = input("Enter product name [0 back]: ")
            if name == "0":
                return
            if name == '':
                print("Product name can't be blank")
                continue

            while True:
                try:
                    price_g = float(input("Enter gallon price: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid float value for gallon price.")
            while True:
                try:
                    price_l = float(input("Enter liter price: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid float value for liter price.")

            self.products[name] = (price_g, price_l)
            print(f"Product '{name}' added successfully.\n")

            filename = "products_wholesale.pkl" if self.wholesale else "products_retail.pkl"
            self.save_products(filename)

            while True:
                again = input("Add another? [1 continue|0 back]: ")
                if again == '0':
                    return
                elif again == '1':
                    break
                else:
                    print("Invalid option. Please enter '1' or '0'\n")

    def delete_product(self):
        if not self.is_admin:
            print("Only admin can delete products.")
            return
        print("\n=====================================================================\n")
        print("\nPRODUCT LIST:")
        print("{:<6} {:<25} {:<20} {:<20}".format("Index", "Name", "[1] Gallon Price", "[2] Liter Price"))
        index = 1
        for name, prices in self.products.items():
            print("{:<6} {:<29} ₱{:<19.2f} ₱{:<19.2f}".format(str(index) + '.', name, prices[0], prices[1]))
            index += 1
        print("\n=====================================================================")

        while True:
            try:
                index = int(input("Enter index to delete [0 back]: "))
                if index == 0:
                    return
                if 1 <= index <= len(self.products):
                    product_name = list(self.products.keys())[index - 1]
                    del self.products[product_name]
                    print(f"Product '{product_name}' deleted successfully.")

                    filename = "products_wholesale.pkl" if self.wholesale else "products_retail.pkl"
                    self.save_products(filename)
                else:
                    print("Invalid index.\n")
                    continue

                while True:
                    again = input("Delete another? [1 continue|0 back]: ")
                    if again == '0':
                        return
                    elif again == '1':
                        print()
                        break
                    else:
                        print("Invalid option. Please enter '1' or '0'\n")

            except ValueError:
                print("Invalid input. Please enter a valid index.\n")

    def new_transaction(self):
        if self.is_admin:
            print("Only guests can buy products.")
            return

        purchase_list = []

        while True:
            self.display_products()
            print("TRANSACTION ITEMS:")
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

            index = input("\nChoose product index ['' checkout | '0' back]: ")

            if index == '0':
                return
            if index == '':
                if not purchase_list:
                    print("No Product Selected")
                    break
                else:
                    break

            try:
                index = int(index)
                if 1 <= index <= len(self.products):
                    product_name = list(self.products.keys())[index - 1]

                    packaging_choice = input("Choose packaging [1|2]: ")
                    if packaging_choice == '1':
                        packaging = 'Gallon'
                    elif packaging_choice == '2':
                        packaging = 'Liter'
                    else:
                        print("Invalid packaging choice.")
                        continue

                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("Invalid quantity.")
                        continue

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
            # Calculate totals and display
            total_amount = 0
            print("---------------------------------------------------------------------"
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

                item_total = price * quantity
                total_amount += item_total
                print("{:<29} {:<7} ₱{:<8.2f} x {:<4}".format(index, packaging, price, quantity))

            # Payment
            while True:
                print("---------------------------------------------------------------------")
                print("{:<29} {:<7} ₱{:<8.2f}".format("", "TOTAL", total_amount))
                try:
                    amount_received = float(input("Payment Amount Received: "))
                    if amount_received < total_amount:
                        print("Insufficient amount received. Please enter a sufficient amount.")
                    else:
                        break
                except ValueError:
                    print("Invalid amount. Please enter a real number.")

            change = amount_received - total_amount
            print(f"Change: ₱{change:.2f}")
            input("Press Enter to continue...")

            # Save purchase history
            transaction_details = {
                "Items": purchase_list,
                "Total Amount": total_amount,
                "Amount Received": amount_received,
                "Change": change
            }
            self.transactions.append(transaction_details)

            if self.wholesale:
                self.save_purchase_history("transactions_wholesale.pkl")
            else:
                self.save_purchase_history("transactions_retail.pkl")

    def save_purchase_history(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.transactions, file)

    def load_purchase_history(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.transactions = pickle.load(file)
        except FileNotFoundError:
            self.transactions = []  # Initialize an empty list if the file doesn't exist
        except Exception as e:
            print("Error loading purchase history:", e)
            self.transactions = []  # Initialize an empty list if there's an error

    def display_purchase_history(self):
        print("\nPURCHASE HISTORY:\n")
        for index, purchase in enumerate(self.transactions, start=1):
            print(f"PURCHASE {index}:")
            if 'Items' in purchase:
                print("Items:")
                for item in purchase['Items']:
                    print(f" - {item['Name']} ({item['Packaging']}): x {item['Quantity']}")
            print(f"{'Total Amount:':<16}   ₱{purchase.get('Total Price', 0):.2f}")
            print(f"{'Amount Received:':<16}   ₱{purchase.get('Amount Received', 0):.2f}")
            print(f"{'Change:':<16}   ₱{purchase.get('Change', 0):.2f}")
            print()
        input("Press enter to continue")

    def clear_transactions(self):
        self.transactions = []
        print("Transaction history cleared.")
        if self.wholesale:
            self.save_purchase_history("transactions_wholesale.pkl")
        else:
            self.save_purchase_history("transactions_retail.pkl")

    def display_products(self):
        print(f"=====================================================================\n"
              f"\nPRODUCT LIST:")
        print("{:<6} {:<25} {:<20} {:<20}".format("Index", "Name", "[1] Gallon Price", "[2] Liter Price"))
        index = 1
        for name, prices in self.products.items():
            print("{:<6} {:<29} ₱{:<19.2f} ₱{:<19.2f}".format(str(index) + '.', name, prices[0], prices[1]))
            index += 1
        print("\n=====================================================================")
        if self.is_admin:
            input("Press enter to continue")

    def clear_products(self):
        self.products = {}
        print("Product list cleared.")
        if self.wholesale:
            self.save_products("products_wholesale.pkl")
        else:
            self.save_products("products_retail.pkl")

    def save_products(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.products, file)

    def load_products(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.products = pickle.load(file)
        except FileNotFoundError:
            self.products = {}
        except Exception as e:
            print("Error loading product list:", e)
            self.products = {}


def main():
    pos = System()
    header = ("\n====================================================================="
              "\n----------------------- POINT OF SALE SYSTEM ------------------------"
              "\n---------------- ALO KLEEN CHEMICAL PRODUCTS TRADING ----------------"
              "\n=====================================================================\n")
    print(f"{header}\n[1] Login\n[2] Exit")

    while True:
        choice = input("\nEnter Option: ")

        if choice == "1":
            username = input("Enter Username [admin|guest|0 Back]: ")
            if username == '0':
                main()
            password = input("Enter Password: ")
            pos.login(username, password)
            if pos.is_logged:
                break
        elif choice == "2":
            print("Exiting System...")
            exit()
        else:
            print("Invalid option. Please enter 1 to login or 2 to exit.")

    while True:
        print(f"{header} \nSALES TYPE: \n[1] Wholesale \n[2] Retail \n\n[0] Logout")

        sale_type = input("\nChoose an Option: ")

        if sale_type == "1":
            pos.wholesale = True
            pos.load_products("products_wholesale.pkl")
            pos.load_purchase_history("transactions_wholesale.pkl")
            sale_type_reminder = "WHOLESALE"
            break
        elif sale_type == "2":
            pos.wholesale = False
            pos.load_products("products_retail.pkl")
            pos.load_purchase_history("transactions_retail.pkl")
            sale_type_reminder = "RETAIL"
            break
        elif sale_type == "0":
            pos.logout()
            main()

        else:
            print("Invalid Option")

    while True:
        if pos.is_logged:
            print(f"{header}\nSALES TYPE: {sale_type_reminder}")
            if pos.is_admin:
                print("[1] Logout\n[2] Add Product\n[3] Delete Product\n[4] Display Products"
                      "\n[5] Save Products to File\n[6] Load Products from File\n[7] Display Purchase History"
                      "\n[8] Clear Purchase History\n[9] Clear Products List\n[10] Switch Sales Type")
            else:
                print("[1] Logout\n[2] New Transaction\n[3] Switch Sales Type")

            choice = input("Enter an Option: ")

            if pos.is_admin:
                if choice == "1":
                    pos.logout()
                    main()
                elif choice == "2":
                    pos.add_product()
                elif choice == "3":
                    pos.delete_product()
                elif choice == "4":
                    pos.display_products()
                elif choice == "5":
                    filename = input("Enter filename to save products: ")
                    pos.save_products(filename)
                    print("Products saved to file.")
                elif choice == "6":
                    filename = input("Enter filename to load products from: ")
                    pos.load_products(filename)
                    print("Products loaded from file.")
                elif choice == "7":
                    pos.display_purchase_history()
                elif choice == "8":
                    pos.clear_transactions()
                elif choice == "9":
                    pos.clear_products()
                elif choice == "10":
                    if pos.wholesale:
                        pos.wholesale = False
                        pos.load_products("products_retail.pkl")
                        pos.load_purchase_history("transactions_retail.pkl")
                        sale_type_reminder = "RETAIL"
                    else:
                        pos.wholesale = True
                        pos.load_products("products_wholesale.pkl")
                        pos.load_purchase_history("transactions_wholesale.pkl")
                        sale_type_reminder = "WHOLESALE"
                else:
                    print("Invalid Option.")
            else:
                if choice == "1":
                    pos.logout()
                    main()
                elif choice == "2":
                    pos.new_transaction()
                elif choice == "3":
                    if pos.wholesale:
                        pos.wholesale = False
                        pos.load_products("products_retail.pkl")
                        pos.load_purchase_history("transactions_retail.pkl")
                        sale_type_reminder = "RETAIL"
                    else:
                        pos.wholesale = True
                        pos.load_products("products_wholesale.pkl")
                        pos.load_purchase_history("transactions_wholesale.pkl")
                        sale_type_reminder = "WHOLESALE"
                else:
                    print("Invalid Option.")
        else:
            print("Invalid option. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
