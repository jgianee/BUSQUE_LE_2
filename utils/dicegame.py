from utils.manager import UserManager
from utils.score import Score
import random
import os

class DiceGame:
    def __init__(self):
        self.user_manager = UserManager()
        self.user_manager.load_users()  # Load existing users
        self.current_user = None
        self.scores = []  # TODO: page 8/10 - The dice_game.py ...
        self.load_scores()  # Load existing scores

    def load_scores(self):
        try:
            with open("data/rankings.txt", "r") as file:
                for line in file:
                    username, game_id, points, wins = line.strip().split(",")
                    # we make sure that we read int values for points and wins instead of str
                    # this is critical info for sorting - top 10 scores!!!
                    self.scores.append(Score(username, game_id, int(points), int(wins)))
                # scores.sort(key=lambda x: (x.points, x.wins), reverse=True)
        except FileNotFoundError:
            os.makedirs("data", exist_ok=True)
            with open("data/rankings.txt", "w"):
                pass

    def save_scores(self):
        print("saving scores...", end='')
        # global scores
        with open("data/rankings.txt", "w") as file:
            # scores.sort(key=lambda x: (x.points, x.wins), reverse=True)
            for score in self.scores:
                file.write(f"{score.username},{score.game_id},{score.points},{score.wins}\n")
        print("done!")

    def register(self):
        print("Registration")
        while True:
            username = input("Enter username (at least 4 characters), or leave blank to cancel: ")
            password = input("Enter password (at least 8 characters), or leave blank to cancel: ")
            if username == '' or password == '':
                print("Registration canceled.\n")
                return

    def login(self):
        # Log in an existing user
        print("Login")
        username = input("Enter username, or leave blank to cancel: ")
        password = input("Enter password, or leave blank to cancel: ")
        if username == '' or password == '':
            print("Login canceled.\n")
            return
        else:
            print("Invalid username or password. Please try again.\n")
            return False

    def play_game(self):
        print(f"Starting game as {self.current_user}...")
        tot_points = 0  # in every game, the starting points will always be 0.
        stages_won = {}
        game_id = random.randint(1001, 9999)

        for stages in range(1, 10 + 1):

            # reset the points for every round
            usr_points = 0
            cpu_points = 0
            exit_stages = False

            # for rounds in range(1, 3 + 1):
            rounds = 1
            roll_count = 3
            while rounds <= roll_count:

                # worth nothing that each game is unique
                usr_roll = random.randint(1, 6)
                cpu_roll = random.randint(1, 6)

                # print(f"{self.current_user} rolled:", usr_roll)
                # print("CPU rolled:", cpu_roll)
                print(f"{self.current_user} rolled: {usr_roll}")
                print(f"CPU rolled: {cpu_roll}")

                # a tie will not count a score for anyone
                if usr_roll == cpu_roll:
                    # allowing for an additional roll, until the best out of three condition is met
                    roll_count = roll_count + 1
                    print("It's a tie!")
                elif usr_roll < cpu_roll:
                    cpu_points = cpu_points + 1
                    print("CPU wins this round!")
                else:
                    usr_points += 1  # every round the player wins, they receive 1 point
                    print(f"You win this round! {self.current_user}")

                rounds = rounds + 1

            # if player wins, the user can choose to continue to the next stage or stop playing the game.
            if usr_points > cpu_points:
                tot_points += usr_points + 3  # if they win the stage, they receive an additional 3 points
                stages_won[stages] = tot_points
                print(f"You won this stage {self.current_user}!")
                print(self.current_user)
                print(f"Total Points: {tot_points}, Stages Won: {stages}")
                self.scores.append(Score(self.current_user, game_id, tot_points, stages))

                valid_input = False
                while not valid_input:
                    choice = input("Do you want to continue to the next stage? (1 for Yes, 0 for No): ")
                    if choice == '1':
                        valid_input = True
                    elif choice == '0':
                        self.save_scores()
                        print(f"Game over. You won {len(stages_won)} stage(s) with a total of {tot_points} points.")
                        valid_input = True
                        exit_stages = True
                    else:
                        print("Invalid input. Please enter 1 for Yes or 0 for No.")
                        valid_input = False

            # if the user loses, the â€œGame over.You didnâ€™t win any stages.â€
            elif usr_points < cpu_points:
                print(f"You lost this stage {self.current_user}.")
                if len(stages_won) == 0:
                    print("Game over. You didn't win any stages.")
                else:
                    self.save_scores()
                    self.show_top_scores()
                # as the user progresses, the points during that game will stack up,
                tot_points = 0  # until the user loses.
                break  # break the for-stages

            # if it's a tie
            else:
                print("It's a tie game, moving to next stages...")

            if exit_stages:
                break  # break the for-stages


    def show_top_scores(self):
        # the user should be able to see the top-10 highest scores attained.
        print("Top Scores:")
        if len(self.scores) == 0:
            print("No games played yet. Play a game to see top scores.")
        else:
            # we sort scores by points then, by wins in descending order
            self.scores.sort(key=lambda x: (x.points, x.wins), reverse=True)
            rank_number = 0
            for score in self.scores:
                rank_number = rank_number + 1
                print(f"{rank_number}. {score.username}: Points - {score.points}, Wins - {score.wins}")
                if rank_number == 10:
                    break

    def logout(self):
        # Log out the current user
        if self.current_user:
            self.save_scores()
            print(f"Goodbye {self.current_user}!")
            # reset them every logout
            self.current_user = None
            self.scores = []
            print("You Logged out successfully.")
        else:
            print("You are not logged in.")

    def menu(self):
        # Display the main menu based on user login status
        while True:
            print("Menu:")
            print("1. Start game")
            print("2. Show top scores")
            print("3. Log out")

            choice = input("Enter your choice, or leave blank to cancel: ")

            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.show_top_scores()
            elif choice == '3':
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.\n")