# from defense_app import *
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = DefenseApp(root)
#     root.mainloop()

from defense import *
from wish_list import *
defenses = DefenseList('data.xlsx')
slots = SlotsList('slots.xlsx')
wishlist = WishList('wish_list.xlsx')

print("Wish list width: ", len(wishlist.wishlist))
print("slots list width: ", len(slots.slots))
print("Defenses list width: ", len(defenses.defense_list))


population = Population(3000,slots, defenses,wishlist)
best_pop = population.evolutionary_method(1)
best_pop.save_to_xlsx('results.xlsx')