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

def first_word():
    # wordlist = ['adieu', 'media', 'arise', 'radio']
    wordlist = ['spoon']
    return random.choice(wordlist)

def generate_five_letter():
    """Generate all 5 letter words. Might not all be Wordle-approved"""
    nltk.download('words')
    words = nltk.corpus.words.words()
    five_letter_words = [word.lower() for word in words if len(word) == 5 and word.isalpha()]
    return five_letter_words

def compare_words(todays_word, wordle_guess):
    """Compare a submitted word against the days Wordle"""
    print('Todays word is: ', todays_word)

    if len(wordle_guess) != 5:
        return print("Error: Your guess word must be 5 letters long")
    
    if wordle_guess == todays_word:
        result = [char for char in todays_word]
        return result, [], [], [todays_word]
    
    result, wrong_letters, close_letters = [], [], []

    for i in range(5):
        if todays_word[i] == wordle_guess[i]:
            result.append(todays_word[i])
        elif todays_word[i] in wordle_guess:
            result.append(None)
            close_letters.append(todays_word[i])
        else:
            result.append(None)
            wrong_letters.append(todays_word[i])
    wrong_letters = [*set(wrong_letters)]
    return result, close_letters, wrong_letters, wordle_guess

def green_letter_check(word, green_letters):
    for i in range(len(word)):
        # Compare positions of random word with matched letters to find viable words
        if word[i] != green_letters[i] and green_letters[i] != None:
            return False
    return True

def yellow_letter_check(word, green_letters, yellow_letters):
    open_spots = [i for i, x in enumerate(green_letters) if x == None]  # Enumeration of unmatched letters
    current_word = [char for char in word]  # List of each letter in the word being tested

    if any(current_word[i] in yellow_letters for i in open_spots):
        return True
    return False

def next_word(green_letters, yellow_letters):
    mocklist = ['sprrt', 'teste', 'spoke', 'spqoo', 'sporn']
    for word in generate_five_letter():
    # for word in mocklist:
        # Compare current matched letters to generated list of five letter words
        if green_letter_check(word, green_letters):
            if yellow_letter_check(word, green_letters, yellow_letters):
                print('✔️  ', word)
                return word
            else:
                print('🟨', word)  # If matched letters == guessed word BUT close letters not in guessed word
        else:
            print('❌ ', word)  # If matched letters != guessed word
    
def play_wordle():
    """ Main function in order to play Wordle"""
    discard_pile, guess_history, close_history = [], [], []

    # todays_word = todays_wordle().lower()
    todays_word = 'spook'

    result, close_letters, wrong_letters, wordle_guess = compare_words(todays_word, first_word())
    discard_pile.extend(wrong_letters)      # List of letters that are not in today's Wordle
    close_history.extend(close_letters)     # List of letters in today's Wordle that are out of order
    guess_history.append(wordle_guess)      # List of guess attempt at today's Wordle

    if result == [char for char in todays_word]:
        return print('WORDLE')

    # The word is: SPOON
    # First guess: SPORT 🟩🟩🟩⬜⬜
    # Secnd guess: SPOOF 🟩🟩🟩🟩⬜
    close_history = []
    print('The next guess should be: ', next_word(result, close_history))

    print(result, close_history, discard_pile, guess_history)

play_wordle()