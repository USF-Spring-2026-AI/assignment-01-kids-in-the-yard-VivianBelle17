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
        



if __name__ == "__main__":
    tree = FamilyTree()

    tree.generate_initial_people()
    print(len(tree.people))
    print(tree.duplicate_names())