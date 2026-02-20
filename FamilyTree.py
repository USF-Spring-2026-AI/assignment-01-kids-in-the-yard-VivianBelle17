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


if __name__ == "__main__":
    tree = FamilyTree()

    tree.generate_initial_people()
    print(len(tree.people))