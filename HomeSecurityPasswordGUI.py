import tkinter as tk
from tkinter import messagebox, simpledialog
from SecurePasswordSystemBackend import SecurePasswordSystemG

class SecurePasswordSystemGUI(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master.title("Secure Password System")
        self.grid(stick="nsew")
        self.create_widgets()

        self.system = SecurePasswordSystemG()

    def create_widgets(self):
        self.master.title("Secure Password System")
        self.master.geometry("500x500")

        self.label = tk.Label(self, text="Welcome to Secure Password System")
        self.label.pack(pady=20)

        self.set_username_btn = tk.Button(self, text="Set Username", command=self.set_initial_username)
        self.set_username_btn.pack(pady=10)

        self.set_password_btn = tk.Button(self, text="Set Password", command=self.set_initial_password)
        self.set_password_btn.pack(pady=10)

        self.verify_password_btn = tk.Button(self, text="Verify Password", command=self.verify_password)
        self.verify_password_btn.pack(pady=10)

        self.guest_access_btn = tk.Button(self, text="Set Guest Access", command=self.set_guest_access)
        self.guest_access_btn.pack(pady=10)

        self.verify_guest_btn = tk.Button(self, text="Verify Guest Access", command=self.verify_guest_access)
        self.verify_guest_btn.pack(pady=10)

        self.status_btn = tk.Button(self, text="Check System Status", command=self.check_system_status)
        self.status_btn.pack(pady=10)

        # More buttons and functionalities can be added as needed

    def set_initial_username(self):
        username = simpledialog.askstring("Set Username", "Enter your username:")
        message = self.system.set_initial_username(username)
        messagebox.showinfo("Info", message)

    def set_initial_password(self):
        password = simpledialog.askstring("Set Password", "Enter your password:", show="*")
        message = self.system.set_initial_password(password)
        messagebox.showinfo("Info", message)

    def verify_password(self):
        password = simpledialog.askstring("Verify Password", "Enter your password:", show="*")
        message = self.system.verify_password(password)
        messagebox.showinfo("Info", message)

    def set_guest_access(self):
        duration = simpledialog.askinteger("Set Guest Access", "Enter duration (1-31):")
        time_choice = simpledialog.askstring("Set Guest Access", "Specify time? (yes/no):")
        time_of_day = None
        if time_choice.lower() == "yes":
            time_of_day = simpledialog.askstring("Set Guest Access", "Enter time (HH:MM in 24-hour format):")
        else:
            time_of_day = None
        message = self.system.set_guest_access(duration, time_choice, time_of_day)
        messagebox.showinfo("Info", message)

    def verify_guest_access(self):
        password = simpledialog.askstring("Verify Guest Access", "Enter guest password:", show="*")
        message = self.system.verify_guest_access(password)
        messagebox.showinfo("Info", message)

    def check_system_status(self):
        status = self.system.check_system_status()
        status_message = "\n".join([f"{key}: {value}" for key, value in status.items()])
        messagebox.showinfo("System Status", status_message)

    def show(self):
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = SecurePasswordSystemGUI(root)
    app.grid(sticky="nsew")
    root.mainloop()
