from wish_list import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
class SetRulesTab:
    def __init__(self, tab, slots_list):
        self.tab = tab
        self.slots_list = slots_list

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



    def load_slots(self):
        # Clear previous data
        for item in self.slots_tree.get_children():
            self.slots_tree.delete(item)

        # Populate Treeview with slots data
        for i, slot in enumerate(self.slots_list.slots, 1):
            self.slots_tree.insert("", 'end', values=(slot.date, slot.start_time, slot.duration))

    def add_slot(self):
        start_hour = int(self.start_hour_entry.get())
        end_hour = int(self.end_hour_entry.get())
        duration = int(self.duration_entry.get())
        self.slots_list.set_start_h(start_hour)
        self.slots_list.set_end_h(end_hour)
        self.slots_list.set_slot_duration(duration)
        self.slots_list.save_data_to_file()
        self.load_slots()

    def remove_slot(self):
        selected_item = self.slots_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a slot to remove.")
            return

        item_id = int(self.slots_tree.item(selected_item)['text'])
        del self.slots_list.slots[item_id - 1]
        self.slots_list.save_data_to_file()
        self.load_slots()