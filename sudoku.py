import time

class MyGV:
    find_ans_count = 1
    ans = []
    call_count = 0
    call_level = 0
    call_level_max = 0
gv = MyGV()

def same_row(i,j): return (i//9 == j//9)
def same_col(i,j): return (i-j) % 9 == 0
def same_block(i,j): return (i//27 == j//27 and i%9//3 == j%9//3)

"""
type of param board in all functions are the same.
it's list of char, e.g., ['1', '2', '.', ...], '.' means space in sudoku
it follows below format:
    question = \
          '3......6.' \
        + '.8.2.....' \
        + '7..43...9' \
        + '.......57' \
        + '4..5..6..' \
        + '1...8....' \
        + '.2.1...9.' \
        + '.....9..3' \
        + '.9.8.61..'
    board = list(question)
"""

def solve_sudoku(board, find_ans_count=1):
    """
    find the ans of sudoku

    param find_ans_count: int, the ans count you want
    """
    gv.find_ans_count = find_ans_count
    gv.ans = []
    gv.call_count = 0
    gv.call_level = 0
    gv.call_level_max = 0

    t1 = time.time()
    __solve_sudoku(board)
    t2 = time.time()
    exec_sec = t2-t1

    return gv.ans, exec_sec, gv.call_count, gv.call_level_max

def print_sudoku(board):
    """
    print sudoku
    """
    for i in range(9):
        a = board[i*9:i*9+9]
        a[6:6] = '|'
        a[3:3] = '|'
        b = ''.join(a)
        print(b)
        if i%3==2:
            print('-'*11)

def __cal_exclude(board, idx):
    """
    return all char already existed in the same row, same column and same block.
    """
    return {board[j] for j in range(81) if same_row(idx,j) or same_col(idx,j) or same_block(idx,j)} - {'.'}

def __solve_sudoku(board):
    """
    find the ans of sudoku
    """
    gv.call_count += 1
    gv.call_level += 1
    gv.call_level_max = max(gv.call_level_max, gv.call_level)

    if 1:
        hit = True
        while hit:
            hit = False
            bidx = -1
            blen = 0
            bexclude = set()
            for idx in range(81):
                if board[idx] == '.':
                    exclude = __cal_exclude(board, idx)
                    ex_len = len(exclude)
                    if ex_len == 9:
                        # board[idx] has no possible numbers, terminate this way, go back to other ways
                        gv.call_level -= 1
                        return
                    if ex_len == 8:
                        # board[idx] has only one possible number, just set it
                        cand = list(set('123456789')-exclude)
                        board[idx] = cand[0]
                        hit = True
                    else:
                        # find the largest set of existing numbers (smallest set of possible numbers)
                        if ex_len > blen:
                            bidx = idx
                            blen = ex_len
                            bexclude = exclude
    else:
        # simple but spend time too much
        bidx = board.index('.') if '.' in board else -1
        bexclude = __cal_exclude(board, bidx)

    # ans is found
    if bidx == -1: 
        gv.ans += [board]
        gv.call_level -= 1
        return
    
    # ans is not found, try next space
    for m in set('123456789')-bexclude:
        __solve_sudoku(board[:bidx]+[m]+board[bidx+1:])
        if len(gv.ans) >= gv.find_ans_count:
            break
    gv.call_level -= 1
    return

def verify_sudoku(board):
    """
    verify sudoku is completed and ans is right
    """
    for idx in range(81):
        exclude = __cal_exclude(board, idx)
        if len(exclude) != 9:
            return False
    return True

def test_sudoku(board, find_ans_count=1):
    """
    test sudoku, including solve, verify and print
    """
    ans, exec_sec, call_count, call_level_max = solve_sudoku(board, find_ans_count)
    print(f'ans count={len(ans)}, exec sec={exec_sec:.2f}, call count={call_count}, call_level_max={call_level_max}')
    
    for one in ans:
        print(f'verify sudoku={verify_sudoku(one)}')
        print_sudoku(one)

if __name__ == '__main__':
    question1 = \
        '3......6.' \
      + '.8.2.....' \
      + '7..43...9' \
      + '.......57' \
      + '4..5..6..' \
      + '1...8....' \
      + '.2.1...9.' \
      + '.....9..3' \
      + '.9.8.61..'
    
    # hardest
    question2 = \
        '8........' \
      + '..36.....' \
      + '.7..9.2..' \
      + '.5...7...' \
      + '....457..' \
      + '...1...3.' \
      + '..1....68' \
      + '..85...1.' \
      + '.9....4..'
    
    test_sudoku(list(question2), 2)