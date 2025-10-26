import random

print(
"""
+--------------------------------+
| Welcome to the guessing game,  |
| guess a number between 1-100.  |
+--------------------------------+
""")

random_number = random.randint(1,100)

user_guess = 0
exit = False
attempts = []


while not exit and user_guess != random_number:
    user_guess = int(input("Your Guess (999 to exit): "))
    attempts.append(user_guess)
    
    if user_guess == random_number:
            exit = True
            print(f"Correct, random number was {random_number}")
            print(f"congratulations, it took you {len(attempts)} guesses!")
    
    elif user_guess == 999:
        exit = True
        print("Exiting programme")

    elif user_guess > random_number:
          print("Guess is too high")

    else:
          print("Guess is too low")
