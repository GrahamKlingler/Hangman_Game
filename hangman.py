# Programming assignment number 1
# Author: Graham Klingler
# Date: October 6, 2022
# File: hangman.py is the main program to run the hangman game
import re
from random import choice, random, randint


# imports a dictionary of words at different lengths from dictionary.txt
def import_dictionary(filename: str) -> dict:
    dictionary = {new_list: [] for new_list in range(3, 13)}
    try:
        with open(filename) as file:
            for line in file:
                line = line.strip()
                if len(line) >= 3 and len(line) <= 12:
                    dictionary[len(line)].append(line)
    except Exception:
        print("Something went wrong")
    return dictionary


# print dictionary for test scenarios
def print_dictionary(dictionary):
    max_size = 12
    for i in range(3, max_size+1):
        print(dictionary[i])


# used at beginning of game
# gets options for what size word length and how many lives
def get_game_options() -> (int, int):
    size = input("Please choose a size of a word to be guessed [3 – 12, default any size]:")
    try:
        size = int(size)
        if size > 12 or size < 3:
            raise Exception
        print(f"The word size is set to {size}.")
    except:
        size = randint(3, 12)
        print("A dictionary word of any size will be chosen.")

    health = input("Please choose a number of lives [1 – 10, default 5]:")
    try:
        health = int(health)
        if health > 10 or health < 1:
            raise Exception
    except:
        health = 5

    print(f"You have {health} lives.")

    return size, health


# prints a list of the letters that have been chosen for the player to see
def print_chosen(letters_guessed):
    print("Letters chosen: ", end=" ")
    for letter in letters_guessed:
        print(letter, end="")
        if letters_guessed.index(letter) != len(letters_guessed)-1:
            print(",", end=" ")
    print()


# searches for and replaces instances of a guessed letter in the hidden word, revealing the letters
def sub_letters(new_word: str, letter_to_find: str, key: str) -> str:
    instances = [_.start() for _ in re.finditer(letter_to_find, key)]
    for instance in instances:
        new_word = new_word[:instance] + letter_to_find.upper() + new_word[instance+1:]
    return new_word


# prints the the health of player
def print_health(starting_health, health):
    print(f"   lives: {health}  ", end=" ")
    print("X" * (starting_health - health) + "O" * health)


# prints the hangman word in game format, hiding letters that have not been guessed
def print_word(hidden_word):
    for character in hidden_word:
        if character == "!":
            print("__", end=" ")
        elif character == "-":
            print("-", end=" ")
        else:
            print(character, end=" ")


# Start of main code segment
if __name__ == '__main__' :

    # make a dictionary from a dictionary file
    dictionary_filename = "dictionary.txt"
    dictionary = import_dictionary(dictionary_filename)

    # print the dictionary (use only for debugging)
    # print_dictionary(dictionary)    # remove after debugging the dictionary function import_dictionary

    # print a game introduction
    print("Welcome to the Hangman Game!")

    # START MAIN LOOP (OUTER PROGRAM LOOP)
    main_loop_running = True

    while main_loop_running:

        # set up game options (the word size and number of lives)
        size, health = get_game_options()
        starting_health = health

        # select a word from a dictionary (according to the game options)
        word_to_guess = choice(dictionary[size]).upper()
        print(word_to_guess)

        # create list to hold letters chosen by player
        letters_guessed = []

        # create the hidden word
        hidden_word = "!"*len(word_to_guess)

        # determine if letter has any hyphens
        if "-" in word_to_guess:
            hidden_word = sub_letters(hidden_word, "-", word_to_guess)
        in_game = True

        # START GAME LOOP   (INNER PROGRAM LOOP)
        while in_game:


            # format and print the game interface:
            # Letters chosen: E, S, P                list of chosen letters
            print_chosen(letters_guessed)

            # __ P P __ E    lives: 4   XOOOO        hidden word and lives
            print_word(hidden_word)
            print_health(starting_health, health)

            '''try:
                if something not right:
                    raise Exception
               except:
                    skip'''

            # asks a user to pick a letter, then checks for letter in word
            letter_guess = input("Please choose a new letter >").upper()
            try:
                letter_guess = letter_guess.strip()

                if len(letter_guess) != 1 or not letter_guess.isalpha():
                    raise Exception

                if letter_guess not in letters_guessed:
                    # update list of chosen letters
                    letters_guessed.append(letter_guess)
                    if letter_guess in word_to_guess:
                        # update hidden word
                        print("You guessed right!")
                        hidden_word = sub_letters(hidden_word, letter_guess, word_to_guess)
                    else:
                        # lose a life
                        print("You guessed wrong, you lost one life.")
                        health -= 1
                else:
                    # repeat loop with no negative or positive effects
                    print("You have already chosen this letter.")
            except:
                print("Invalid input type.")


            # END GAME LOOP   (INNER PROGRAM LOOP)
            if health < 1:
                # print final game board and announce the loss
                in_game = False
                print_chosen(letters_guessed)
                print_word(hidden_word)
                print_health(starting_health, health)
                print(f"You lost! The word was {word_to_guess.upper()}.")
            elif "!" not in hidden_word:
                # print final game board and announce the win
                in_game = False
                print_chosen(letters_guessed)
                print_word(hidden_word)
                print_health(starting_health, health)
                print(f"Congratulations!!! You won! The word is {word_to_guess.upper()}!")

        # ask if the user wants to continue playing
        while True:
            answer = input("Would you like to play again [Y/N]?").upper()
            try:
                if answer == "N":
                    main_loop_running = False
                    break
                elif answer == "Y":
                    break
                else:
                    raise Exception
            except:
                continue
    # ask if the user wants to continue playing,
    # if yes start a new game, otherwise terminate the program
    # END MAIN LOOP (OUTER PROGRAM LOOP)

print("Goodbye!")
