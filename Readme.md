```python
from wordleBot import *
```


```python
bot = WordleBot()
```


```python
len(bot.words_df)
```




    2309



### Enter Your Guess and The Game's Response

To Enter The Game's Response, Enter a string:
R - Red: letter is not in the puzzle's secret word
Y - Yellow: letter is in the puzzle, but in a different position
G = Green: correct letter in the correct placement

For example, 

If you guessed the word `least` and got the folliwing response:  

<img src="./wordle_feedback_example.jpeg"></img>

You'd enter `RRYRY` as the games response.

The entire entry would be:

`bot.clue_update('least', 'RRYRY')`


```python
bot.clue_update('least', 'RRYRY')
# bot.return_best_words(toPrint=True)
# print(bot.words_and_scores[:5])
```

    43 words still remaining.



```python
bot.return_best_words()
print("\nTop guesses and average words remaning if guessed:\n",
      bot.words_and_scores[:5])
```

    1 of 43   [                   ] Time Remaining: 29.6
    Long compute time. Defaulting to heuristic sampling.
    10 of 10   [====================] Complete. Process took: 10.3
    Top guesses and average words remaning if guessed:
     [('batty', 4.02), ('party', 4.12), ('tacky', 4.49), ('tawny', 4.81), ('antic', 4.95)]

