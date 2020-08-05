import random
import json
import os
import datetime
from colorama import Fore


rolls = {"NOTHING": "HERE"}


def main():
    try:
        print(Fore.WHITE)
        log("App starting up")

        load_rolls()
        show_header()
        show_leaderboard()
        player1, player2 = get_players()
        log(f"{player1} has logged in")
        play_game(player1, player2)
        log("Game Over!")
    except json.decoder.JSONDecodeError as je:
        print()
        print(Fore.RED + "ERROR: The file rolls.json is invalid JSON" + Fore.WHITE)
        print(Fore.RED + f"ERROR {je}" + Fore.WHITE)
    except FileNotFoundError as fe:
        print()
        print(Fore.RED + "ERROR: File Not Found" + Fore.WHITE)
        print(Fore.RED + f"ERROR {fe}" + Fore.WHITE)
    except KeyboardInterrupt:
        print()
        print(Fore.LIGHTMAGENTA_EX + "You Have to Run? Ok, see you next time" + Fore.WHITE)
    except Exception as e:
        print(Fore.RED + f"Unknown ERROR {e}" + Fore.WHITE)


def show_header():
    print(Fore.LIGHTMAGENTA_EX)
    print("--------------------------------------------------")
    print("Rock, Paper, Scissors v2")
    print("--------------------------------------------------")


def show_leaderboard():
    print(Fore.WHITE)
    leaders = load_leaders()

    sorted_leaders = list(leaders.items())
    sorted_leaders.sort(key=lambda l: l[1], reverse=True)

    print()
    print("LEADERBOARD: ")

    for name, wins in sorted_leaders[0:5]:
        print(f"{wins:,} -- {name}")
    print()
    print("--------------------------------------------------")
    print()


def get_players():
    p1 = input("Enter your name: ")
    p2 = "Computer"

    return p1, p2


def play_game(player_1, player_2):
    log(f"New game starting between {player_1} and {player_2}")
    wins = {player_1: 0, player_2: 0}
    roll_names = list(rolls.keys())

    while not find_winner(wins, wins.keys()):
        roll1 = get_roll(player_1, roll_names)
        roll2 = random.choice(roll_names)

        if not roll1:
            print(Fore.RED + "Sorry, try again!")
            print(Fore.WHITE)
            continue

        log(f"Round: {player_1} roll {roll1} and {player_2} roll {roll2}")
        print(Fore.LIGHTBLUE_EX + f"{player_1} rolls {roll1}")
        print(Fore.YELLOW + f"{player_2} rolls {roll2}")
        print(Fore.WHITE)

        # test for a winner
        winner = check_for_winner(player_1, player_2, roll1, roll2)

        if winner is None:
            msg = "This round is a tie!"
            print(Fore.GREEN + msg)
            log(msg)
            print(Fore.WHITE)
        else:
            msg = f"{winner} wins the round!"
            fore = Fore.LIGHTBLUE_EX if winner == player_1 else Fore.LIGHTRED_EX
            print(fore + msg)
            log(msg)
            print(Fore.WHITE)
            wins[winner] += 1

        player1_fore = Fore.LIGHTBLUE_EX
        player2_fore = Fore.YELLOW
        msg = f"Score is {player_1}: {wins[player_1]} and {player_2}: {wins[player_2]}"
        print(msg)
        log(msg)
        print()

    overall_winner = find_winner(wins, wins.keys())
    fore = Fore.LIGHTBLUE_EX if overall_winner == player_1 else Fore.LIGHTRED_EX
    msg = fore + f"{overall_winner} wins the game!"
    print(msg + Fore.WHITE)
    log(msg)
    record_win(overall_winner)


def find_winner(wins, names):
    best_of = 3
    for name in names:
        if wins.get(name, 0) >= best_of:
            return name
    return None


def check_for_winner(player_1, player_2, roll1, roll2):

    if roll1 == roll2:
        winner = None

    outcome = rolls.get(roll1, {})
    if roll2 in outcome.get('defeats'):
        return player_1
    elif roll2 in outcome.get('defeated_by'):
        return player_2


def get_roll(player_name, roll_names):
    try:
        print(f"Available rolls: ")
        for index, r in enumerate(roll_names, start=1):
            print(f"{index}. {r}")

        text = input(f"{player_name}, what is your roll?")
        selected_index = int(text) - 1

        if selected_index < 0 or selected_index >= len(rolls):
            print(f"Sorry, {text} is not a valid play.")
            return None

        return roll_names[selected_index]
    except ValueError as ve:
        print(Fore.RED + f"There was a Value Error. {ve}." + Fore.WHITE)
        return None


def load_rolls():
    global rolls

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, "rolls.json")

    with open(filename, 'r', encoding='utf-8') as fin:
        rolls = json.load(fin)

    log(f"Loaded Rolls: {list(rolls.keys())} from {os.path.basename(filename)}.")


def load_leaders():

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, "leaderboard.json")

    if not os.path.exists(filename):
        return {}

    with open(filename, 'r', encoding='utf-8') as fin:
        return json.load(fin)


def record_win(winner_name):
    leaders = load_leaders()

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, "leaderboard.json")

    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)


def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, "rps.log")

    with open(filename, 'a', encoding='utf-8') as fout:
        fout.write(f"[{datetime.datetime.now().isoformat()}]")
        fout.write(msg)
        fout.write('\n')


if __name__ == '__main__':
    main()