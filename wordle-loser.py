import requests
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

def generate_five_letter():
    """Generate all 5 letter words. Might not all be Wordle-approved"""
    nltk.download('words')
    words = nltk.corpus.words.words()
    five_letter_words = [word.lower() for word in words if len(word) == 5 and word.isalpha()]
    return five_letter_words

def compare_words(wordle_guess):
    """Compare a submitted word against the days Wordle"""
    # todays_word = todays_wordle().lower()
    todays_word = 'spoon'
    if len(wordle_guess) != 5:
        return print("Error: Your guess word must be 5 letters long")
    
    result, wrong_letters, close_letters = [], [], []

    for i in range(5):
        if todays_word[i] == wordle_guess[i]:
            # result.append("match")
            result.append(todays_word[i])
        elif todays_word[i] in wordle_guess:
            # result.append("close")
            result.append(None)
            close_letters.append(todays_word[i])
        else:
            # result.append("wrong")
            result.append(None)
            wrong_letters.append(todays_word[i])
    wrong_letters = [*set(wrong_letters)]
    return result, close_letters, wrong_letters, wordle_guess

def play_wordle():
    """ Main function in order to play Wordle"""
    discard_pile, guess_history, close_history = [], [], []

    result, close_letters, wrong_letters, wordle_guess = compare_words("sport")
    discard_pile.extend(wrong_letters)      # List of letters that are not in today's Wordle
    close_history.extend(close_letters)     # List of letters in today's Wordle that are out of order
    guess_history.append(wordle_guess)      # List of guess attempt at today's Wordle

    print(result, close_history, discard_pile, guess_history)

play_wordle()