import tkinter as tk
from tkinter import messagebox
import os
import random

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
        text="Username"
    ).pack(pady=5)

    new_username = tk.Entry(
        create_window,
        width=30
    )
    new_username.pack()

    tk.Label(
        create_window,
        text="Password"
    ).pack(pady=5)

    new_password = tk.Entry(
        create_window,
        width=30,
        show="*"
    )
    new_password.pack()

    def register():

        username = new_username.get()
        password = new_password.get()

        if username == "" or password == "":

            messagebox.showwarning(
                "Warning",
                "Please fill all fields!"
            )

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
        bg="green",
        fg="white",
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
        bg="orange",
        fg="white",
        width=20,
        command=send_otp
    ).pack(pady=10)

    tk.Button(
        forgot_window,
        text="Verify OTP",
        bg="green",
        fg="white",
        width=20,
        command=verify_otp
    ).pack(pady=10)

# -----------------------------
# MAIN WINDOW
# -----------------------------
root = tk.Tk()

root.title("Login System")
root.geometry("350x300")
root.resizable(False, False)

tk.Label(
    root,
    text="LOGIN SYSTEM",
    font=("Arial", 18, "bold")
).pack(pady=20)

tk.Label(
    root,
    text="Username"
).pack()

username_entry = tk.Entry(
    root,
    width=30
)
username_entry.pack(pady=5)

tk.Label(
    root,
    text="Password"
).pack()

password_entry = tk.Entry(
    root,
    width=30,
    show="*"
)
password_entry.pack(pady=5)

tk.Button(
    root,
    text="Login",
    width=20,
    bg="blue",
    fg="white",
    command=login
).pack(pady=10)

tk.Button(
    root,
    text="Forgot Password",
    width=20,
    command=forgot_password
).pack(pady=5)

tk.Button(
    root,
    text="Create Account",
    width=20,
    command=create_account
).pack(pady=5)

root.mainloop()