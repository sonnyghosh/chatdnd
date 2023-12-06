import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))

from game.gamefiles import g_vars, hypers, save_load
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

dataset_file = "./api/game/gamefiles/data/dataset.txt"

data_parser = save_load.DataSaverLoader(dataset_file)

if True:
    X, Y = data_parser.load_data()

    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Initialize the Decision Tree Regressor
    decision_tree_model = DecisionTreeRegressor()

    # Train the model
    decision_tree_model.fit(X_train, Y_train)

    # Make predictions on the test set
    predictions = decision_tree_model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(Y_test, predictions)
    print(f"Mean Squared Error: {mse}")


def make_move(state):
    pass



    