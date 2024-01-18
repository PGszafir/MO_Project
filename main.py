# from defense_app import *
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = DefenseApp(root)
#     root.mainloop()
from defense import *
from wish_list import *

def main():
    defenses = DefenseList('data.xlsx')
    slots = SlotsList('slots.xlsx')
    wishlist = WishList('wish_list.xlsx')

    print("Wish list width:", len(wishlist.wishlist))
    print("Slots list width:", len(slots.slots))
    print("Defenses list width:", len(defenses.defense_list))

    while True:
        population_size = int(input("Enter the population size(10): "))
        iterations = int(input("Enter the number of iterations(50): "))

        population = Population(population_size, slots, defenses, wishlist)
        best_pop = population.evolutionary_method(iterations)

        best_pop.print_conflicts()

        to_save = input("Would you like to save? (y/n/exit): ")
        if to_save.lower() == 'y':
            best_pop.save_to_xlsx('results.xlsx')
            print("Results saved to 'results.xlsx'")
        elif to_save.lower() == 'exit':
            break
        else:
            print("Continuing to the next iteration...\n")

if __name__ == "__main__":
    main()
