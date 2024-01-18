import random
import pandas as pd
from datetime import datetime, timedelta
import openpyxl
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
    def __init__(self, date, hour, duration, chairman, hall_no = 1):
        self.date = date
        self.hour = hour
        self.duration = duration
        self.chairman = chairman
        self.hall = hall_no

class DefenseTerm():
    def __init__(self, defense, slot):
        self.defense = defense
        self.slot = slot

    def return_academics(self):
        return [self.slot.chairman, self.defense.promoter, self.defense.reviewer]

    def is_academic_in_defense(self, academic):
        return academic in self.return_academics()

    def check_academics_collisions(self, other):
        collisions = 0
        for i in other.return_academics():
            if self.is_academic_in_defense(i):
                collisions += 1
        return collisions

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

    def save_to_xlsx(self, filename):
        # Create a DataFrame with the information about defenses
        data = {
            'Surname': [term.defense.surname for term in self.defenses_terms],
            'Name': [term.defense.name for term in self.defenses_terms],
            'Date': [term.slot.date for term in self.defenses_terms],
            'Hour': [term.slot.hour for term in self.defenses_terms],
            'Chairman': [term.slot.chairman for term in self.defenses_terms],
            'Promoter': [term.defense.promoter.name for term in self.defenses_terms],
            'Reviewer': [term.defense.reviewer.name for term in self.defenses_terms]
        }
        df = pd.DataFrame(data)

        # Sort the DataFrame by 'Date' and 'Hour'
        df['Hour'] = pd.to_datetime(df['Hour'], format='%H:%M:%S').dt.time
        df = df.sort_values(by=['Date', 'Hour']).reset_index(drop=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.to_excel(filename, index=False)

    def mix_value(self): # todo: implement
        mix_value = 0
        # distances = []
        #
        # for term in self.defenses_terms:
        #     if term.defense.promoter is not None:
        #         mix_value += term.defense.promoter.coefficient * term.defense.promoter.factor
        #     if term.defense.reviewer is not None:
        #         mix_value += term.defense.reviewer.coefficient * term.defense.reviewer.factor
        # for i in range(1, len(self.defenses_terms)):
        #     distances.append(abs(i - (i - 1)))
        # mix_value += sum(distances)

        return mix_value

    def correction_score(self):
        points = 0

        for term in self.defenses_terms:
            # Sprawdzenie czy przewodniczący nie zajmuje innej pozycji
            if term.slot.chairman == term.defense.promoter or term.slot.chairman == term.defense.reviewer:
                points -= 1  # Minus za złe przypisanie przewodniczącego
            else:
                points += 1  # Plus za poprawne przypisanie przewodniczącego

            hall_colisions = -1
            person_colisions = -1
            for i in range(len(self.defenses_terms)):
                if term.slot.date == self.defenses_terms[i].slot.date:
                    if term.slot.hour == self.defenses_terms[i].slot.hour:
                        if term.slot.hall == self.defenses_terms[i].slot.hall:
                            hall_colisions += 1
                        person_colisions += term.check_academics_collisions(self.defenses_terms[i])

            # Sprawdzanie kolidujących obron i przyznawanie punktów
            points -= hall_colisions  # Minus za kolidujące sale
            points -= person_colisions  # Minus za kolidujące osoby

        return points

    def wishes_score(self, wish_list):
        conflicts = 0
        for i in self.defenses_terms:
            conflicts += wish_list.count_conflicts(i.slot.tate,i.slot.hour,i.slot.hour+i.duration)

    def fitness(self, wish_list):
        value = 0
        value += self.mix_value()
        value += self.correction_score()
        return value


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
                date, start_time, duration,chairman, hall_no = row[:5]
                slot = Slot(date, start_time, duration, chairman, hall_no)
                slots.append(slot)

        except Exception as e:
            print(f"Error loading slots from file: {e}")

        return slots

class WishList():
    def __init__(self, filename):
        self.wishlist = self.load_from_file(filename)

    def __getitem__(self, index):
        return self.wishlist[index]

    def load_from_file(self, filename):
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active

        wishlist = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            academic_name, date, start_time, end_time = row[:4]

            # Create Academic object
            academic = Academic(academic_name)

            # Create Wish object and add it to the wishlist
            wish = Wish(academic, date, start_time, end_time)
            wishlist.append(wish)

        return wishlist

    def count_conflicts(self,date, start_time, end_time):
        counter = 0
        for i in self.wishlist:
            if i.check_availability(date, start_time, end_time):
                counter += 1

        return counter


class Wish():
    def __init__(self, academic, date, start_hour, end_hour):
        self.academic = academic
        self.date = date
        self.start_hour = start_hour
        self.end_hour = end_hour

    def check_availability(self, wish_date, wish_start_time, wish_end_time):
        # Convert wish and stored start/end times to datetime objects
        start_datetime_str = f"{self.date} {self.start_hour}"
        end_datetime_str = f"{self.date} {self.end_hour}"
        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")

        wish_start_datetime = datetime.strptime(f"{wish_date} {wish_start_time}", "%Y-%m-%d %H:%M")
        wish_end_datetime = datetime.strptime(f"{wish_date} {wish_end_time}", "%Y-%m-%d %H:%M")

        # Check if the wish is available
        if (start_datetime is None or end_datetime is None or
                not (start_datetime <= wish_start_datetime <= end_datetime) or
                not (wish_end_datetime <= start_datetime or wish_start_datetime >= end_datetime)):
            return False  # The wish is available
        else:
            return True  # The wish is not available

class Academic():
    def __init__(self, name):
        self.name = name


import random

import random


class Population():
    def __init__(self, pop_size, slots, defenses,wish_list):
        self.defense_terms_pop = [DefensesTermsList(self.generate_random_sequence(slots, defenses)) for _ in
                                  range(pop_size)]
        self.slots = slots
        self.wish_list = wish_list
    def generate_random_sequence(self, slots, defenses):
        return [DefenseTerm(random.choice(defenses.defense_list), random.choice(slots.slots)) for _ in
                range(min(len(defenses.defense_list), len(slots.slots)))]

    def mutate(self, defense_terms_list, slots):
        mutated_sequence = defense_terms_list.copy()
        index1, index2 = random.sample(range(len(mutated_sequence)), 2)

        # Swap slots in the mutated sequence
        mutated_sequence[index1].slot = random.choice(slots.slots)
        mutated_sequence[index2].slot = random.choice(slots.slots)

        return mutated_sequence

    def cross(self, parent1, parent2, slots):
        crossover_point = random.randint(1, len(parent1.defenses_terms) - 1)
        child1 = DefensesTermsList(parent1.defenses_terms[:crossover_point] + parent2.defenses_terms[crossover_point:])
        child2 = DefensesTermsList(parent2.defenses_terms[:crossover_point] + parent1.defenses_terms[crossover_point:])

        # Swap slots in the crossover children
        for i in range(len(child1.defenses_terms)):
            child1.defenses_terms[i].slot = random.choice(slots.slots)
            child2.defenses_terms[i].slot = random.choice(slots.slots)

        return child1, child2

    def calculate_fitness(self):
        fitness = [self.defense_terms_pop[i].fitness(self.wish_list) for i in range(len(self.defense_terms_pop))]
        return fitness

    def evolutionary_method(self, generations):
        for generation in range(generations):
            # Calculate fitness for the current population
            fitness_scores = self.calculate_fitness()

            # Find the index of the best-rated individual
            best_index = fitness_scores.index(max(fitness_scores))

            # Create a copy of the best individual to preserve it
            best_individual = self.defense_terms_pop[best_index]

            # Print the progress of the current generation
            print(f"Generation {generation + 1}: Best Fitness = {max(fitness_scores)}", " population size",
                  len(self.defense_terms_pop))

            # Generate a new population through mutation and crossover
            new_population = [best_individual]
            for _ in range(len(self.defense_terms_pop) - 1):
                if random.random() < 0.5:
                    # Mutate
                    mutated_individual = self.mutate(best_individual.defenses_terms, self.slots)
                    new_population.append(DefensesTermsList(mutated_individual))
                else:
                    # Crossover
                    parent1 = random.choice(self.defense_terms_pop)
                    parent2 = random.choice(self.defense_terms_pop)
                    child1, child2 = self.cross(parent1, parent2, self.slots)
                    new_population.extend([child1, child2])

            # Trim the new population to maintain the original population size
            new_population = new_population[:len(self.defense_terms_pop)]

            # Update the population with the new one
            self.defense_terms_pop = new_population

        # Return the best-rated population
        best_individual = self.defense_terms_pop[best_index]
        print(f"Evolution finished. Best Fitness = {best_individual.fitness(self.wish_list)}")
        return best_individual


