import unittest
from unittest.mock import patch, MagicMock
from project import (
    connect_to_database,
    create_employees_table,
    consult_employee,
    list_employees,
    add_employee,
    update_employee,
    remove_employee,
    create_pdf,
    close_database,
    show_menu,
)


class TestProjectFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a temporary SQLite database and cursor for testing
        cls.connection, cls.cursor = connect_to_database()
        create_employees_table(cls.cursor)

    @classmethod
    def tearDownClass(cls):
        # Close the connection to the temporary SQLite database after all tests
        close_database(cls.connection)

    def test_consult_employee(self):
        # Test the consult_employee function
        with patch("builtins.input", return_value="John Doe"):
            with patch("sys.stdout", MagicMock()):
                consult_employee(self.cursor)

    def test_list_employees(self):
        # Test the list_employees function
        with patch("sys.stdout", MagicMock()):
            list_employees(self.cursor)

    def test_add_employee(self):
        # Test the add_employee function
        with patch(
            "builtins.input",
            side_effect=[
                "John Doe",
                "Manager",
                "50000",
                "123456789",
                "john@example.com",
            ],
        ):
            add_employee(self.cursor)

    def test_update_employee(self):
        # Test the update_employee function
        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "John Doe",
                "Manager",
                "55000",
                "987654321",
                "john.doe@example.com",
            ],
        ):
            update_employee(self.cursor)

    def test_remove_employee(self):
        # Test the remove_employee function
        with patch("builtins.input", return_value="1"):
            remove_employee(self.cursor)

    def test_create_pdf(self):
        # Test the create_pdf function
        with patch("sys.stdout", MagicMock()):
            create_pdf(self.cursor)

    def test_show_menu(self):
        # Test the show_menu function
        with patch("sys.stdout", MagicMock()):
            show_menu()


if __name__ == "__main__":
    unittest.main()
