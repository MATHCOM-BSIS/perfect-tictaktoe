from ursina import *
import numpy as np

####################### 보드 UI 생성 클래스

class Board():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.board = np.zeros((self.h, self.w), dtype=np.int)
        self.big_board = np.zeros((3,3), dtype = np.int)

    def __repr__(self):
        string = ''
        for y in range(self.h):
            for x in range(self.w):
                string += '%d ' % self.board[y][x]
            string += '\n'
        return string

################### 게임 총 관리 클래스

class Omok():  
    def __init__(self, board):
        self.board = board
        self.current_player = 1
        self.won_player = 0
        self.last_pos = [-1,-1]

    def reset(self):
        self.board.board = 0
        self.board.big_board = 0
        self.current_player = 1
        self.won_player = 0

    def put(self, x=None, y=None):
        if x is None and y is None:
            while True:
                rand_x = np.random.randint(0, self.board.w)
                rand_y = np.random.randint(0, self.board.h)

                if self.board.board[rand_y][rand_x] == 0:
                    self.board.board[rand_y][rand_x] = self.current_player
                    break
        else:
            self.board.board[y][x] = self.current_player

    def next(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    ######################################################################## 승리조건 함수 시작

    def check_won(self):
        player = self.current_player
        for t in range(0,10,3):
            for y in range(3):
                for x in range(3):
                    try:
                        if (self.board.board[t][x] == player
                            and self.board.board[t+1][x] == player
                            and self.board.board[t+2][x] == player):
                            
                            self.won_player = player
                            break
                    except:
                        pass

                    try:
                        if (self.board.board[y][x] == player
                            and self.board.board[y][x+1] == player
                            and self.board.board[y][x+2] == player):
                            
                            self.won_player = player
                            break
                    except:
                        pass

                    try:
                        if (self.board.board[y][x] == player
                            and self.board.board[y+1][x+1] == player
                            and self.board.board[y+2][x+2] == player):
                            
                            self.won_player = player
                            break
                    except:
                        pass

                    try:
                        if (x >= 4 and self.board.board[y][x] == player
                            and self.board.board[y+1][x-1] == player
                            and self.board.board[y+2][x-2] == player):
                            
                            self.won_player = player
                            break
                    except:
                        pass

                if self.won_player > 0:
                    break
            
            return self.won_player

    ############################################################################## 승리조건 함수 끝



##################### 메인 UI 함수

w, h = 9, 9

app = Ursina()

window.borderless = False
window.color = color._50

camera.orthographic = True
camera.fov = 23
camera.position = (w//2, h//2)

board = Board(w=w, h=h)
board_buttons = [[None for x in range(w)] for y in range(h)]
game = Omok(board=board)

last_pos = [-1,-1]

Entity(model='cube', scale=12, color=color._230, x=w//2, y=h//2, z=20)

Entity(model=Grid(w, h), scale=w, color=color.black,
       x=w//2, y=h//2, z=0.1)

Entity(model=Grid(w//3, h//3, thickness=3), scale=w, color=color.black,
       x=w//2, y=h//2, z=0.1)

for y in range(h):
    for x in range(w):
        b = Button(parent=scene, position=(x, y),
                   color=color.clear,scale=0.9)
        board_buttons[y][x] = b

        def placement(x3, pos):
            npos = [pos[0]%3, pos[1]%3]

            avpos = []
            for j in range(0, 3):
                temp = []
                for i in range(0, 3):
                    temp.append(0)
                avpos.append(temp)

            if x3[npos[1]][npos[0]] == 0:
                avpos[npos[1]][npos[0]] = 1
            else:
                for i in range(0, 3):
                    for j in range(0, 3):
                        if x3[i][j] == 0:
                            avpos[i][j] = 1

            return avpos

        def on_mouse_enter(b=b):
            if b.collision:
                b.color = color._200
                
        def on_mouse_exit(b=b):
            if b.collision:
                b.color = color.clear

        b.on_mouse_enter = on_mouse_enter
        b.on_mouse_exit = on_mouse_exit

        def on_click(b=b):

            x, y = int(b.position.x), int(h - b.position.y - 1)
            if game.last_pos[0] == -1 and game.last_pos[1] == -1:
                avpos = np.ones((3,3), dtype=int)
            else:
                avpos = np.array(placement(board.big_board, game.last_pos))

            if avpos[x//3][y//3]:
                if game.current_player == 1:
                    b.model = Circle(resolution=32, mode='line', radius=0.4, thickness=3)
                    b.color = color.blue
                else:
                    b.texture = 'x.png'
                b.collision = False

                game.put(x=x, y=y)

                won_player = game.check_won()
                if won_player:
                    Panel(z=1, scale=10, model='quad')
                    _string = "Player "

                    if won_player == 1: _string+="1 (O) won!"
                    elif won_player == 2: _string+="2 (X) won!"

                    t = Text(_string, scale=3, origin=(0, 0), background=True)
                    t.create_background(padding=(.5,.25), radius=Text.size/2)
                
                game.last_pos = [x,y]

                game.next()

                print(game.board)

        b.on_click = on_click

app.run()
