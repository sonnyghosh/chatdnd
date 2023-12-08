import csv
import sys

class DataSaverLoader:
    def __init__(self, savefile):
        self.savefile = savefile
        self.states = []
        self.rewards = []

    def add_data(self, state, reward):
        self.states.append(state)
        self.rewards.append(reward)

    def save_data(self):
        data = {'states': self.states, 'rewards': self.rewards}
        with open(self.savefile, 'a', newline='') as csvfile:
            fieldnames = ['states', 'rewards']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Check if the file is empty, if yes, write the header
            csvfile.seek(0, 2)  # Move the cursor to the end of the file
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(data)

    def load_data(self):
        try:
            csv.field_size_limit(sys.maxsize)
            with open(self.savefile, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                
                states = []
                rewards = []
                for row in reader:
                    states.extend(eval(row['states']))
                    rewards.extend(eval(row['rewards']))
                
                if len(states) == 0:
                    print(f"No data found in {self.savefile}. Returning empty lists.")
                    return [], []
                
                return states, rewards
        except FileNotFoundError:
            print(f"No data found in {self.savefile}. Returning empty lists.")
            return [], []

# Example usage:
#savefile_path = 'your_savefile.pkl'
#data_saver_loader = DataSaverLoader(savefile_path)

# Iteratively add [state, reward] pairs
#data_saver_loader.add_data([1, 2, 3], 0.5)
#data_saver_loader.add_data([4, 5, 6], 1.0)

# Load data in another program
#loaded_states, loaded_rewards = data_saver_loader.load_data()
#print("Loaded States:", loaded_states)
#print("Loaded Rewards:", loaded_rewards)
