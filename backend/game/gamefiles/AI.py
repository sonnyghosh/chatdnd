import sys
import os
import pickle
import random
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))

from game.gamefiles import g_vars, hypers, save_load, item
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
pass_item = item.Pass
fist_item = item.Fist
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def train_model(X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    # Train model
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    
    # Evaluate model
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print('Train Results:')
    print(f"MSE: {mse}")
    print(f"MAE: {mae}")
    print(f"R^2: {r2}")
    max_diff = 0
    for a,b in zip(preds, y_test):
        diff = b-a
        if abs(diff) > max_diff:
            max_diff = diff
    print(max_diff)
    return model

def save_model(model):
    with open('./api/game/gamefiles/models/DTR_2_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
def load_model():
    with open('./api/game/gamefiles/models/DTR_2_model.pkl', 'rb') as f:
        return pickle.load(f)

class Agent:

    def __init__(self):
        self.model = load_model()

    def make_move(self, state):
        player = state['player']
        friends = state['friends']
        enemies = state['enemies']
        alive_f = friends.get_alive_players()
        alive_e = enemies.get_alive_players()
        moves = []
        
        action = 0
        possible = player.get_top_n_item(ItemType.ranged, 2) + player.get_top_n_item(ItemType.melee, 2) + [fist_item]
        for item in possible:
            for target in alive_e:
                state = friends.get_inputs() + enemies.get_inputs() + player.get_inputs() + target.get_inputs() + item.get_inputs() + [action]
                pred = self.model.predict([state])[0]
                moves.append([(action, item, target), pred])

        action = 1
        possible = player.get_top_n_item(ItemType.potion, 2)
        for item in possible:
            for target in alive_f:
                state = friends.get_inputs() + enemies.get_inputs() + player.get_inputs() + target.get_inputs() + item.get_inputs() + [action]
                pred = self.model.predict([state])[0]
                moves.append([(action, item, target), pred])

        possible = player.get_top_n_item(ItemType.magic, 2)
        for item in possible:
            if PlayerStat.attack in list(item.effects.keys()):
                for target in alive_e:
                    state = friends.get_inputs() + enemies.get_inputs() + player.get_inputs() + target.get_inputs() + item.get_inputs() + [action]
                    pred = self.model.predict([state])[0]
                    moves.append([(action, item, target), pred])
            else:
                for target in alive_f:
                    state = friends.get_inputs() + enemies.get_inputs() + player.get_inputs() + target.get_inputs() + item.get_inputs() + [action]
                    pred = self.model.predict([state])[0]
                    moves.append([(action, item, target), pred])

        action = 2
        possible = player.get_top_n_item(ItemType.ranged, 2) + player.get_top_n_item(ItemType.melee, 2) + player.get_top_n_item(ItemType.magic, 3) + player.get_top_n_item(ItemType.potion, 3) + player.get_top_n_item(ItemType.armor, 2)
        for item in possible: 
            for target in alive_f:
                state = friends.get_inputs() + enemies.get_inputs() + player.get_inputs() + target.get_inputs() + item.get_inputs() + [action]
                pred = self.model.predict([state])[0]
                moves.append([(action, item, target), pred])

        state = friends.get_inputs() + enemies.get_inputs() + player.get_inputs() + player.get_inputs() + pass_item.get_inputs() + [3]
        pred = self.model.predict([state])[0]
        moves.append([(3, pass_item, player), pred])

        moves.sort(key=lambda x: x[1], reverse=True)
        move_idx = min(len(moves)-1, random.randint(0,4))
        return moves[move_idx][0]


if __name__ == '__main__':
    train_dataset_file = "./api/game/gamefiles/data/train_dataset.txt"
    #test_dataset_file = "./api/game/gamefiles/data/test_dataset.txt"
    train_data_parser = save_load.DataSaverLoader(train_dataset_file)
    #test_data_parser = save_load.DataSaverLoader(test_dataset_file)
    X_train, Y_train = train_data_parser.load_data()
    #X_test, Y_test = test_data_parser.load_data()
    model = train_model(X_train, Y_train)
    #Y_hat = model.predict(X_test)
    save_model(model=model)
    #mse = mean_squared_error(Y_test, Y_hat)
    #mae = mean_absolute_error(Y_test, Y_hat)
    #r2 = r2_score(Y_test, Y_hat)
    #print('Test Results:')
    #print(f"MSE: {mse}")
    #print(f"MAE: {mae}")
    #print(f"R^2: {r2}")
    
    