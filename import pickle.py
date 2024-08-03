import pickle
import getpass

# Data storage files
USER_DB = 'users.pkl'
BOOK_DB = 'books.pkl'

class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_borrowed = False

    def __str__(self):
        return f"{self.title} by {self.author} - Genre: {self.genre} (Borrowed: {self.is_borrowed})"

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.borrowed_books = []

    def __str__(self):
        return f"User: {self.username} - Borrowed Books: {self.borrowed_books}"

class Library:
    def __init__(self):
        self.users = self.load_data(USER_DB)
        self.books = self.load_data(BOOK_DB)

    def save_data(self, filename, data):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    def load_data(self, filename):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def add_book(self, title, author, genre):
        new_book = Book(title, author, genre)
        self.books[title] = new_book
        self.save_data(BOOK_DB, self.books)

    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return False
        self.users[username] = User(username, password)
        self.save_data(USER_DB, self.users)
        print("User registered successfully.")
        return True

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    def borrow_book(self, username, book_title):
        user = self.users.get(username)
        book = self.books.get(book_title)

        if not user:
            print("User not found.")
            return False

        if not book:
            print("Book not found.")
            return False

        if book.is_borrowed:
            print("Book is already borrowed.")
            return False

        book.is_borrowed = True
        user.borrowed_books.append(book_title)
        self.save_data(BOOK_DB, self.books)
        self.save_data(USER_DB, self.users)
        print(f"Book '{book_title}' borrowed successfully.")
        return True

    def return_book(self, username, book_title):
        user = self.users.get(username)
        book = self.books.get(book_title)

        if not user:
            print("User not found.")
            return False

        if not book:
            print("Book not found.")
            return False

        if book_title not in user.borrowed_books:
            print("Book was not borrowed by user.")
            return False

        book.is_borrowed = False
        user.borrowed_books.remove(book_title)
        self.save_data(BOOK_DB, self.books)
        self.save_data(USER_DB, self.users)
        print(f"Book '{book_title}' returned successfully.")
        return True

    def list_books(self):
        for book in self.books.values():
            print(book)

    def list_users(self):
        for user in self.users.values():
            print(user)

def main():
    library = Library()

    while True:
        print("\n--- E-Library System ---")
        print("1. Register User")
        print("2. Authenticate User")
        print("3. Add Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. List Books")
        print("7. List Users")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            library.register_user(username, password)

        elif choice == '2':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            user = library.authenticate_user(username, password)
            if user:
                print(f"Welcome {username}!")
            else:
                print("Invalid username or password.")

        elif choice == '3':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            genre = input("Enter book genre: ")
            library.add_book(title, author, genre)

        elif choice == '4':
            username = input("Enter username: ")
            book_title = input("Enter book title to borrow: ")
            library.borrow_book(username, book_title)

        elif choice == '5':
            username = input("Enter username: ")
            book_title = input("Enter book title to return: ")
            library.return_book(username, book_title)

        elif choice == '6':
            library.list_books()

        elif choice == '7':
            library.list_users()

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
