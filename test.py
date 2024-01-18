import unittest
from defense import Defense, Slot, DefenseTerm, DefensesTermsList


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Przygotowanie danych testowych
        self.promoter = Defense("PromoterSurname", "PromoterName", "Thesis1", "PhD", "Full-time", "Speciality1", None,
                                None)
        self.reviewer = Defense("ReviewerSurname", "ReviewerName", "Thesis2", "PhD", "Part-time", "Speciality2", None,
                                None)

        self.slot1 = Slot(date="2022-01-18", hour="10:00", duration=30)
        self.slot2 = Slot(date="2022-01-18", hour="11:00", duration=30)

        self.defense1 = DefenseTerm(self.promoter, self.slot1, chairman="Chairman1", hall_no=1)
        self.defense2 = DefenseTerm(self.reviewer, self.slot2, chairman="Chairman2", hall_no=2)

    def test_mix_value(self):
        # Tworzenie instancji klasy DefensesTermsList
        defenses_list = DefensesTermsList([self.defense1, self.defense2])

        # Wywołanie funkcji mix_value
        result = defenses_list.mix_value()

        # Sprawdzenie, czy wynik jest zgodny z oczekiwaniami
        self.assertEqual(result, 0)  # Pamiętaj, aby dostosować wartość oczekiwaną do rzeczywistych danych

    def test_correction_score(self):
        # Tworzenie instancji klasy DefensesTermsList
        defenses_list = DefensesTermsList([self.defense1, self.defense2])

        # Wywołanie funkcji correction_score
        result = defenses_list.correction_score()

        # Sprawdzenie, czy wynik jest zgodny z oczekiwaniami
        self.assertEqual(result, 2)  # Pamiętaj, aby dostosować wartość oczekiwaną do rzeczywistych danych


if __name__ == '__main__':
    unittest.main()
