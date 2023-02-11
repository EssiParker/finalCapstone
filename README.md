# finalCapstone
bookstore_clerk
A python based app used to perform functions on a sqlite3 Database. Modelled for this purpose on an imaginary Bookstore. Designed to demonstrate my understanding of manipulating databases in python.

Credentials for demo use:
username: admin password: adm1n

To run this file in Docker play ground open an instance and type: docker run -i admbjmn/bookstore_clerk

The files is easier to interpret in VS code and will provide you with more functionality - ie: viewing generated files.

This Task Management system is a simple stand alone program that allows a user to read, update and delete entries in an sqlite database details about inventory items.

Key Components
Functions

add_book
update_info
delete_book
search_book
view_all
Functions explained.
The Program starts with a Login function that references users and passwords from a separate text file. The program can be accessed by default with username: admin password: adm1n

add_book
add_book allows the user to update the data base with a new entry. The user is asked to provide information about the object which wil then be updated to the relevent fields within the database.

update_info
Update info allows the user to change the value in a certain feild for a particualar entry. The user is asked to input the code of the book they wish to update and is shown their selection for confirmation. A follow up question is asked as to which field they wish to update. New information is then gathered through the user interface and the appropriate field is then updated via the UPDATE sqlite3 function.

delete_book
Delete book allows the user to remove an entry from the database. The user is asked to enter the code of the book they wish to delete. The user is then shown the full entry for this book and asked to confirm if they wish to delete this item

search_book
Search allows the user to search based on a chosen criteria. The search results will show all items that have associate feilds for example if the user chooses to search by author, all books written by the search author will be displayed, however if the user chooses to search by code then only the book with that code will be displayed.

view_all
View all gathers all information form the database and displays it to the user in a readible manner.

Basic Program flow.
Once logged in the user is presented with a main menu.

By selecting one of the commands as instructed the user is then prompted with new instructions based on the selection.

By continuing to follow the prompts on screen tasks can be taken care of and the database will be updated. Any functions that do not need user input will be displayed on screen and the menu will be re shown for any further requests.

View all, for example, will display all information and then the function will end automatically.

Once the user has finished the program can be closed from the main menu by typing exit.
