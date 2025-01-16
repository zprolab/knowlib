#    _  __                    _ _ _       ____           ____ _
#   | |/ /_ __   _____      _| (_) |__   | __ ) _   _   / ___| |__   ___ _ __  _   _ _   _ _ __
#   | ' /| '_ \ / _ \ \ /\ / / | | '_ \  |  _ \| | | | | |   | '_ \ / _ \ '_ \| | | | | | | '_ \
#   | . \| | | | (_) \ V  V /| | | |_) | | |_) | |_| | | |___| | | |  __/ | | | |_| | |_| | | | |
#   |_|\_\_| |_|\___/ \_/\_/ |_|_|_.__/  |____/ \__, |  \____|_| |_|\___|_| |_|\__, |\__,_|_| |_|
#                                               |___/                          |___/

import os
import sys
import json
import shlex
import hashlib

COMMON_BASE_DIR = "./dynamic"
MAIN_HELP = """
Knowlib System Command List:
    User Commands:
        register <username> <password>        - Register a new user.
        login <username> <password>           - Login to your account.
        add <title> <author>                  - Add a book to your library.
        search <keyword>                      - Search books in your library.
        delete <title>                        - Delete a book from your library.
        list                                  - List all books in your library.
    
    Public Library Commands:
        add_public <title> <author>           - Add a book to the public library.
        search_public <keyword>               - Search books in the public library.
        delete_public <title>                 - Delete a book from the public library.
        list_public                           - List all books in the public library.

    Admin Commands:
        admin_login <password>                - Login as an admin.
        list_users                            - List all registered users.
        view_user_library <username>          - View a user's library (Admin only).
        delete_user <username>                - Delete a user and their library.

    General Commands:
        help                                  - Show this help message.
        exit                                  - Exit the system.
"""
LINEFEED = (
    "\r\n"
    if sys.platform.startswith("win")
    else (
        "\n"
        if sys.platform.startswith("linux")
        else "\n" if sys.platform.startswith("darwin") else "\x0A"
    )
)

if not os.path.exists(COMMON_BASE_DIR):
    os.mkdir(COMMON_BASE_DIR)


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append({"title": title, "author": author})
        return f'Book "{title}" by {author} added successfully.'

    def search_books(self, keyword):
        results = [
            book for book in self.books if keyword.lower() in book["title"].lower()
        ]
        if results:
            return "\n".join(
                [
                    f"{idx + 1}. {book['title']} by {book['author']}"
                    for idx, book in enumerate(results)
                ]
            )
        return "No books found matching your search."

    def delete_book(self, title):
        for book in self.books:
            if book["title"].lower() == title.lower():
                self.books.remove(book)
                return f'Book "{title}" removed successfully.'
        return f'Book "{title}" not found.'

    def list_books(self):
        if not self.books:
            return "No books available in your library."
        return "\n".join(
            [
                f"{idx + 1}. {book['title']} by {book['author']}"
                for idx, book in enumerate(self.books)
            ]
        )


class PublicLibrary:
    """
    Public library pool shared by all users.
    """

    DATA_FILE = os.path.join(COMMON_BASE_DIR, "public_library_data.json")

    def __init__(self):
        self.public_books = self.load_public_data()

    def load_public_data(self):
        """
        Load public library data from the JSON file.
        """
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as file:
                return json.load(file)
        return []

    def save_public_data(self):
        """
        Save public library data to the JSON file.
        """
        with open(self.DATA_FILE, "w") as file:
            json.dump(self.public_books, file, indent=4)

    def add_public_book(self, title, author):
        self.public_books.append({"title": title, "author": author})
        return f'Book "{title}" by {author} added to the public library.'

    def search_public_books(self, keyword):
        results = [
            book
            for book in self.public_books
            if keyword.lower() in book["title"].lower()
        ]
        if results:
            return "\n".join(
                [
                    f"{idx + 1}. {book['title']} by {book['author']}"
                    for idx, book in enumerate(results)
                ]
            )
        return "No public books found matching your search."

    def delete_public_book(self, title):
        for book in self.public_books:
            if book["title"].lower() == title.lower():
                self.public_books.remove(book)
                return f'Book "{title}" removed from the public library.'
        return f'Book "{title}" not found in the public library.'

    def list_public_books(self):
        if not self.public_books:
            return "No books available in the public library."
        return "\n".join(
            [
                f"{idx + 1}. {book['title']} by {book['author']}"
                for idx, book in enumerate(self.public_books)
            ]
        )


class UserManager:
    """
    A user management system with password authentication.
    """

    DATA_FILE = os.path.join(COMMON_BASE_DIR, "library_data.json")

    def __init__(self):
        self.users = self.load_data()
        self.current_user = None

    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_data(self):
        with open(self.DATA_FILE, "w") as file:
            json.dump(self.users, file, indent=4)

    def hash_password(self, password):
        """
        Hashes the password using SHA-256.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        if username in self.users:
            return f'User "{username}" already exists.'
        self.users[username] = {"password": self.hash_password(password), "books": []}
        return f'User "{username}" registered successfully.'

    def login_user(self, username, password):
        if username not in self.users:
            return f'User "{username}" does not exist. Please register first.'
        hashed_password = self.hash_password(password)
        if self.users[username]["password"] != hashed_password:
            return "Invalid password. Please try again."
        self.current_user = username
        return f'User "{username}" logged in successfully.'

    def get_current_library(self):
        if not self.current_user:
            raise ValueError("No user is currently logged in.")
        return LibraryManager(self.users[self.current_user]["books"])


class AdministratorManager:
    """
    Manages the root/admin password and provides highest-level access to all user data.
    """

    ROOT_FILE = os.path.join(COMMON_BASE_DIR, "admin_data.json")

    def __init__(self):
        self.root_password = self.load_root_password()

    def load_root_password(self):
        """
        Load the root password from the JSON file.
        If the file does not exist, prompt for password setup.
        """
        if os.path.exists(self.ROOT_FILE):
            with open(self.ROOT_FILE, "r") as file:
                data = json.load(file)
                return data.get("root_password")
        # First-time setup
        print("Initializing system. Please set the root password:")
        while True:
            password = input("Enter root password: ").strip()
            confirm_password = input("Confirm root password: ").strip()
            if password == confirm_password:
                hashed_password = self.hash_password(password)
                with open(self.ROOT_FILE, "w") as file:
                    json.dump({"root_password": hashed_password}, file)
                print("Root password set successfully.")
                return hashed_password
            else:
                print("Passwords do not match. Please try again.")

    def hash_password(self, password):
        """
        Hashes the password using SHA-256.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_root(self, password):
        """
        Authenticate root password for admin access.
        """
        return self.hash_password(password) == self.root_password


class LibraryManager(Library):
    def __init__(self, books_ref):
        super().__init__()
        self.books = books_ref


class LibraryShell:
    def __init__(self):
        self.user_manager = UserManager()
        self.admin_manager = AdministratorManager()
        self.admin_mode = False
        self.current_library = None
        self.public_library = PublicLibrary()  # Initialize public library
        self.username = None
        self.commands = {
            "register": self.register_user,
            "login": self.login_user,
            "admin_login": self.admin_login,
            "view_users_library": self.view_user_library,
            "add": self.add_book,
            "search": self.search_books,
            "delete": self.delete_book,
            "list": self.list_books,
            "add_public": self.add_public_book,
            "search_public": self.search_public_books,
            "delete_public": self.delete_public_book,
            "list_public": self.list_public_books,
            "list_users": self.list_all_users,
            "delete_user": self.delete_user,
            "help": self.show_help,
            "exit": self.exit_shell,
        }
        self.running = True

    def show_help(self, *args):
        help_text = MAIN_HELP[:]
        return help_text.strip()

    def register_user(self, *args):
        if len(args) < 2:
            return "Usage: register <username> <password>"
        username, password = args[0], args[1]
        return self.user_manager.register_user(username, password)

    def login_user(self, *args):
        if len(args) < 2:
            return "Usage: login <username> <password>"
        username, password = args[0], args[1]
        result = self.user_manager.login_user(username, password)
        if "successfully" in result:
            self.current_library = self.user_manager.get_current_library()
            self.username = args[0]
        return result

    def admin_login(self, *args):
        if len(args) < 1:
            return "Usage: admin_login <password>"
        password = args[0]
        if self.admin_manager.authenticate_root(password):
            self.admin_mode = True
            admin_logged_in_warn = (
                "WARNING! Admin mode set successfully. "
                + LINEFEED
                + "You now have full access to all users and their libraries. "
                + LINEFEED
                + "You may harm your system, so be CAREFUL!"
            )
            return admin_logged_in_warn.strip()
        return "Invalid root password."

    def list_all_users(self, *args):
        if not self.admin_mode:
            return "Admin access required. Please login as admin."
        users = self.user_manager.users
        if not users:
            return "No users registered."
        return "\n".join(
            [f"{idx + 1}. {user}" for idx, user in enumerate(users.keys())]
        )

    def view_user_library(self, *args):
        if not self.admin_mode:
            return "Admin access required. Please login as admin."
        if len(args) < 1:
            return "Usage: view_user_library <username>"
        username = args[0]
        if username not in self.user_manager.users:
            return f'User "{username}" does not exist.'
        user_books = self.user_manager.users[username]["books"]
        if not user_books:
            return f'No books in {username}"s library.'
        return "\n".join(
            [
                f"{idx + 1}. {book['title']} by {book['author']}"
                for idx, book in enumerate(user_books)
            ]
        )

    def delete_user(self, *args):
        if not self.admin_mode:
            return "Admin access required. Please login as admin."
        if len(args) < 1:
            return "Usage: delete_user <username>"
        username = args[0]
        if username not in self.user_manager.users:
            return f'User "{username}" does not exist.'
        del self.user_manager.users[username]
        return f'User "{username}" and their library have been deleted.'

    def add_book(self, *args):
        if not self.current_library:
            return "Please login first."
        if len(args) < 2:
            return "Usage: add <title> <author>"
        title, author = args[0], args[1]
        return self.current_library.add_book(title, author)

    def search_books(self, *args):
        if not self.current_library:
            return "Please login first."
        if len(args) < 1:
            return "Usage: search <keyword>"
        keyword = args[0]
        return self.current_library.search_books(keyword)

    def delete_book(self, *args):
        if not self.current_library:
            return "Please login first."
        if len(args) < 1:
            return "Usage: delete <title>"
        title = args[0]
        return self.current_library.delete_book(title)

    def list_books(self, *args):
        if not self.current_library:
            return "Please login first."
        return self.current_library.list_books()

    # Public library commands
    def add_public_book(self, *args):
        if len(args) < 2:
            return "Usage: add_public <title> <author>"
        title, author = args[0], args[1]
        return self.public_library.add_public_book(title, author)

    def search_public_books(self, *args):
        if len(args) < 1:
            return "Usage: search_public <keyword>"
        keyword = args[0]
        return self.public_library.search_public_books(keyword)

    def delete_public_book(self, *args):
        if len(args) < 1:
            return "Usage: delete_public <title>"
        title = args[0]
        return self.public_library.delete_public_book(title)

    def list_public_books(self, *args):
        return self.public_library.list_public_books()

    def exit_shell(self, *args):
        self.user_manager.save_data()
        self.public_library.save_public_data()  # Save public library data
        self.running = False
        return "Exiting the library shell. Goodbye!"

    def run(self):
        print("Welcome to the Intelligent Multi-User Library Platform!")
        print("Type 'help' for a list of commands.")
        while self.running:
            try:
                sig = "#" if self.admin_mode else "$"
                username_disp = "public" if self.username is None else self.username
                user_input = input(f"[knowlib@{username_disp}]{sig} ").strip()
                if not user_input:
                    continue
                args = shlex.split(user_input)
                command, *params = args
                if command in self.commands:
                    result = self.commands[command](*params)
                    print(result)
                else:
                    print(f'Unknown command: "{command}". Type "help" for assistance.')
            except Exception as e:
                print(f"Error: {e}")


class CliApp:
    def __init__(self, _init_args=None):
        self.shell = LibraryShell()

    def cli(self, _argv):
        # library.py
        if len(_argv) == 1:
            self.shell.run()

        # library.py command
        elif len(_argv) == 2:
            if _argv[1] == "help":
                print(MAIN_HELP)
            elif _argv[1] == "shell":
                self.shell.run()

            # TODO: Full-Featured Command Support...
            else:
                print(
                    f'Unknow command: "{_argv[1]}". '
                    + f'To run a shell command, please use "library.py shell {_argv[1]}"'
                )

        # library.py command param1 [param2[...]]
        else:
            print(self.shell.commands[_argv[2]](*_argv[3:]))


if __name__ == "__main__":
    app = CliApp()
    app.cli(sys.argv)
