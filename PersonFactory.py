import math
import pandas as pd
import random as rand

from Person import Person


class PersonFactory:
    """A PersonFactory class that creates a Person object and assigns the Person's attributes.
    This class reads CSV files that have information for life expectancy, names, marriage rates,
    birth rates, and the frequency of those values
    """

    def __init__(self):
        self.birth_marriage_rate = None
        self.first_names = None
        self.last_names = None
        self.life_expectancy = None
        self.rank_to_prob = None

    # Read all the files for data
    def read_files(self):

        print("Reading files...")

        try:
            self.life_expectancy = pd.read_csv("life_expectancy.csv")
            self.first_names = pd.read_csv("first_names.csv")
            self.last_names = pd.read_csv("last_names.csv")
            # Since this file was a single row of probabilities, you need to read it a differenlty
            self.rank_to_prob = pd.read_csv("rank_to_probability.csv", header=None)
            self.birth_marriage_rate = pd.read_csv("birth_and_marriage_rates.csv")

        except FileNotFoundError as e:
            print(f"Error: File not found: {e.filename}")
            print("Please ensure all CSV files are in the current directory")
            exit(1)
        except Exception as e:
            print("Unexpected error while trying to read data files")
            print(str(e))
            exit(1)

        required_files = [
            self.life_expectancy,
            self.first_names,
            self.last_names,
            self.rank_to_prob,
            self.birth_marriage_rate,
        ]

        if any(file is None for file in required_files):
            print("File needed is missing")
            exit(1)

        print("Read files: Completed")

    # Generate the year died based on the year they were born
    def generate_year_died(self, year_born):
        year_born = int(year_born)
        length = rand.randint(-10, 11)

        # Assigning to local variable to improve readability
        data = self.life_expectancy

        # Select the row for this birth year and grab the the life expectancy number for that year
        index = data["Year"] == year_born
        life_expec = data[index]["Period life expectancy at birth"].values[0]

        year_died = int(life_expec) + length + year_born

        return year_died

    # Generate a random gender
    def choose_gender(self):
        return rand.choice(["female", "male"])

    # Chose a first name based on the first_name csv and the frequency of that name
    def choose_first_name(self, year_born, gender):
        decade = self.get_decade_s(year_born)

        # From the csv file, get the matching decade and gender
        data = self.first_names[
            (self.first_names["decade"] == decade)
            & (self.first_names["gender"] == gender)
        ]

        # Get 1 random row based on the frequency column of the data
        name_row = data.sample(n=1, weights="frequency")

        # Return the first value from the name column of that row
        return name_row["name"].values[0]

    # Choosing a last name for a non-descendant based on rank
    def choose_last_name(self, year_born):
        decade_str = self.get_decade_s(year_born)
        data = self.last_names[self.last_names["Decade"] == decade_str]

        # Since the data is in one row, grab that row and convert to an array
        prob = self.rank_to_prob.iloc[0].to_numpy()

        # Build weights corresponding to the rows in last_names.csv by mapping the rank to the probability
        weights = [prob[int(rank) - 1] for rank in data["Rank"]]

        return data.sample(n=1, weights=weights)["LastName"].values[0]

    # Choosing one of the descendants last name for descendants
    def choose_last_name_d(self, founders_last_names):
        return rand.choice(founders_last_names)

    # Creating a person with year born, descendants, gender, and name attributes. The FLN are required when descendant is True
    def create_person(self, year_born, descendant, founders_last_names=None):

        # A cap for creating people
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

    # Coverts a decade number to match the decade str in the files
    def get_decade_s(self, year_born):
        return f"{(year_born // 10) * 10}s"

    # Generate a spouse based on the probability on the marriage rates for the decade
    def generate_spouse(self, year_born, descendant=False):
        m_rate = self.birth_marriage_rate

        index = m_rate["decade"] == self.get_decade_s(year_born)
        prob = m_rate[index]["marriage_rate"].values[0]

        # If a spouse is generated then they are created within ten years of their partner
        if rand.random() < prob:
            spouse_born = rand.randint(-10, 11) + year_born
            if spouse_born > 2120:
                return None
            return self.create_person(spouse_born, descendant)

        return None

    # Generate a list of of Person objects for a parent. Returns a list of Person objects; possibly empty.
    def generate_children(self, elder_year, parent_year, founders_last_names):

        data = self.birth_marriage_rate

        index = data["decade"] == self.get_decade_s(parent_year)
        birth_rate = data[index]["birth_rate"].values[0]

        # Compute the lower and upper bounds of children the parent can have
        lower = int(max(0, math.ceil(birth_rate - 1.5)))
        upper = int(math.ceil(birth_rate + 1.5))

        num_childs = rand.randint(lower, upper + 1)

        starting_year = elder_year + 25
        ending_year = elder_year + 45

        children = []

        if num_childs == 0:
            return []

        # If there is 1 child then create that one one person. Used to avoid division by 0
        if num_childs == 1:
            if starting_year > 2120:
                return []

            children.append(
                self.create_person(
                    starting_year,
                    descendant=True,
                    founders_last_names=founders_last_names,
                )
            )
            return children

        # Creating a window so children are born equally within each other
        window = (ending_year - starting_year) / (num_childs - 1)

        # Looping through the children list to create each of therm
        for child in range(num_childs):
            child_year = round(starting_year + (child * window))

            if child_year > 2120:
                break
            else:
                children.append(
                    self.create_person(
                        child_year,
                        founders_last_names=founders_last_names,
                        descendant=True,
                    )
                )

        return children
