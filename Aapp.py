import tkinter as tk
from tkinter import ttk, messagebox
import os

# -------------------- File Handling Helpers --------------------

USERS_FILE = "users.txt"
BOOKS_FILE = "books.txt"

# Ensure files exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        f.write("admin,admin123,admin\n")  # default admin

if not os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "w") as f:
        f.write("Python Basics,John Smith\nData Science 101,Jane Doe\n")

# -------------------- Utility Functions --------------------

def load_users():
    users = {}
    with open(USERS_FILE, "r") as f:
        for line in f:
            if line.strip():
                username, password, role = line.strip().split(",")
                users[username] = {"password": password, "role": role}
    return users

def save_user(username, password, role="user"):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password},{role}\n")

def load_books():
    books = []
    with open(BOOKS_FILE, "r") as f:
        for line in f:
            if line.strip():
                title, author = line.strip().split(",")
                books.append({"title": title, "author": author})
    return books

def save_books(books):
    with open(BOOKS_FILE, "w") as f:
        for book in books:
            f.write(f"{book['title']},{book['author']}\n")

# -------------------- GUI Application --------------------

class ELibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Library Management System")
        self.geometry("600x400")
        self.resizable(False, False)

        self.current_user = None

        self.login_screen()

    # ---------------- Login & Registration ----------------
    def login_screen(self):
        self.clear_frame()
        tk.Label(self, text="Login", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        tk.Button(self, text="Register", command=self.register_screen).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = load_users()

        if username in users and users[username]["password"] == password:
            self.current_user = {"username": username, "role": users[username]["role"]}
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            if self.current_user["role"] == "admin":
                self.admin_dashboard()
            else:
                self.user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register_screen(self):
        self.clear_frame()
        tk.Label(self, text="Register", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text="Username").pack()
        self.reg_username = tk.Entry(self)
        self.reg_username.pack()

        tk.Label(self, text="Password").pack()
        self.reg_password = tk.Entry(self, show="*")
        self.reg_password.pack()

        tk.Button(self, text="Submit", command=self.register).pack(pady=5)
        tk.Button(self, text="Back", command=self.login_screen).pack()

    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        users = load_users()

        if username in users:
            messagebox.showerror("Error", "Username already exists")
        else:
            save_user(username, password, "user")
            messagebox.showinfo("Success", "User registered successfully")
            self.login_screen()

    # ---------------- User Dashboard ----------------
    def user_dashboard(self):
        self.clear_frame()
        tk.Label(self, text=f"User Dashboard - {self.current_user['username']}", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self, text="Search Books", command=self.search_books).pack(pady=5)
        tk.Button(self, text="View All Books", command=self.view_books).pack(pady=5)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

    def search_books(self):
        self.clear_frame()
        tk.Label(self, text="Search Books", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Enter Title").pack()
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        tk.Button(self, text="Search", command=self.display_search).pack(pady=5)
        tk.Button(self, text="Back", command=self.user_dashboard).pack()

    def display_search(self):
        keyword = self.search_entry.get().lower()
        books = load_books()
        results = [f"{b['title']} by {b['author']}" for b in books if keyword in b['title'].lower()]
        messagebox.showinfo("Search Results", "\n".join(results) if results else "No books found")

    def view_books(self):
        books = load_books()
        book_list = "\n".join([f"{b['title']} by {b['author']}" for b in books])
        messagebox.showinfo("Available Books", book_list if book_list else "No books available")

    # ---------------- Admin Dashboard ----------------
    def admin_dashboard(self):
        self.clear_frame()
        tk.Label(self, text="Admin Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self, text="Add Book", command=self.add_book_screen).pack(pady=5)
        tk.Button(self, text="Remove Book", command=self.remove_book_screen).pack(pady=5)
        tk.Button(self, text="View All Books", command=self.view_books).pack(pady=5)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

    def add_book_screen(self):
        self.clear_frame()
        tk.Label(self, text="Add Book", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Title").pack()
        self.book_title = tk.Entry(self)
        self.book_title.pack()

        tk.Label(self, text="Author").pack()
        self.book_author = tk.Entry(self)
        self.book_author.pack()

        tk.Button(self, text="Add", command=self.add_book).pack(pady=5)
        tk.Button(self, text="Back", command=self.admin_dashboard).pack()

    def add_book(self):
        title = self.book_title.get()
        author = self.book_author.get()
        books = load_books()
        books.append({"title": title, "author": author})
        save_books(books)
        messagebox.showinfo("Success", "Book added successfully")
        self.admin_dashboard()

    def remove_book_screen(self):
        self.clear_frame()
        tk.Label(self, text="Remove Book", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Enter Title").pack()
        self.remove_title = tk.Entry(self)
        self.remove_title.pack()

        tk.Button(self, text="Remove", command=self.remove_book).pack(pady=5)
        tk.Button(self, text="Back", command=self.admin_dashboard).pack()

    def remove_book(self):
        title = self.remove_title.get()
        books = load_books()
        books = [b for b in books if b["title"].lower() != title.lower()]
        save_books(books)
        messagebox.showinfo("Success", "Book removed successfully")
        self.admin_dashboard()

    # ---------------- Logout ----------------
    def logout(self):
        self.current_user = None
        self.login_screen()

    # ---------------- Utility ----------------
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

# -------------------- Run Application --------------------
if __name__ == "__main__":
    app = ELibraryApp()
    app.mainloop()
