import random
from itertools import permutations
import tkinter as tk
from tkinter import messagebox, ttk

class Guess1A2B:

    ans = []
    n = 0

    def __init__(self, n=4):
        self.n = n
        self.ans = random.sample(list(range(0, 10)), n)
    
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


class Guess1A2BGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('1A2B 猜數字')
        self.root.geometry('520x520')
        self.root.resizable(False, False)
        self.digits = tk.StringVar()
        self.attempts = 0
        self.max_attempts = 20
        self.game = None

        style = ttk.Style()
        style.configure('Title.TLabel', font=('TkDefaultFont', 18, 'bold'))
        style.configure('Result.TLabel', font=('TkDefaultFont', 12))

        main = ttk.Frame(root, padding=20)
        main.pack(fill='both', expand=True)

        ttk.Label(
            main,
            text='1A2B 猜數字',
            style='Title.TLabel',
        ).pack(pady=(0, 5))
        self.instruction = ttk.Label(
            main,
            text='猜一組 4 個不重複的數字',
            foreground='#555555',
        )
        self.instruction.pack(pady=(0, 15))

        controls = ttk.Frame(main)
        controls.pack(fill='x')

        self.guess_entry = ttk.Entry(
            controls,
            textvariable=self.digits,
            font=('TkDefaultFont', 16),
            width=12,
            justify='center',
        )
        self.guess_entry.pack(side='left', expand=True, padx=(0, 10))
        self.guess_entry.bind('<Return>', lambda event: self.submit_guess())

        ttk.Button(
            controls,
            text='猜！',
            command=self.submit_guess,
        ).pack(side='left', padx=(0, 10))
        ttk.Button(
            controls,
            text='開新遊戲',
            command=self.new_game,
        ).pack(side='left')

        self.status = ttk.Label(
            main,
            text='',
            style='Result.TLabel',
        )
        self.status.pack(pady=12)

        history_frame = ttk.LabelFrame(main, text='猜測紀錄', padding=10)
        history_frame.pack(fill='both', expand=True)

        columns = ('number', 'guess', 'result')
        self.history = ttk.Treeview(
            history_frame,
            columns=columns,
            show='headings',
            height=12,
        )
        self.history.heading('number', text='#')
        self.history.heading('guess', text='猜測')
        self.history.heading('result', text='結果')
        self.history.column('number', width=40, anchor='center')
        self.history.column('guess', width=180, anchor='center')
        self.history.column('result', width=180, anchor='center')
        self.history.pack(fill='both', expand=True)

        self.new_game()

    def new_game(self):
        self.game = Guess1A2B(4)
        self.attempts = 0
        self.digits.set('')
        self.status.config(text='遊戲開始！請輸入 4 個不重複的數字。')
        self.history.delete(*self.history.get_children())
        self.guess_entry.config(state='normal')
        self.guess_entry.focus_set()

    def submit_guess(self):
        if self.game is None:
            return

        text = self.digits.get().strip()
        if len(text) != self.game.n:
            messagebox.showwarning(
                '輸入錯誤',
                f'請輸入剛好 {self.game.n} 個數字。',
                parent=self.root,
            )
            return
        if not text.isdigit():
            messagebox.showwarning(
                '輸入錯誤',
                '請只輸入數字 0 到 9。',
                parent=self.root,
            )
            return
        if len(set(text)) != self.game.n:
            messagebox.showwarning(
                '輸入錯誤',
                '每個數字只能使用一次。',
                parent=self.root,
            )
            return

        guess = [int(digit) for digit in text]
        a, b = self.game.check_ans(guess)
        self.attempts += 1
        self.history.insert(
            '',
            'end',
            values=(self.attempts, text, f'{a}A{b}B'),
        )
        self.history.see(self.history.get_children()[-1])

        if a == self.game.n:
            self.status.config(text=f'答對了！答案是 {text}')
            self.guess_entry.config(state='disabled')
            messagebox.showinfo(
                '恭喜過關',
                f'答案正確：{text}\n共猜了 {self.attempts} 次。',
                parent=self.root,
            )
        elif self.attempts >= self.max_attempts:
            answer = ''.join(str(digit) for digit in self.game.ans)
            self.status.config(text=f'遊戲結束！答案是 {answer}')
            self.guess_entry.config(state='disabled')
            messagebox.showinfo(
                '遊戲結束',
                f'已達 {self.max_attempts} 次猜測上限。\n答案是 {answer}。',
                parent=self.root,
            )
        else:
            self.status.config(
                text=f'結果：{a}A{b}B，剩餘 {self.max_attempts - self.attempts} 次'
            )

        self.digits.set('')
        self.guess_entry.focus_set()


def main():
    root = tk.Tk()
    Guess1A2BGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    