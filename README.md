# Intelligent Multi-User Library Platform

## Overview

The Intelligent Multi-User Library Platform is a Python-based application that allows users to manage personal libraries, share books in a public library, and provides an admin panel for managing users and their libraries. This system is designed for both individual and collaborative use, making it suitable for personal collections or shared library management.

---

## Features

### User Management
- **Registration**: Create user accounts with secure password storage.
- **Login**: Authenticate users to access personal libraries.
- **Admin Access**: Manage all users and libraries with a root password.

### Library Management
- **Personal Library**:
  - Add, delete, search, and list books.
- **Public Library**:
  - Share books with the public, search and manage public collections.

### Administrative Tools
- View and manage all registered users.
- Delete user accounts and their associated libraries.

---

## Getting Started

### Prerequisites
- Python 3.7 or higher(for shlex)
- `shlex`, `hashlib`, and `json` (default Python modules)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/zprolab/knowlib.git
   cd knowlib
   ```

2. Run the program:
   ```bash
   python library.py [...]
   ```

3. On the first run, you will be prompted to set up an admin/root password.

---

## Usage

### Commands
#### User Commands
- **Register**:  
  `register <username> <password>`  
  Create a new user account.

- **Login**:  
  `login <username> <password>`  
  Access your personal library.

- **Personal Library Operations**:
  - `add <title> <author>`: Add a book to your library.
  - `search <keyword>`: Search for books in your library.
  - `delete <title>`: Remove a book from your library.
  - `list`: List all books in your library.

#### Public Library Commands
- `add_public <title> <author>`: Add a book to the public library.
- `search_public <keyword>`: Search for books in the public library.
- `delete_public <title>`: Remove a book from the public library.
- `list_public`: List all books in the public library.

#### Admin Commands
- `admin_login <password>`: Log in as admin.
- `list_users`: List all registered users.
- `view_user_library <username>`: View a specific user's library.
- `delete_user <username>`: Delete a user account and their library.

#### General Commands
- `help`: Display the list of available commands.
- `exit`: Save all changes and exit the program.

---

## Architecture

The system is structured into the following classes:
1. **Library**: Manages personal libraries.
2. **PublicLibrary**: Handles shared public book collections.
3. **UserManager**: Provides user account management and secure authentication.
4. **AdministratorManager**: Enables root-level management tools.
5. **LibraryShell**: The main command-line interface for user interaction.

---

## Security
- Passwords are hashed using SHA-256 for secure storage.
- Separate data files are maintained for user accounts, admin credentials, and public library data.

---

## Data Persistence
- **User Data**: Stored in `dynamic/library_data.json`.
- **Public Library**: Stored in `dynamic/public_library_data.json`.
- **Admin Credentials**: Stored in `dynamic/admin_data.json`.

---

## Contribution
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b username/new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:
   ```bash
   git push origin username/new-feature
   ```
5. Open a pull request and call <zhang dot chenyun at outlook dot com>!

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.