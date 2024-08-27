import tkinter as tk
from tkinter import ttk, messagebox
import json

class Book:
    def __init__(self, title, author, isbn, genre, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.year = year

class Member:
    def __init__(self, name, member_id, contact):
        self.name = name
        self.member_id = member_id
        self.contact = contact

class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.checkouts = {}  

    def add_book(self, book):
        self.books.append(book)

    def add_member(self, member):
        self.members.append(member)

    def delete_book(self, book):
        if book in self.books:
            self.books.remove(book)
          
            if book.title in self.checkouts:
                del self.checkouts[book.title]

    def delete_member(self, member):
        if member in self.members:
            self.members.remove(member)
           
            self.checkouts = {title: (m_id, due_date) for title, (m_id, due_date) in self.checkouts.items() if m_id != member.member_id}

    def checkout_book(self, book, member, days):
        if book.title not in self.checkouts:
            due_date = self.calculate_due_date(days)
            self.checkouts[book.title] = (member.member_id, due_date)
        else:
            messagebox.showwarning("Error", "Book is already checked out.")

    def return_book(self, book, member):
        if book.title in self.checkouts and self.checkouts[book.title][0] == member.member_id:
            del self.checkouts[book.title]
        else:
            messagebox.showwarning("Error", "This book is not checked out by this member.")

    def calculate_due_date(self, days):
        from datetime import datetime, timedelta
        return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

class MainGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.library = Library()
        self.member_combobox = None
        self.book_combobox = None
        self.init_components()
        self.load_data()

    def init_components(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        book_panel = self.create_book_panel()
        member_panel = self.create_member_panel()
        checkout_panel = self.create_checkout_panel()

        notebook.add(book_panel, text="Book Management")
        notebook.add(member_panel, text="Member Management")
        notebook.add(checkout_panel, text="Checkout/Return")

    def create_book_panel(self):
        panel = ttk.Frame(self)

        title_label = ttk.Label(panel, text="Title:")
        title_entry = ttk.Entry(panel, width=50)
        author_label = ttk.Label(panel, text="Author:")
        author_entry = ttk.Entry(panel, width=50)
        isbn_label = ttk.Label(panel, text="ISBN:")
        isbn_entry = ttk.Entry(panel, width=30)
        genre_label = ttk.Label(panel, text="Genre:")
        genre_entry = ttk.Entry(panel, width=30)
        year_label = ttk.Label(panel, text="Year:")
        year_entry = ttk.Entry(panel, width=15)

        add_button = ttk.Button(panel, text="Add Book", width=20,
                                command=lambda: self.add_book(title_entry, author_entry, isbn_entry, genre_entry,
                                                              year_entry, book_listbox))
        edit_button = ttk.Button(panel, text="Edit Book", width=20,
                                 command=lambda: self.edit_book(book_listbox, title_entry, author_entry, isbn_entry,
                                                                genre_entry, year_entry))
        delete_button = ttk.Button(panel, text="Delete Book", width=20, command=lambda: self.delete_book(book_listbox))
        search_button = ttk.Button(panel, text="Search", width=15,
                                   command=lambda: self.search_books(search_entry.get(), book_listbox))
        search_entry = ttk.Entry(panel, width=50)

        book_listbox = tk.Listbox(panel)
        scrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=book_listbox.yview)
        book_listbox.config(yscrollcommand=scrollbar.set)

        title_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        author_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        author_entry.grid(row=1, column=1, padx=10, pady=5)
        isbn_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        isbn_entry.grid(row=2, column=1, padx=10, pady=5)
        genre_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        genre_entry.grid(row=3, column=1, padx=10, pady=5)
        year_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        year_entry.grid(row=4, column=1, padx=10, pady=5)

        add_button.grid(row=5, column=0, padx=10, pady=5)
        edit_button.grid(row=5, column=1, padx=10, pady=5)
        delete_button.grid(row=5, column=2, padx=10, pady=5)

        search_entry.grid(row=6, column=0, padx=10, pady=5, columnspan=2)
        search_button.grid(row=6, column=2, padx=10, pady=5)

        book_listbox.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W + tk.E)
        scrollbar.grid(row=7, column=3, sticky=tk.NS)

        return panel

    def create_member_panel(self):
        panel = ttk.Frame(self)

        name_label = ttk.Label(panel, text="Name:")
        name_entry = ttk.Entry(panel, width=50)
        id_label = ttk.Label(panel, text="ID:")
        id_entry = ttk.Entry(panel, width=30)
        contact_label = ttk.Label(panel, text="Contact:")
        contact_entry = ttk.Entry(panel, width=50)

        add_button = ttk.Button(panel, text="Add Member", width=20,
                                command=lambda: self.add_member(name_entry, id_entry, contact_entry, member_listbox))
        edit_button = ttk.Button(panel, text="Edit Member", width=20,
                                 command=lambda: self.edit_member(member_listbox, name_entry, id_entry, contact_entry))
        delete_button = ttk.Button(panel, text="Delete Member", width=20,
                                   command=lambda: self.delete_member(member_listbox))
        search_button = ttk.Button(panel, text="Search", width=15,
                                   command=lambda: self.search_members(search_entry.get(), member_listbox))
        search_entry = ttk.Entry(panel, width=50)

        member_listbox = tk.Listbox(panel)
        scrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=member_listbox.yview)
        member_listbox.config(yscrollcommand=scrollbar.set)

        name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        id_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        id_entry.grid(row=1, column=1, padx=10, pady=5)
        contact_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        contact_entry.grid(row=2, column=1, padx=10, pady=5)

        add_button.grid(row=3, column=0, padx=10, pady=5)
        edit_button.grid(row=3, column=1, padx=10, pady=5)
        delete_button.grid(row=3, column=2, padx=10, pady=5)

        search_entry.grid(row=4, column=0, padx=10, pady=5, columnspan=2)
        search_button.grid(row=4, column=2, padx=10, pady=5)

        member_listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W + tk.E)
        scrollbar.grid(row=5, column=3, sticky=tk.NS)

        return panel

    def create_checkout_panel(self):
        panel = ttk.Frame(self)

        book_label = ttk.Label(panel, text="Book:")
        self.book_combobox = ttk.Combobox(panel, width=50)
        member_label = ttk.Label(panel, text="Member:")
        self.member_combobox = ttk.Combobox(panel, width=50)
        days_label = ttk.Label(panel, text="Days:")
        days_entry = ttk.Entry(panel, width=10)

        checkout_button = ttk.Button(panel, text="Checkout", width=20,
                                     command=lambda: self.checkout_book(days_entry.get()))
        return_button = ttk.Button(panel, text="Return", width=20, command=self.return_book)

        book_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.book_combobox.grid(row=0, column=1, padx=10, pady=5)
        member_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.member_combobox.grid(row=1, column=1, padx=10, pady=5)
        days_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        days_entry.grid(row=2, column=1, padx=10, pady=5)

        checkout_button.grid(row=3, column=0, padx=10, pady=5)
        return_button.grid(row=3, column=1, padx=10, pady=5)

        return panel

    def add_book(self, title_entry, author_entry, isbn_entry, genre_entry, year_entry, book_listbox):
        title = title_entry.get()
        author = author_entry.get()
        isbn = isbn_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()

        try:
            year = int(year)
        except ValueError:
            messagebox.showwarning("Input Error", "Year must be an integer.")
            return

        book = Book(title, author, isbn, genre, year)
        self.library.add_book(book)
        self.update_book_listbox(book_listbox)

    def update_book_listbox(self, listbox):
        listbox.delete(0, tk.END)
        for book in self.library.books:
            listbox.insert(tk.END, book.title)
        self.update_book_combobox()

    def update_book_combobox(self):
        self.book_combobox['values'] = [book.title for book in self.library.books]

    def add_member(self, name_entry, id_entry, contact_entry, member_listbox):
        name = name_entry.get()
        member_id = id_entry.get()
        contact = contact_entry.get()

        if not name or not member_id or not contact:
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return

        member = Member(name, member_id, contact)
        self.library.add_member(member)
        self.update_member_listbox(member_listbox)

    def update_member_listbox(self, listbox):
        listbox.delete(0, tk.END)
        for member in self.library.members:
            listbox.insert(tk.END, member.member_id)
        self.update_member_combobox()

    def update_member_listbox(self, listbox):
    listbox.delete(0, tk.END)
    for member in self.library.members:
        display_text = f"{member.name} ({member.member_id})"
        listbox.insert(tk.END, display_text)
    self.update_member_combobox()


    def update_member_combobox(self):
        self.member_combobox['values'] = [member.member_id for member in self.library.members]

    def checkout_book(self, days):
        try:
            days = int(days)
        except ValueError:
            messagebox.showwarning("Input Error", "Number of days must be an integer.")
            return

        book_title = self.book_combobox.get()
        member_id = self.member_combobox.get()

        if not book_title or not member_id:
            messagebox.showwarning("Input Error", "Book title and member ID must be selected.")
            return

        book = next((b for b in self.library.books if b.title == book_title), None)
        member = next((m for m in self.library.members if m.member_id == member_id), None)

        if not book or not member:
            messagebox.showwarning("Error", "Selected book or member not found.")
            return

        self.library.checkout_book(book, member, days)
        messagebox.showinfo("Success", "Book checked out successfully.")

    def return_book(self):
        book_title = self.book_combobox.get()
        member_id = self.member_combobox.get()

        if not book_title or not member_id:
            messagebox.showwarning("Input Error", "Book title and member ID must be selected.")
            return

        book = next((b for b in self.library.books if b.title == book_title), None)
        member = next((m for m in self.library.members if m.member_id == member_id), None)

        if not book or not member:
            messagebox.showwarning("Error", "Selected book or member not found.")
            return

        self.library.return_book(book, member)
        messagebox.showinfo("Success", "Book returned successfully.")

    def search_books(self, query, book_listbox):
        results = [book.title for book in self.library.books if query.lower() in book.title.lower()]
        book_listbox.delete(0, tk.END)
        for result in results:
            book_listbox.insert(tk.END, result)

    def search_members(self, query, member_listbox):
        results = [member.member_id for member in self.library.members if query.lower() in member.member_id.lower()]
        member_listbox.delete(0, tk.END)
        for result in results:
            member_listbox.insert(tk.END, result)

    def edit_book(self, book_listbox, title_entry, author_entry, isbn_entry, genre_entry, year_entry):
        selected_index = book_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No book selected.")
            return

        selected_title = book_listbox.get(selected_index)
        book = next((b for b in self.library.books if b.title == selected_title), None)

        if book:
            book.title = title_entry.get() or book.title
            book.author = author_entry.get() or book.author
            book.isbn = isbn_entry.get() or book.isbn
            book.genre = genre_entry.get() or book.genre
            book.year = int(year_entry.get()) if year_entry.get() else book.year
            self.update_book_listbox(book_listbox)

    def edit_member(self, member_listbox, name_entry, id_entry, contact_entry):
        selected_index = member_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No member selected.")
            return

        selected_id = member_listbox.get(selected_index)
        member = next((m for m in self.library.members if m.member_id == selected_id), None)

        if member:
            member.name = name_entry.get() or member.name
            member.member_id = id_entry.get() or member.member_id
            member.contact = contact_entry.get() or member.contact
            self.update_member_listbox(member_listbox)

    def delete_book(self, book_listbox):
        selected_index = book_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No book selected.")
            return

        selected_title = book_listbox.get(selected_index)
        book = next((b for b in self.library.books if b.title == selected_title), None)

        if book:
            self.library.delete_book(book)
            self.update_book_listbox(book_listbox)

    def delete_member(self, member_listbox):
        selected_index = member_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No member selected.")
            return

        selected_id = member_listbox.get(selected_index)
        member = next((m for m in self.library.members if m.member_id == selected_id), None)

        if member:
            self.library.delete_member(member)
            self.update_member_listbox(member_listbox)

    def load_data(self):
        try:
            with open('library_data.json', 'r') as file:
                data = json.load(file)
                for book_data in data.get('books', []):
                    book = Book(**book_data)
                    self.library.add_book(book)
                for member_data in data.get('members', []):
                    member = Member(**member_data)
                    self.library.add_member(member)
        except FileNotFoundError:
            pass  # No data file found, start with an empty library

    def save_data(self):
        data = {
            'books': [vars(book) for book in self.library.books],
            'members': [vars(member) for member in self.library.members]
        }
        with open('library_data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def on_closing(self):
        self.save_data()
        self.master.destroy()

def main():
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("800x600")
    app = MainGUI(master=root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
