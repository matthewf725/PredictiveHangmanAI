import os
import pickle
import numpy as np
import tensorflow as tf
import random

def create_ai():
        # Generate some example data
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    input_value = 5  # For example

    # Create a mapping from letters to indices
    letter_to_index = {letter: index for index, letter in enumerate(alphabet)}

    # Create the training data
    num_examples = len(alphabet)  # Number of examples
    x = np.full((num_examples, 1), input_value)  # Each input is the input_value
    y = np.eye(len(alphabet))  # One-hot encoded labels for each letter

    # Define the neural network architecture
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(1,)),  # Input shape for input_sequence_length
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(len(alphabet), activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(x, y, epochs=1)  # Increase the number of epochs if needed
    return model

def load_profile(profile_name):
    try:
        with open(profile_name, "rb") as file:
            profile_data = pickle.load(file)
        return profile_data['ai']
    except FileNotFoundError:
        print("Profile not found.")
        return 0

def create_profile(profile_name):
    ai = create_ai()
    with open(profile_name, "wb") as file:
        pickle.dump({'ai': ai}, file)

def save_profile(profile_name, ai):
    with open(profile_name, "wb") as file:
        pickle.dump({'ai': ai}, file)
def load_dictionary(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]
def choose_word(dictionary, wordList, ranNum):
    def select_word(dictionary, letters, x):
        preferred_letters = letters[:6]  # Letters at the front with preference

        remaining_letters = set(letters[6:])
            # After defining remaining_letters
    
        valid_words = [word for word in dictionary if len(word) == x and all(letter in preferred_letters for letter in word)]
        while not valid_words:
            x += 1
            valid_words = [word for word in dictionary if len(word) == x and all(letter in remaining_letters for letter in word)]
        
        # Sort valid words by preferred letters and then alphabetically
        def key_function(word):
            return (-sum(letter in preferred_letters for letter in word), word)
        
        sorted_words = sorted(valid_words, key=key_function)
        
        # Find the highest priority value
        highest_priority = key_function(sorted_words[0])[0]
        
        # Filter top candidates with the highest priority value
        top_candidates = [word for word in sorted_words if key_function(word)[0] == highest_priority]
        
        # Randomly select a word from the top candidates
        selected_word = random.choice(top_candidates)
        
        return selected_word

    # Example usage

    letters = wordList
    x = ranNum


    selected_word = select_word(dictionary, letters, x)
    return selected_word




def display_word(current_word, guesses):
    display = ""
    for letter in current_word:
        if letter in guesses:
            display += letter
        else:
            display += "_"
    return display

def getLetters(ai, ranNum):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    input_data = np.array([[ranNum]])
        # Predict scores for each letter
    predicted_scores = ai.predict(input_data)

    # Sort letters based on predicted scores (least likely to most)
    sorted_letters = [letter for _, letter in sorted(zip(predicted_scores[0], alphabet))]
    return sorted_letters

def adapt(input_value, target_letters, ai):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # Create a mapping from letters to indices
    letter_to_index = {letter: index for index, letter in enumerate(alphabet)}

    # Create the training data
    num_examples = len(alphabet)  # Number of examples
    x = np.full((num_examples, 1), input_value)  # Each input is the input_value
    y = np.eye(len(alphabet))  # One-hot encoded labels for each letter


    for i, target_letter in enumerate(target_letters):
        # Assign weights inversely proportional to the position of the target letter
        weight = 1.0 / (i + 1)  # Higher weight for letters closer to the beginning
        y[i, letter_to_index[target_letter]] = weight

    ai.fit(x, y, epochs=5)
    return ai

def play_game(ai, dictionary, ranNum):
    current_word = choose_word(dictionary, getLetters(ai, ranNum), ranNum)
    guesses = []
    attempts = 6
    score = 0

    while attempts > 0:
        print("\nCurrent word:", display_word(current_word, guesses))
        print("Attempts left:", attempts)
        guess = input("Guess a letter: ").lower()

        if guess in guesses:
            print("You've already guessed that letter.")
            continue

        guesses.append(guess)

        if guess in current_word:
            print("Correct guess!")
            if display_word(current_word, guesses) == current_word:
                print("Congratulations! You've guessed the word:", current_word)
                score += 1
                break
        else:
            print("Incorrect guess.")
            attempts -= 1

    if attempts == 0:
        print("Sorry, you're out of attempts. The word was:", current_word)

    ai = adapt(ranNum, guesses, ai)
    return ai

def main():
    dictionary_path = ''
    dictionary = load_dictionary(dictionary_path)
    profile_name = input("Enter your profile name: ")
    profile_exists = os.path.exists(profile_name)

    if profile_exists:
        choice = input("Do you want to load your existing profile? (y/n): ").lower()
        if choice == 'y':
            ai = load_profile(profile_name)  # You might want to modify this to actually load the AI model from the profile
        else:
            create_profile(profile_name)
            score = 0
            ai = create_ai()
    else:
        create_profile(profile_name)
        score = 0
        ai = create_ai()

    while True:
        ai = play_game(ai, dictionary, random.randint(1, 10))
        save_profile(profile_name, ai)
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thank you for playing!")
            break

if __name__ == "__main__":
    main()
