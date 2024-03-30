from random import choice
import yaml
from rich.console import Console
import pandas as pd


class Guesser:
    '''
        INSTRUCTIONS: This function should return your next guess. 
        Currently it picks a random word from wordlist and returns that.
        You will need to parse the output from Wordle:
        - If your guess contains that character in a different position, Wordle will return a '-' in that position.
        - If your guess does not contain thta character at all, Wordle will return a '+' in that position.
        - If you guesses the character placement correctly, Wordle will return the character. 

        You CANNOT just get the word from the Wordle class, obviously :)
    '''
    def __init__(self, manual):
        self.word_list = yaml.load(open('wordlist.yaml'), Loader=yaml.FullLoader)
        #self.word_list = yaml.load(open('dev_word_list.yaml'), Loader=yaml.FullLoader)
        self.word_list1 = pd.DataFrame(self.word_list)
        self.word_list1[['Letter1', 'Letter2', 'Letter3', 'Letter4', 'Letter5']] = self.word_list1[0].str.split('', expand=True).iloc[:, 1:6]
        self.word_list1.drop(0, axis=1, inplace=True)
        self._manual = manual
        self.console = Console()
        self._tried = []

    def restart_game(self):
        self._tried = []
        self.word_list1 = pd.DataFrame(self.word_list)
        self.word_list1[['Letter1', 'Letter2', 'Letter3', 'Letter4', 'Letter5']] = self.word_list1[0].str.split('', expand=True).iloc[:, 1:6]
        self.word_list1.drop(0, axis=1, inplace=True)



    def get_guess(self, result):
        #if self._manual=='manual':
        #    return self.console.input('Your guess:\n')
        #else:

        # Creating the dataframe that will be filtered
        df = self.word_list1

        # Filtering the dataframe based on the result
        if self._tried != []:
            for i in range(5):
                if result[i] == '+':
                    if str(self._tried[-1][i]) in result or str(self._tried[-1][i]) in str(self._tried[-1][0:i])+str(self._tried[-1][i+1:5]):
                        for j in range(5):
                            if str(self._tried[-1][j]) != str(self._tried[-1][j]):
                                df = df.loc[df.iloc[:, j] != str(self._tried[-1][i])]
                        df = df.loc[df.iloc[:, i] != str(self._tried[-1][i])]
                    else:
                        mask = ~df.apply(lambda row: row.str.contains(str(self._tried[-1][i]))).any(axis=1)
                        df = df[mask]
                elif result[i] == '-':
                    if str(self._tried[-1][i]) in result:
                        df = df.loc[df.iloc[:, i] != str(self._tried[-1][i])]
                    else:
                        df = df[df.apply(lambda row: row.str.contains(str(self._tried[-1][i])).any(), axis=1)]
                        df = df.loc[df.iloc[:, i] != str(self._tried[-1][i])]
                else:
                    df = df[(df.iloc[:, i].str.contains(str(result[i])))]

        # Creating list of the most possible letters
        dict1 = dict(df['Letter1'].value_counts())
        dict2 = dict(df['Letter2'].value_counts())
        dict3 = dict(df['Letter3'].value_counts())
        dict4 = dict(df['Letter4'].value_counts())
        dict5 = dict(df['Letter5'].value_counts())

        list1 = []
        for key, val in dict1.items():
            list1.append([key, val, 0])
        for key, val in dict2.items():
            list1.append([key, val, 1])
        for key, val in dict3.items():
            list1.append([key, val, 2])
        for key, val in dict4.items():
            list1.append([key, val, 3])
        for key, val in dict5.items():
            list1.append([key, val, 4])

        sorted_list = sorted(list1, key=lambda x: x[1], reverse=True)

        proposal = [0, 0, 0, 0, 0]
        if len(dict1) > 3 and len(dict2) > 3 and len(dict3) > 3 and len(dict4) > 3 and len(dict5) > 3:
            for litera, wart, numer in sorted_list:
                if proposal[numer] == 0 and litera not in proposal:
                    proposal[numer] = str(litera)
                if 0 not in proposal:
                    break
        else:
            for litera, wart, numer in sorted_list:
                if proposal[numer] == 0:
                    proposal[numer] = str(litera)
                if 0 not in proposal:
                    break

        guess = ''.join(proposal)


        if len(df) <= 2: #guess if there are only two or less possibilieties
            guess = df.iloc[0, 0] + df.iloc[0, 1] + df.iloc[0, 2] + df.iloc[0, 3] + df.iloc[0, 4]
        elif self._tried != []: #guess if 4 letters are already guessed and there are still more than two possibilities
            counter = 0
            pointer = 0
            for i in range(5):
                if result[i] == self._tried[-1][i]:
                    counter = counter + 1
                else:
                    pointer = i
            if counter == 4:
                pr = str()
                for i in range(min(5, len(df))):
                    proposal[i] = df.iloc[i, pointer]
                guess = ''.join(proposal)

        self.word_list1 = df
        self._tried.append(guess)
        self.console.print(guess)
        return guess