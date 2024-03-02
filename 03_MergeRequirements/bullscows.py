import random
import cowsay
import sys
import urllib.request


def random_cow(strok: str)->str:
    who=random.choice(cowsay.list_cows())
    print(cowsay.cowsay(strok, cow=who))


def  inform(format_string: str, bulls: int, cows: int) -> None:
    random_cow(format_string.format(bulls, cows))


def ask(prompt: str, valid: list[str] = None) -> str:
    with open('R2-D2.cow','r') as my_cow_file:
        my_cow=cowsay.read_dot_cow(my_cow_file)
        print(cowsay.cowsay(prompt,cowfile=my_cow))
    if valid == None:
        return input()
    else:
        while True:
            result = input()
            if result in valid:
                return result
            print('Слово не подходит')


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = [(guess[i] == secret[i]) for i in range(min(len(guess),len(secret)))].count(True)
    cows = len(set(guess).intersection(set(secret)))
    return (bulls, cows)

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
            exit()




if len(sys.argv)<2:
    print("Нет словаря")
    exit()
try:
    dictionary=get_dictionary(sys.argv[1])
    if len(sys.argv)>2:
        wordslen=int(sys.argv[2])
    else:
        wordslen=5
    dictionary=[i for i in dictionary if len(i)==wordslen]
    gameplay(ask, inform, dictionary)
except Exception as e:
    print("Error")
