import re
import random

HANGING_THING = """
-------------------
|                 |
|                 |
|             =========
|           ||   0 0   ||    
|           ||   ___   ||
|             =========   
|                /|\\      
|               / | \\     
|              /  |  \\    
|                 |            
|                / \\
|               /   \\
|              /     \\
|             /       \\
|                 
|------------------------------
"""


class Hangman:
    """Terminal Hangman"""
    def __init__(self, length=4, word=None):
        if not word:
            with open('words.txt', 'r') as f:
                words = [w for w in f.read().split('\n') if len(w) == length]

            self.word = random.choice(words)

        else:
            self.word = word.lower()

        self.wrongs_so_far = 0
        self.found = []
        self.wrongs = []
        self.template = re.sub(pattern='[^\s]', repl='_', string=self.word)
        print(self.template)

    def __str__(self):
        return f"""
            Word: {self.word},
            Hint: {self.template}
        """

    def update_template(self):
        self.template = re.sub(pattern=f'[^\s{"".join([l for l in self.found])}]', repl='_', string=self.word)

    def attempt(self):

        not_guessed_yet = False
        guess = ''
        while not not_guessed_yet:
            if guess:
                print('You have already tried that letter. Try again!')
            guess = input('Try a letter: ')
            if len(guess) > 1:
                if guess == self.word:

                    self.template = self.word

                else:
                    print('that is not the word')
                    self.wrongs_so_far += 1
                    self.wrongs.append(guess)

                print(self.draw())
                print()
                print(self.template)
                print()
                print(f'Wrongs: {", ".join([letter for letter in self.wrongs])}')
                return

            not_guessed_yet = guess not in self.wrongs

        # [indexes]
        occurrences = []
        for i in range(len(self.word)):
            if self.word[i] == guess:
                print('Correct letter')
                occurrences.append(i)

        # len of occurrences > 0:
        #   guess is correct
        # else
        #   guess in incorrect
        if occurrences:
            self.found.append(guess)

        else:
            self.wrongs_so_far += 1
            self.wrongs.append(guess)

        self.update_template()

        print(self.draw())
        print()
        print(self.template)
        print()
        print(f'Wrongs: {", ".join([letter for letter in self.wrongs])}')

    def draw(self):
        lines = ""
        hanging_thing_lines = HANGING_THING.split('\n')

        for i in range(len(hanging_thing_lines)):
            conditions = (
                    i <= 3 or
                    i >= 16 or
                    (self.wrongs_so_far >= 1 and i <= 7) or
                    (self.wrongs_so_far >= 4 and i <= 11) or
                    (self.wrongs_so_far >= 7 and i <= 15)
            )

            if conditions:
                to_add = hanging_thing_lines[i]

                if self.wrongs_so_far < 6 or (self.wrongs_so_far < 8 and i >= 12):
                    to_add = to_add.replace('\\', ' ')

                    if self.wrongs_so_far < 5:
                        to_add = to_add.replace('/', ' ')

                        if self.wrongs_so_far < 3:
                            to_add = to_add.replace(' ___ ', '     ')

                            if self.wrongs_so_far < 2:
                                to_add = to_add.replace('0', ' ')

                lines = lines + '\n' + to_add

            else:
                lines = lines + '\n' + '|'

        if self.wrongs_so_far >= 9:
            return lines.replace('0', 'x')
        return lines

    def play(self):
        # game loop
        while self.wrongs_so_far < 9:
            self.attempt()
            if self.word == self.template:
                print(f'You won!\nThe word was {self.word}')
                return

        print(f'You Lost!\nThe word was {self.word}')


def main():
    h = Hangman()
    h.play()


if __name__ == '__main__':
    main()
