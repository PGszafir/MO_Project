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

population = Population(100,slots, defenses,wishlist)

best_pop = population.evolutionary_method(100)

best_pop.save_to_xlsx('results.xlsx')

