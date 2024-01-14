
from defense import *
from wish_list import *
from set_rules_tab import *
class DefenseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Defense List App")
        self.master.geometry("1920x1080")  # Set the size to 1920x1080

        # Set the icon
        self.master.iconbitmap("favicon.ico")

        # Style configuration
        self.style = ttk.Style()

        self.style.configure("TFrame", background="#1E2A38")
        self.style.configure("TButton", background="#35475C", foreground="black", padding=(5, 2))
        self.style.configure("TLabel", background="#1E2A38", foreground="#FFFFFF", font=('Arial', 12))
        self.style.configure("TCombobox", background="#2D3C4F", foreground="white", fieldbackground="#2D3C4F",
                             selectbackground="#2D3C4F")

        # Kolor obramowania aplikacji
        self.master.configure(bg="#1E2A38")

        # Load defense data and wishlist by default from the local directory
        #self.defenses = DefenseList("data.xlsx")
        #self.wishlist = WishList("wish_list.xlsx")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.master)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Load Data")
        self.notebook.add(self.tab2, text="Set Rules")
        self.notebook.add(self.tab3, text="Generate Results")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Use fill and expand options

        # Tab 1 - Load Data
        self.label_tab1 = ttk.Label(self.tab1, text="Choose data.xlsx file:")
        self.label_tab1.grid(row=0, column=0, pady=10)

        self.file_var = tk.StringVar()
        self.file_var.set("data.xlsx")  # Default path
        self.file_entry = ttk.Entry(self.tab1, textvariable=self.file_var, state="readonly", width=30)
        self.file_entry.grid(row=0, column=1, pady=10)

        self.browse_button = ttk.Button(self.tab1, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, pady=10)

        self.load_data_button = ttk.Button(self.tab1, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=1, column=1, pady=10)

        # Display loaded data in a table
        self.defense_tree = ttk.Treeview(self.tab1, columns=('Surname', 'Name', 'Thesis', 'Degree', 'Form', 'Speciality',
                                                              'Promoter', 'Reviewer'))
        self.defense_tree.grid(row=2, column=0, columnspan=3, pady=10)
        self.defense_tree.heading('#0', text='ID')
        self.defense_tree.heading('Surname', text='Surname')
        self.defense_tree.heading('Name', text='Name')
        self.defense_tree.heading('Thesis', text='Thesis')
        self.defense_tree.heading('Degree', text='Degree')
        self.defense_tree.heading('Form', text='Form')
        self.defense_tree.heading('Speciality', text='Speciality')
        self.defense_tree.heading('Promoter', text='Promoter')
        self.defense_tree.heading('Reviewer', text='Reviewer')
        self.defense_tree['show'] = 'headings'

        # Add scrollbar
        scroll_y = ttk.Scrollbar(self.tab1, orient='vertical', command=self.defense_tree.yview)
        scroll_y.grid(row=2, column=3, sticky='ns')
        self.defense_tree.configure(yscrollcommand=scroll_y.set)

        # Set column widths
        for col in ('Surname', 'Name', 'Thesis', 'Degree', 'Form', 'Speciality', 'Promoter', 'Reviewer'):
            self.defense_tree.column(col, width=120, anchor='center')

        # Wishlist Section
        self.label_wishlist = ttk.Label(self.tab1, text="Choose wishlist.xlsx file:")
        self.label_wishlist.grid(row=3, column=0, pady=10)

        self.file_var_wishlist = tk.StringVar()
        self.file_var_wishlist.set("wishlist.xlsx")  # Default path
        self.file_entry_wishlist = ttk.Entry(self.tab1, textvariable=self.file_var_wishlist, state="readonly", width=30)
        self.file_entry_wishlist.grid(row=3, column=1, pady=10)

        self.browse_button_wishlist = ttk.Button(self.tab1, text="Browse", command=self.browse_file_wishlist)
        self.browse_button_wishlist.grid(row=3, column=2, pady=10)

        self.load_wishlist_button = ttk.Button(self.tab1, text="Load Wishlist", command=self.load_wishlist)
        self.load_wishlist_button.grid(row=4, column=1, pady=10)

        # Display loaded wishlist data in a table
        self.wishlist_tree = ttk.Treeview(self.tab1, columns=('Academic', 'Date', 'Start Time', 'End Time'))
        self.wishlist_tree.grid(row=5, column=0, columnspan=3, pady=10)
        self.wishlist_tree.heading('#0', text='ID')
        self.wishlist_tree.heading('Academic', text='Academic')
        self.wishlist_tree.heading('Date', text='Date')
        self.wishlist_tree.heading('Start Time', text='Start Time')
        self.wishlist_tree.heading('End Time', text='End Time')
        self.wishlist_tree['show'] = 'headings'

        # Add scrollbar for wishlist
        scroll_y_wishlist = ttk.Scrollbar(self.tab1, orient='vertical', command=self.wishlist_tree.yview)
        scroll_y_wishlist.grid(row=5, column=3, sticky='ns')
        self.wishlist_tree.configure(yscrollcommand=scroll_y_wishlist.set)

        # Set column widths for wishlist
        for col in ('Academic','Date', 'Start Time', 'End Time'):
            self.wishlist_tree.column(col, width=120, anchor='center')

        # Configure grid weights and minsize for the tabs
        self.tab1.columnconfigure(0, weight=1, minsize=200)
        self.tab1.rowconfigure(6, weight=1, minsize=50)
        self.tab2.columnconfigure(0, weight=1, minsize=200)
        self.tab2.rowconfigure(2, weight=1, minsize=50)
        self.tab3.columnconfigure(0, weight=1, minsize=200)
        self.tab3.rowconfigure(2, weight=1, minsize=50)
        # Tab 2 - Set Rules
        self.set_rules_tab = SetRulesTab(self.tab2, SlotsList("slots.xlsx"))
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.file_var.set(file_path)

    def load_data(self):
        if not self.file_var.get():
            messagebox.showerror("Error", "Please choose a data.xlsx file.")
            return

        self.defenses = DefenseList(self.file_var.get())
        self.populate_defense_tree()

    def browse_file_wishlist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.file_var_wishlist.set(file_path)

    def load_wishlist(self):
        if not self.file_var_wishlist.get():
            messagebox.showerror("Error", "Please choose a wishlist.xlsx file.")
            return

        self.wishlist = WishList(self.file_var_wishlist.get())
        self.populate_wishlist_tree()

    def populate_defense_tree(self):
        for item in self.defense_tree.get_children():
            self.defense_tree.delete(item)

        for i, defense in enumerate(self.defenses.defense_list, 1):
            self.defense_tree.insert("", 'end', values=(i, defense.surname, defense.name, defense.thesis,
                                                        defense.degree, defense.form, defense.speciality,
                                                        defense.promoter.name, defense.reviewer.name))

    def populate_wishlist_tree(self):
        for item in self.wishlist_tree.get_children():
            self.wishlist_tree.delete(item)

        for i, wish in enumerate(self.wishlist.wishlist, 1):
            self.wishlist_tree.insert("", 'end', values=(wish.academic.name, wish.date, wish.start_hour, wish.end_hour))
