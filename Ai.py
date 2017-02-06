from tkinter import *
from logic import *
from random import *
from copy import *
import math
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

def getScore(board):
  score = 0
  for x in board:
    for y in x:
      score += y
  return score

def getLargest(board):
  result = 0
  for x in board:
    for y in x:
      if y >= result:
        result = y
  return result

# returns locations of empty cells
def emptycell(board):
  res =[]
  for y in range(0, len(board)):
    for x in range (0, len(board[y])):
      if board[y][x] == 0:
        res.append([y, x])
  return res

def AiMove(board):
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
      curval = beta_val(future, alpha, beta, 2)

      if curval >= alpha:
        alpha = curval
        bestMove = moveTrans(move)
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
            
  #values of 1 and 2, 1 being 2 tile, 2 being 4 tile
  for i in range(1, 3):
    for legalmove in legalMoves:
      future = copy(board)

      future[legalmove[0]][legalmove[1]] = (i * 2)

      curval = alpha_val(future, alpha, beta, level - 1)

      curmin = min(beta, curval)
      if curmin <= alpha:
        return curmin
      beta = min(beta, curmin)
  return curmin
  
def evaluate(board):
  return getScore(board)



















  
