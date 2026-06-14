import sqlite3
import unittest
from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from library import Library, LibraryError


SCHEMA_PATH = PROJECT_DIR / "schema.sql"


class TestLibraryManagementSystem(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            self.connection.executescript(schema_file.read())
        self.library = Library(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_add_and_list_book(self):
        book_id = self.library.add_book("Python Basics", "John Smith", "ISBN001", 2024, 3)
        books = self.library.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["id"], book_id)
        self.assertEqual(books[0]["title"], "Python Basics")
        self.assertEqual(books[0]["copies_available"], 3)

    def test_update_book_information(self):
        book_id = self.library.add_book("Old Title", "Old Author", "ISBN002", 2020, 2)
        self.library.update_book(book_id, title="New Title", author="New Author", published_year=2025, copies_total=5)
        book = self.library.get_book(book_id)
        self.assertEqual(book["title"], "New Title")
        self.assertEqual(book["author"], "New Author")
        self.assertEqual(book["published_year"], 2025)
        self.assertEqual(book["copies_total"], 5)
        self.assertEqual(book["copies_available"], 5)

    def test_add_and_update_member(self):
        member_id = self.library.add_member("Ali Hassan", "ali@example.com", "123456")
        self.library.update_member(member_id, name="Ali Mohamed", phone="987654")
        member = self.library.get_member(member_id)
        self.assertEqual(member["name"], "Ali Mohamed")
        self.assertEqual(member["email"], "ali@example.com")
        self.assertEqual(member["phone"], "987654")

    def test_borrow_and_return_book(self):
        book_id = self.library.add_book("Database Systems", "Mary Brown", "ISBN003", 2022, 1)
        member_id = self.library.add_member("Sara Ahmed", "sara@example.com", "555")
        borrowing_id = self.library.borrow_book(book_id, member_id)

        book_after_borrow = self.library.get_book(book_id)
        self.assertEqual(book_after_borrow["copies_available"], 0)

        self.library.return_book(borrowing_id)
        book_after_return = self.library.get_book(book_id)
        borrowing = self.library.get_borrowing(borrowing_id)
        self.assertEqual(book_after_return["copies_available"], 1)
        self.assertEqual(borrowing["status"], "returned")

    def test_prevent_borrowing_when_no_copies_available(self):
        book_id = self.library.add_book("Networking", "David Lee", "ISBN004", 2023, 1)
        member_one = self.library.add_member("Member One", "one@example.com", "111")
        member_two = self.library.add_member("Member Two", "two@example.com", "222")

        self.library.borrow_book(book_id, member_one)
        with self.assertRaises(LibraryError):
            self.library.borrow_book(book_id, member_two)

    def test_delete_book_without_active_borrowing(self):
        book_id = self.library.add_book("Clean Code", "Robert Martin", "ISBN005", 2008, 1)
        self.library.delete_book(book_id)
        self.assertIsNone(self.library.get_book(book_id))

    def test_prevent_delete_borrowed_book(self):
        book_id = self.library.add_book("Algorithms", "Thomas Cormen", "ISBN006", 2021, 1)
        member_id = self.library.add_member("Omar Ali", "omar@example.com", "333")
        self.library.borrow_book(book_id, member_id)

        with self.assertRaises(LibraryError):
            self.library.delete_book(book_id)

    def test_prevent_delete_member_with_active_borrowing(self):
        book_id = self.library.add_book("Data Science", "Jane Doe", "ISBN007", 2022, 1)
        member_id = self.library.add_member("Aisha Noor", "aisha@example.com", "444")
        self.library.borrow_book(book_id, member_id)

        with self.assertRaises(LibraryError):
            self.library.delete_member(member_id)

    def test_returned_book_cannot_be_returned_again(self):
        book_id = self.library.add_book("AI Basics", "Alan White", "ISBN008", 2024, 1)
        member_id = self.library.add_member("Khalid Jama", "khalid@example.com", "777")
        borrowing_id = self.library.borrow_book(book_id, member_id)
        self.library.return_book(borrowing_id)

        with self.assertRaises(LibraryError):
            self.library.return_book(borrowing_id)

    def test_total_copies_cannot_be_less_than_borrowed_copies(self):
        book_id = self.library.add_book("Cyber Security", "Sam Green", "ISBN009", 2025, 3)
        member_id = self.library.add_member("Mohamed Said", "mohamed@example.com", "888")
        self.library.borrow_book(book_id, member_id)

        with self.assertRaises(LibraryError):
            self.library.update_book(book_id, copies_total=0)


if __name__ == "__main__":
    unittest.main()
