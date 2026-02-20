class Person:

    def __init__(self, year_born, first_name, last_name, year_died):
        self.year_born = year_born
        self.first_name = first_name
        self.last_name = last_name
        self.year_died = year_died

        self.partner = None
        self.children = []