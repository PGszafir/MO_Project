import openpyxl
import random
from datetime import datetime, timedelta

class Defense():
    def __init__(self, surname, name, thesis, degree, form, speciality, promoter, reviewer):
        self.surname = surname
        self.name = name
        self.thesis = thesis
        self.degree = degree
        self.form = form
        self.speciality = speciality
        self.promoter = promoter  # Academic class instance
        self.reviewer = reviewer  # Academic class instance

class Slot():
    def __init__(self, date, hour, duration):
        self.date = date
        self.hour = hour
        self.duration = duration

class DefenseTerm():
    def __init__(self, defense, slot, chairman):
        self.defense = defense
        self.slot = slot
        self.chairman = chairman

class DefenseList():
    def __init__(self, filename):
        self.academics, self.defense_list = self.load_defenses_from_file(filename)

    def __getitem__(self, index):
        return self.defense_list[index]

    def load_defenses_from_file(self, filename):
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active

        # Extract list of academics
        academics_set = set()
        for row in sheet.iter_rows(min_row=2, values_only=True):
            academics_set.add(str(row[6]).strip().lower())
            academics_set.add(str(row[7]).strip().lower())

        academics_list = [Academic(academic_name) for academic_name in academics_set]

        # Create list of defenses
        defense_list = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            surname, name, thesis, degree, form, speciality, promoter_name, reviewer_name = map(
                lambda x: str(x).strip(), row[:8])

            promoter = next((academic for academic in academics_list if academic.name.lower() == promoter_name.lower()),
                            None)
            reviewer = next((academic for academic in academics_list if academic.name.lower() == reviewer_name.lower()),
                            None)

            if promoter is None:
                print(f"Promoter not found for {surname}, {name}.")
            if reviewer is None:
                print(f"Reviewer not found for {surname}, {name}.")

            defense = Defense(surname, name, thesis, degree, form, speciality, promoter, reviewer)
            defense_list.append(defense)

        return academics_list, defense_list


class DefensesTermsList():
    def __init__(self, defenses_terms):
        self.defenses_terms = defenses_terms

    def print_list(self):
        for term in self.defenses_terms:
            print(
                f"{term.defense.surname} {term.defense.name} - Date: {term.date}, Hour: {term.hour}, Chairman: {term.chairman}")
        # Add more attributes as needed

    def save_to_xlsx(self, filename):
        # Implement saving to Excel
        pass

from datetime import timedelta, datetime
import openpyxl

class Slot:
    def __init__(self, date, start_time, duration):
        self.date = date
        self.start_time = start_time
        self.duration = duration

class SlotsList:
    def __init__(self, filename):
        self.filename = filename
        self.slots = self.load_data_from_file()
        self.slot_duration = timedelta(minutes=30)

    def load_data_from_file(self):
        slots = []
        try:
            workbook = openpyxl.load_workbook(self.filename)
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                date, start_time, duration = row[:3]
                slot = Slot(date, start_time, duration)
                slots.append(slot)

        except Exception as e:
            print(f"Error loading data from file: {e}")

        return slots

    def save_data_to_file(self):
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(['Date', 'Start Time', 'Duration'])

            for slot in self.slots:
                sheet.append([slot.date, slot.start_time, slot.duration])

            workbook.save(self.filename)

        except Exception as e:
            print(f"Error saving data to file: {e}")

    def set_start_h(self, start_hour):
        for slot in self.slots:
            slot.start_time = f"{start_hour:02}:00:00"

    def set_end_h(self, end_hour):
        for slot in self.slots:
            end_time = datetime.strptime(slot.start_time, "%H:%M:%S") + timedelta(hours=end_hour)
            slot.start_time = end_time.strftime("%H:%M:%S")

    def set_slot_duration(self, duration_minutes):
        self.slot_duration = timedelta(minutes=duration_minutes)

    def set_break(self, start_hour, duration_minutes):
        break_slot = Slot("", f"{start_hour:02}:00:00", timedelta(minutes=duration_minutes))
        self.slots.append(break_slot)

    def generate_new_slots(self, start_hour, end_hour, pause=False):
        new_slots = []
        for slot in self.slots:
            current_time = datetime.strptime(slot.start_time, "%H:%M:%S")
            while current_time.hour < end_hour:
                new_slots.append(Slot(slot.date, current_time.strftime("%H:%M:%S"), self.slot_duration))
                current_time += self.slot_duration
        self.slots = new_slots

class Academic():
    def __init__(self, name):
        self.name = name


class Population():
    def __init__(self, pop_size, defense_terms_list):
        self.defense_terms_pop = [DefensesTermsList(self.generate_random_sequence(defense_terms_list)) for _ in
                                  range(pop_size)]

    def generate_random_sequence(self, defense_terms_list):
        return random.sample(defense_terms_list, len(defense_terms_list))

    def mutate(self, defense_terms_list):
        mutated_sequence = defense_terms_list.copy()
        index1, index2 = random.sample(range(len(mutated_sequence)), 2)
        mutated_sequence[index1], mutated_sequence[index2] = mutated_sequence[index2], mutated_sequence[index1]
        return mutated_sequence

    def cross(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1.defenses_terms) - 1)
        child1 = DefensesTermsList(parent1.defenses_terms[:crossover_point] + parent2.defenses_terms[crossover_point:])
        child2 = DefensesTermsList(parent2.defenses_terms[:crossover_point] + parent1.defenses_terms[crossover_point:])
        return child1, child2

