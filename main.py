import tkinter as tk
from tkinter import messagebox
import os
import random
import re

# -----------------------------
# DATABASE FILE
# -----------------------------
DATABASE_FILE = "accounts.txt"

# Create file if not existing
if not os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, "w") as file:
        file.write("")

# -----------------------------
# LOGIN FUNCTION
# -----------------------------
def login():

    username = username_entry.get()
    password = password_entry.get()

    with open(DATABASE_FILE, "r") as file:

        for line in file:

            data = line.strip().split(",")

            if len(data) == 2:

                saved_username = data[0]
                saved_password = data[1]

                if (
                    username == saved_username and
                    password == saved_password
                ):

                    messagebox.showinfo(
                        "Login Successful",
                        f"Welcome, {username}!"
                    )

                    return

    messagebox.showerror(
        "Login Failed",
        "Invalid Username or Password"
    )

# -----------------------------
# CREATE ACCOUNT FUNCTION
# -----------------------------
def create_account():

    create_window = tk.Toplevel(root)
    create_window.title("Create Account")
    create_window.geometry("300x250")
    create_window.resizable(False, False)

    tk.Label(
        create_window,
        text="Username",
        fg ="#1F2937",
    ).pack(pady=5)

    new_username = tk.Entry(
        create_window,
        width=30
    )
    new_username.pack()

    tk.Label(
    create_window,
    text="Password",
    fg ="#1F2937",
    ).pack(pady=5)

# -----------------------------
# PASSWORD FRAME (CREATE ACCOUNT)
# -----------------------------
    password_frame_create = tk.Frame(create_window)
    password_frame_create.pack()

    new_password = tk.Entry(
        password_frame_create,
        width=27,
        show="*"
    )
    new_password.pack(side="left")

# -----------------------------
# SHOW / HIDE PASSWORD
# -----------------------------
    show_create_password = False

    def toggle_create_password():

        nonlocal show_create_password

        if show_create_password:

            new_password.config(show="*")
            show_create_button.config(text="👁")
            show_create_password = False

        else:

            new_password.config(show="")
            show_create_button.config(text="🙈")
            show_create_password = True

# Eye button
    show_create_button = tk.Button(
        password_frame_create,
        text="👁",
        command=toggle_create_password
    )
    show_create_button.pack(side="left", padx=5)

    def register():

        username = new_username.get()
        password = new_password.get()

        if username == "" or password == "":

            messagebox.showwarning(
                "Warning",
                "Please fill all fields!"
            )

            create_window.lift()
            create_window.focus_force()

            return
        
        # Password validation
        # Must be at least 8 characters long
        if len(password) < 8:

            messagebox.showerror(
                "Weak Password",
                "Password must be at least 8 characters long!"
            )

            create_window.lift()
            create_window.focus_force()

            return

        # Must contain digit
        if not re.search(r"\d", password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least one digit!"
            )

            create_window.lift()
            create_window.focus_force()

            return

        # Must contain special character
        if not re.search(r"[-_!@#$%^&*(),.?\":{}|<>]", password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least one special character!"
            )

            create_window.lift()
            create_window.focus_force()

            return

        # Check if username exists
        with open(DATABASE_FILE, "r") as file:

            for line in file:

                data = line.strip().split(",")

                if (
                    len(data) == 2 and
                    username == data[0]
                ):

                    messagebox.showerror(
                        "Error",
                        "Username already exists!"
                    )

                    create_window.lift()
                    create_window.focus_force()

                    return

        # Save account
        with open(DATABASE_FILE, "a") as file:

            file.write(
                f"{username},{password}\n"
            )

        messagebox.showinfo(
            "Success",
            "Account Created Successfully!"
        )

        create_window.destroy()

    tk.Button(
        create_window,
        text="Register",
        bg="white",
        fg="#EC4899",
        width=20,
        command=register
    ).pack(pady=20)

# -----------------------------
# FORGOT PASSWORD FUNCTION
# -----------------------------
generated_otp = ""

def forgot_password():

    forgot_window = tk.Toplevel(root)
    forgot_window.title("Forgot Password")
    forgot_window.geometry("300x250")
    forgot_window.resizable(False, False)

    tk.Label(
        forgot_window,
        text="Enter Username"
    ).pack(pady=5)

    forgot_username = tk.Entry(
        forgot_window,
        width=30
    )
    forgot_username.pack()

    tk.Label(
        forgot_window,
        text="Enter OTP"
    ).pack(pady=5)

    otp_entry = tk.Entry(
        forgot_window,
        width=30
    )
    otp_entry.pack()

    def send_otp():

        global generated_otp

        username = forgot_username.get()

        with open(DATABASE_FILE, "r") as file:

            for line in file:

                data = line.strip().split(",")

                if len(data) == 2:

                    saved_username = data[0]

                    if username == saved_username:

                        generated_otp = str(
                            random.randint(100000, 999999)
                        )

                        messagebox.showinfo(
                            "OTP Sent",
                            f"Your OTP is: {generated_otp}"
                        )

                        return

        messagebox.showerror(
            "Error",
            "Username not found!"
        )

    def verify_otp():

        username = forgot_username.get()
        entered_otp = otp_entry.get()

        if entered_otp == generated_otp:

            with open(DATABASE_FILE, "r") as file:

                for line in file:

                    data = line.strip().split(",")

                    if len(data) == 2:

                        saved_username = data[0]
                        saved_password = data[1]

                        if username == saved_username:

                            messagebox.showinfo(
                                "Recovered Password",
                                f"Your password is: {saved_password}"
                            )

                            return

        else:

            messagebox.showerror(
                "Error",
                "Invalid OTP!"
            )

    tk.Button(
        forgot_window,
        text="Send OTP",
        bg="#EC4899",
        fg="white",
        font=("Poppins", 11, bold),
        width=20,
        command=send_otp
    ).pack(pady=10)

    tk.Button(
        forgot_window,
        text="Verify OTP",
        bg="#3B82F6",
        fg="white",
        font=("Poppins", 11, bold),
        width=20,
        command=verify_otp
    ).pack(pady=10)

# -----------------------------
# MAIN WINDOW
# -----------------------------
root = tk.Tk()

root.title("Login System")
root.geometry("350x450")
root.resizable(False, False)

tk.Label(
    root,
    text="LOGIN SYSTEM",
    fg="#3B82F6",
    bg="#FDF2F8",
    font=("Poppins", 18, "bold")
).pack(pady=20)

tk.Label(
    root,
    text="Username",
    fg="#1F2937",
).pack()

username_entry = tk.Entry(
    root,
    width=30
)
username_entry.pack(pady=5)

tk.Label(
    root,
    text="Password",
    fg="#1F2937",
).pack()

# PASSWORD FRAME (NEW)
# -----------------------------
password_frame = tk.Frame(root)
password_frame.pack(pady=5)

password_entry = tk.Entry(
    password_frame,
    width=27,
    show="*"
)
password_entry.pack(side="left")

# -----------------------------
# SHOW / HIDE PASSWORD
# -----------------------------
show_password = False

def toggle_password():

    global show_password

    if show_password:

        password_entry.config(show="*")
        show_button.config(text="👁")
        show_password = False

    else:

        password_entry.config(show="")
        show_button.config(text="🙈")
        show_password = True

# Eye button
show_button = tk.Button(
    password_frame,
    text="👁",
    command=toggle_password
)
show_button.pack(side="left", padx=5)

tk.Button(
    root,
    text="Login",
    bg="blue",
    fg="white",
    width=20,
    command=login
    
).pack(pady=10)

tk.Button(
    root,
    text="Forgot Password",
    fg="#EC4899",
    bg="#FDF2F8",
    border=0,
    width=20,
    command=forgot_password
).pack(pady=5)

tk.Button(
    root,
    text="Create Account",
    bg="#EC4899",
    fg="white",
    width=20,
    command=create_account
).pack(pady=5)

root.mainloop()