# ======================= BOOKSTORE DATABASE ================================

# Import sqlite3 as this is needed in the program to create database.
import sqlite3

# Create/open database for the books, make sure to set cursor.
try:
    db = sqlite3.connect('ebookstore_db')
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(
        ID VARCHAR(4) PRIMARY KEY NOT NULL, 
        TITLE VARCHAR(30) NOT NULL, 
        AUTHOR VARCHAR(20), 
        QTY INTEGER(2))
        ''')
    db.commit

# if the database is not found then display an error
except Exception as e:
    db.rollback()
    raise e
finally:
    db.close

# ====== DEFINE FUNCTIONS ======

def add_book():
    '''Add book allows the user to add new books to the database.
    '''
    # Ask user for information about the book that they want to add to the database.
    stock_id = input('Please enter the stock ID:\n').lower()
    book_title = input('Please enter the title of the book:\n').lower()
    author = input("Please enter the Author:\n").lower()
    stock_value = int(input('Please enter the number of copies you want to add:\n'))

    # The new information is then added to the database using sqlite3 INSERT.
    cursor.execute('''INSERT INTO books(ID,TITLE,AUTHOR,QTY)
    VALUES(?,?,?,?)''',(stock_id,book_title,author,stock_value))
    db.commit()
    # Print out a confirmation that new item was successfully added.
    return print("\nNew item has been added to the database.\n")

def update_book():
    '''This allows the user to update any information on any of the books in the database.
    The appropriate field is then updated using the UPDATE sqlite3 function.
    '''
    # Ask the user for information to identify which book they want to update.
    book_to_update = input(
        "Please enter the ID for the book you want to update.\n"
        +"If ID is not known, type 'not known' to search:").lower()

    # IF the ID is not known, the user is then asked to search for the ID and start again.
    if book_to_update == 'not known':
        search_book()
    else:
        # Display the book details to confirm the selection.
        cursor.execute('''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE ID = ?''',(book_to_update,))
        data = cursor.fetchall()
        for row in data:
            print("\nBOOK FOUND:\n")
            print(f"ID:{row[0]}")
            print(f"Title: {row[1]}")
            print(f"Author: {row[2]}")
            print(f"QTY: {row[3]}")

        # Ask the user which field they would like to update.
        user_selection = True
        while user_selection:
            field_update = input("\nPlease enter the field you wish to update.\n"
                +"ID - to update ID.\n"
                +"Title - to change a books title.\n"
                +"Author - to change the Author.\n"
                +"QTY - to update stock.\n"
                +"Type Selection here: "
                ).upper()

            # Ask the user for the information they want to update.
            if field_update == 'ID':
                update_info = input(
                    "Please enter the new ID code for the book:\n")
                cursor.execute(
                    '''UPDATE books SET ID = ? WHERE ID = ?''',
                    (update_info,book_to_update,))
                db.commit
                user_selection = False

            elif field_update == 'TITLE':
                update_info = input(
                    "Please enter the new title for this book:\n")
                cursor.execute('''UPDATE books SET TITLE = ? WHERE ID = ?''',
                (update_info,book_to_update,))
                db.commit
                user_selection = False

            elif field_update == 'AUTHOR':
                update_info = input(
                    "Please type the updated author name:\n")
                cursor.execute('''UPDATE books SET AUTHOR = ? WHERE ID = ?''',
                (update_info,book_to_update,))
                db.commit
                user_selection = False

            elif field_update == 'QTY':
                update_info = input(
                    "Please enter the new total stock quantity:\n")
                cursor.execute('''UPDATE books SET QTY = ? WHERE ID = ?''',
                (update_info,book_to_update))
                db.commit
                user_selection = False

            # If the user makes an invalid entry, ask for the selection again.
            else:
                print("Invalid request, please try again.")

    # Print a statement to confirm the database has been updated.
    return print("\nThe database has been successfully updated.\n")


def delete_book():
    '''This will allow the user to delete a book from the database.
    Ask the user for the unique ID for the book they would like to delete,
    the deletion will be confirmed before it's deleted.
    '''

    # Ask the user for the information for the book they would like to delete.
    user_selection = True
    while user_selection:
        book_to_delete = input(
            "Please enter the ID for the book you would like to delete from the database.\n"
            +"If you do not know the ID, please enter 'title' to search by the book title:\n").lower()
        if book_to_delete == 'title':
            book_to_delete = input(
                "Please enter the title of the book you want to delete:\n"
            ).lower()
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE TITLE = ?''',
                (book_to_delete,))
            data = cursor.fetchall()
            # Display the details of the book to confirm the deletion with the user.
            for row in data:
                print("\n")
                print(f"ID:{row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"QTY: {row[3]}")
            correct_entry = input("Please confirm you would like to delete this from the database, 'yes' to delete:\n").lower()

            if correct_entry =='yes':
                # Delete the entry from the database.
                book_id = row[0]
                user_selection = False
            # If the user types anything other than 'yes', they will be taken back to the main menu.
            else:
                return print("\nNothing has been deleted, returning to the main menu.\n")

        # If the ID is known, the details of the book will be displayed to confirm the action.
        else:
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE ID = ?''',
                (book_to_delete,))
            data = cursor.fetchall()
            for row in data:
                print("\n")
                print(f"ID:{row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"QTY: {row[3]}")
            correct_entry = input(
                "\nAre you sure you want to delete this item? Type 'yes' to confirm:\n").lower()

            if correct_entry =='yes':
                # Delete the entry from the database.
                book_id = row[0]
                user_selection = False
            # Use else statement to take the user to the main menu if they don't type 'yes'.
            else:
                return print("\nReturn to the main menu. \n")

    # Delete the book information from database using the book's ID information.
    cursor.execute('''DELETE FROM books WHERE ID = ?''',(book_id,))
    db.commit
    # Display a confirmation that the database has been updated.
    return print("\nThe book details has been removed from the database. \n")

def search_books():
    '''This will allow the user to search for books in the database.
    The user can choose what criteria they want to use to search for the books.
    '''
    # Ask the user what criteria they would like to use in the search.
    user_selection = True
    while user_selection:
        search_items = input(
            "Please choose how you would like to search for items.\n"
            +"Enter 'ID' to search by using the entry's ID code.\n"
            +"Enter 'title' to search by the book title.\n"
            +"Enter 'author' to search by the author.\n"
            +"Please type your choice here: "
            ).upper()
        # Depending on the user's choice, different method will be used.
        if search_items == 'ID':
            search_criteria = input(
                "Please enter the ID code for the book you want to find:\n")
            # Use SELECT function to retrieve the relevant data.
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE ID = ?'''
                ,(search_criteria,))
            data = cursor.fetchall()
            user_selection = False

        elif search_items == 'title':
            search_criteria = input("Please enter the title of the book:\n")
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE TITLE = ?'''
                ,(search_criteria,))
            data = cursor.fetchall()
            user_selection = False

        elif search_items == 'author':
            search_criteria = input("Please enter the name of the author:\n")
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE AUTHOR = ?'''
                ,(search_criteria,))
            data = cursor.fetchall()
            user_selection = False

        else:
            print("Incorrect entry, please try again.")
            user_selection = True

    # Use for loop to iterate through the data to display the information wanted.
    for row in data:
        print('\n')
        print(f"ID:{row[0]}")
        print(f"Title: {row[1]}")
        print(f"Author: {row[2]}")
        print(f"QTY: {row[3]}")
        print('\n')
    return print('\n- END OF RECORDS -\n')


def view_all():
    '''This allows the user to view all data stored in the database.
    This function will display all the data that is currently stored in the database.
        '''
    cursor.execute('''SELECT ID,TITLE,AUTHOR,QTY FROM books''')
    for row in cursor:
            print("\n======\n")
            print(f"ID:{row[0]}")
            print(f"Title: {row[1]}")
            print(f"Author: {row[2]}")
            print(f"QTY: {row[3]}")
            print("\n=======\n")

#========== MAIN MENU =============
# The following username and password are stored in the user.txt file and can be used to access the program.
# username : admin
# password : adm1n

username_requested = True
password_requested = True

# Use a loop to ask for correct login details to access the database.
while username_requested:
    with open('user.txt', 'r') as users:
        username = input("Please enter a valid username:\n")
        for lines in users:
            if username in lines:
                    print('Correct username has been entered.')
                    username_requested = False
                    # once a valid username is entered the program will ask for a valid password.
                    true_password = [lines.split()[1]]

# Use a loop to check for the correct password.
while password_requested:
    password = input("Please enter your password:\n")
    if password in true_password:  # if the password matches true_password
        print("\nCorrect password.")
        # When the user enters the correct password, the password_requested becomes false and loop is closed.
        # Login_correct will then become true.
        password_requested = False
        login_correct = True
    # If incorrect password was entered, ask the user to re-enter the password.
    else:
        print("The password entered was incorrect, please try again.")

# When the user has successfully logged it, the menu is presented to them.
while login_correct:
    menu = input('''Choose one of the following actions:
    add - Add new items to the database.
    update - Update book information.
    search - Search the database to find a specific book.
    delete - Delete books from the database.
    view - View all books in the database.
    exit - Exit the program.
    Type the action here: ''').lower()

    if menu == "add":
        add_book()

    elif menu == "update":
        update_book()
    
    elif menu == "search":
        search_books()

    elif menu == "delete":
        delete_book()

    elif menu == "view":
        view_all()
    
    elif menu == "exit":
        print("You are now exiting the program, goodbye.")
        exit()

    else:
        print("\nIncorrect selection, please try again.")