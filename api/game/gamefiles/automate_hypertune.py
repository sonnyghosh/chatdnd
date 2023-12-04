import subprocess
import math

threshold = 0.7  # Set your desired threshold here

while True:
    # Run the first command
    subprocess.run(['/bin/python3', '/mnt/q/Codes/chatdnd/api/game/gamefiles/randomize_hypers.py'])

    # Run the second command and capture the output
    result = subprocess.run(['/bin/python3', '/mnt/q/Codes/chatdnd/api/game/gamefiles/hyper_loop.py'], capture_output=True, text=True)

    # Extract the numeric value from the output
    games, correct = result.stdout.split(' ')
    games, correct = int(games), int(correct)
    fit = correct/games
    sd = math.sqrt(games*fit*(1-fit))
    print(f'Games: {games}, Correct: {correct}, SD: {sd}, Fit: {fit}')
    # Check if the threshold is reached
    if fit >= threshold and sd < 10:
        print(f"Threshold of {threshold} reached. Stopping.")
        break