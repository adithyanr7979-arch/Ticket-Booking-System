import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from mysql.connector import Error

from database import connect_db, setup_database


# -------------------- THEME --------------------
BG = "#F4F7FB"
CARD = "#FFFFFF"
NAVY = "#12233F"
BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
LIGHT_BLUE = "#E8F0FF"
TEXT = "#172033"
MUTED = "#667085"
GREEN = "#16A34A"
RED = "#DC2626"
LIGHT_RED = "#FEECEC"
BORDER = "#D9E1EC"


class TicketBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Railway Ticket Booking System")
        self.root.geometry("1000x680")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG)

        self.setup_styles()

        if not setup_database():
            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL.\n\n"
                "Please check MySQL is running and verify the password "
                "in database.py."
            )

        self.build_main_window()

    # -------------------- STYLE --------------------
    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            rowheight=34,
            fieldbackground=CARD,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )
        style.map(
            "Treeview",
            background=[("selected", "#DCE8FF")],
            foreground=[("selected", TEXT)]
        )

    def make_button(self, parent, text, command, width=18, danger=False):
        bg = RED if danger else BLUE
        active = "#B91C1C" if danger else BLUE_DARK

        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=("Segoe UI", 11, "bold"),
            bg=bg,
            fg="white",
            activebackground=active,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=11
        )

    def make_secondary_button(self, parent, text, command, width=14):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=("Segoe UI", 10, "bold"),
            bg=LIGHT_BLUE,
            fg=NAVY,
            activebackground="#D6E3FF",
            activeforeground=NAVY,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=8,
            pady=9
        )

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self, title, subtitle):
        frame = tk.Frame(self.root, bg=NAVY, height=110)
        frame.pack(fill="x")
        frame.pack_propagate(False)

        left = tk.Frame(frame, bg=NAVY)
        left.pack(side="left", padx=35, pady=17)

        tk.Label(
            left,
            text="🚆  RAILWAY TICKET",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg=NAVY
        ).pack(anchor="w")

        tk.Label(
            left,
            text=subtitle,
            font=("Segoe UI", 10),
            fg="#C8D5EA",
            bg=NAVY
        ).pack(anchor="w", pady=(4, 0))

        tk.Button(
            frame,
            text="HOME",
            command=self.build_main_window,
            font=("Segoe UI", 10, "bold"),
            bg="#203A61",
            fg="white",
            activebackground="#2B4B79",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=8
        ).pack(side="right", padx=30)

    def card(self, parent):
        frame = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0
        )
        return frame

    # -------------------- HOME --------------------
    def build_main_window(self):
        self.clear_root()

        top = tk.Frame(self.root, bg=NAVY, height=135)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top,
            text="🚆  RAILWAY TICKET",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg=NAVY
        ).pack(pady=(23, 3))

        tk.Label(
            top,
            text="TICKET BOOKING SYSTEM",
            font=("Segoe UI", 12, "bold"),
            fg="#C8D5EA",
            bg=NAVY
        ).pack()

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text="Welcome to Ticket Booking System",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(pady=(35, 7))

        tk.Label(
            body,
            text="Book your train ticket quickly and manage your bookings.",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=BG
        ).pack()

        menu = self.card(body)
        menu.pack(pady=25, ipadx=35, ipady=20)

        buttons = [
            ("VIEW TRAINS", self.view_trains),
            ("BOOK TICKET", self.book_ticket),
            ("VIEW BOOKING", self.view_booking),
            ("CANCEL BOOKING", self.cancel_booking),
        ]

        for text, command in buttons:
            b = self.make_button(menu, text, command, width=25)
            b.pack(pady=7)

        bottom = tk.Frame(body, bg=BG)
        bottom.pack(pady=5)

        self.make_secondary_button(
            bottom, "RESET", self.reset_application, width=13
        ).grid(row=0, column=0, padx=8)

        self.make_secondary_button(
            bottom, "EXIT", self.root.destroy, width=13
        ).grid(row=0, column=1, padx=8)

        tk.Label(
            body,
            text="Python • Tkinter • MySQL",
            font=("Segoe UI", 9),
            fg="#98A2B3",
            bg=BG
        ).pack(side="bottom", pady=12)

    def reset_application(self):
        """Return to the initial home screen."""
        self.build_main_window()

    # -------------------- VIEW TRAINS --------------------
    def view_trains(self):
        self.clear_root()
        self.header("View Trains", "AVAILABLE TRAINS")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=30, pady=25)

        card = self.card(body)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="AVAILABLE TRAINS",
            font=("Segoe UI", 18, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=22, pady=(20, 4))

        tk.Label(
            card,
            text="Choose a train and check the current seat availability.",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w", padx=22, pady=(0, 15))

        table_frame = tk.Frame(card, bg=CARD)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = (
            "id", "name", "source", "destination",
            "departure", "arrival", "seats"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "Train ID",
            "name": "Train Name",
            "source": "From",
            "destination": "To",
            "departure": "Departure",
            "arrival": "Arrival",
            "seats": "Available Seats"
        }

        widths = {
            "id": 75,
            "name": 170,
            "source": 120,
            "destination": 120,
            "departure": 105,
            "arrival": 105,
            "seats": 125
        }

        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT train_id, train_name, source, destination,
                           departure_time, arrival_time, available_seats
                    FROM trains
                    ORDER BY train_id
                """)
                for row in cursor.fetchall():
                    tree.insert("", "end", values=row)
                cursor.close()
            except Error as error:
                messagebox.showerror("Database Error", str(error))
            finally:
                connection.close()

        buttons = tk.Frame(body, bg=BG)
        buttons.pack(fill="x", pady=(0, 5))

        self.make_secondary_button(
            buttons, "BACK TO HOME", self.build_main_window, width=16
        ).pack(side="left")

        self.make_button(
            buttons, "BOOK TICKET", self.book_ticket, width=16
        ).pack(side="right")

    # -------------------- BOOK TICKET --------------------
    def book_ticket(self):
        self.clear_root()
        self.header("Book Ticket", "ENTER PASSENGER AND JOURNEY DETAILS")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=45, pady=22)

        card = self.card(body)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="BOOK TICKET",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=(18, 4))

        tk.Label(
            card,
            text="Fill in the details below to confirm your railway ticket.",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        ).pack(pady=(0, 10))

        form = tk.Frame(card, bg=CARD)
        form.pack(pady=3)

        self.passenger_name_entry = self.form_entry(
            form, "Passenger Name", 0
        )
        self.age_entry = self.form_entry(form, "Age", 1)

        tk.Label(
            form, text="Gender", font=("Segoe UI", 10, "bold"),
            fg=TEXT, bg=CARD
        ).grid(row=2, column=0, sticky="w", padx=10, pady=(7, 3))

        self.gender_var = tk.StringVar(value="Male")
        gender = ttk.Combobox(
            form,
            textvariable=self.gender_var,
            values=("Male", "Female", "Other"),
            state="readonly",
            width=34,
            font=("Segoe UI", 10)
        )
        gender.grid(row=2, column=1, padx=10, pady=(7, 3), ipady=4)

        self.train_id_entry = self.form_entry(form, "Train ID", 3)
        self.travel_date_entry = self.form_entry(
            form, "Travel Date (YYYY-MM-DD)", 4
        )
        self.seats_entry = self.form_entry(form, "Number of Seats", 5)

        hint = tk.Label(
            card,
            text="Tip: Click VIEW TRAINS to see Train IDs and available seats.",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=CARD
        )
        hint.pack(pady=3)

        buttons = tk.Frame(card, bg=CARD)
        buttons.pack(pady=13)

        self.make_button(
            buttons, "BOOK TICKET", self.save_booking, width=16
        ).grid(row=0, column=0, padx=6)

        self.make_secondary_button(
            buttons, "RESET", self.reset_booking_form, width=12
        ).grid(row=0, column=1, padx=6)

        self.make_secondary_button(
            buttons, "EXIT", self.build_main_window, width=12
        ).grid(row=0, column=2, padx=6)

    def form_entry(self, parent, label, row):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 10, "bold"),
            fg=TEXT,
            bg=CARD
        ).grid(row=row, column=0, sticky="w", padx=10, pady=3)

        entry = tk.Entry(
            parent,
            width=37,
            font=("Segoe UI", 10),
            bg="#FBFCFE",
            fg=TEXT,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE
        )
        entry.grid(row=row, column=1, padx=10, pady=3, ipady=5)
        return entry

    def reset_booking_form(self):
        self.passenger_name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_var.set("Male")
        self.train_id_entry.delete(0, tk.END)
        self.travel_date_entry.delete(0, tk.END)
        self.seats_entry.delete(0, tk.END)
        self.passenger_name_entry.focus()

    def save_booking(self):
        name = self.passenger_name_entry.get().strip()
        age_text = self.age_entry.get().strip()
        gender = self.gender_var.get().strip()
        train_id_text = self.train_id_entry.get().strip()
        travel_date = self.travel_date_entry.get().strip()
        seats_text = self.seats_entry.get().strip()

        if not all([name, age_text, gender, train_id_text, travel_date, seats_text]):
            messagebox.showwarning(
                "Missing Details",
                "Please fill in all fields."
            )
            return

        try:
            age = int(age_text)
            train_id = int(train_id_text)
            seats = int(seats_text)
        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Age, Train ID and Number of Seats must be numbers."
            )
            return

        if age < 1 or age > 120:
            messagebox.showwarning("Invalid Age", "Enter an age between 1 and 120.")
            return

        if seats < 1:
            messagebox.showwarning(
                "Invalid Seats", "Number of seats must be at least 1."
            )
            return

        try:
            travel_date_obj = datetime.strptime(
                travel_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            messagebox.showwarning(
                "Invalid Date",
                "Please enter the date as YYYY-MM-DD.\nExample: 2026-09-23"
            )
            return

        connection = connect_db()
        if not connection:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        cursor = None
        try:
            # Transaction prevents two users from overselling seats.
            connection.start_transaction()

            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT train_id, train_name, source, destination,
                       departure_time, arrival_time, available_seats
                FROM trains
                WHERE train_id = %s
                FOR UPDATE
            """, (train_id,))
            train = cursor.fetchone()

            if not train:
                connection.rollback()
                messagebox.showerror(
                    "Invalid Train",
                    "Train ID not found. Please check View Trains."
                )
                return

            if seats > train["available_seats"]:
                connection.rollback()
                messagebox.showwarning(
                    "Not Enough Seats",
                    f"Only {train['available_seats']} seat(s) are available."
                )
                return

            cursor.execute("""
                INSERT INTO bookings
                (passenger_name, age, gender, train_id, travel_date, seats)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, age, gender, train_id, travel_date_obj, seats))

            booking_id = cursor.lastrowid

            cursor.execute("""
                UPDATE trains
                SET available_seats = available_seats - %s
                WHERE train_id = %s
            """, (seats, train_id))

            connection.commit()

            self.show_booking_confirmation(
                booking_id, name, age, gender, train, travel_date, seats
            )

        except Error as error:
            connection.rollback()
            messagebox.showerror("Booking Error", str(error))
        finally:
            if cursor:
                cursor.close()
            connection.close()

    # -------------------- CONFIRMATION --------------------
    def show_booking_confirmation(
        self, booking_id, name, age, gender, train, travel_date, seats
    ):
        window = tk.Toplevel(self.root)
        window.title("Booking Confirmed")
        window.geometry("590x610")
        window.configure(bg=CARD)
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text="🎫  RAILWAY TICKET",
            font=("Segoe UI", 24, "bold"),
            fg=NAVY,
            bg=CARD
        ).pack(pady=(25, 3))

        tk.Label(
            window,
            text="TICKET BOOKING SYSTEM",
            font=("Segoe UI", 11, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack()

        tk.Frame(window, bg=BORDER, height=1).pack(
            fill="x", padx=55, pady=18
        )

        tk.Label(
            window,
            text=f"BOOKING ID : {booking_id}",
            font=("Segoe UI", 19, "bold"),
            fg=BLUE,
            bg=CARD
        ).pack(pady=(0, 18))

        details = tk.Frame(window, bg=CARD)
        details.pack(anchor="w", padx=85)

        rows = [
            ("Passenger Name", name),
            ("Age", age),
            ("Gender", gender),
            ("Train", train["train_name"]),
            ("From", train["source"]),
            ("To", train["destination"]),
            ("Departure", train["departure_time"]),
            ("Arrival", train["arrival_time"]),
            ("Travel Date", travel_date),
            ("Seats", seats),
        ]

        for label, value in rows:
            row = tk.Frame(details, bg=CARD)
            row.pack(fill="x", pady=3)

            tk.Label(
                row, text=label, width=17, anchor="w",
                font=("Segoe UI", 10), fg=MUTED, bg=CARD
            ).pack(side="left")

            tk.Label(
                row, text=f": {value}", anchor="w",
                font=("Segoe UI", 10, "bold"), fg=TEXT, bg=CARD
            ).pack(side="left")

        tk.Frame(window, bg=BORDER, height=1).pack(
            fill="x", padx=55, pady=18
        )

        tk.Label(
            window,
            text="✓  BOOKING CONFIRMED",
            font=("Segoe UI", 12, "bold"),
            fg=GREEN,
            bg=CARD
        ).pack()

        tk.Label(
            window,
            text="Thank you for using our Ticket Booking System!",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=CARD
        ).pack(pady=7)

        self.make_secondary_button(
            window, "CLOSE", window.destroy, width=12
        ).pack(pady=12)

    # -------------------- VIEW BOOKING --------------------
    def view_booking(self):
        self.clear_root()
        self.header("View Booking", "SEARCH YOUR BOOKING")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=45, pady=25)

        card = self.card(body)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="VIEW BOOKING",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=(25, 4))

        tk.Label(
            card,
            text="Enter your Booking ID to view the ticket details.",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        ).pack()

        search_frame = tk.Frame(card, bg=CARD)
        search_frame.pack(pady=18)

        tk.Label(
            search_frame,
            text="Booking ID",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(side="left", padx=7)

        self.view_id_entry = tk.Entry(
            search_frame,
            width=22,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        self.view_id_entry.pack(side="left", padx=7, ipady=5)

        self.make_button(
            search_frame, "SEARCH", self.search_booking, width=10
        ).pack(side="left", padx=7)

        self.booking_result = tk.Frame(card, bg=CARD)
        self.booking_result.pack(fill="both", expand=True, padx=30, pady=5)

        self.make_secondary_button(
            card, "EXIT", self.build_main_window, width=12
        ).pack(pady=15)

        self.view_id_entry.focus()

    def search_booking(self):
        booking_id_text = self.view_id_entry.get().strip()

        if not booking_id_text.isdigit():
            messagebox.showwarning(
                "Invalid Booking ID",
                "Please enter a valid numeric Booking ID."
            )
            return

        booking_id = int(booking_id_text)

        for widget in self.booking_result.winfo_children():
            widget.destroy()

        connection = connect_db()
        if not connection:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT b.booking_id, b.passenger_name, b.age, b.gender,
                       t.train_name, t.source, t.destination,
                       t.departure_time, t.arrival_time,
                       b.travel_date, b.seats
                FROM bookings b
                JOIN trains t ON b.train_id = t.train_id
                WHERE b.booking_id = %s
            """, (booking_id,))

            booking = cursor.fetchone()

            if not booking:
                messagebox.showinfo(
                    "Not Found",
                    "No booking found with this Booking ID."
                )
                return

            self.display_booking(booking)

        except Error as error:
            messagebox.showerror("Database Error", str(error))
        finally:
            if cursor:
                cursor.close()
            connection.close()

    def display_booking(self, booking):
        box = tk.Frame(
            self.booking_result,
            bg="#F8FAFC",
            highlightbackground=BORDER,
            highlightthickness=1
        )
        box.pack(fill="both", expand=True, padx=20, pady=5)

        tk.Label(
            box,
            text=f"BOOKING ID : {booking['booking_id']}",
            font=("Segoe UI", 17, "bold"),
            fg=BLUE,
            bg="#F8FAFC"
        ).pack(pady=(18, 12))

        details = tk.Frame(box, bg="#F8FAFC")
        details.pack()

        values = [
            ("Passenger", booking["passenger_name"]),
            ("Age", booking["age"]),
            ("Gender", booking["gender"]),
            ("Train", booking["train_name"]),
            ("From", booking["source"]),
            ("To", booking["destination"]),
            ("Departure", booking["departure_time"]),
            ("Arrival", booking["arrival_time"]),
            ("Travel Date", booking["travel_date"]),
            ("Seats", booking["seats"]),
        ]

        for label, value in values:
            tk.Label(
                details,
                text=f"{label} :",
                width=18,
                anchor="e",
                font=("Segoe UI", 10),
                fg=MUTED,
                bg="#F8FAFC"
            ).grid(row=values.index((label, value)), column=0, padx=7, pady=2)

            tk.Label(
                details,
                text=str(value),
                width=25,
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                fg=TEXT,
                bg="#F8FAFC"
            ).grid(row=values.index((label, value)), column=1, padx=7, pady=2)

    # -------------------- CANCEL BOOKING --------------------
    def cancel_booking(self):
        self.clear_root()
        self.header("Cancel Booking", "CANCEL AN EXISTING TICKET")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=45, pady=30)

        card = self.card(body)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="CANCEL BOOKING",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=(40, 6))

        tk.Label(
            card,
            text="Enter the Booking ID of the ticket you want to cancel.",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        ).pack()

        frame = tk.Frame(card, bg=CARD)
        frame.pack(pady=25)

        tk.Label(
            frame,
            text="Booking ID",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack()

        self.cancel_id_entry = tk.Entry(
            frame,
            width=28,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        self.cancel_id_entry.pack(pady=7, ipady=6)

        tk.Label(
            card,
            text="⚠  Cancelling a booking will return its seats to the train.",
            font=("Segoe UI", 9),
            fg=RED,
            bg=CARD
        ).pack(pady=5)

        buttons = tk.Frame(card, bg=CARD)
        buttons.pack(pady=18)

        self.make_button(
            buttons, "CANCEL TICKET", self.delete_booking,
            width=16, danger=True
        ).grid(row=0, column=0, padx=7)

        self.make_secondary_button(
            buttons, "RESET", self.reset_cancel_form, width=12
        ).grid(row=0, column=1, padx=7)

        self.make_secondary_button(
            buttons, "EXIT", self.build_main_window, width=12
        ).grid(row=0, column=2, padx=7)

        self.cancel_id_entry.focus()

    def reset_cancel_form(self):
        self.cancel_id_entry.delete(0, tk.END)
        self.cancel_id_entry.focus()

    def delete_booking(self):
        booking_id_text = self.cancel_id_entry.get().strip()

        if not booking_id_text.isdigit():
            messagebox.showwarning(
                "Invalid Booking ID",
                "Please enter a valid numeric Booking ID."
            )
            return

        booking_id = int(booking_id_text)

        connection = connect_db()
        if not connection:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        cursor = None
        try:
            connection.start_transaction()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT booking_id, train_id, seats, passenger_name
                FROM bookings
                WHERE booking_id = %s
                FOR UPDATE
            """, (booking_id,))

            booking = cursor.fetchone()

            if not booking:
                connection.rollback()
                messagebox.showinfo(
                    "Not Found",
                    "No booking found with this Booking ID."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Cancellation",
                f"Cancel Booking ID {booking_id} for "
                f"{booking['passenger_name']}?"
            )

            if not confirm:
                connection.rollback()
                return

            cursor.execute("""
                UPDATE trains
                SET available_seats = available_seats + %s
                WHERE train_id = %s
            """, (booking["seats"], booking["train_id"]))

            cursor.execute("""
                DELETE FROM bookings
                WHERE booking_id = %s
            """, (booking_id,))

            connection.commit()

            messagebox.showinfo(
                "Booking Cancelled",
                f"Booking ID {booking_id} was cancelled successfully."
            )
            self.build_main_window()

        except Error as error:
            connection.rollback()
            messagebox.showerror("Cancellation Error", str(error))
        finally:
            if cursor:
                cursor.close()
            connection.close()


# -------------------- START APPLICATION --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingSystem(root)
    root.mainloop()
