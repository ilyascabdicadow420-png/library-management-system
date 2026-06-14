"""Command Line Interface for the Library Management System."""

from database import initialize_database
from library import Library, LibraryError


def print_books(books):
    if not books:
        print("No books found.")
        return
    print("\nID | Title | Author | ISBN | Year | Total | Available")
    print("-" * 75)
    for book in books:
        print(
            f"{book['id']} | {book['title']} | {book['author']} | {book['isbn']} | "
            f"{book['published_year']} | {book['copies_total']} | {book['copies_available']}"
        )


def print_members(members):
    if not members:
        print("No members found.")
        return
    print("\nID | Name | Email | Phone")
    print("-" * 60)
    for member in members:
        print(f"{member['id']} | {member['name']} | {member['email']} | {member['phone']}")


def print_borrowings(records):
    if not records:
        print("No borrowing records found.")
        return
    print("\nID | Book | Member | Borrow Date | Due Date | Return Date | Status")
    print("-" * 90)
    for record in records:
        print(
            f"{record['id']} | {record['title']} | {record['name']} | {record['borrow_date']} | "
            f"{record['due_date']} | {record['return_date']} | {record['status']}"
        )


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def book_menu(library):
    while True:
        print("\n--- Book Management ---")
        print("1. Add book")
        print("2. List books")
        print("3. Search books")
        print("4. Update book")
        print("5. Delete book")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                year = read_int("Published year: ")
                copies = read_int("Total copies: ")
                book_id = library.add_book(title, author, isbn, year, copies)
                print(f"Book added successfully. ID: {book_id}")
            elif choice == "2":
                print_books(library.list_books())
            elif choice == "3":
                keyword = input("Enter title, author, or ISBN: ")
                print_books(library.search_books(keyword))
            elif choice == "4":
                book_id = read_int("Book ID: ")
                print("Leave a field empty to keep the current value.")
                title = input("New title: ")
                author = input("New author: ")
                isbn = input("New ISBN: ")
                year_text = input("New published year: ").strip()
                copies_text = input("New total copies: ").strip()
                year = None if year_text == "" else int(year_text)
                copies = None if copies_text == "" else int(copies_text)
                library.update_book(book_id, title, author, isbn, year, copies)
                print("Book updated successfully.")
            elif choice == "5":
                book_id = read_int("Book ID: ")
                library.delete_book(book_id)
                print("Book deleted successfully.")
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except LibraryError as error:
            print(f"Error: {error}")


def member_menu(library):
    while True:
        print("\n--- Member Management ---")
        print("1. Add member")
        print("2. List members")
        print("3. Update member")
        print("4. Delete member")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                member_id = library.add_member(name, email, phone)
                print(f"Member added successfully. ID: {member_id}")
            elif choice == "2":
                print_members(library.list_members())
            elif choice == "3":
                member_id = read_int("Member ID: ")
                print("Leave a field empty to keep the current value.")
                name = input("New name: ")
                email = input("New email: ")
                phone = input("New phone: ")
                library.update_member(member_id, name, email, phone)
                print("Member updated successfully.")
            elif choice == "4":
                member_id = read_int("Member ID: ")
                library.delete_member(member_id)
                print("Member deleted successfully.")
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except LibraryError as error:
            print(f"Error: {error}")


def borrowing_menu(library):
    while True:
        print("\n--- Borrowing Management ---")
        print("1. Borrow book")
        print("2. Return book")
        print("3. List all borrowing records")
        print("4. List active borrowing records")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                book_id = read_int("Book ID: ")
                member_id = read_int("Member ID: ")
                days = read_int("Borrowing days: ")
                borrowing_id = library.borrow_book(book_id, member_id, days)
                print(f"Book borrowed successfully. Borrowing ID: {borrowing_id}")
            elif choice == "2":
                borrowing_id = read_int("Borrowing ID: ")
                library.return_book(borrowing_id)
                print("Book returned successfully.")
            elif choice == "3":
                print_borrowings(library.list_borrowings())
            elif choice == "4":
                print_borrowings(library.list_borrowings(active_only=True))
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except LibraryError as error:
            print(f"Error: {error}")


def main():
    connection = initialize_database()
    library = Library(connection)

    while True:
        print("\n==============================")
        print(" Library Management System")
        print("==============================")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Borrowing Management")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            book_menu(library)
        elif choice == "2":
            member_menu(library)
        elif choice == "3":
            borrowing_menu(library)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

    connection.close()


if __name__ == "__main__":
    main()
