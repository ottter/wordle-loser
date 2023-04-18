from nltk.corpus import brown
import nltk


def sort_plurals(word):
    """Option within sort_textfile to have plural words looked at last"""
    if word[-1] == 's':
        return True     # Move to end of file
    else:
        return False    # Pass

def sort_repeats(word):
    with open('wordlists/wordles-so-far.txt', 'r', encoding="utf-8") as previous_wordles:
        if word in previous_wordles.read() and word[-1] != 's':
            return True     # Move to end of file
        else:
            return False    # Pass

def sort_textfile(subdir='wordlists/',
                  infile='valid-wordle-words.txt',
                  outfile='sorted-valid-wordle-words.txt',
                  filter_plurals=False,
                  filter_repeats=False):
    """Standalone function that sorts a textfile by most common words (Brown Corpus)"""
    # Open and read the original text file
    with open(subdir + infile, "r", encoding="utf-8") as my_infile:
        data_list = my_infile.read().split("\n")
    # Sort the file based on frequency in Brown Corpus
    frequency = nltk.FreqDist([w.lower() for w in brown.words()])
    wordlist_sorted = sorted(data_list, key=lambda x: frequency[x.lower()], reverse=True)

    if filter_repeats:
        # If word has been a Wordle already, move to end of the guess list
        wordlist_sorted = sorted(wordlist_sorted, key=sort_repeats)

    if filter_plurals:
        # If the word ends in a plural, move to the end of the guess list
        wordlist_sorted = sorted(wordlist_sorted, key=sort_plurals)

    # Write sorted list to new text file
    with open(subdir + outfile, "w", encoding="utf-8") as my_outfile:
        for word in wordlist_sorted:
            my_outfile.write(word + "\n")

sort_textfile(filter_plurals=True, filter_repeats=True)