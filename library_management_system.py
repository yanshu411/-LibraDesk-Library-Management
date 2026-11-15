
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ==========================================
# LIBRADESK - LIBRARY MANAGEMENT SYSTEM
# ==========================================

BG = "#F4F7FB"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
DARK = "#172554"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#DCE4EF"
GREEN = "#16A34A"
RED = "#DC2626"

DB_NAME = "library.db"

# ==========================================
# DATABASE
# ==========================================

def connect_db():
    return sqlite3.connect(DB_NAME)


def setup_database():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL
                    CHECK(quantity >= 0),
                available INTEGER NOT NULL
                    CHECK(available >= 0
                    AND available <= quantity)
            )
        """)


setup_database()

# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("LibraDesk | Library Management System")
root.geometry("1200x760")
root.minsize(1000, 650)
root.configure(bg=BG)

selected_id = None

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    fieldbackground=WHITE,
    rowheight=35,
    font=("Segoe UI", 10),
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background="#EAF0F9",
    foreground=DARK,
    font=("Segoe UI", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#DBEAFE")],
    foreground=[("selected", TEXT)]
)

# ==========================================
# LAYOUT
# ==========================================

sidebar = tk.Frame(root, bg=WHITE, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(root, bg=BG)
content.pack(side="left", fill="both", expand=True)

tk.Label(
    sidebar,
    text="📚 LibraDesk",
    bg=WHITE,
    fg=PRIMARY,
    font=("Segoe UI", 20, "bold")
).pack(pady=(30, 8))

tk.Label(
    sidebar,
    text="LIBRARY MANAGEMENT",
    bg=WHITE,
    fg=MUTED,
    font=("Segoe UI", 9, "bold")
).pack(pady=(0, 35))

# ==========================================
# HEADER
# ==========================================

header = tk.Frame(content, bg=BG)
header.pack(fill="x", padx=30, pady=(25, 15))

tk.Label(
    header,
    text="Library Dashboard",
    bg=BG,
    fg=DARK,
    font=("Segoe UI", 24, "bold")
).pack(anchor="w")

tk.Label(
    header,
    text="Manage your library collection in one place.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", pady=5)

# ==========================================
# DASHBOARD CARDS
# ==========================================

cards_frame = tk.Frame(content, bg=BG)
cards_frame.pack(fill="x", padx=25, pady=10)

stats = {}

def create_card(title, color):
    card = tk.Frame(
        cards_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5,
        ipady=12
    )

    tk.Label(
        card,
        text=title,
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=18, pady=(8, 5))

    value = tk.Label(
        card,
        text="0",
        bg=WHITE,
        fg=color,
        font=("Segoe UI", 25, "bold")
    )
    value.pack(anchor="w", padx=18)

    return value


stats["titles"] = create_card("Book Titles", PRIMARY)
stats["copies"] = create_card("Total Copies", DARK)
stats["available"] = create_card("Available", GREEN)
stats["issued"] = create_card("Issued", RED)

# ==========================================
# BOOK FORM
# ==========================================

form_panel = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
form_panel.pack(fill="x", padx=30, pady=12)

tk.Label(
    form_panel,
    text="Book Information",
    bg=WHITE,
    fg=DARK,
    font=("Segoe UI", 15, "bold")
).pack(anchor="w", padx=20, pady=(15, 10))

fields_frame = tk.Frame(form_panel, bg=WHITE)
fields_frame.pack(fill="x", padx=20)

entries = {}

field_names = [
    ("Title", "title"),
    ("Author", "author"),
    ("Category", "category"),
    ("ISBN", "isbn"),
    ("Quantity", "quantity")
]

for index, (label_text, key) in enumerate(field_names):
    field = tk.Frame(fields_frame, bg=WHITE)
    field.grid(
        row=index // 3,
        column=index % 3,
        sticky="ew",
        padx=8,
        pady=8
    )

    tk.Label(
        field,
        text=label_text,
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(0, 5))

    entry = tk.Entry(
        field,
        font=("Segoe UI", 11),
        bg="#F8FAFC",
        fg=TEXT,
        relief="solid",
        bd=1
    )
    entry.pack(fill="x", ipady=7)

    entries[key] = entry

for i in range(3):
    fields_frame.columnconfigure(i, weight=1)

# ==========================================
# DATABASE OPERATIONS
# ==========================================

def get_form_data():
    data = {
        key: entry.get().strip()
        for key, entry in entries.items()
    }

    if any(not value for value in data.values()):
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return None

    try:
        quantity = int(data["quantity"])

        if quantity < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Quantity",
            "Quantity must be a non-negative integer."
        )
        return None

    data["quantity"] = quantity
    return data


def clear_form():
    global selected_id

    selected_id = None

    for entry in entries.values():
        entry.delete(0, tk.END)

    if tree.selection():
        tree.selection_remove(tree.selection())


def add_book():
    data = get_form_data()

    if data is None:
        return

    try:
        with connect_db() as conn:
            conn.execute("""
                INSERT INTO books
                (title, author, category, isbn,
                 quantity, available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data["title"],
                data["author"],
                data["category"],
                data["isbn"],
                data["quantity"],
                data["quantity"]
            ))

        clear_form()
        refresh_all()

        messagebox.showinfo(
            "Success",
            "Book added successfully!"
        )

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Duplicate ISBN",
            "A book with this ISBN already exists."
        )


def update_book():
    if selected_id is None:
        messagebox.showwarning(
            "Select Book",
            "Please select a book to update."
        )
        return

    data = get_form_data()

    if data is None:
        return

    try:
        with connect_db() as conn:
            row = conn.execute("""
                SELECT quantity, available
                FROM books WHERE id = ?
            """, (selected_id,)).fetchone()

            if row is None:
                messagebox.showerror(
                    "Not Found",
                    "This book no longer exists."
                )
                return

            old_quantity, old_available = row
            issued = old_quantity - old_available

            if data["quantity"] < issued:
                messagebox.showerror(
                    "Invalid Quantity",
                    "Quantity cannot be less than "
                    "the number of issued copies."
                )
                return

            new_available = data["quantity"] - issued

            conn.execute("""
                UPDATE books
                SET title=?, author=?, category=?,
                    isbn=?, quantity=?, available=?
                WHERE id=?
            """, (
                data["title"],
                data["author"],
                data["category"],
                data["isbn"],
                data["quantity"],
                new_available,
                selected_id
            ))

        clear_form()
        refresh_all()

        messagebox.showinfo(
            "Success",
            "Book updated successfully!"
        )

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Duplicate ISBN",
            "Another book already uses this ISBN."
        )


def delete_book():
    if selected_id is None:
        messagebox.showwarning(
            "Select Book",
            "Please select a book first."
        )
        return

    if not messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this book?"
    ):
        return

    with connect_db() as conn:
        row = conn.execute("""
            SELECT quantity, available
            FROM books WHERE id=?
        """, (selected_id,)).fetchone()

        if row is None:
            clear_form()
            refresh_all()
            return

        if row[0] != row[1]:
            messagebox.showerror(
                "Cannot Delete",
                "This book has issued copies."
            )
            return

        conn.execute(
            "DELETE FROM books WHERE id=?",
            (selected_id,)
        )

    clear_form()
    refresh_all()


# ==========================================
# FORM BUTTONS
# ==========================================

button_frame = tk.Frame(form_panel, bg=WHITE)
button_frame.pack(
    fill="x",
    padx=25,
    pady=(10, 18)
)

def action_button(text, command, color):
    tk.Button(
        button_frame,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=18,
        pady=9,
        cursor="hand2"
    ).pack(side="left", padx=5)


action_button("Add Book", add_book, PRIMARY)
action_button("Update", update_book, GREEN)
action_button("Delete", delete_book, RED)
action_button("Clear", clear_form, "#64748B")

# ==========================================
# BOOK TABLE
# ==========================================

table_panel = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
table_panel.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(5, 25)
)

table_header = tk.Frame(table_panel, bg=WHITE)
table_header.pack(fill="x", padx=15, pady=12)

tk.Label(
    table_header,
    text="Book Inventory",
    bg=WHITE,
    fg=DARK,
    font=("Segoe UI", 15, "bold")
).pack(side="left")

search_var = tk.StringVar()

search_entry = tk.Entry(
    table_header,
    textvariable=search_var,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    relief="solid",
    bd=1,
    width=28
)
search_entry.pack(side="right", ipady=7)

tk.Label(
    table_header,
    text="Search:",
    bg=WHITE,
    fg=MUTED
).pack(side="right", padx=8)

table_container = tk.Frame(table_panel, bg=WHITE)
table_container.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(0, 15)
)

columns = (
    "id", "title", "author", "category",
    "isbn", "quantity", "available"
)

tree = ttk.Treeview(
    table_container,
    columns=columns,
    show="headings",
    selectmode="browse"
)

headings = [
    "ID", "Title", "Author", "Category",
    "ISBN", "Total", "Available"
]

for col, heading in zip(columns, headings):
    tree.heading(col, text=heading)

    tree.column(
        col,
        width=70 if col in
        ("id", "quantity", "available") else 140,
        anchor="center" if col in
        ("id", "quantity", "available") else "w"
    )

scrollbar = ttk.Scrollbar(
    table_container,
    orient="vertical",
    command=tree.yview
)
tree.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
tree.pack(side="left", fill="both", expand=True)

# ==========================================
# LOAD AND SEARCH
# ==========================================

def load_books(*args):
    keyword = search_var.get().strip()

    for item in tree.get_children():
        tree.delete(item)

    with connect_db() as conn:
        if keyword:
            pattern = f"%{keyword}%"

            rows = conn.execute("""
                SELECT * FROM books
                WHERE title LIKE ?
                   OR author LIKE ?
                   OR category LIKE ?
                   OR isbn LIKE ?
                ORDER BY id DESC
            """, (pattern,) * 4).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM books
                ORDER BY id DESC
            """).fetchall()

    for row in rows:
        tree.insert("", "end", values=row)


def load_stats():
    with connect_db() as conn:
        result = conn.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(quantity), 0),
                COALESCE(SUM(available), 0),
                COALESCE(SUM(quantity - available), 0)
            FROM books
        """).fetchone()

    for key, value in zip(
        ("titles", "copies", "available", "issued"),
        result
    ):
        stats[key].config(text=str(value))


def refresh_all():
    load_books()
    load_stats()


def select_book(event):
    global selected_id

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(selected[0], "values")
    selected_id = int(values[0])

    keys = [
        "title", "author", "category",
        "isbn", "quantity"
    ]

    for key, value in zip(keys, values[1:6]):
        entries[key].delete(0, tk.END)
        entries[key].insert(0, str(value))


tree.bind("<<TreeviewSelect>>", select_book)
search_var.trace_add("write", load_books)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

def sidebar_button(text, command):
    tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=WHITE,
        fg=TEXT,
        activebackground="#DBEAFE",
        relief="flat",
        anchor="w",
        font=("Segoe UI", 11),
        padx=22,
        pady=13,
        cursor="hand2"
    ).pack(fill="x", padx=10, pady=4)


sidebar_button("Dashboard", refresh_all)

sidebar_button(
    "Book Management",
    lambda: entries["title"].focus_set()
)

sidebar_button("Refresh Records", refresh_all)

tk.Label(
    sidebar,
    text="Version 1.0",
    bg=WHITE,
    fg=MUTED,
    font=("Segoe UI", 9)
).pack(side="bottom", pady=20)

# ==========================================
# START APPLICATION
# ==========================================

refresh_all()
root.mainloop()
