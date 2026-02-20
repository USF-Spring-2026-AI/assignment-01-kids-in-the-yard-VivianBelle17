# Read the data files and generate new instances of the Person class.

# get_person(year_born), read_files()

import pandas as pd
import random as rand

class PersonFactory:
    def __init__(self):
        self.birth_marriage_rate = None
        self.first_names = None
        self.last_names = None
        self.life_expectancy = None
        self.rank_to_prob = None
        

    def read_files(self):
        self.life_expectancy = pd.read_csv('life_expectancy.csv')
        self.first_names = pd.read_csv("first_names.csv")
        self.last_names = pd.read_csv("last_names.csv")
        self.rank_to_prob = pd.read_csv("rank_to_probability.csv")
        self.birth_marriage_rate = pd.read_csv("birth_and_marriage_rates.csv")

    def generate_year_died(self, year_born):
        length = rand.randint(-10, 10)

        index = self.life_expectancy["Year"] == year_born

        # Returns the whole row so you need to get the value at the str column
        life_expec = self.life_expectancy[index]["Period life expectancy at birth"].values[0]
        
        year_died = int(life_expec) + length + year_born

        return year_died
    
    def choose_gender(self):
        return rand.choice(['female', 'male'])
    

    def choose_first_name(self, year_born, gender):
        decade = (year_born // 10) * 10

        # From the csv file, get the matching decade and gender
        data = self.first_names[
            (self.first_names['decade'] == decade) &
            (self.first_names['gender'] == gender)
        ]

        # Get 1 random row based on the frequency column of the data
        name_row = data.sample(n=1, weights='frequency')

        # Return the first value from the name column of that row
        return name_row['name'].values[0]
        

    def choose_last_name(self):
        pass

    def create_person(self, year_born):
        gender = self.choose_gender()
        first_name = self.choose_first_name(year_born, gender)
        last_name = self.choose_last_name()

        year_died = self.generate_year_died(year_born)

        return Person(year_born, first_name, last_name, year_died)



