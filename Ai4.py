from tkinter import *
from logic import *
from random import *
from copy import *
import math
import time
# 0 = w, 1 = a, 2 = s, 3= d
# these need to be outputs of move
possible = ["'w'", "'a'", "'s'", "'d'"]

#these are commands
commands = [up,left,down,right]

def AiRandomMove(board):
  legal = getLegalMoves(board)
  x = randint(0, len(legal)-1)
  print(getScore(board))
  print(getLargest(board))
  return legal[x]



  


def getLegalMoves(board):
  legal = []
  for x in range(0, len(commands)):
    temp = copy(commands[x](board))
    if temp[0] != board:
      legal.append(commands[x])
  return legal



# returns locations of empty cells
def emptycell(board):
  res =[]
  for y in range(0, len(board)):
    for x in range (0, len(board[y])):
      if board[y][x] == 0:
        res.append([y, x])
  return res


def AiMove(board):
  timeout = time.time() + 1
  x = 0
  while time.time() < timeout:
    legalMoves = getLegalMoves(board)
    if len(legalMoves) == 0:
      return "'n'"
    else:
      alpha = -math.inf
      beta = math.inf
      bestMove = "'n'"
      for move in legalMoves:
        future = copy(board)
        future = move(future)[0]
        curval = beta_val(future, alpha, beta, x)

        if curval >= alpha:
          alpha = curval
          bestMove = moveTrans(move)
    x = x + 1
  return bestMove
def moveTrans(m):
  for x in range(0, len(commands)):
    if commands[x] == m:
      return possible[x]
  return "'n'"


#this function does the pushing            
def alpha_val(board, alpha, beta, level):
  curMax = -math.inf
  legalMoves = getLegalMoves(board)

  # will give out values for board scoring
  if len(legalMoves) == 0:
    #it never wants to stop!
    return curMax
  if level <= 0:
    return evaluate(board)

  for move in legalMoves:
    future = copy(board)
    future = move(future)[0]
    curval = beta_val(future, alpha, beta, level - 1)

    curmax = max(alpha, curval)
    if curmax >= beta:
      return curmax
    alpha = max(alpha, curmax)
  return curmax

#this function places 2s and 4s
def beta_val(board, alpha, beta, level):
  curMin = math.inf
  legalMoves = emptycell(board)
            
  if len(legalMoves) == 0:
    return alpha_val(board, alpha, beta, level - 1)
  if level <= 0:
    return evaluate(board)


  future_moves=[]
  future_clean=[]
  #values of 1 and 2, 1 being 2 tile, 2 being 4 tile
  #make a list of possible spawns
  for i in range(1, 3):
    for legalmove in legalMoves:
      future = copy(board)

      future[legalmove[0]][legalmove[1]] = (i * 2)
      future_clean.append(clean(future))
      future_moves.append(future)

  relevantSpawn = []
  for x in range(0,2):
    if len(future_moves) == 0:
      break
    else:
      temp = max(future_clean)
      temp2 = future_clean.index(temp)
      relevantSpawn.append(future_moves[temp2])
      future_moves.remove(future_moves[temp2])
      future_clean.remove(future_clean[temp2])
  for x in relevantSpawn:
    
    curval = alpha_val(x, alpha, beta, level - 1)

    curmin = min(beta, curval)
    if curmin <= alpha:
      return curmin
    beta = min(beta, curmin)
  return curmin

#evaluating heuristic  
def evaluate(board):
  sl = slope(board) * 1
  if emptynodes(board) == 0:
    em = 0
  else:
    em = math.log(emptynodes(board)) * 2.7
  cl = clean(board) * .1
  lg = math.log(getLargest(board), 2)
  return sl + em + cl + lg

#total Score
def getScore(board):
  score = 0
  for x in board:
    for y in x:
      score += y
  return score
#largest node
def getLargest(board):
  result = 0
  for x in board:
    for y in x:
      if y >= result:
        result = y
  return math.log(result, 2)

#heuristic showing the ability for each closest piece to merge
def clean(board):
  res = 0
  for y in range(0, len(board)):
    for x in range(0, len(board[y])):
      if board[y][x] != 0:
        #log base 2 of value
        baseval = math.log(board[y][x], 2)

        #get closest node
        y2 = y + 1
        x2 = x + 1
        
        while y2 < len(board):
          if board[y2][x] != 0:
            closeval = math.log(board[y2][x], 2)
            #if res == 0 then they are the same and it will connect
            #positive values will be bad for the solution
            res -= abs(baseval - closeval)
            break
          y2 = y2 + 1
        while x2 < len(board[y]):
          if board[y][x2] != 0:
            closeval = math.log(board[y][x2], 2)
            #if res == 0 then they are the same and it will connect
            #positive values will be bad for the solution
            res -= abs(baseval - closeval)
            break
          x2 = x2 + 1
  return res
#increasing by directions
#measured in all four directions
def slope(board):
  total = [0,0,0,0]

  #first is up and down
  for y in range (0, 4):
    cur = 0
    nex = 1
    while nex < 4:
      curval = 0
      nexval = 0
      if board[y][cur] != 0:
        curval = math.log(board[y][cur], 2)
      if board[y][nex] != 0:
        nexval = math.log(board[y][nex], 2)
        
      if curval > nexval:
        total[0] += nexval - curval
      if curval < nexval:
        total[1] += curval - nexval
      cur = nex
      nex += 1
  for x in range (0, 4):
    cur = 0
    nex = 1
    while nex < 4:
      curval = 0
      nexval = 0
      if board[cur][x] != 0:
        curval = math.log(board[cur][x], 2)
      if board[nex][x] != 0:
        nexval = math.log(board[nex][x], 2)
        
      if curval > nexval:
        total[2] += nexval - curval
      if curval < nexval:
        total[3] += curval - nexval
        
      cur = nex
      nex += 1

  return max(total[0],total[1]) + max(total[2],total[3])
#number of empty nodes
def emptynodes(matrix):
  res = 0
  for y in range(0, len(matrix)):
    for x in range(0,len(matrix[y])):
      if matrix[y][x] == 0:
        
        res = res + 1
  return res
  

ori = [ [2,2,0,4],
        [0,0,0,2],
        [0,0,0,0],
        [0,0,0,0]]
new = [ [0,0,0,0],
        [0,0,0,0],
        [0,0,0,4],
        [2,2,0,2]]
new2 = [[0,0,4,4],
        [0,0,0,2],
        [0,0,0,0],
        [0,0,0,0]]
new3 = [[0,2,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,2,0]]













  
