import tkinter as tk
from tkinter import ttk
from auth import login, signup_main


def login_user():
    """Placeholder function for handling login."""
    print("###############################", login_username_entry.get(), 
          login_password_entry.get())
    login(login_username_entry.get(), login_password_entry.get())
    print("Login button clicked")


def signup_user():
    """Placeholder function for handling signup."""
    signup_main(signup_username_entry.get(), signup_password_entry.get(),
                email_entry.get(), pin_entry.get(), code_editor_entry.get(),
                browser_entry.get())
    print("Signup button clicked")


def show_signup():
    """Switch to the signup screen."""
    login_frame.pack_forget()
    signup_frame.pack()


def show_login():
    """Switch to the login screen."""
    signup_frame.pack_forget()
    login_frame.pack()


# Create main window
root = tk.Tk()
root.title("Login/Signup")
root.geometry("800x800")

# Style
style = ttk.Style()
style.configure("TButton", padding=5, font=("Helvetica", 12))
style.configure("TLabel", padding=5, font=("Helvetica", 12))

# Center content
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Login Frame
login_frame = tk.Frame(root)
tk.Label(login_frame, text="Username").pack()
login_username_entry = tk.Entry(login_frame, font=("Helvetica", 12))
login_username_entry.pack()
tk.Label(login_frame, text="Password").pack()
login_password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
login_password_entry.pack()
login_button = ttk.Button(login_frame, text="Login", command=login_user)
login_button.pack(pady=5)
signup_button = ttk.Button(login_frame, text="Signup", command=show_signup)
signup_button.pack(pady=5)
login_frame.pack(expand=True, fill="both", padx=200, pady=200)

# Signup Frame
signup_frame = tk.Frame(root)
tk.Label(signup_frame, text="Username").pack()
signup_username_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
signup_username_entry.pack()

tk.Label(signup_frame, text="Email").pack()
email_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
email_entry.pack()

tk.Label(signup_frame, text="PIN").pack()
pin_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
pin_entry.pack()

tk.Label(signup_frame, text="Password").pack()
signup_password_entry = tk.Entry(signup_frame, show="*", font=("Helvetica", 12))
signup_password_entry.pack()

tk.Label(signup_frame, text="Confirm Password").pack()
confirm_password_entry = tk.Entry(signup_frame, show="*", font=("Helvetica", 12))
confirm_password_entry.pack()

tk.Label(signup_frame, text="Code Editor").pack()
code_editor_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
code_editor_entry.pack()

tk.Label(signup_frame, text="Browser").pack()
browser_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
browser_entry.pack()

signup_button = ttk.Button(signup_frame, text="Signup", command=signup_user)
signup_button.pack(pady=5)
back_button = ttk.Button(signup_frame, text="Back to Login", command=show_login)
back_button.pack(pady=5)


# Hide signup frame initially
signup_frame.pack_forget()

root.mainloop()
