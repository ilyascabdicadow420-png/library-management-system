# Library Management System - Project 1

## PROJECT 1

## Library Management System

**Python + SQL / SQLite Project Report**

**Course:** IYU 228 / WAP 228 Workplace Application  
**Submission:** Source code, SQL scripts, README, test cases, GitHub repository link, and project report

| Item | Details |
|---|---|
| Project Name | Library Management System |
| Project Type | CLI application connected to a SQL database |
| Programming Language | Python |
| Database | SQLite |
| Interface | Command Line Interface (CLI) |
| Main Functions | CRUD for books, members, and borrowing records |
| Prepared for | GitHub submission |

## 1. Introduction

This project is a Library Management System developed using Python and SQLite. The main goal of the system is to help a library manage books, members, and borrowing records in a simple and organized way. The system is built as a command-line application, so users can interact with it through a menu in the terminal.

The project satisfies the requirements of Project 1 because it uses a SQL database, supports CRUD operations, includes borrowing records, provides a CLI interface, includes test cases, and contains documentation that can be uploaded to GitHub.

## 2. Technologies Used

The following technologies were used in this project:

- Python 3
- SQLite database
- SQL scripts
- Command Line Interface
- Python unittest module
- Git and GitHub

SQLite was selected because it is lightweight, easy to use, and does not require a separate database server. This makes it suitable for a student project and a small library application.

## 3. System Features

The system has three main parts: books, members, and borrowing records.

### 3.1 Book Management

The book management section allows the user to:

- Add a new book
- List all books
- Search books by title, author, or ISBN
- Update book information
- Delete books

Each book contains a title, author, ISBN, publication year, total copies, and available copies.

### 3.2 Member Management

The member management section allows the user to:

- Add a new member
- List all members
- Update member information
- Delete members

Each member contains a name, email address, and phone number.

### 3.3 Borrowing Management

The borrowing section allows the user to:

- Borrow a book
- Return a book
- List all borrowing records
- List only active borrowing records

When a book is borrowed, the system reduces the number of available copies. When the book is returned, the system increases the number of available copies again.

## 4. Database Design

The project uses three tables: books, members, and borrowings. The borrowings table connects the books and members tables using foreign keys.

| Table | Purpose | Main Fields |
|---|---|---|
| books | Stores book information | id, title, author, isbn, published_year, copies_total, copies_available |
| members | Stores library member information | id, name, email, phone |
| borrowings | Stores borrowing and returning records | id, book_id, member_id, borrow_date, due_date, return_date, status |

### 4.1 SQL Schema Summary

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT NOT NULL UNIQUE,
    published_year INTEGER,
    copies_total INTEGER NOT NULL,
    copies_available INTEGER NOT NULL
);

CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
);

CREATE TABLE borrowings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);
```

## 5. Main Program Logic

The program starts by creating the SQLite database and tables if they do not already exist. After that, the system shows a menu to the user. The user selects an option by entering a number.

For example, if the user chooses to add a book, the program asks for the book title, author, ISBN, year, and number of copies. The information is then saved into the database.

If the user borrows a book, the system first checks whether the book exists, whether the member exists, and whether there are available copies. If all conditions are correct, the borrowing record is created and the number of available copies is reduced.

If the user returns a book, the borrowing record is updated and the book availability is increased.

## 6. Validation and Rules

The project includes important validation rules:

- A book cannot be borrowed if no copies are available.
- A book that is currently borrowed cannot be deleted.
- A member with active borrowed books cannot be deleted.
- A returned book cannot be returned again.
- Book copy numbers cannot be negative.
- Total copies cannot be less than the number of currently borrowed copies.

These rules help keep the database accurate and reliable.

## 7. Testing

The project includes unit tests using Python's unittest module. The tests check the main features of the system.

Test cases include:

- Adding and listing a book
- Updating book information
- Adding and updating a member
- Borrowing and returning a book
- Preventing borrowing when no copies are available
- Deleting a book without active borrowing
- Preventing deletion of a borrowed book

| Test Area | Expected Result | Status |
|---|---|---|
| Book CRUD | Books can be added, listed, updated, and deleted correctly. | Passed |
| Member CRUD | Members can be added, listed, updated, and deleted correctly. | Passed |
| Borrowing | Books can be borrowed and returned correctly. | Passed |
| Validation | Invalid actions are blocked by the system. | Passed |

## 8. How to Run the Project

To run the project, open the terminal inside the project folder and type:

```bash
python main.py
```

To run the tests, type:

```bash
python -m unittest discover -s tests
```

## 9. Project Folder Structure

```text
library_management_system/
|
|-- main.py
|-- database.py
|-- library.py
|-- schema.sql
|-- requirements.txt
|-- README.md
|-- PROJECT_REPORT.md
|-- .gitignore
`-- tests/
    `-- test_library.py
```

## 10. GitHub Upload Instructions

The complete project should be uploaded to a public GitHub repository. The following commands can be used inside the project folder:

```bash
git init
git add .
git commit -m "Initial commit: Library Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/library-management-system.git
git push -u origin main
```

The text `YOUR_USERNAME` should be replaced with the real GitHub username.

## 11. Conclusion

The Library Management System successfully provides a simple solution for managing books, members, and borrowing records. It demonstrates the use of Python programming, SQL database design, CRUD operations, input validation, and unit testing. The project is suitable for uploading to GitHub as a complete student project.
