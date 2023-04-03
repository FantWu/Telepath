import pickle


class Brain:
    def __init__(self):
        self.my_dict = {}

    def save(self):
        with open("brain.pkl", "wb") as f:
            pickle.dump(self.my_dict, f)

    def read(self):
        with open("brain.pkl", "rb") as f:
            self.my_dict = pickle.load(f)

    def append(self, key: str, value: str):
        self.my_dict[key] = value

    def get(self, key: str):
        return self.my_dict[key]


if __name__ == "__main__":
    brain = Brain()
    brain.read()
    print(brain.my_dict)
