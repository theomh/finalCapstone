# Database management system for a book store using sqlite, python

from tabulate import tabulate
import sqlite3

# opens/creates ebookstore database binds to "db", bind cursor object to "cursor"
db = sqlite3.connect("ebookstore")
cursor = db.cursor()

# try to create and populate table, skip if db already exists.
try:
    cursor.execute("""
        CREATE TABLE ebookstore (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        qty INTEGER)
    """)
    db.commit()

    # The initial table of books to add:
    books_ = [
        (3001, """A Tale of Two Cities""", """Charles Dickens""", 30),
        (3002, """Harry Potter and the Philosopher's Stone""", """J.K Rowling""", 40),
        (3003, """The Lion, the Witch and the Wardrobe""", """C.S Lewis""", 25),
        (3004, """The Lord of the Rings""", """J.R.R Tolkien""", 37),
        (3005, """Alice in Wonderland""", """Lewis Carrol""", 12), ]

    cursor.executemany("""
        INSERT INTO ebookstore(id, title, author, qty)
        VALUES (?,?,?, ?)""", books_)
    db.commit()
    print("Database Created.")

except sqlite3.OperationalError:
    pass

except sqlite3.InternalError:
    print("Database error: duplicate unique IDs registered.")


# a function to supply data from the database
# args accepted id, title, author, quantity
# default is to return whole database
def get_data(**search_args):
    for key, value in search_args.items():
        if key == "ID":
            cursor.execute("""SELECT * FROM ebookstore WHERE id = ?""", (value,))
            return cursor.fetchall()

        elif key == "TITLE":
            cursor.execute("""SELECT * FROM ebookstore WHERE title = ?""", (value,))
            return cursor.fetchall()

        elif key == "AUTHOR":
            cursor.execute("""SELECT * FROM ebookstore WHERE author = ?""", (value,))
            return cursor.fetchall()

        elif key == "QUANTITY":
            cursor.execute("""SELECT * FROM ebookstore WHERE qty = ?""", (value,))
            return cursor.fetchall()

    cursor.execute("""SELECT * FROM ebookstore""")
    return cursor.fetchall()


def user_search():  # Gets how the user wants to search
    user_choice = ''

    while user_choice != "quit":
        user_choice = input(
            "Search by id/title/author/quantity/quit\n> ").upper()

        if user_choice == "ID":
            search_term = input("Enter ID: ")
            search_results = get_data(ID=search_term)
            if search_results:
                print(tabulate(search_results, headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]),
                      "\n")  # use tabulate to print table.
            else:
                print(f"ID: {search_term} not found in database.")

        elif user_choice == "TITLE":
            search_term = input("Enter Title: ")
            search_results = get_data(TITLE=search_term)
            if search_results:
                print(tabulate(search_results, headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]),
                      "\n")  # use tabulate to print table.
            else:
                print(f"TITLE: {search_term} not found in database.")

        elif user_choice == "AUTHOR":
            search_term = input("Enter Author: ")
            search_results = get_data(AUTHOR=search_term)
            if search_results:
                print(tabulate(search_results, headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]),
                      "\n")  # use tabulate to print table.
            else:
                print(f"AUTHOR: {search_term} not found in database.")

        elif user_choice == "QUANTITY":
            search_term = input("Enter Quantity: ")
            search_results = get_data(QUANTITY=search_term)
            if search_results:
                print(tabulate(search_results, headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]),
                      "\n")  # use tabulate to print table.
            else:
                print(f"QUANTITY: {search_term} not found in database.")

        elif user_choice == "QUIT":
            return

        else:
            print("Input not recognised!")  # fail


def delete_book():
    delete_choice = ""

    while delete_choice != "quit":
        delete_choice = input("You can delete a book by typing it's ID or type quit.\n> ").lower()

        if delete_choice == "quit":
            return
        else:
            try:
                if get_data(ID=delete_choice):
                    print("Record found. Please check record before confirming deletion!")
                    print(tabulate(get_data(ID=delete_choice, headers=["ID", "TITLE", "AUTHOR", "QUANTITY"])))

                    if confirm_choice() == "YES":  # Get confirmation
                        cursor.execute("""DELETE FROM ebookstore WHERE id=?""", (delete_choice,))
                        print(f"ID: {delete_choice} deleted.")
                        return
                    else:
                        return

                else:
                    print(f"ID: {delete_choice} not found.")
            except Exception:
                raise


def confirm_choice():
    confirm_action = ""

    while confirm_action != "YES":
        confirm_action = input("type YES to confirm, type NO to return to main menu.\n> ").upper()
        if confirm_action == "NO":
            return "NO"
        elif confirm_action != "YES":
            print("Input not recognised!")  # fail
    return "YES"


def add_book():
    add_book_id = ""

    while add_book_id != "quit":
        add_book_id = input("Add a book by entering a 4 digit ID or type quit.\n> ").lower()

        if add_book_id == "quit":
            return
        elif get_data(ID=add_book_id):
            print(f"ID already in use.")
        elif len(add_book_id) == 4 and add_book_id.isnumeric():
            new_data = []
            new_data.append(add_book_id)
            new_data.append((input(f"Enter Title: ") or "default_book_title"))
            new_data.append((input(f"Enter Author: ") or "default_book_author"))
            new_data.append((input(f"Enter Quantity: ") or "default_book_quantity"))
            print(tabulate([new_data], headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]))
            print("Is all this information correct?")
            if confirm_choice() == "YES":  # Get confirmation

                cursor.execute("""
                INSERT INTO ebookstore(id, title, author, qty)
                    VALUES (?,?,?,?)""", (new_data[0], new_data[1], new_data[2], new_data[3]))
                db.commit()
                print(f"ID: {new_data[0]} added to database.\n")
                print(tabulate(get_data(), headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]),
                      "\n")  # use tabulate to print table.
            else:
                return
            return


def modify_book():
    modify_choice = ""

    while modify_choice != "quit":
        modify_choice = input("You can modify a book by typing it's ID or type quit.\n> ").lower()

        if modify_choice == "quit":
            return
        else:
            try:
                if get_data(ID=modify_choice):
                    print("Record found. Please check record is correct!")
                    print(tabulate(get_data(ID=modify_choice, headers=["ID", "TITLE", "AUTHOR", "QUANTITY"])))
                    book_data = get_data(ID=modify_choice)
                    book_id, book_title, book_author, book_quantity = book_data[(0)]
                    new_data = []
                    print("\nType the new value or hit enter to keep it the same")
                    new_data.append(book_id)
                    new_data.append((input(f"{book_title}: ") or book_title))
                    new_data.append((input(f"{book_author}: ") or book_author))
                    new_data.append((input(f"{book_quantity}: ") or book_quantity))
                    book_data.append(new_data)
                    print(tabulate(book_data, headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]))
                    print("Are these updated values correct?")
                    if confirm_choice() == "YES":  # Get confirmation, if YES write using SQL to db
                        cursor.execute("""
                            UPDATE ebookstore
                            SET
                            title = ?,
                            author = ?,
                            qty = ?
                            WHERE
                            id = ?
                            """, (new_data[1], new_data[2], new_data[3], new_data[0]))
                        db.commit()
                        print(f"ID: {book_id} modified.")
                        return
                    else:
                        return

                else:
                    print(f"ID: {modify_choice} not found.")
            except Exception:
                raise


#  MAIN ===


user_choice = ""

while user_choice != "quit":
    user_choice = input(
        "What would you like to do? - view all/add/search/delete/modify/quit\n> ").lower()

    if user_choice in ["view", "view all"]:
        print(tabulate(get_data(), headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]), "\n")  # use tabulate to print table.
    elif user_choice in ["search", "search books"]:
        user_search()
    elif user_choice in ["delete", "delete book"]:
        print(tabulate(get_data(), headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]), "\n")  # use tabulate to print table.
        delete_book()
    elif user_choice in ["add", "add book"]:
        print(tabulate(get_data(), headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]), "\n")  # use tabulate to print table.
        add_book()
    elif user_choice in ["modify", "modify book"]:
        print(tabulate(get_data(), headers=["ID", "TITLE", "AUTHOR", "QUANTITY"]), "\n")  # use tabulate to print table.
        modify_book()
    elif user_choice in ["quit", "exit"]:
        print("Goodbye!")
    else:
        print("Input not recognised!")  # fail
