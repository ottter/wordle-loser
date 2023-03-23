import requests
import random
import nltk
from config import API_KEY


def todays_wordle():
    """Send GET request to get the Wordle of the day"""

    url = "https://wordle-answers-solutions.p.rapidapi.com/today"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "wordle-answers-solutions.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    return response.json().get('today')

def download_wordlist():
    nltk.download('words')
    return nltk.corpus.words.words()

def first_word():
    # wordlist = ['adieu', 'media', 'arise', 'radio']
    first_guess_list = ['scoon']
    return random.choice(first_guess_list)

def generate_five_letter(wordlist, green_letters, guess_history):
    """Generate all 5 letter words. Might not all be Wordle-approved"""

    five_letter_words = [word.lower() for word in wordlist if len(word) == 5]
    # Remove words from the list that don't match the correct letter placements
    # Does not remove words that aren't possible due to close/yellow letters
    for word in five_letter_words.copy():
        for j, letter in enumerate(word):
                if word in guess_history:
                    five_letter_words.remove(word)
                    break
                if letter != green_letters[j] and green_letters[j] != None:
                    five_letter_words.remove(word)
                    break
    return five_letter_words

def compare_words(todays_word, wordle_guess):
    """Compare a submitted word against the days Wordle"""

    if len(wordle_guess) != 5:
        return print("Error: Your guess word must be 5 letters long")
    
    if wordle_guess == todays_word:
        result = [char for char in todays_word]
        return result, [], [], [todays_word]
    
    result, wrong_letters, close_letters = [], [], []

    for i in range(5):
        print(todays_word[i], wordle_guess[i])
        # If the letter in todays_word matches the guess, add to result list
        if todays_word[i] == wordle_guess[i]:
            result.append(todays_word[i])
        # If the letter is anywhere within the guess, add to the close
        elif wordle_guess[i] in todays_word:
            result.append(None)                     # None gets added if there is no exact match to keep position
            close_letters.append(wordle_guess[i])
        # If the letter is neither correct or misplaced, add to the discard pile
        else:
            result.append(None)
            wrong_letters.append(wordle_guess[i])
    wrong_letters = [*set(wrong_letters)]           # Remove repeats from the discard pile
    return result, close_letters, wrong_letters, wordle_guess

def green_letter_check(word, green_letters):
    for i in range(len(word)):
        # Compare positions of random word with matched letters to find viable words
        if word[i] != green_letters[i] and green_letters[i] != None:
            return False
    return True

def yellow_letter_check(word, green_letters, yellow_letters):
    open_spots = [i for i, x in enumerate(green_letters) if x == None]  # Enumeration of unmatched letters
    current_word = [char for char in word]                              # List of each letter in the word being tested

    if any(current_word[i] in yellow_letters for i in open_spots):
        return True
    return False

def next_word(wordlist, green_letters, yellow_letters, guess_history):
    next_guess = None
    for word in generate_five_letter(wordlist, green_letters, guess_history):
        # Compare current matched letters to generated list of five letter words
        if green_letter_check(word, green_letters):
            if yellow_letter_check(word, green_letters, yellow_letters):
                print('✔️  ', word)
                next_guess = word
            else:
                print('🟨', word)  # If matched letters == guessed word BUT close letters not in guessed word
                if next_guess == None:
                    next_guess = word
        else:
            print('❌ ', word)  # If matched letters != guessed word
    return next_guess
    
    
def play_wordle():
    """ Main function in order to play Wordle"""

    discard_pile, guess_history, close_history = [], [], []

    # todays_word = todays_wordle().lower()
    todays_word = 'snoop'
    wordlist = download_wordlist()

    print(f"\nTodays wordle is:  {todays_word}\nYour guess is:\t   {first_word()}\n{'='*9}")

    result, close_letters, wrong_letters, wordle_guess = compare_words(todays_word, first_word())
    print(close_letters, wrong_letters)
    discard_pile.extend(wrong_letters)      # List of letters that are not in today's Wordle
    close_history.extend(close_letters)     # List of letters in today's Wordle that are out of order
    guess_history.append(wordle_guess)      # List of guess attempt at today's Wordle

    if result == [char for char in todays_word]:
        return print('WORDLE')

    # The word is: SPOON
    # First guess: SPORT 🟩🟩🟩⬜⬜
    # Secnd guess: SPOOF 🟩🟩🟩🟩⬜

    print(f"""{'='*9}
The next guess should be:  {next_word(wordlist, result, close_history, guess_history)}
Current board:  {result}
Yellow letters: {close_history}
Discard pile:   {discard_pile}
Guess history:  {guess_history}
""")

play_wordle()