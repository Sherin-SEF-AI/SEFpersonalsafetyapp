import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class SafetyApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Safety App")
        self.geometry("500x500")
        self.current_user_id = None

        # Create and initialize database tables if not already present
        self.create_tables()
        self.initialize_ui()

    def create_tables(self):
        conn = sqlite3.connect('safety_app.db')
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                notification INTEGER DEFAULT 0,
                notification_sound TEXT DEFAULT '',
                vibration_pattern TEXT DEFAULT '',
                location_tracking INTEGER DEFAULT 0,
                location_sharing INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TEXT NOT NULL,
                location TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                alert_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        conn.commit()
        conn.close()

    def initialize_ui(self):
        # Create login and registration forms
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=20)

        ctk.CTkLabel(self.login_frame, text="Username").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = ctk.CTkEntry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.login_frame, text="Password").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self.login_frame, text="Don't have an account?").grid(row=3, column=0, padx=10, pady=5)
        ctk.CTkButton(self.login_frame, text="Register", command=self.show_registration_form).grid(row=3, column=1, padx=10, pady=5)

        self.registration_frame = ctk.CTkFrame(self)
        
        ctk.CTkLabel(self.registration_frame, text="Username").grid(row=0, column=0, padx=10, pady=5)
        self.reg_username_entry = ctk.CTkEntry(self.registration_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.registration_frame, text="Password").grid(row=1, column=0, padx=10, pady=5)
        self.reg_password_entry = ctk.CTkEntry(self.registration_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.registration_frame, text="Name").grid(row=2, column=0, padx=10, pady=5)
        self.reg_name_entry = ctk.CTkEntry(self.registration_frame)
        self.reg_name_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.registration_frame, text="Email").grid(row=3, column=0, padx=10, pady=5)
        self.reg_email_entry = ctk.CTkEntry(self.registration_frame)
        self.reg_email_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkButton(self.registration_frame, text="Register", command=self.register).grid(row=4, column=0, columnspan=2, pady=10)
        ctk.CTkButton(self.registration_frame, text="Back to Login", command=self.show_login_form).grid(row=5, column=0, columnspan=2, pady=10)

        self.main_frame = ctk.CTkFrame(self)
        ctk.CTkButton(self.main_frame, text="Update Profile", command=self.update_profile).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(self.main_frame, text="Settings", command=self.show_settings).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(self.main_frame, text="Check-in", command=self.check_in).grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(self.main_frame, text="View Check-ins", command=self.view_checkins).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(self.main_frame, text="Send Alert", command=self.send_alert).grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkButton(self.main_frame, text="View Alerts", command=self.view_alerts).grid(row=2, column=1, padx=10, pady=5)
        ctk.CTkButton(self.main_frame, text="Manage Contacts", command=self.manage_contacts).grid(row=3, column=0, padx=10, pady=5)
        ctk.CTkButton(self.main_frame, text="Logout", command=self.logout).grid(row=3, column=1, padx=10, pady=5)

        self.profile_frame = ctk.CTkFrame(self)
        ctk.CTkLabel(self.profile_frame, text="Name").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(self.profile_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.profile_frame, text="Email").grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(self.profile_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self.profile_frame, text="Back to Main", command=self.return_to_main_from_profile).grid(row=2, column=0, columnspan=2, pady=10)

        self.settings_frame = ctk.CTkFrame(self)
        ctk.CTkLabel(self.settings_frame, text="Notifications").grid(row=0, column=0, padx=10, pady=5)
        self.notification_var = tk.BooleanVar()
        ctk.CTkCheckBox(self.settings_frame, text="", variable=self.notification_var).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.settings_frame, text="Notification Sound").grid(row=1, column=0, padx=10, pady=5)
        self.notification_sound_entry = ctk.CTkEntry(self.settings_frame)
        self.notification_sound_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.settings_frame, text="Vibration Pattern").grid(row=2, column=0, padx=10, pady=5)
        self.vibration_pattern_entry = ctk.CTkEntry(self.settings_frame)
        self.vibration_pattern_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.settings_frame, text="Location Tracking").grid(row=3, column=0, padx=10, pady=5)
        self.location_tracking_var = tk.BooleanVar()
        ctk.CTkCheckBox(self.settings_frame, text="", variable=self.location_tracking_var).grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.settings_frame, text="Location Sharing").grid(row=4, column=0, padx=10, pady=5)
        self.location_sharing_var = tk.BooleanVar()
        ctk.CTkCheckBox(self.settings_frame, text="", variable=self.location_sharing_var).grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkButton(self.settings_frame, text="Save Settings", command=self.save_settings).grid(row=5, column=0, columnspan=2, pady=10)
        ctk.CTkButton(self.settings_frame, text="Back to Main", command=self.return_to_main_from_settings).grid(row=6, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = hash_password(self.password_entry.get())
        
        conn = sqlite3.connect('safety_app.db')
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            self.current_user_id = result[0]
            self.login_frame.pack_forget()
            self.main_frame.pack(pady=20)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_registration_form(self):
        self.login_frame.pack_forget()
        self.registration_frame.pack(pady=20)

    def show_login_form(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def register(self):
        username = self.reg_username_entry.get()
        password = hash_password(self.reg_password_entry.get())
        name = self.reg_name_entry.get()
        email = self.reg_email_entry.get()
        
        conn = sqlite3.connect('safety_app.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, name, email) VALUES (?, ?, ?, ?)", (username, password, name, email))
            conn.commit()
            messagebox.showinfo("Registration Successful", "You can now log in with your username and password")
            self.show_login_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Failed", "Username already exists")
        conn.close()

    def update_profile(self):
        self.main_frame.pack_forget()
        self.profile_frame.pack(pady=20)

        conn = sqlite3.connect('safety_app.db')
        c = conn.cursor()
        c.execute("SELECT name, email FROM users WHERE user_id=?", (self.current_user_id,))
        result = c.fetchone()
        conn.close()

        if result:
            self.name_entry.insert(0, result[0])
            self.email_entry.insert(0, result[1])

    def return_to_main_from_profile(self):
        self.profile_frame.pack_forget()
        self.main_frame.pack(pady=20)

    def show_settings(self):
        self.main_frame.pack_forget()
        self.settings_frame.pack(pady=20)

        conn = sqlite3.connect('safety_app.db')
        c = conn.cursor()
        c.execute("SELECT notification, notification_sound, vibration_pattern, location_tracking, location_sharing FROM settings WHERE user_id=?", (self.current_user_id,))
        result = c.fetchone()
        conn.close()

        if result:
            self.notification_var.set(result[0])
            self.notification_sound_entry.insert(0, result[1])
            self.vibration_pattern_entry.insert(0, result[2])
            self.location_tracking_var.set(result[3])
            self.location_sharing_var.set(result[4])

    def save_settings(self):
        notification = self.notification_var.get()
        notification_sound = self.notification_sound_entry.get()
        vibration_pattern = self.vibration_pattern_entry.get()
        location_tracking = self.location_tracking_var.get()
        location_sharing = self.location_sharing_var.get()

        conn = sqlite3.connect('safety_app.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO settings (user_id, notification, notification_sound, vibration_pattern, location_tracking, location_sharing)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            notification=excluded.notification,
            notification_sound=excluded.notification_sound,
            vibration_pattern=excluded.vibration_pattern,
            location_tracking=excluded.location_tracking,
            location_sharing=excluded.location_sharing
        ''', (self.current_user_id, notification, notification_sound, vibration_pattern, location_tracking, location_sharing))
        conn.commit()
        conn.close()

        self.return_to_main_from_settings()

    def return_to_main_from_settings(self):
        self.settings_frame.pack_forget()
        self.main_frame.pack(pady=20)

    def check_in(self):
        # Logic for checking in (add check-in record to the database)
        pass

    def view_checkins(self):
        # Logic for viewing check-ins
        pass

    def send_alert(self):
        # Logic for sending alerts (add alert record to the database)
        pass

    def view_alerts(self):
        # Logic for viewing alerts
        pass

    def manage_contacts(self):
        # Logic for managing contacts
        pass

    def logout(self):
        self.current_user_id = None
        self.main_frame.pack_forget()
        self.login_frame.pack(pady=20)

if __name__ == "__main__":
    app = SafetyApp()
    app.mainloop()

