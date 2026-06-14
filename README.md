# Library Management System

This is a simple Library Management System built with Python and SQLite. It is a command-line interface application that allows a library to manage books, members, and borrowing records.

## Project Information

- **Project Type:** CLI application connected to a SQL database
- **Programming Language:** Python
- **Database:** SQLite
- **Main Features:** CRUD operations for books, members, and borrowings
- **Testing:** Python unittest

## Features

### Book Management

- Add a new book
- List all books
- Search books by title, author, or ISBN
- Update book information
- Delete books

### Member Management

- Add a new member
- List all members
- Update member information
- Delete members

### Borrowing Management

- Borrow a book
- Return a book
- List all borrowing records
- List active borrowing records

## Validation Rules

- A book cannot be borrowed if no copies are available.
- A book that is currently borrowed cannot be deleted.
- A member with active borrowed books cannot be deleted.
- A returned book cannot be returned again.
- Book copy numbers cannot be negative.
- Total copies cannot be less than the number of currently borrowed copies.

## Database Tables

The project uses three tables:

1. `books`
2. `members`
3. `borrowings`

The `borrowings` table connects books and members using foreign keys.

## Folder Structure

```text
library_management_system/
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

## How to Run

Open the terminal inside the project folder and run:

```bash
python main.py
```

## How to Run Tests

```bash
python -m unittest discover -s tests
```

## GitHub Upload Commands

```bash
git init
git add .
git commit -m "Initial commit: Library Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/library-management-system.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your real GitHub username.
