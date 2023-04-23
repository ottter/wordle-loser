from nltk.corpus import brown
import nltk

"""
Sorting order of operations:
1. Start with all valid Wordle words in alphabetical order
2. Sort list by frequency in Brown Corpus. 
3. (Optional) Send some quality words to the front
4. (Optional) Send words with uncommon letters to end of the list
5. (Optional) Send words with repeated letters to the end of the list
6. (Optional) Send words ending in 'y' to end. Explained in sort_y_words function
7. (Optional) Send plural words to end of list. These are rarely used
8. (Optional) Send previous Wordles to end of list. These are not (rarely?) reused
"""

def sort_bestchoice(word):
    """
    List of favorite/best words to use are sent to the front.
    Source: https://artofproblemsolving.com/blog/articles/the-math-of-winning-wordle
    """

    best_words = ['chare', 'crate', 'peart', 'speat', 'reast', 'trine', 
              'tread', 'blate', 'reist', 'alist', 'roate', 'raise',
              'raile', 'soare', 'arise', 'irate', 'orate', 'ariel',
              'arose', 'raine']

    if word in best_words:
        return False    # Pass (leave in place)
    else:
        return True     # Move to end of file

def sort_repeats(word):
    """
    Option within sort_textfile to have words with repeated letters looked at last.
    It will get to these eventually, but guessing words with unique letters should open
    up the board better. SHELL is more likely than SHOAT, but the latter has beter letters
    """
    for letter in word:
        if word.count(letter) > 1:
            return True         # Move to end of file
    return False                # Pass

def sort_uncommon(word):
    """
    Option to send words with uncommon letters to end of search list
    Letters: Q J X Z
    """
    uncommon_letters = ['q', 'j', 'x', 'z']
    for letter in uncommon_letters:
        if letter in word:
            return True         # Move to end of file
    return False                # Pass

def sort_history(word):
    """
    Option within sort_textfile to have previous Wordles looked at last.
    Previous Wordles are rarely, if ever used.
    """
    with open('wordlists/wordles-so-far.txt', 'r', encoding="utf-8") as previous_wordles:
        if word in previous_wordles.read() and word[-1] != 's':
            return True     # Move to end of file
        else:
            return False    # Pass
  
def sort_y_words(word):
    """
    Option within sort_textfile to have words ending in 'y' looked at last.
    If a 'y' is found in the word, but isn't the last letter, it'll get caught
    guessing many 'y'-ending words even though it's yellow. Not needed once
    hard mode is enabled.
    """
    if word[-1] == "y":
        return True     # Move to end of file
    else:
        return False    # Pass

def sort_plurals(word):
    """
    Option within sort_textfile to have plural words looked at last.
    Plural words are rarely, if ever used.
    """
    if word[-2] != 's' and word[-1] == "s":
        return True     # Move to end of file
    else:
        return False    # Pass

def sort_textfile(subdir='wordlists/',
                  infile='valid-wordle-words.txt',
                  outfile='sorted-valid-wordle-words.txt',
                  filter_plurals=False,
                  filter_history=False,
                  filter_y_words=False,
                  filter_repeats=False,
                  filter_uncommon=False,
                  filter_bestchoice=False):
    """Standalone function that sorts a textfile by most common words (Brown Corpus)"""
    # Open and read the original text file
    with open(subdir + infile, "r", encoding="utf-8") as my_infile:
        wordlist_sorted = my_infile.read().split("\n")
        print(f"Importing file: {subdir + infile}\n")

    # Sort the file based on frequency in Brown Corpus
    frequency = nltk.FreqDist([w.lower() for w in brown.words()])
    wordlist_sorted = sorted(wordlist_sorted, key=lambda x: frequency[x.lower()], reverse=True)
    print("-> Sorted all words by Brown Corpus frequency.")

    if filter_bestchoice:
        # If word is considered high quality due to letter dist, send to front
        # https://artofproblemsolving.com/blog/articles/the-math-of-winning-wordle
        print("-> Moved best words to the top.")
        wordlist_sorted = sorted(wordlist_sorted, key=sort_bestchoice)

    if filter_uncommon:
        # If the word contains uncommon letters, move to the end of the guess list
        print("-> Moved words with uncommon letters to the end.")
        wordlist_sorted = sorted(wordlist_sorted, key=sort_uncommon)

    if filter_repeats:
        # If the word ends in a plural, move to the end of the guess list
        print("-> Moved words with repeated letters to the end.")
        wordlist_sorted = sorted(wordlist_sorted, key=sort_repeats)

    if filter_y_words:
        # If word ends in 'y', move to end of the guess list
        print("-> Moved words ending in 'y' to the end.")
        wordlist_sorted = sorted(wordlist_sorted, key=sort_y_words)

    if filter_plurals:
        # If the word ends in a plural, move to the end of the guess list
        print("-> Moved plural-appearing words to the end.")
        wordlist_sorted = sorted(wordlist_sorted, key=sort_plurals)

    if filter_history:
        # If word has been a Wordle already, move to end of the guess list
        print("-> Moved words from previous Wordle days to the end.")
        wordlist_sorted = sorted(wordlist_sorted, key=sort_history)

    # Write sorted list to new text file
    with open(subdir + outfile, "w", encoding="utf-8") as my_outfile:
        for word in wordlist_sorted:
            my_outfile.write(word + "\n")
        print(f"\nWrote all changes to: {subdir + outfile}")

sort_textfile(filter_plurals=True,
              filter_history=True,
              filter_y_words=True,
              filter_repeats=True,
              filter_uncommon=True,
              filter_bestchoice=True
              )