import tkinter as tk
from tkinter import messagebox

from database import register_user
from database import login_user


class LoginWindow:

    def __init__(self, root, start_exam_callback):

        self.root = root
        self.start_exam_callback = start_exam_callback

        self.frame = tk.Frame(
            root,
            padx=20,
            pady=20
        )

        self.frame.pack()

        title = tk.Label(
            self.frame,
            text="SMART EXAM CYBER FORENSICS SYSTEM",
            font=("Arial", 14, "bold"),
            fg="navy"
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=15
        )

        tk.Label(
            self.frame,
            text="Username"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.username = tk.Entry(
            self.frame,
            width=30
        )

        self.username.grid(
            row=1,
            column=1,
            pady=5
        )

        tk.Label(
            self.frame,
            text="Password"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.password = tk.Entry(
            self.frame,
            show="*",
            width=30
        )

        self.password.grid(
            row=2,
            column=1,
            pady=5
        )

        login_btn = tk.Button(
            self.frame,
            text="Login",
            width=15,
            bg="#4CAF50",
            fg="white",
            command=self.login
        )

        login_btn.grid(
            row=3,
            column=0,
            pady=15
        )

        register_btn = tk.Button(
            self.frame,
            text="Register",
            width=15,
            bg="#2196F3",
            fg="white",
            command=self.register
        )

        register_btn.grid(
            row=3,
            column=1,
            pady=15
        )

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

    def clear_fields(self):

        self.username.delete(
            0,
            tk.END
        )

        self.password.delete(
            0,
            tk.END
        )

    def register(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:

            messagebox.showerror(
                "Error",
                "Please enter username and password."
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must be at least 6 characters."
            )

            return

        success = register_user(
            username,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Registration Successful."
            )

            self.clear_fields()

        else:

            messagebox.showerror(
                "Error",
                "Username already exists."
            )

    def login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:

            messagebox.showerror(
                "Error",
                "Please enter username and password."
            )

            return

        success = login_user(
            username,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                f"Welcome {username}"
            )

            self.frame.destroy()

            self.start_exam_callback(
                username
            )

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password"
            )