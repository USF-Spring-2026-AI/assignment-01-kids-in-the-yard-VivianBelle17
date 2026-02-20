import math
import pandas as pd
import random as rand

from Person import Person

class PersonFactory:
    def __init__(self):
        self.birth_marriage_rate = None
        self.first_names = None
        self.last_names = None
        self.life_expectancy = None
        self.rank_to_prob = None
        

    def read_files(self):

        print("Reading files...")

        self.life_expectancy = pd.read_csv('life_expectancy.csv')
        self.first_names = pd.read_csv("first_names.csv")
        self.last_names = pd.read_csv("last_names.csv")
        self.rank_to_prob = pd.read_csv("rank_to_probability.csv", header=None)
        self.birth_marriage_rate = pd.read_csv("birth_and_marriage_rates.csv")

        print("Read files: Completed")

    def generate_year_died(self, year_born):
        year_born = int(year_born)
        length = rand.randint(-10, 11)

        data = self.life_expectancy

        index = data["Year"] == year_born

        # Returns the whole row so you need to get the value at the str column

        life_expec = self.life_expectancy[index]["Period life expectancy at birth"].values[0]
        
        year_died = int(life_expec) + length + year_born

        return year_died
    
    def choose_gender(self):
        return rand.choice(['female', 'male'])
    

    def choose_first_name(self, year_born, gender):
        decade = self.get_decade_s(year_born)

        # From the csv file, get the matching decade and gender
        data = self.first_names[
            (self.first_names['decade'] == decade) &
            (self.first_names['gender'] == gender)
        ]

        # Get 1 random row based on the frequency column of the data
        name_row = data.sample(n=1, weights='frequency')

        # Return the first value from the name column of that row
        return name_row['name'].values[0]
        

    def choose_last_name(self, year_born):
        decade_str = self.get_decade_s(year_born)
        data = self.last_names[self.last_names['Decade'] == decade_str]

        prob = self.rank_to_prob.iloc[0].to_numpy()

        weights = [prob[int(rank) - 1] for rank in data['Rank']]

        return data.sample(n=1, weights=weights)['LastName'].values[0]
    
    def choose_last_name_d(self, founders_last_names):
        return rand.choice(founders_last_names)
        

    def create_person(self, year_born, descendant, founders_last_names=None):

        if year_born > 2120:
            return None


        gender = self.choose_gender()
        first_name = self.choose_first_name(year_born, gender)
        
        if descendant:
            last_name = self.choose_last_name_d(founders_last_names)
        else:
            last_name = self.choose_last_name(year_born)


        year_died = self.generate_year_died(year_born)

        return Person(year_born, first_name, last_name, year_died)
    
    def get_decade_s(self, year_born):
        return f"{(year_born // 10) * 10}s"

    def generate_spouse(self, year_born, descendant=False):
        m_rate = self.birth_marriage_rate

        index = m_rate['decade'] == self.get_decade_s(year_born)

        prob = m_rate[index]['marriage_rate'].values[0]

        if rand.random() < prob:
            spouse_born = rand.randint(-10, 11) + year_born
            if spouse_born > 2120:
                return None
            
            return self.create_person(spouse_born, descendant)
        
        return None
    
    def generate_children(self, elder_year, parent_year, founders_last_names):

        data = self.birth_marriage_rate

        index = data['decade'] == self.get_decade_s(parent_year)
        birth_rate = data[index]['birth_rate'].values[0]
        
        lower = int(max(0, math.ceil(birth_rate - 1.5)))
        upper = int(math.ceil(birth_rate + 1.5))

        num_childs = rand.randint(lower, upper + 1)

        starting_year = elder_year + 25
        ending_year = elder_year + 45
        
        children = []

        if num_childs == 1:
            if starting_year > 2120:
                return []
            
            children.append(self.create_person(starting_year, descendant=True, founders_last_names=founders_last_names))

        elif num_childs == 0:
            return []
        else:
            inc = (ending_year - starting_year) / (num_childs - 1)

            for i in range(num_childs):
                child_year = round(starting_year + (i * inc))
                
                if child_year > 2120:
                    break
                else:
                    children.append(self.create_person(child_year, founders_last_names=founders_last_names, descendant=True))

        return children



        