# wordle-loser

Unintelligent Wordle solving AI that is designed to be plugged in to a Discord chatbot

## Usage

`play_wordle(starting_word='crane', custom_list='wordlists/sorted-valid-wordle-words.txt', print_output=True)`

Accepted arguments for `play_wordle()`:

```txt
Argument      | Default                  | Action
starting_word=| first_word()             | Add any chosen 5 letter word as string
custom_list=  | False                    | Add a '\n' separated text file to /wordlists
wordle=       | todays_wordle()['answer']| Add any 5 letter word to be the Wordle
method=       | 'quick'                  | Use 'brown' to sort custom wordlist by usage
print_output= | False                    | Print output to the console
```

```py
# Returned values from running play_wordle()
wordle_dictionary = {
    "wordle": wordle,               # (str) Wordle used being word
    "wordle_num": wordle_num,       # (int) Which Wordle number it is
    "emoji_block": emoji_block,     # (str) Emoji squares showing the guesses
    "guess_history": guess_history, # (list) All words used as guesses
    "guess_count": i+1,             # (int) How many guesses it took to solve
    "guess_path": " > ".join(guess_history),  # (str) All words used as guesses
    "discard_pile": discard_pile    # (list) Letters guessed that aren't used
    }
```

## Custom Wordlist

Custom wordlists can also be used, if in a `\n` separated text file, like the contents of `./wordlists`. There
are some methods of sorting these custom word lists by running `sort_textfile()`. This only needs to be ran once
per wordlist and can be removed after.

`sort_textfile(outfile='sorted-valid-wordle-words.txt', plurals=True)`

 ```txt
Argument   | Default                        | Action
subdir=    | 'wordlists/'                   | Directory path where wordlists are stored
infile=    | 'valid-wordle-words.txt'       | Input filename (to be sorted)
outfile=   | 'sorted-valid-wordle-words.txt'| Output filename
plurals=   | False                          | Choose to put plural words at the end of list
```

## Example Run

Result from `play_wordle(custom_list='wordlists/sorted-valid-wordle-words.txt', print_output=True)`

```txt
Opening guess: adieu

========================================
Next guess:     group
Current board:  [None, None, None, None, None]
Yellow letters: ['u']
Discard pile:   ['d', 'i', 'a', 'e']
Guess history:  ['adieu']

⬜⬜⬜⬜🟨

========================================
Next guess:     grouf
Current board:  ['g', 'r', 'o', 'u', None]
Yellow letters: []
Discard pile:   ['d', 'i', 'a', 'e', 'p']
Guess history:  ['adieu', 'group']

⬜⬜⬜⬜🟨
🟩🟩🟩🟩⬜

========================================
Next guess:     grout
Current board:  ['g', 'r', 'o', 'u', None]
Yellow letters: []
Discard pile:   ['d', 'i', 'a', 'e', 'p', 'f']
Guess history:  ['adieu', 'group', 'grouf']

⬜⬜⬜⬜🟨
🟩🟩🟩🟩⬜
🟩🟩🟩🟩⬜

========================================

WORDLE 640 4/6* GROUT
⬜⬜⬜⬜🟨
🟩🟩🟩🟩⬜
🟩🟩🟩🟩⬜
🟩🟩🟩🟩🟩
Path: adieu > group > grouf > grout
```

Some improved sorting by word popularity can still be done, unless `grouf` really is more common than `grout`.

## Sources

- [RapidAPI used to gather daily Wordle info](https://rapidapi.com/Alejandro99aru/api/wordle-answers-solutions/)
- [List of valid Wordle words](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93)
- [More on language processing, NLTK, and sorting words](https://www.nltk.org/book_1ed/ch05.html)
- [Brown Corpus](https://en.wikipedia.org/wiki/Brown_Corpus)
