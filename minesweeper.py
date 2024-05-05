import random

class MinesGame:
    w = 1
    h = 1
    mines_count = 1
    board = [] # ans
    game = [] # game current view from user
    brain = [] # game view from AI brain, 
               # -2 is unkown
               # -1 is no mines or all mines appear and AI already click spaces around this cell
               # -3 is mine
    status = 'alive' # 'alive', 'pass', 'fail'
    click_count = 0

    def __init__(self, h, w, mines_count):
        self.h = h
        self.w = w
        self.mines_count = mines_count

        for i in range(h):
            self.board += [ [0]*w ]

        m_loc = random.sample(list(range(0, w*h)), mines_count)

        for loc in m_loc:
            i = loc//w
            j = loc%w
            self.board[i][j] = 'x'
            for a in range(i-1, i+2):
                for b in range(j-1, j+2):
                    if a>=0 and a<self.h and b>=0 and b<self.w:
                        if self.board[a][b] != 'x':
                            self.board[a][b] += 1
        
        for i in range(self.h):
            for j in range(self.w):
                if self.board[i][j] == 'x':
                    pass
                elif self.board[i][j] == 0:
                    self.board[i][j] = ' '
                else:
                    self.board[i][j] = chr(ord('0') + self.board[i][j])

    def print_sub(self, m):
        print('-'*(self.w+2))
        for one in m:
            print('|' + ''.join(one) + '|')
        print('-'*(self.w+2))

    def print(self):
        print(f'h={self.h}, w={self.w}, mines_count={self.mines_count}, click_count={self.click_count}')
        self.print_sub(self.board)
        self.print_sub(self.game)

        if 0:
            tmp_brain = []
            for i in range(self.h):
                tmp_brain += [ ['?']*self.w ]
            for i in range(self.h):
                for j in range(self.w):
                    if self.brain[i][j] == -1:
                        tmp_brain[i][j] = '*'
                    elif self.brain[i][j] == -3:
                        tmp_brain[i][j] = 'x'
                    elif self.brain[i][j] >= 0:
                        tmp_brain[i][j] = chr(ord('0') + self.brain[i][j])
            self.print_sub(tmp_brain)

        if self.status != 'alive':
            print(f'game ends! result={self.status}')

    def cal_mines_count(self, i, j):
        mines = 0
        unknown = 0
        for a in range(i-1, i+2):
            for b in range(j-1, j+2):
                if a>=0 and a<self.h and b>=0 and b<self.w:
                    if self.game[a][b] == 'x':
                        mines += 1
                    elif self.game[a][b] == '?':
                        unknown += 1
        return mines, unknown

    def click_sub(self, i, j):
        if self.game[i][j] != '?': return
        bb = self.board[i][j]
        #print(f'click_sub: {i}, {j}, {bb}')

        if bb == 'x':
            self.game[i][j] = '!'
            raise Exception()
        elif bb == ' ':
            self.game[i][j] = ' '
            self.brain[i][j] = 0
        else:
            self.game[i][j] = bb
            self.brain[i][j] = ord(bb) - ord('0')

    def click_0(self):
        hit = True
        hit_ever = False
        while hit:
            hit = False
            for i in range(self.h):
                for j in range(self.w):
                    if self.brain[i][j] == 0:
                        self.brain[i][j] = -1
                        hit = True
                        hit_ever = True
                        for a in range(i-1, i+2):
                            for b in range(j-1, j+2):
                                if a>=0 and a<self.h and b>=0 and b<self.w:
                                    self.click_sub(a, b)
        return hit_ever

    def set_mines_flag(self):
        hit = True
        hit_0 = False
        while hit:
            hit = False
            for i in range(self.h):
                for j in range(self.w):
                    if self.brain[i][j] > 0:
                        mines, unknown = self.cal_mines_count(i, j)
                        if self.brain[i][j] == mines:
                            self.brain[i][j] = 0
                            hit_0 = True
                        elif self.brain[i][j] == (mines+unknown):
                            self.brain[i][j] = -1
                            hit = True
                            for a in range(i-1, i+2):
                                for b in range(j-1, j+2):
                                    if a>=0 and a<self.h and b>=0 and b<self.w:
                                        if self.game[a][b] == '?':
                                            self.game[a][b] = 'x'
                                            self.brain[a][b] = -3
        return hit_0

    def verify_complete(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.game[i][j] == '?': return False
        return True

    def click(self, i, j):
        try:
            if self.game[i][j] == '?':
                #print(f'click: {i:02}, {j:02}')
                self.click_count += 1

                self.click_sub(i, j)
                self.click_0()
                hit = self.set_mines_flag()
                while hit:
                    hit = self.click_0()
                    if hit:
                        hit = self.set_mines_flag()
                if self.verify_complete():
                    self.status = 'pass'
        except:
            self.status = 'fail'

    def go(self):
        self.click_count = 0
        self.status = 'alive'

        self.game = []
        for i in range(self.h):
            self.game += [ ['?']*self.w ]

        self.brain = []
        for i in range(self.h):
            self.brain += [ [-2]*self.w ]

        click_loc = list(range(self.h*self.w))
        random.shuffle(click_loc)
        for loc in click_loc:
            i = loc//self.w
            j = loc%self.w
            self.click(i, j)
            if self.status != 'alive':
                break

    def go_performance(self):
        pass_count = 0
        total_count = 100
        for i in range(total_count):
            self.go()
            if self.status == 'pass':
                pass_count += 1
        print(f'total_count={total_count}, pass_count={pass_count}')

if __name__ == '__main__':
    mines_game = MinesGame(16, 16, 40)
    
    mines_game.go_performance()
    
    #mines_game.go()
    #mines_game.print()