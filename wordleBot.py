import nltk
from collections import Counter
# from functools import reduce
import pandas as pd
import numpy as np
from mTimer import mtimer

def letterfy(word_list) :
    return [element.lower() for w in word_list for element in list(set(w))]

def generate_word_query(L, isIn=True):
    if isIn:
        symbol = "="
        conjunction = "or"
    else:
        symbol = "!"
        conjunction = "and"
    query = "and (Letter1 {}= '{}' ". format (symbol, L)
    for i in range (2,6) :
        query+= "{} Letter{} {}='{}' ".format(conjunction, i, symbol, L)
    query += ")"
    return query

def clue_Update_Query(guessword, response):
    query = ""
    for idx, letter in enumerate(guessword):
        letterJudgement = response[idx]
        if letterJudgement == "G":
            query += "and (Letter{} == '{}')".format(idx+1, letter)
        elif letterJudgement == "Y":
            query += "and (Letter{} != '{}')".format(idx+1, letter)
            query += generate_word_query(letter)
        elif letterJudgement == "R":
            query += generate_word_query(letter, isIn=False)
        else:
            assert False, "Please ensure response is a string of RGY: GYGRY"
    query = query.strip("and ")
    return query

def generate_clueDeduction_query (guessword, possibleWord):
    query = ""
    for idx, letter in enumerate(guessword):
        #Does this letter match prospectword?
        if letter == possibleWord[idx]:
            #print(idx, Letter, possiblewordfidx)) #for debugging
            query += "and (Letter{} == '{}')".format(idx+1, letter)
        elif letter in possibleWord:
            query += "and (Letter{} != '{}')".format(idx+1, letter)
            query += generate_word_query(letter)
        else:
            query += generate_word_query(letter, isIn=False)
    query = query.strip("and ")
    return query

def score_first_guess(guess_word, toPrint=False):
    temp = words_df.copy()
    # letters_retrieved = 
    word_vector = temp.word.apply(lambda x: len(set(guess_word).intersection(x)))
    positions_vector = temp.word.apply(lambda x: sum([1 if x[i] == guess_word[i] else 0 for i in range(5) ]))
    if toPrint:
        print("Average letters retrieved: ", np.mean(word_vector),
              "Average correct number of positions: ", np.mean(positions_vector)
             )
    return (np.mean(word_vector), np.mean(positions_vector))

class WordleBot:
    def __init__(self):
        solution_words = []
        with open('solutions_nyt.txt') as f:
            for line in f.readlines():
                for w in line.split(","):
                    solution_words.append(w.strip().strip('"'))
        words_df = pd.DataFrame(solution_words)
        words_df.columns = ['word']
        for i in range(5):
            words_df['Letter{}'.format(i+1)] = words_df['word'].apply(lambda x: x[i])
        self.words_df = words_df

    def get_all_dict_words(self):
        word_list = nltk.corpus.words.words ()
        five_letter_words = [w for w in word_list if len(w)==5]
        all_all_words_df = pd.DataFrame(five_letter_words)
        all_words_df.columns = ['word']
        for i in range (5):
            all_words_df['Letter{}'.format(i+1)] = all_words_df['word'].apply(lambda x: x[i])
        all_words_df = all_words_df[all_words_df.Letter1 == all_words_df.Letter1.str.lower()]
        self.all_words_df = all_words_df

    def simulate(self, guessWord):
        #for each potential word, simulate the remaining words possible given the guess word
        haystacks =[]
        temp = self.words_df
        for possibleWord in temp.word:
            #Return clue from word
            #For Letter in, guessiond:
            haystacks.append(len(temp.query(generate_clueDeduction_query(guessWord, possibleWord))))
        return haystacks

    def return_best_words(self, toPrint=False):
        guessList = self.words_df.word
        guessList = list(guessList)
        scores = []
        words_and_scores = []
        timer = mtimer(guessList)
        cutoff = 10 #Maximum allowable compute time in seconds
        for i, word in enumerate(guessList):
            timer.progress(i)
            haystacks = self.simulate(word)
            score = round(np.mean(haystacks),2)
            scores.append(score)
            words_and_scores.append((word, score))
            if toPrint:
                print(f"{word} - average guesses till solution: {round(score,2)}")
            if (timer.estimated_process_length) and (timer.estimated_process_length)>cutoff:
                print("\nLong compute time. Defaulting to heuristic sampling.")
                df = self.words_df
                counts = Counter()
                for col in df.columns[1:]:
                    counts += Counter(df[col])
                    
                temp = df.set_index('word').copy()
                for col in temp.columns:
                    temp[col] = temp[col].map(counts)
                #Ensure 5 unique letters
                temp = temp[temp.nunique(axis=1)==5]
                temp = temp.sum(axis=1).sort_values(ascending=False)
                guessList = list(temp.sample(10, weights=temp).index)
                timer.len_tot = len(guessList)
                for i, word in enumerate(guessList):
                    timer.progress(i)
                    haystacks = self.simulate(word)
                    score = round(np.mean(haystacks),2)
                    scores.append(score)
                    words_and_scores.append((word, score))
                break

        min_idx = np.argmin(scores)
        best_score = scores[min_idx]
        best_word = guessList[min_idx]
        if toPrint:
            print ("In\n")
            print ("Best score: {} From word: {}".format(best_score, best_word))
        words_and_scores = sorted(words_and_scores, key=lambda x: x[1])
        self.words_and_scores = words_and_scores
        timer.complete()
    def clue_update(self, guessword, response):
    	query = clue_Update_Query(guessword, response)
    	self.words_df = self.words_df.query(query)
    	print("{} words still remaining.".format(len(self.words_df)))