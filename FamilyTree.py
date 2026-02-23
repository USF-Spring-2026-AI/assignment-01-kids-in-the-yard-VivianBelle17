from PersonFactory import PersonFactory


class FamilyTree:
    """Driver class that generates a family tree with simple reports about the tree
    - Uses PersonFactory to create spouses, children, founders
    - stores all Person objects in self.people
    - Gives menu options for simple reports on the tree
    """

    def __init__(self):
        self.factory = PersonFactory()
        self.people = []
        self.founders_last_names = []

    """Generates a family tree with spouses and children, starting from two founders born in 1950. 
    Tree stops generating with there is no more children of when the birth year exceed 2120 
    """

    def generate_tree(self):

        self.factory.read_files()

        print("Generating family tree...")

        p1 = self.factory.create_person(1950, descendant=False)
        p2 = self.factory.create_person(1950, descendant=False)

        p1.set_partner(p2)
        p2.set_partner(p1)

        # Keeping track of founders last names so their decendants can inherit it
        self.founders_last_names = [p1.get_last_name(), p2.get_last_name()]

        self.people = [p1, p2]

        # Put the people in a queue so we can pop it off and make their descendants, spouses, etc.
        process = [p1]

        while process:

            parent = process.pop(0)
            spouse = parent.get_partner()

            # Create a spouse Person object and add it to the lists
            if spouse is None:
                spouse = self.factory.generate_spouse(
                    parent.get_birth_year(), descendant=False
                )

                if spouse:
                    self.people.append(spouse)

                    parent.set_partner(spouse)
                    spouse.set_partner(parent)

            # Get the older year to computate the birth year (minimum of the two years)
            if spouse:
                elder_year = min(parent.get_birth_year(), spouse.get_birth_year())

            # An else here because it is possible for the parent to not have a spouse
            else:
                elder_year = parent.get_birth_year()

            # Generate a number of children based on the parents birth year, using the lower birth year
            children = self.factory.generate_children(
                elder_year, parent.get_birth_year(), self.founders_last_names
            )

            # Updating lists
            for child in children:
                if child is None:
                    continue

                process.append(child)
                self.people.append(child)
                parent.add_child(child)

                if spouse:
                    spouse.add_child(child)

        print("Family tree generated!")

    # Returns the number of people in the family tree
    def total_people(self):
        return len(self.people)

    # Returns the count of people born in each decade
    def total_decade(self):
        count = {}

        for p in self.people:
            decade = (p.get_birth_year() // 10) * 10
            count[decade] = count.get(decade, 0) + 1

        return count

    # Returns the names of descendants who have the same names
    def duplicate_names(self):
        name_count = {}

        for p in self.people:
            name = f"{p.get_first_name()} {p.get_last_name()}"
            name_count[name] = name_count.get(name, 0) + 1

        return [name for name, count in name_count.items() if count > 1]

    # Returns the number of people born in each year
    def total_year(self):
        count = {}
        for p in self.people:
            year = p.get_birth_year()
            count[year] = count.get(year, 0) + 1

        return count

    # Menu Options
    def menu(self):
        while True:

            print("Are you interested in: ")
            print("(T)otal number of people in the tree")
            print("Total number of people in the tree by (D)ecade")
            print("(N)ames duplicated")
            print("Total number of people in the tree by (Y)ear")
            print("(Q)uit")

            choice = input("--> ").strip().upper()

            if choice == "T":
                print(f"The tree contains {self.total_people()} people total")

            elif choice == "D":
                total_decade = self.total_decade()
                for decade, count in sorted(total_decade.items()):
                    print(f"{decade}: {count}")

            elif choice == "N":
                dups = self.duplicate_names()
                print(f"There are {len(dups)} duplicate names in the tree ")
                for name in dups:
                    print(f"- {name}")

            elif choice == "Q":
                break
            elif choice == "Y":
                total_year = self.total_year()
                for year, count in sorted(total_year.items()):
                    print(f"{year}: {count}")

            else:
                print("Invalid choice. Please choose T, D, N, Y, or Q.")

            print("------------------------------------------")


if __name__ == "__main__":
    tree = FamilyTree()

    tree.generate_tree()
    tree.menu()
