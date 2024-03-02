import random
import cowsay
import sys
import urllib.request


def print_random_cow(strok: str)->str:
    print(cowsay.cowsay(strok))


def  inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def ask(prompt: str, valid: list[str] = None) -> str:
    if valid == None:
        return input()
    else:
        while True:
            result = input()
            if result in valid:
                return result
            print('Слово не подходит')


def bullscows(guess: str, secret: str) -> (int, int):
    bools = [(guess[i] == secret[i]) for i in range(min(len(guess),len(secret)))].count(True)
    cows = len(set(guess).intersection(set(secret)))
    return (bools, cows)

def get_dictionary(file:str)->list[str]:
    try:
    
        with open(file,'r') as f:
            dictionary=f.read().split()
            return dictionary
    except FileNotFoundError:
        try:
            maybeurl=urllib.request.urlopen(file)
            dictionary=maybeurl.read().decode().split()
            return dictionary
        except Exception as e:
            raise Exception("Словарь не найден")
        

def gameplay(ask:callable, inform:callable, words:list[str])-> int:
    word=random.choice(words)
    tries=0
    while True:
        guess=ask("Введите слово: ", words)
        tries+=1
        bulls, cows=bullscows(word, guess)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if word==guess:
            print(f'Потребовалось {tries} попыток')




if len(sys.argv)<2:
    print("Нет словаря")
    exit()
try:
    dictionary=get_dictionary(sys.argv[1])
    if len(sys.argv)>2:
        wordslen=int(sys.argv[2])
    else:
        wordslen=5
    dictioonary=[i for i in dictionary if len(i)==wordslen]
    gameplay(ask, inform, dictionary)
except Exception as e:
    print("Error")
