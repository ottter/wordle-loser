# wordle-loser

Unintelligent Wordle solving AI that is designed to be plugged in to a Discord chatbot

## Usage

```py
starting_word=| first_word()             | Add any chosen 5 letter word as string
custom_list=  | False                    | Add a '\n' separated text file to /wordlists
wordle=       | todays_wordle()['answer']| Add any 5 letter word to be the Wordle
method=       | 'quick'                  | Use 'brown' to sort custom wordlist by usage
print_output= | False                    | Print output to the console
```

```py
# Output from running play_wordle()
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

## Sources

- API to gather Wordle info: [source](https://rapidapi.com/Alejandro99aru/api/wordle-answers-solutions/)
- Valid Word list:           [source](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93)
