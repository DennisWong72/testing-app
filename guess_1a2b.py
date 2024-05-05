import random
from itertools import permutations

class Guess1A2B:

    ans = []
    n = 0

    def __init__(self, n=4):
        self.n = n
        self.ans = random.sample(list(range(0, 10)), n)
        print(f'ans={self.ans}')
    
    def check(self, guess, target):
        a = 0
        b = 0
        for i in range(self.n):
            if guess[i] == target[i]:
                a += 1
            elif guess[i] in target:
                b += 1
        return a,b
    
    def check_ans(self, guess):
        a,b = self.check(guess, self.ans)
        print(f'guess={guess}, result={a}a{b}b')
        return a,b
    
    def go(self):
        all_guess = list(permutations(range(0, 10), self.n))
        step = 0
        result = 'fail'
        while step < 20:
            print('len of all_guess =', len(all_guess))
            step += 1
            guess = random.choice(all_guess)
            a,b = self.check_ans(guess)
            if a == self.n:
                result = 'succ'
                break
            all_guess = [x for x in all_guess if self.check(x, guess) == (a, b)]

        print(f'result={result}, step={step}')
        return result, step

if __name__ == '__main__':
    guess = Guess1A2B(5)
    guess.go()
    