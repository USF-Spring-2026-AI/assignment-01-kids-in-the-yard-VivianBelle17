from PersonFactory import PersonFactory

class FamilyTree:
    def __init__(self):
        self.factory = PersonFactory()
        self.people = []


    def generate_initial_people(self):
        self.factory.read_files()
        person_one = self.factory.create_person(1950)
        person_two = self.factory.create_person(1950)

        self.people.extend([person_one, person_two])

    def total_people(self):
        return len(self.people)
    
    def total_decade(self):
        count = {}

        for p in self.people:
            decade = (p.year_born // 10) * 10
            count[decade] = count.get(decade, 0) + 1

        return count
    

    def duplicate_names(self):
        name_count = {}

        for p in self.people:
            name = f"{p.first_name} {p.last_name}"
            name_count[name] = name_count.get(name, 0) + 1

        return [name for name, count in name_count.items() if count > 1]
    
    def menu(self):
        while True:

            print("Are you interested in: ")
            print("(T)otal number of people in the tree")
            print("Total number of people in the tree by (D)ecade") 
            print("(N)ames duplicated")
            print("(Q)uit")
        
            choice = input("--> ").strip().upper()

            if choice == "T":
                print(f"The tree contains {self.total_people()} people total")

            elif choice == "D":
                td = self.total_decade()
                for decade, count in sorted(td.items()):
                    print(f"{decade}: {count}")

            elif choice == "N":
                dups = self.duplicate_names()
                print(f"There are {len(dups)} duplicate names in the tree ")
                for name in dups:
                    print(f"* {name}")

            elif choice == "Q":
                break

            else:
                print("Invalid choice. Please choose T, D, N, or Q.")

            print("------------------------------------------")


if __name__ == "__main__":
    tree = FamilyTree()

    tree.generate_initial_people()
    tree.menu()

