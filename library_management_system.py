import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta


class Book:
    def __init__(self, title, author, isbn, genre, publication_year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.publication_year = publication_year
        self.is_checked_out = False
        self.checked_out_to = None
        self.checkout_date = None
        self.due_date = None

    def check_out(self, member, checkout_date, due_date):
        self.is_checked_out = True
        self.checked_out_to = member
        self.checkout_date = checkout_date
        self.due_date = due_date

    def return_book(self):
        self.is_checked_out = False
        self.checked_out_to = None
        self.checkout_date = None
        self.due_date = None

    def is_overdue(self):
        return self.is_checked_out and date.today() > self.due_date

    def __str__(self):
        return f"{self.title} by {self.author}"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

    def __hash__(self):
        return hash(self.isbn)


class Member:
    def __init__(self, name, id, contact):
        self.name = name
        self.id = id
        self.contact = contact

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def __eq__(self, other):
        if isinstance(other, Member):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def search_books(self, query):
        return [book for book in self.books if query.lower() in book.title.lower() or
                query.lower() in book.author.lower() or
                query.lower() in book.isbn.lower() or
                query.lower() in book.genre.lower()]

    def get_books(self):
        return self.books.copy()

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def search_members(self, query):
        return [member for member in self.members if query.lower() in member.name.lower() or
                query.lower() in member.id.lower()]

    def get_members(self):
        return self.members.copy()

    def checkout_book(self, book, member, loan_days):
        if not book.is_checked_out:
            checkout_date = date.today()
            due_date = checkout_date + timedelta(days=loan_days)
            book.check_out(member, checkout_date, due_date)
        else:
            raise ValueError("Book is already checked out.")

    def return_book(self, book):
        if book.is_checked_out:
            book.return_book()
        else:
            raise ValueError("Book is not checked out.")

    def get_overdue_books(self):
        return [book for book in self.books if book.is_overdue()]

    def get_books_checked_out_by_member(self, member):
        return [book for book in self.books if book.is_checked_out and book.checked_out_to == member]


class MainGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.library = Library()
        self.member_combobox = None
        self.book_combobox = None
        self.init_components()

    def init_components(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill=tk.BOTH, expand=True)

        book_panel = self.create_book_panel()
        member_panel = self.create_member_panel()
        checkout_panel = self.create_checkout_panel()

        notebook.add(book_panel, text="Book Management")
        notebook.add(member_panel, text="Member Management")
        notebook.add(checkout_panel, text="Checkout/Return")

    def create_book_panel(self):
        panel = ttk.Frame(self.master)

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

        for button in [add_button, edit_button, delete_button, search_button]:
            button.configure(takefocus=False)

        title_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        author_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        isbn_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        isbn_entry.grid(row=2, column=1, padx=5, pady=5)
        genre_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        genre_entry.grid(row=3, column=1, padx=5, pady=5)
        year_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        year_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        edit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        delete_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        search_entry.grid(row=8, column=0, padx=5, pady=5)
        search_button.grid(row=8, column=1, padx=5, pady=5)

        book_listbox.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=9, column=2, sticky="ns", padx=5, pady=5)

        panel.columnconfigure(1, weight=1)
        panel.rowconfigure(9, weight=1)

        return panel

    def add_book(self, title_entry, author_entry, isbn_entry, genre_entry, year_entry, listbox):
        try:
            title = title_entry.get()
            author = author_entry.get()
            isbn = isbn_entry.get()
            genre = genre_entry.get()
            year = int(year_entry.get())

            new_book = Book(title, author, isbn, genre, year)
            self.library.add_book(new_book)
            listbox.insert(tk.END, str(new_book))

            title_entry.delete(0, tk.END)
            author_entry.delete(0, tk.END)
            isbn_entry.delete(0, tk.END)
            genre_entry.delete(0, tk.END)
            year_entry.delete(0, tk.END)

            self.update_book_combobox()
        except ValueError:
            messagebox.showerror("Error", "Invalid year format")

    def edit_book(self, listbox, title_entry, author_entry, isbn_entry, genre_entry, year_entry):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            book = self.library.books[index]
            try:
                book.title = title_entry.get()
                book.author = author_entry.get()
                book.isbn = isbn_entry.get()
                book.genre = genre_entry.get()
                book.publication_year = int(year_entry.get())

                listbox.delete(index)
                listbox.insert(index, str(book))
            except ValueError:
                messagebox.showerror("Error", "Invalid year format")
        else:
            messagebox.showerror("Error", "Please select a book to edit.")

    def delete_book(self, listbox):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            book = self.library.books[index]
            self.library.remove_book(book)
            listbox.delete(index)
            self.update_book_combobox()
        else:
            messagebox.showerror("Error", "Please select a book to delete")

    def search_books(self, query, listbox):
        listbox.delete(0, tk.END)
        search_results = self.library.search_books(query)
        for book in search_results:
            listbox.insert(tk.END, str(book))

    def create_member_panel(self):
        panel = ttk.Frame(self.master)

        name_label = ttk.Label(panel, text="Name:")
        name_entry = ttk.Entry(panel, width=50)
        id_label = ttk.Label(panel, text="Member ID:")
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

        for button in [add_button, edit_button, delete_button, search_button]:
            button.configure(takefocus=False)

        name_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        id_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        id_entry.grid(row=1, column=1, padx=5, pady=5)
        contact_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        contact_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        edit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        search_entry.grid(row=6, column=0, padx=5, pady=5)
        search_button.grid(row=6, column=1, padx=5, pady=5)

        member_listbox.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(row=7, column=2, sticky="ns", padx=5, pady=5)

        panel.columnconfigure(1, weight=1)
        panel.rowconfigure(7, weight=1)

        return panel

    def add_member(self, name_entry, id_entry, contact_entry, listbox):
        name = name_entry.get()
        id = id_entry.get()
        contact = contact_entry.get()

        if name and id:
            new_member = Member(name, id, contact)
            self.library.add_member(new_member)
            listbox.insert(tk.END, str(new_member))

            name_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)
            contact_entry.delete(0, tk.END)

            self.update_member_combobox()
        else:
            messagebox.showerror("Error", "Name and Member ID are required")

    def edit_member(self, listbox, name_entry, id_entry, contact_entry):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            member = self.library.members[index]
            member.name = name_entry.get()
            member.id = id_entry.get()
            member.contact = contact_entry.get()

            listbox.delete(index)
            listbox.insert(index, str(member))
        else:
            messagebox.showerror("Error", "Please select a member to edit.")

    def delete_member(self, listbox):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            member = self.library.members[index]
            self.library.remove_member(member)
            listbox.delete(index)
            self.update_member_combobox()
        else:
            messagebox.showerror("Error", "Please select a member to delete")

    def search_members(self, query, listbox):
        listbox.delete(0, tk.END)
        search_results = self.library.search_members(query)
        for member in search_results:
            listbox.insert(tk.END, str(member))

    def create_checkout_panel(self):
        panel = ttk.Frame(self.master)

        member_label = ttk.Label(panel, text="Member:")
        self.member_combobox = ttk.Combobox(panel, width=50)
        book_label = ttk.Label(panel, text="Book:")
        self.book_combobox = ttk.Combobox(panel, width=50)

        checkout_button = ttk.Button(panel, text="Checkout", width=20,
                                     command=lambda: self.checkout_book(self.member_combobox, self.book_combobox,
                                                                        status_text))
        return_button = ttk.Button(panel, text="Return", width=20,
                                   command=lambda: self.return_book(self.book_combobox, status_text))
        overdue_button = ttk.Button(panel, text="Check Overdue Books",
                                    command=lambda: self.check_overdue_books(status_text))

        status_text = tk.Text(panel, height=10, width=60)
        status_text.config(state=tk.DISABLED)

        member_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.member_combobox.grid(row=0, column=1, padx=5, pady=5)
        book_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.book_combobox.grid(row=1, column=1, padx=5, pady=5)

        checkout_button.grid(row=2, column=0, padx=5, pady=5)
        return_button.grid(row=2, column=1, padx=5, pady=5)
        overdue_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        status_text.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        panel.columnconfigure(1, weight=1)
        panel.rowconfigure(4, weight=1)

        self.update_member_combobox()
        self.update_book_combobox()

        return panel

    def update_member_combobox(self):
        self.member_combobox['values'] = [str(member) for member in self.library.get_members()]

    def update_book_combobox(self):
        self.book_combobox['values'] = [str(book) for book in self.library.get_books() if not book.is_checked_out]

    def checkout_book(self, member_combobox, book_combobox, status_text):
        member = self.library.members[member_combobox.current()]
        book = self.library.books[book_combobox.current()]

        try:
            self.library.checkout_book(book, member, 14)
            self.update_status(status_text, f"Book checked out successfully: {book} to {member}")
            self.update_book_combobox()
        except ValueError as e:
            self.update_status(status_text, f"Error: {str(e)}")

    def return_book(self, book_combobox, status_text):
        book = self.library.books[book_combobox.current()]

        try:
            self.library.return_book(book)
            self.update_status(status_text, f"Book returned successfully: {book}")
            self.update_book_combobox()
        except ValueError as e:
            self.update_status(status_text, f"Error: {str(e)}")

    def check_overdue_books(self, status_text):
        overdue_books = self.library.get_overdue_books()
        if overdue_books:
            self.update_status(status_text, "Overdue books:")
            for book in overdue_books:
                self.update_status(status_text, f"{book} - Due date: {book.due_date}")
        else:
            self.update_status(status_text, "No overdue books.")

    def update_status(self, status_text, message):
        status_text.config(state=tk.NORMAL)
        status_text.insert(tk.END, message + "\n")
        status_text.config(state=tk.DISABLED)
        status_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library Management System")
    app = MainGUI(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.geometry("1000x800")
    root.mainloop()
