# Stock Management System

This project is a Stock Management System built using Django. It helps manage products, stock levels, sales, and expenses efficiently. The system includes models for Categories, Items, Stock, Reorder Levels, Sales, Expenses, Accounts, and Transactions.

## Project Structure

### Models

1. **Category**
   - Represents the categories to which items belong.
   - Fields:
     - `name`: The name of the category.

2. **Item**
   - Represents an item in the inventory.
   - Fields:
     - `code`: Unique identifier for the item.
     - `name`: The name of the item.
     - `category`: ForeignKey linking to the Category model.
     - `unit_price`: The price per unit of the item.

3. **Stock**
   - Represents the stock details of an item.
   - Fields:
     - `item`: OneToOneField linking to the Item model.
     - `quantity`: The quantity of the item in stock.
     - `selling_price`: The price at which the item is being sold.
     - `date`: The date when the stock entry was created.

   - Methods:
     - `get_item_value()`: Returns the total value of the item in stock.

4. **Reorder**
   - Represents the reorder level for stock items.
   - Fields:
     - `stock`: ForeignKey linking to the Stock model.
     - `level`: The level at which the item needs to be reordered.

5. **Sale**
   - Represents a sale transaction.
   - Fields:
     - `first_name`: First name of the customer.
     - `last_name`: Last name of the customer.
     - `item`: ForeignKey linking to the Stock model.
     - `quantity`: The quantity of the item sold.
     - `amount_paid`: The total amount paid by the customer.
     - `mode_of_payment`: The mode of payment used (Cash or M-Pesa).
     - `date`: The date when the sale was made.

   - Methods:
     - `clean()`: Validates that the sale quantity does not exceed the available stock.
     - `save()`: Decreases the stock quantity by the sold amount and saves a credit transaction.

6. **Expenses**
   - Represents an expense entry.
   - Fields:
     - `description`: A description of the expense.
     - `amount`: The amount spent.

   - Methods:
     - `save()`: Creates a debit transaction for the expense.

7. **Account**
   - Represents an account for managing financial transactions.
   - Fields:
     - `name`: The name of the account.
     - `description`: A description of the account.

8. **CreditTransaction**
   - Represents a credit transaction.
   - Fields:
     - `account`: ForeignKey linking to the Account model.
     - `amount`: The amount of the credit transaction.
     - `transaction_date`: The date of the transaction.

9. **DebitTransaction**
   - Represents a debit transaction.
   - Fields:
     - `account`: ForeignKey linking to the Account model.
     - `amount`: The amount of the debit transaction.
     - `transaction_date`: The date of the transaction.

The Project will be updated soon regards

Me.
