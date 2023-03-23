import requests
import random
import nltk
from config import API_KEY
from nltk.corpus import brown


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
    nltk.download('brown')
    return nltk.corpus.words.words()

def first_word():
    wordlist = ['adieu', 'media', 'arise', 'radio']
    return random.choice(wordlist)

def generate_five_letter(wordlist, green_letters, yellow_letters, discard_pile, guess_history):
    """Generate all 5 letter words. Might not all be Wordle-approved
       Remove words that don't match parameters determined by compare_words()
       """

    five_letter_words = [word.lower() for word in wordlist if len(word) == 5]
    # Remove words from the list that don't match the correct letter placements
    # Does not remove words that aren't possible due to close/yellow letters
    for word in five_letter_words.copy():
        for j, letter in enumerate(word):
            # Remove already guessed words from possible list
            if word in guess_history:
                five_letter_words.remove(word)
                break
            # Remove words with any discarded letters from list
            if letter in discard_pile:
                five_letter_words.remove(word)
                break
            # Remove words that have incorrect letters in previously solved positions
            if letter != green_letters[j] and green_letters[j] != None:
                five_letter_words.remove(word)
                break
    for word in five_letter_words.copy():
        for i in yellow_letters:
            if i not in word:
                five_letter_words.remove(word)
                break
    # for word in five_letter_words:
    #     print('✔️  ', word)
    # print(f"Possible words remaining: {len(five_letter_words)}")
    return five_letter_words

def compare_words(todays_word, wordle_guess):
    """Compare a submitted word against the days Wordle"""

    emoji_output = ""

    result, wrong_letters, close_letters = [], [], []

    if len(wordle_guess) != 5:
        return print("Error: Your guess word must be 5 letters long")
    
    if wordle_guess == todays_word:
        result = [char for char in todays_word]
        emoji_output = f"🟩🟩🟩🟩🟩"
        return result, [], [], todays_word, emoji_output

    for i in range(5):
        # If the letter in todays_word matches the guess, add to result list
        if todays_word[i] == wordle_guess[i]:
            result.append(todays_word[i])
            emoji_output = emoji_output + "🟩"
        # If the letter is anywhere within the guess, add to the close
        elif wordle_guess[i] in todays_word:
            result.append(None)                     # None gets added if there is no exact match to keep position
            close_letters.append(wordle_guess[i])
            emoji_output = emoji_output + "🟨"
        # If the letter is neither correct or misplaced, add to the discard pile
        else:
            result.append(None)
            wrong_letters.append(wordle_guess[i])
            emoji_output = emoji_output + "⬜"
    wrong_letters = [*set(wrong_letters)]           # Remove repeats from the discard pile
    return result, close_letters, wrong_letters, wordle_guess, emoji_output

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

def next_word(wordlist, green_letters, yellow_letters, discard_pile, guess_history, method):
    next_guess = None
    wordlist_sorted = []
    for word in generate_five_letter(wordlist, green_letters, yellow_letters, discard_pile, guess_history):
        # Compare current matched letters to generated list of five letter words
        if green_letter_check(word, green_letters):
            if yellow_letter_check(word, green_letters, yellow_letters):
                next_guess = word
            else:
                if next_guess == None:
                    next_guess = word
        wordlist_sorted.append(next_guess)

    if method == 'brown':
        frequency = nltk.FreqDist([w.lower() for w in brown.words()])
        wordlist_sorted = sorted(wordlist_sorted, key=lambda x: frequency[x.lower()], reverse=True)
    return wordlist_sorted[0]
    
def play_wordle(starting_word=first_word(), wordle=todays_wordle().lower(), method='quick', print_output=False):
    discard_pile, guess_history, close_history = [], [], []

    todays_word = wordle
    guess = starting_word.lower()
    wordlist = download_wordlist()
    emoji_block = ""

    for i in range(6):
        # Compare the guess word with the wordle of the day
        result, close_letters, wrong_letters, wordle_guess, emoji_output = compare_words(todays_word, guess)
        discard_pile.extend(wrong_letters)      # List of letters that are not in today's Wordle
        close_history.extend(close_letters)     # List of letters in today's Wordle that are out of order
        guess_history.append(wordle_guess)      # List of guess attempt at today's Wordle

        close_history = [*set(close_history)]   # Remove dupllicates from close_history

        emoji_block = f"{emoji_block}\n{emoji_output}"

        if result == [char for char in todays_word]:
            if print_output:
                print(f"{emoji_block}")
                print(f'WORDLE: {guess_history[-1]}\n'
                    f'It took {len(guess_history)} guesses\n'
                    f'Path: {" > ".join(guess_history)}\n')
            break
        
        # Update the guess word based on previous results and remamining words
        guess = next_word(wordlist, result, close_history, discard_pile, guess_history, method)
        if print_output:
            print(f"Next guess:   {guess}\n"
                f"Current board:  {result}\n"
                f"Yellow letters: {close_history}\n"
                f"Discard pile:   {discard_pile}\n"
                f"Guess history:  {guess_history}\n"
                f"{emoji_block}\n{'='*40}")

    wordle_dictionary = {
        "wordle": wordle,
        "emoji_block": emoji_block,
        "guess_history": guess_history,
        "guess_count": len(guess_history),
        "guess_path": " > ".join(guess_history),
    }
    return wordle_dictionary

play_wordle(method='quick', print_output=True)