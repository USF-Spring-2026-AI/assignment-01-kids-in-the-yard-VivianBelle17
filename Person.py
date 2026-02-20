class Person:

    def __init__(self, year_born, first_name, last_name, year_died):
        self.__year_born = year_born
        self.__first_name = first_name
        self.__last_name = last_name
        self.__year_died = year_died

        self.__partner = None
        self.__children = []

    def set_partner(self, partner):
        self.__partner = partner

    def add_child(self, child):
        self.__children.append(child)

    def get_birth_year(self):
        return self.__year_born
    
    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def get_partner(self):
        return self.__partner
    
    def get_children(self):
        return list(self.__children)
    
    def get_year_died(self):
        return self.__year_died
