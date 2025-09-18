import streamlit as st
import os
from datetime import datetime

# -------------------- File Setup --------------------
USERS_FILE = "users.txt"
BOOKS_FILE = "books.txt"
BORROW_FILE = "borrow_records.txt"

# Ensure files exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        f.write("admin,admin123,admin\n")  # default admin

if not os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "w") as f:
        f.write("Python Basics,John Smith\nData Science 101,Jane Doe\n")

if not os.path.exists(BORROW_FILE):
    with open(BORROW_FILE, "w") as f:
        pass

# -------------------- Utility Functions --------------------
def load_users():
    users = {}
    with open(USERS_FILE, "r") as f:
        for line in f:
            if line.strip():
                username, password, role = line.strip().split(",")
                users[username] = {"password": password, "role": role}
    return users

def save_user(username, password, role="student"):
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

def record_borrow(username, title, action):
    with open(BORROW_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{username},{title},{action},{timestamp}\n")

def load_borrow_records():
    records = []
    with open(BORROW_FILE, "r") as f:
        for line in f:
            if line.strip():
                user, title, action, timestamp = line.strip().split(",")
                records.append({"user": user, "title": title, "action": action, "time": timestamp})
    return records

# -------------------- Streamlit App --------------------
st.set_page_config(page_title="E-Library System", layout="centered")
st.title("📚 E-Library Management System")

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------- Login & Register --------------------
if st.session_state.user is None:
    menu = st.sidebar.radio("Menu", ["Login", "Register"])

    if menu == "Login":
        st.subheader("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            users = load_users()
            if username in users and users[username]["password"] == password:
                st.session_state.user = {"username": username, "role": users[username]["role"]}
                st.success(f"Welcome {username}! You are logged in as {users[username]['role']}.")
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif menu == "Register":
        st.subheader("📝 Register")
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        role = st.selectbox("Choose Role", ["student", "user", "admin"])  # ✅ role selection

        if st.button("Register"):
            users = load_users()
            if new_user in users:
                st.error("Username already exists")
            else:
                save_user(new_user, new_pass, role)
                st.success(f"Registration successful as {role}! Please login.")

# -------------------- Logged-In Section --------------------
else:
    user = st.session_state.user
    st.sidebar.write(f"👤 Logged in as: {user['username']} ({user['role']})")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    # -------------------- Student/User Dashboard --------------------
    if user["role"] in ["student", "user"]:
        st.subheader("📖 Library Dashboard")

        choice = st.radio("Choose Action", ["Search Books", "View All Books", "Borrow Book", "Return Book"])

        if choice == "Search Books":
            st.subheader("🔍 Search Books")
            keyword = st.text_input("Enter book title")
            if st.button("Search"):
                books = load_books()
                results = [f"{b['title']} by {b['author']}" for b in books if keyword.lower() in b['title'].lower()]
                if results:
                    st.success("Results found:")
                    st.write("\n".join(results))
                else:
                    st.warning("No books found")

        elif choice == "View All Books":
            st.subheader("📚 Available Books")
            books = load_books()
            if books:
                for b in books:
                    st.write(f"- {b['title']} by {b['author']}")
            else:
                st.info("No books available")

        elif choice == "Borrow Book":
            st.subheader("📥 Borrow Book")
            title = st.text_input("Enter book title to borrow")
            if st.button("Borrow"):
                books = load_books()
                if any(b["title"].lower() == title.lower() for b in books):
                    record_borrow(user["username"], title, "borrowed")
                    st.success(f"You borrowed '{title}'")
                else:
                    st.error("Book not found")

        elif choice == "Return Book":
            st.subheader("📤 Return Book")
            title = st.text_input("Enter book title to return")
            if st.button("Return"):
                books = load_books()
                if any(b["title"].lower() == title.lower() for b in books):
                    record_borrow(user["username"], title, "returned")
                    st.success(f"You returned '{title}'")
                else:
                    st.error("Book not found")

    # -------------------- Admin Dashboard --------------------
    elif user["role"] == "admin":
        st.subheader("🛠️ Admin Dashboard")

        choice = st.radio(
            "Choose Action",
            ["Add Book", "Remove Book", "View All Books", "View Borrowed Books", "View Returned Books", "Borrow Records"]
        )

        if choice == "Add Book":
            st.subheader("➕ Add Book")
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            if st.button("Add"):
                books = load_books()
                books.append({"title": title, "author": author})
                save_books(books)
                st.success("Book added successfully")

        elif choice == "Remove Book":
            st.subheader("🗑️ Remove Book")
            title = st.text_input("Enter book title to remove")
            if st.button("Remove"):
                books = load_books()
                new_books = [b for b in books if b["title"].lower() != title.lower()]
                save_books(new_books)
                st.success("Book removed successfully")

        elif choice == "View All Books":
            st.subheader("📚 All Books in Library")
            books = load_books()
            if books:
                for b in books:
                    st.write(f"- {b['title']} by {b['author']}")
            else:
                st.info("No books available")

        elif choice == "View Borrowed Books":
            st.subheader("📥 Currently Borrowed Books")
            records = load_borrow_records()
            borrowed = {}
            for r in records:
                if r["action"] == "borrowed":
                    borrowed[r["title"]] = r
                elif r["action"] == "returned" and r["title"] in borrowed:
                    del borrowed[r["title"]]
            if borrowed:
                for title, r in borrowed.items():
                    st.write(f"📕 '{title}' borrowed by {r['user']} on {r['time']}")
            else:
                st.info("No books currently borrowed.")

        elif choice == "View Returned Books":
            st.subheader("📤 Returned Books")
            records = [r for r in load_borrow_records() if r["action"] == "returned"]
            if records:
                for r in records:
                    st.write(f"📗 '{r['title']}' returned by {r['user']} on {r['time']}")
            else:
                st.info("No returned books yet.")

        elif choice == "Borrow Records":
            st.subheader("📜 Full Borrow/Return History")
            records = load_borrow_records()
            if records:
                for r in records:
                    st.write(f"👤 {r['user']} {r['action']} '{r['title']}' on {r['time']}")
            else:
                st.info("No borrow records yet.")
