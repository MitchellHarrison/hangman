from random_word import RandomWords
from time import sleep
from re import match
from random import choice

word_min_len = 0
word_max_len = 0
num_of_wrong_guesses = 0
max_wrong_guesses = 5
user_guess = ""
already_guessed = []
board = []

wrong_guess_phrases = [
    "You're killing him!",
    "Another limb hangs!",
    "HA! The gallows are full today!"
    ]
correct_guess_phrases = [
    "Everyone gets lucky sometimes...",
    "A broken clock...",
    "Hm. A blind squirrel sometimes finds a nut."
    ]
loss_phrases = [
    "MWAHAHAHA!! You LOSE!!",
    "Hm. As expected... You LOSE!!"
]
victory_phrases = [
    "YOU CHEATED!!!",
    "Hm. You win this battle, but not the WAR!!"
]


def choose_diff():

    global word_min_len
    global word_max_len

    difficulty = input("Choose a difficulty 1-3: ")
    if difficulty.isdigit():
        difficulty = int(difficulty)
        if difficulty == 1:
            word_min_len = 3
            word_max_len = 5
            return
        elif difficulty == 2:
            word_min_len = 6
            word_max_len = 10
            return
        elif difficulty == 3:
            word_min_len = 11
            word_max_len = 15
            return
        else:
            print("I said 1-3! Can you not count to three? AGAIN!")
            choose_diff()
    else:
        print("That's not even a number. Seems like your odds are slim.")
        choose_diff()


def choose_word(min_len, max_len):
    goal_word = RandomWords().get_random_word(hasDictionaryDef = "true", minLength = min_len, maxLength = max_len)

    # check for accents or nums
    if match('^[a-zA-Z]+$', goal_word):
        goal_word = goal_word.upper()
        return goal_word
    else:
        choose_word(word_min_len, word_max_len)
    

def get_user_guess(guessed):
    
    global already_guessed
    global user_guess
    
    guess = input("Enter your choice: ")
    if match('^[a-zA-Z]$', guess):
        guess = guess.upper()
        if guess in already_guessed:
            print("You've already guessed that. Are you even trying?")
            get_user_guess(guessed)
    else:
        print("Try a valid guess...")
        get_user_guess(guessed)
    already_guessed.append(guess)
    user_guess = guess


def check_guess(word, guess, board):

    global num_of_wrong_guesses

    correct_pos = [pos for pos, char in enumerate(word) if char == guess]
    if len(correct_pos) == 0:
        num_of_wrong_guesses += 1
        if num_of_wrong_guesses == 1:
            print(f"{choice(wrong_guess_phrases)} You have guessed wrong {num_of_wrong_guesses} time!")
            return
        else:
            print(f"{choice(wrong_guess_phrases)} You have guessed wrong {num_of_wrong_guesses} times!")
            return
    print(f"{choice(correct_guess_phrases)}")


def display_board(board):
    print(" ".join(board))


def update_board(word, guess):

    global board

    correct_pos = [pos for pos, char in enumerate(word) if char == guess]
    for i in correct_pos:
        board[i] = guess


def victory_check(board):
    for i in board:
        if i == "_":
            return False
    return True


def loss_check(guess_num, max_guess_num):
    if guess_num == max_guess_num:
        return True
    return False
    

choose_diff()
word = choose_word(word_min_len, word_max_len)

for i in word:
    board.append("_")

display_board(board)

print(f"You have {max_wrong_guesses} guesses to defeat me. BEGIN!")
while True:
    get_user_guess(already_guessed)
    check_guess(word, user_guess, board)
    update_board(word, user_guess)
    display_board(board)
    if victory_check(board):
        print(f"{choice(victory_phrases)}")
        break
    if loss_check(num_of_wrong_guesses, max_wrong_guesses):
        print(f"{choice(loss_phrases)} The word was {word}! >:)")
        break