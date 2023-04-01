import random
import urllib.request
from colorama import init, Fore, Back, Style

init(autoreset=True)


class WordGame:
    def __init__(self):
        self.base_word = ""
        self.wordlist = []

    def generate_base_word(self):
        vowels = ['a', 'e', 'i', 'o', 'u']
        while True:
            base_word = "".join(random.choices(list('abcdefghijklmnopqrstuvwxyz'), k=15))
            if sum(base_word.count(vowel) for vowel in vowels) > 1:
                self.base_word = base_word
                break

    def load_wordlist(self):
        url = 'https://cwcodetest.s3.ca-central-1.amazonaws.com/wordlist.txt'
        response = urllib.request.urlopen(url)
        wordlist = response.read().decode().split('\n')
        return set(wordlist)

    def is_valid_word(self, word):
        return word in self.wordlist

    def calculate_score(self, word):
        score = 0
        for letter in word:
            score += 1
        return score

    def get_top_scores(self, scores_dict, n=10):
        scores = [(k, v) for k, v in scores_dict.items()]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]

    def play_game(self):
        print(f"{Fore.GREEN}Welcome to Word Game!{Style.RESET_ALL}")
        print("====================================")

        self.generate_base_word()
        print(f"Base word: {Fore.YELLOW}{self.base_word}{Style.RESET_ALL}")
        print("====================================")

        self.wordlist = self.load_wordlist()

        scores_dict = {}

        while True:
            print("Enter a word (or type 'exit' to quit): ")
            word = input().lower()

            if word == "exit":
                break

            if not all(letter in self.base_word for letter in word):
                print(f"{Fore.RED}Warning: Invalid input!{Style.RESET_ALL}")
                continue

            if not self.is_valid_word(word):
                print(f"{Fore.RED}Warning: '{word}' is not a valid word!{Style.RESET_ALL}")
                continue

            if word in scores_dict:
                print(f"{Fore.YELLOW}You've already submitted '{word}'!{Style.RESET_ALL}")
                continue

            score = self.calculate_score(word)
            scores_dict[word] = score

            print(f"{Fore.GREEN}Nice job! Your score is {score}.{Style.RESET_ALL}")
            print("====================================")

        top_scores = self.get_top_scores(scores_dict)

        if top_scores:
            print("Top scores:")
            for i, score in enumerate(top_scores):
                print(f"{i+1}. '{score[0]}' - {score[1]} points")
        else:
            print(f"{Fore.YELLOW}No top scores yet!{Style.RESET_ALL}")


game = WordGame()
game.play_game()
