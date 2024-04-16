import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from auth import login, signup_main


def login_error_box(message):
    """Display an error message box for login errors."""
    messagebox.showerror("Login Error", message)

def login_user():
    """Placeholder function for handling login."""
    print("############CHECK###################", login_username_entry.get(),
          login_password_entry.get())
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username == "" or password == "":
        login_error_box("Username or password is empty")
        return
    else:
        try:
            login(username, password)
            print("Login button clicked")
        except Exception as e:
            error = str(e)
            print(error)
            if error.startswith("InvalidToken"):
                print('InvalidToken', {e})
                login_error_box("CRITICAL ERROR: Invalid Token")
            else:
                print('Error while loggin in user',{e})
                login_error_box("Error while logging in user, please try again")



def get_signup_inputs():
    """Get all the signup inputs from the entry widgets."""
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    confirm_password = confirm_password_entry.get()
    pin = pin_entry.get()
    confirm_pin = confirm_pin_entry.get()
    email = email_entry.get()
    code_editor = code_editor_entry.get()
    browser = browser_entry.get()
    return username, password, confirm_password, pin, confirm_pin, email, code_editor, browser

def validate_signup_inputs(username, password, confirm_password, pin, confirm_pin, email, code_editor, browser):
    """Validate all the signup inputs."""
    if not all((username, password, confirm_password, pin, confirm_pin, email, code_editor, browser)):
        return False, "All fields are required"
    elif password != confirm_password:
        return False, "Passwords do not match"
    elif pin != confirm_pin:
        return False, "PINs do not match"
    else:
        return True, ""

def signup_user():
    """Handle signup process."""
    username, password, confirm_password, pin, confirm_pin, email, code_editor, browser = get_signup_inputs()
    valid, message = validate_signup_inputs(username, password, confirm_password, pin, confirm_pin, email, code_editor, browser)
    if valid:
        # Perform signup process
        signup_main(username, password, email, pin, code_editor, browser)
        print("Signup button clicked")
    else:
        # Display error message
        login_error_box(message)


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

tk.Label(signup_frame, text="Confirm PIN").pack()
confirm_pin_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
confirm_pin_entry.pack()

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
