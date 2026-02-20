from PersonFactory import PersonFactory

class FamilyTree:
    def __init__(self):
        self.factory = PersonFactory()
        self.people = []


    def generate_tree(self):

        self.factory.read_files()

        print("Generating family tree...")

        p1 = self.factory.create_person(1950)
        p2 = self.factory.create_person(1950)

        p1.set_partner(p2)
        p2.set_partner(p1)

        self.people = [p1, p2]

        process = [p1]

        while process:

            parent = process.pop(0)
            spouse = parent.partner

            if spouse is None:
                spouse = self.factory.generate_spouse(parent.get_birth_year())
                
                if spouse:
                    self.people.append(spouse)

                    parent.set_partner(spouse)
                    spouse.set_partner(parent)
                
                    
            if spouse:
                elder_year = min(parent.get_birth_year(), spouse.get_birth_year())
            
            else:
                elder_year = parent.get_birth_year()

            
            children = self.factory.generate_children(elder_year, parent.get_birth_year())

            for child in children:
                if child is None:
                    continue

                process.append(child)
                self.people.append(child)
                parent.children.append(child)

                if spouse:
                    spouse.children.append(child)

        print("Family tree generated!")






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
                    print(f"- {name}")

            elif choice == "Q":
                break

            else:
                print("Invalid choice. Please choose T, D, N, or Q.")

            print("------------------------------------------")


if __name__ == "__main__":
    tree = FamilyTree()

    tree.generate_tree()
    tree.menu()

