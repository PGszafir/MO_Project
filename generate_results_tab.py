from tkinter import ttk
from tkinter import filedialog, messagebox
from defense import SlotsList, Academic, DefensesTermsList
from defense import Population

class GenerateResultsTab:
    def __init__(self, tab, defense_terms_list):
        self.tab = tab
        self.defense_terms_list = defense_terms_list

        # Load slots data
        self.load_slots_button = ttk.Button(self.tab, text="Load Slots", command=self.load_slots)
        self.load_slots_button.grid(row=0, column=0, pady=10)

        # Display loaded slots data in a table
        self.slots_tree = ttk.Treeview(self.tab, columns=('Date', 'Start Time', 'Duration'))
        self.slots_tree.grid(row=1, column=0, columnspan=3, pady=10)
        self.slots_tree.heading('#0', text='ID')
        self.slots_tree.heading('Date', text='Date')
        self.slots_tree.heading('Start Time', text='Start Time')
        self.slots_tree.heading('Duration', text='Duration')
        self.slots_tree['show'] = 'headings'

        # Add scrollbar for slots
        scroll_y_slots = ttk.Scrollbar(self.tab, orient='vertical', command=self.slots_tree.yview)
        scroll_y_slots.grid(row=1, column=3, sticky='ns')
        self.slots_tree.configure(yscrollcommand=scroll_y_slots.set)

        # Set column widths for slots
        for col in ('Date', 'Start Time', 'Duration'):
            self.slots_tree.column(col, width=120, anchor='center')

        # Button to generate and display populations
        self.generate_populations_button = ttk.Button(self.tab, text="Generate Populations", command=self.generate_populations)
        self.generate_populations_button.grid(row=2, column=0, pady=10)

        # Display generated populations in a table
        self.populations_tree = ttk.Treeview(self.tab, columns=('Population', 'Fitness'))
        self.populations_tree.grid(row=3, column=0, columnspan=3, pady=10)
        self.populations_tree.heading('#0', text='ID')
        self.populations_tree.heading('Population', text='Population')
        self.populations_tree.heading('Fitness', text='Fitness')
        self.populations_tree['show'] = 'headings'

        # Add scrollbar for populations
        scroll_y_populations = ttk.Scrollbar(self.tab, orient='vertical', command=self.populations_tree.yview)
        scroll_y_populations.grid(row=3, column=3, sticky='ns')
        self.populations_tree.configure(yscrollcommand=scroll_y_populations.set)

        # Set column widths for populations
        for col in ('Population', 'Fitness'):
            self.populations_tree.column(col, width=120, anchor='center')

    def load_slots(self):
        # Clear previous data
        for item in self.slots_tree.get_children():
            self.slots_tree.delete(item)

        # Populate Treeview with slots data
        for i, slot in enumerate(self.defense_terms_list.defenses_terms, 1):
            self.slots_tree.insert("", 'end', values=(slot.slot.date, slot.slot.start_time, slot.slot.duration))

    def generate_populations(self):
        # Clear previous data
        for item in self.populations_tree.get_children():
            self.populations_tree.delete(item)

        # Get the number of populations to generate
        num_populations = int(input("Enter the number of populations to generate: "))

        # Generate and display populations
        for i in range(num_populations):
            population = Population(pop_size=10, defense_terms_list=self.defense_terms_list.defenses_terms)
            fitness = self.calculate_fitness(population)
            self.populations_tree.insert("", 'end', values=(f"Population {i+1}", fitness))

    def calculate_fitness(self, population):

        return
