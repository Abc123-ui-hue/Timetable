import tkinter as tk
from tkinter import messagebox
import os

# ------------------ File Setup ------------------
USER_FILE = "users.txt"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        f.write("admin,admin123,Admin\n")  # Default admin account

# ------------------ Helper Functions ------------------
def save_user(username, password, role):
    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password},{role}\n")

def validate_user(username, password, role):
    with open(USER_FILE, "r") as f:
        for line in f:
            u, p, r = line.strip().split(",")
            if u == username and p == password and r == role:
                return True
    return False

# ------------------ UI Windows ------------------
def show_dashboard(role, username):
    dashboard = tk.Toplevel(root)
    dashboard.title(f"{role} Dashboard")
    dashboard.geometry("400x400")

    tk.Label(dashboard, text=f"Welcome {username} ({role})", font=("Arial", 14)).pack(pady=10)

    if role == "Admin":
        tk.Button(dashboard, text="Add Book", width=20).pack(pady=5)
        tk.Button(dashboard, text="Remove Book", width=20).pack(pady=5)
        tk.Button(dashboard, text="View All Books", width=20).pack(pady=5)
        tk.Button(dashboard, text="View Borrow Records", width=20).pack(pady=5)
    else:
        tk.Button(dashboard, text="Search Book", width=20).pack(pady=5)
        tk.Button(dashboard, text="Borrow Book", width=20).pack(pady=5)
        tk.Button(dashboard, text="Return Book", width=20).pack(pady=5)
        tk.Button(dashboard, text="My Borrow History", width=20).pack(pady=5)

# ------------------ Registration ------------------
def register():
    username = reg_username.get()
    password = reg_password.get()
    role = reg_role.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    save_user(username, password, role)
    messagebox.showinfo("Success", "Registration successful!")
    reg_window.destroy()

def open_register():
    global reg_username, reg_password, reg_role, reg_window
    reg_window = tk.Toplevel(root)
    reg_window.title("Register")
    reg_window.geometry("300x300")

    tk.Label(reg_window, text="Username").pack(pady=5)
    reg_username = tk.Entry(reg_window)
    reg_username.pack(pady=5)

    tk.Label(reg_window, text="Password").pack(pady=5)
    reg_password = tk.Entry(reg_window, show="*")
    reg_password.pack(pady=5)

    tk.Label(reg_window, text="Role").pack(pady=5)
    reg_role = tk.StringVar(value="User")
    tk.OptionMenu(reg_window, reg_role, "User", "Admin").pack(pady=5)

    tk.Button(reg_window, text="Register", command=register).pack(pady=20)

# ------------------ Login ------------------
def login():
    username = login_username.get()
    password = login_password.get()
    role = login_role.get()

    if validate_user(username, password, role):
        messagebox.showinfo("Success", f"Welcome {username}!")
        show_dashboard(role, username)
    else:
        messagebox.showerror("Error", "Invalid credentials")

# ------------------ Main Window ------------------
root = tk.Tk()
root.title("E-Library Management System - Phase 2")
root.geometry("350x300")

tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Username").pack()
login_username = tk.Entry(root)
login_username.pack(pady=5)

tk.Label(root, text="Password").pack()
login_password = tk.Entry(root, show="*")
login_password.pack(pady=5)

tk.Label(root, text="Role").pack()
login_role = tk.StringVar(value="User")
tk.OptionMenu(root, login_role, "User", "Admin").pack(pady=5)

tk.Button(root, text="Login", command=login).pack(pady=10)
tk.Button(root, text="Register", command=open_register).pack(pady=5)

root.mainloop()
