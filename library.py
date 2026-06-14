"""Core business logic for the Library Management System."""

from datetime import date, timedelta
import sqlite3


class LibraryError(Exception):
    """Custom exception for library validation errors."""


def _row_to_dict(row):
    return dict(row) if row is not None else None


class Library:
    """Service class that manages books, members, and borrowing records."""

    def __init__(self, connection):
        self.connection = connection
        self.connection.execute("PRAGMA foreign_keys = ON")

    # -------------------------
    # Book Management
    # -------------------------
    def add_book(self, title, author, isbn, published_year, copies_total):
        if not title.strip():
            raise LibraryError("Book title cannot be empty.")
        if not author.strip():
            raise LibraryError("Author name cannot be empty.")
        if not isbn.strip():
            raise LibraryError("ISBN cannot be empty.")
        if int(copies_total) < 0:
            raise LibraryError("Total copies cannot be negative.")

        try:
            cursor = self.connection.execute(
                """
                INSERT INTO books (title, author, isbn, published_year, copies_total, copies_available)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title.strip(), author.strip(), isbn.strip(), published_year, int(copies_total), int(copies_total)),
            )
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise LibraryError("A book with this ISBN already exists.") from exc

    def list_books(self):
        cursor = self.connection.execute("SELECT * FROM books ORDER BY id")
        return [dict(row) for row in cursor.fetchall()]

    def get_book(self, book_id):
        cursor = self.connection.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        return _row_to_dict(cursor.fetchone())

    def search_books(self, keyword):
        keyword = f"%{keyword.strip()}%"
        cursor = self.connection.execute(
            """
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ORDER BY id
            """,
            (keyword, keyword, keyword),
        )
        return [dict(row) for row in cursor.fetchall()]

    def update_book(self, book_id, title=None, author=None, isbn=None, published_year=None, copies_total=None):
        book = self.get_book(book_id)
        if book is None:
            raise LibraryError("Book not found.")

        borrowed_count = book["copies_total"] - book["copies_available"]
        new_copies_total = book["copies_total"] if copies_total is None else int(copies_total)

        if new_copies_total < 0:
            raise LibraryError("Total copies cannot be negative.")
        if new_copies_total < borrowed_count:
            raise LibraryError("Total copies cannot be less than currently borrowed copies.")

        new_available = new_copies_total - borrowed_count

        new_title = book["title"] if title is None or title.strip() == "" else title.strip()
        new_author = book["author"] if author is None or author.strip() == "" else author.strip()
        new_isbn = book["isbn"] if isbn is None or isbn.strip() == "" else isbn.strip()
        new_year = book["published_year"] if published_year is None else published_year

        try:
            self.connection.execute(
                """
                UPDATE books
                SET title = ?, author = ?, isbn = ?, published_year = ?, copies_total = ?, copies_available = ?
                WHERE id = ?
                """,
                (new_title, new_author, new_isbn, new_year, new_copies_total, new_available, book_id),
            )
            self.connection.commit()
        except sqlite3.IntegrityError as exc:
            raise LibraryError("Another book with this ISBN already exists.") from exc

    def delete_book(self, book_id):
        book = self.get_book(book_id)
        if book is None:
            raise LibraryError("Book not found.")

        active = self.connection.execute(
            "SELECT COUNT(*) AS total FROM borrowings WHERE book_id = ? AND status = 'active'",
            (book_id,),
        ).fetchone()["total"]

        if active > 0:
            raise LibraryError("This book cannot be deleted because it is currently borrowed.")

        self.connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.connection.commit()

    # -------------------------
    # Member Management
    # -------------------------
    def add_member(self, name, email, phone=""):
        if not name.strip():
            raise LibraryError("Member name cannot be empty.")
        if not email.strip():
            raise LibraryError("Email cannot be empty.")

        try:
            cursor = self.connection.execute(
                "INSERT INTO members (name, email, phone) VALUES (?, ?, ?)",
                (name.strip(), email.strip(), phone.strip()),
            )
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise LibraryError("A member with this email already exists.") from exc

    def list_members(self):
        cursor = self.connection.execute("SELECT * FROM members ORDER BY id")
        return [dict(row) for row in cursor.fetchall()]

    def get_member(self, member_id):
        cursor = self.connection.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        return _row_to_dict(cursor.fetchone())

    def update_member(self, member_id, name=None, email=None, phone=None):
        member = self.get_member(member_id)
        if member is None:
            raise LibraryError("Member not found.")

        new_name = member["name"] if name is None or name.strip() == "" else name.strip()
        new_email = member["email"] if email is None or email.strip() == "" else email.strip()
        new_phone = member["phone"] if phone is None else phone.strip()

        try:
            self.connection.execute(
                "UPDATE members SET name = ?, email = ?, phone = ? WHERE id = ?",
                (new_name, new_email, new_phone, member_id),
            )
            self.connection.commit()
        except sqlite3.IntegrityError as exc:
            raise LibraryError("Another member with this email already exists.") from exc

    def delete_member(self, member_id):
        member = self.get_member(member_id)
        if member is None:
            raise LibraryError("Member not found.")

        active = self.connection.execute(
            "SELECT COUNT(*) AS total FROM borrowings WHERE member_id = ? AND status = 'active'",
            (member_id,),
        ).fetchone()["total"]

        if active > 0:
            raise LibraryError("This member cannot be deleted because they have active borrowed books.")

        self.connection.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.connection.commit()

    # -------------------------
    # Borrowing Management
    # -------------------------
    def borrow_book(self, book_id, member_id, days=14):
        book = self.get_book(book_id)
        if book is None:
            raise LibraryError("Book not found.")

        member = self.get_member(member_id)
        if member is None:
            raise LibraryError("Member not found.")

        if book["copies_available"] <= 0:
            raise LibraryError("This book is not available for borrowing.")

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=int(days))

        cursor = self.connection.execute(
            """
            INSERT INTO borrowings (book_id, member_id, borrow_date, due_date, return_date, status)
            VALUES (?, ?, ?, ?, NULL, 'active')
            """,
            (book_id, member_id, borrow_date.isoformat(), due_date.isoformat()),
        )
        self.connection.execute(
            "UPDATE books SET copies_available = copies_available - 1 WHERE id = ?",
            (book_id,),
        )
        self.connection.commit()
        return cursor.lastrowid

    def return_book(self, borrowing_id):
        borrowing = self.get_borrowing(borrowing_id)
        if borrowing is None:
            raise LibraryError("Borrowing record not found.")

        if borrowing["status"] == "returned":
            raise LibraryError("This book has already been returned.")

        return_date = date.today().isoformat()
        self.connection.execute(
            "UPDATE borrowings SET return_date = ?, status = 'returned' WHERE id = ?",
            (return_date, borrowing_id),
        )
        self.connection.execute(
            "UPDATE books SET copies_available = copies_available + 1 WHERE id = ?",
            (borrowing["book_id"],),
        )
        self.connection.commit()

    def get_borrowing(self, borrowing_id):
        cursor = self.connection.execute("SELECT * FROM borrowings WHERE id = ?", (borrowing_id,))
        return _row_to_dict(cursor.fetchone())

    def list_borrowings(self, active_only=False):
        if active_only:
            query = """
                SELECT b.id, books.title, members.name, b.borrow_date, b.due_date, b.return_date, b.status
                FROM borrowings b
                JOIN books ON b.book_id = books.id
                JOIN members ON b.member_id = members.id
                WHERE b.status = 'active'
                ORDER BY b.id
            """
            cursor = self.connection.execute(query)
        else:
            query = """
                SELECT b.id, books.title, members.name, b.borrow_date, b.due_date, b.return_date, b.status
                FROM borrowings b
                JOIN books ON b.book_id = books.id
                JOIN members ON b.member_id = members.id
                ORDER BY b.id
            """
            cursor = self.connection.execute(query)

        return [dict(row) for row in cursor.fetchall()]
