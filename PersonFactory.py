# Read the data files and generate new instances of the Person class.

# get_person(year_born), read_files()

import pandas as pd

class PersonFactory:
    def __init__(self):
        self.birth_marriage_rate = None
        self.first_names = None
        self.last_names = None
        self.life_expectancy = None
        self.rank_to_prob = None
        

    def read_files(self):
        self.life_expectancy = pd.read_csv('life_expectancy.csv')
        self.first_name = pd.read_csv("first_names.csv")
        self.last_names = pd.read_csv("last_names.csv")
        self.rank_to_prob = pd.read_csv("rank_to_probability.csv")
        self.birth_marriage_rate = pd.read_csv("birth_and_marriage_rates.csv")
