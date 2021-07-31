import tkinter
from tkinter import font
from tkinter.font import Font
from pprint import pprint
# from tkinter import Button # Windows, Linux
from tkmacosx import Button # for macOS (because of tkinter issue)
import random as rand
import time


# game settings
board = [' ' for _ in range(10)] # we leave board[0] always empty
USER = 'O'
BOT = 'X'

#tkinter settings
main = tkinter.Tk()
font1 = Font(family='Segoe UI', size=60)
font2 = Font(family='Segoe UI', size=24)


def isWin(board, turn):
    if board[1]==board[2]==board[3]==turn:
        return True
    if board[4]==board[5]==board[6]==turn:
        return True
    if board[7]==board[8]==board[9]==turn:
        return True
    if board[1]==board[4]==board[7]==turn:
        return True
    if board[2]==board[5]==board[8]==turn:
        return True
    if board[3]==board[6]==board[9]==turn:
        return True
    if board[1]==board[5]==board[9]==turn:
        return True
    if board[3]==board[5]==board[7]==turn:
        return True
    return False

def isDraw(board):
    for i in range(1, 10):
        if board[i] == ' ':
            return False
    return True

def clear():
    print('clear')
    # clear display
    for button in btns:
        button.config(text=' ')
    # clear board
    for i in range(1, 10):
        board[i] = ' '
    # re-initialize turn
    turn = USER
    NavLabel.config(text = turn + "'s turn")


def getMove(board):
    # try to attack
    for i in range(1, 10):
        # skip if already occupied
        if board[i] != ' ':
            continue
        copyBoard = [board[i] for i in range(10)]
        copyBoard[i] = BOT
        if isWin(copyBoard, BOT):
            return i

    # try to defend
    for i in range(1, 10):
        # skip if already occupied
        if board[i] != ' ':
            continue
        copyBoard = [board[i] for i in range(10)]
        copyBoard[i] = USER
        if isWin(copyBoard, USER):
            return i
    # middle first
    if board[5] == ' ':
        return 5
    # random move
    loc = rand.randint(1, 9)
    while(board[loc] != ' '):
        loc = rand.randint(1, 9)
    return loc

def endGame(who=None):
    if not who:
        msgLabel.config(text= 'Draw')
    else:
        msgLabel.config(text= who + ' Win!')
    msgArea.place(anchor="c", relx=.5, rely=.5)

def BOTMove():
    move = getMove(board)
    btns[move - 1].config(text='X')
    board[move] = BOT
    NavLabel.config(text = USER + "'s turn")
    if isWin(board, BOT):

        endGame(BOT)
        return
    elif isDraw(board):
        endGame(BOT)
        return 

def onClick(event):
    for button in btns:
        if button is event.widget:
            # check if this move is valid
            if button['text'] != ' ': 
                return 
            # always user's turn when clicked
            button.config(text=USER)
            btn_id = int(str(button).split(".")[-1])
            board[btn_id] = USER
            

            if isWin(board, USER):
                endGame(USER)
                return

            elif isDraw(board):
                endGame(None)
                return 
            
            # BOT's turn
            NavLabel.config(text = BOT + "'s turn")
            
            msgArea.after(1000, BOTMove)
            
            
            return

# build GUI
NavArea = tkinter.LabelFrame(main, width=300, height=50)
NavLabel = tkinter.Label(NavArea, text="O's turn", font=font2,
                       padx=5, pady=10, bg='#C0FFEE')
NavArea.pack()
NavLabel.pack()
gameArea = tkinter.LabelFrame(main, width=300, height=300)
frames = [tkinter.Frame(gameArea, width=100, height=100) for _ in range(9)]
btns = [Button(frames[i],image=tkinter.PhotoImage(width=100, height=100), text=board[i+1], font=font1, name=str(i+1)) for i in range(9)]
gameArea.pack()
msgArea = tkinter.LabelFrame(gameArea, width=250, height=150, bg='#C0FFEE')
msgLabel = tkinter.Label(msgArea, text= ' ', font=font1,
            padx=10, pady=30)
msgButton = Button(msgArea ,image=tkinter.PhotoImage(width=50, height=30), text='restart', command=lambda: [clear(), msgArea.place_forget()]  )
msgLabel.pack()
msgButton.pack()
for i in range(3):
    for j in range(3):
        # to keep a button in the middle of a frame
        frames[i*3+j].grid_propagate(False) #disables resizing of frame
        frames[i*3+j].columnconfigure(0, weight=1) #enables button to fill frame
        frames[i*3+j].rowconfigure(0,weight=1) #any positive number would do the trick
        frames[i*3+j].grid(row=i, column=j)
        
        btns[i*3+j].pack(side=tkinter.LEFT)
        btns[i*3+j].bind("<Button-1>", onClick)
        

main.mainloop()