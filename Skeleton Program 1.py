import random, pickle, os
from datetime import date

NO_OF_RECENT_SCORES = 10

SameCard = False
AceHigh = False

class TCard():
  def __init__(self):
    self.Suit = 0
    self.Rank = 0

class TRecentScore():
  def __init__(self):
    self.Name = ''
    self.Score = 0
    self.Date = None

Deck = [None]
RecentScores = [None]
Choice = ''

def GetRank(RankNo):
  Rank = ''
  if RankNo == 1 and not AceHigh:
      Rank = 'Ace'
  elif RankNo == 2:
      Rank = 'Two'
  elif RankNo == 3:
      Rank = 'Three'
  elif RankNo == 4:
      Rank = 'Four'
  elif RankNo == 5:
      Rank = 'Five'
  elif RankNo == 6:
      Rank = 'Six'
  elif RankNo == 7:
      Rank = 'Seven'
  elif RankNo == 8:
      Rank = 'Eight'
  elif RankNo == 9:
      Rank = 'Nine'
  elif RankNo == 10:
      Rank = 'Ten'
  elif RankNo == 11:
      Rank = 'Jack'
  elif RankNo == 12:
      Rank = 'Queen'
  elif RankNo == 13:
      Rank = 'King'
  else:
      Rank = "Ace"
  return Rank

def GetSuit(SuitNo):
  Suit = ''
  if SuitNo == 1:
    Suit = 'Clubs'
  elif SuitNo == 2:
    Suit = 'Diamonds'
  elif SuitNo == 3:
    Suit = 'Hearts'
  else:
    Suit = 'Spades'
  return Suit

def DisplayMenu():
  print()
  print('MAIN MENU')
  print()
  print('1. Play game (with shuffle)')
  print('2. Play game (without shuffle)')
  print('3. Display recent scores')
  print('4. Reset recent scores')
  print("5. Options")
  print("6. Save Scores ")
  print()
  
  print('Select an option from the menu (or enter q to quit): ', end='')

def GetMenuChoice():
  Choice = input()
  print()
  return Choice.lower()[0]

def LoadDeck(Deck):
  CurrentFile = open('deck.txt', 'r')
  Count = 1
  while True:
    LineFromFile = CurrentFile.readline()
    if not LineFromFile:
      CurrentFile.close()
      break
    Deck[Count].Suit = int(LineFromFile)
    LineFromFile = CurrentFile.readline()
    Deck[Count].Rank = int(LineFromFile)
    Count = Count + 1
 
def ShuffleDeck(Deck):
  SwapSpace = TCard()
  NoOfSwaps = 1000
  for NoOfSwapsMadeSoFar in range(1, NoOfSwaps + 1):
    Position1 = random.randint(1, 52)
    Position2 = random.randint(1, 52)
    SwapSpace.Rank = Deck[Position1].Rank
    SwapSpace.Suit = Deck[Position1].Suit
    Deck[Position1].Rank = Deck[Position2].Rank
    Deck[Position1].Suit = Deck[Position2].Suit
    Deck[Position2].Rank = SwapSpace.Rank
    Deck[Position2].Suit = SwapSpace.Suit

def DisplayCard(ThisCard):
  print()
  print('Card is the', GetRank(ThisCard.Rank), 'of', GetSuit(ThisCard.Suit))
  print()

def GetCard(ThisCard, Deck, NoOfCardsTurnedOver):
  ThisCard.Rank = Deck[1].Rank
  if ThisCard.Rank == 1 and AceHigh:
    ThisCard.Rank = 14
  print(Deck[1].Rank)
  ThisCard.Suit = Deck[1].Suit
  for Count in range(1, 52 - NoOfCardsTurnedOver):
    Deck[Count].Rank = Deck[Count + 1].Rank
    Deck[Count].Suit = Deck[Count + 1].Suit
  Deck[52 - NoOfCardsTurnedOver].Suit = 0
  Deck[52 - NoOfCardsTurnedOver].Rank = 0

def IsNextCardHigher(LastCard, NextCard):
  Higher = False
  if (NextCard.Rank > LastCard.Rank):
    Higher = True
  return Higher

def GetPlayerName():
  print()
  valid = False
  while not valid:
    PlayerName = input('Please enter your name: ')
    if len(PlayerName) > 0:
      valid = True
    else:
      print("You must enter something for your name!")
  print()
  return PlayerName

def GetChoiceFromUser():
  Choice = input('Do you think the next card will be higher than the last card (enter y or n)? ').lower()
  return Choice

def DisplayEndOfGameMessage(Score):
  print()
  print('GAME OVER!')
  print('Your score was', Score)
  if Score == 51:
    print('WOW! You completed a perfect game.')
  print()

def DisplayCorrectGuessMessage(Score):
  print()
  print('Well done! You guessed correctly.')
  print('Your score is now ', Score, '.', sep='')
  print()

def ResetRecentScores(RecentScores):
  for Count in range(1, NO_OF_RECENT_SCORES + 1):
    RecentScores[Count].Name = ''
    RecentScores[Count].Score = 0
    RecentScores[Count].Date = None

def DisplayRecentScores(RecentScores):
  print()
  print('Recent Scores: ')
  print()
  print("{0:<12}{1:<10}{2:<5}".format("Date","Name","Score"))
  print()
  for Count in range(1, NO_OF_RECENT_SCORES + 1):
    if RecentScores[Count].Date != None:
      ScoreDate = RecentScores[Count].Date.strftime("%d/%m/%Y")
    else:
      ScoreDate = ""
    print("{0:<12}{1:<10}{2:<5}".format(ScoreDate,RecentScores[Count].Name,RecentScores[Count].Score))
  print()
  print('Press the Enter key to return to the main menu')
  input()
  print()

def UpdateRecentScores(RecentScores, Score):
  valid = False
  while not valid:
    Choice = input("Do you want to add your score to the high score table? (y or n): ")
    Choice = Choice.lower()[0]
    if Choice in ["y","n"]:
      valid = True
    else:
      print("Please enter a valid choice (y or n)")

  if Choice == "y":
    PlayerName = GetPlayerName()
    FoundSpace = False
    Count = 0
    while (not FoundSpace) and (Count <= NO_OF_RECENT_SCORES):
      Count += 1
      if RecentScores[Count].Name == '':
        FoundSpace = True
      else:
        Count += 1
    if not FoundSpace:
      for Count in range(1, NO_OF_RECENT_SCORES):
        RecentScores[Count].Name = RecentScores[Count + 1].Name
        RecentScores[Count].Score = RecentScores[Count + 1].Score
      Count = NO_OF_RECENT_SCORES
    RecentScores[Count].Name = PlayerName
    RecentScores[Count].Score = Score
    RecentScores[Count].Date = date.today()
    

def SaveDuringGame(LastCard, NextCard, NoOfCardsTurnedOver, Deck):
  
  with open("deck.txt", mode = "w", encoding = "utf-8") as MyFile:
    for count in range(1,53):
      MyFile.write(str(Deck[count])+"\n")
    MyFile.write(str(LastCard.Suit) + "\n")
    MyFile.write(str(LastCard.Rank) + "\n")
    MyFile.write(str(NextCard.Suit) + "\n")
    MyFile.write(str(NextCard.Rank) + "\n")
    MyFile.write(str(NoOfCardsTurnedOver) + "\n")
  print("Game Saves.")

def GameAvailibleToLoad():
  CWD = os.getcwd
  FilesInCWD = os.listdir()
  if "deck.dat" in FilesInCWD:
    AvailibleFile = True
  else:
    AvailibleFile = False
  return AvailibleFile

def LoadSavedGame():
  with open("deck.dat", mode = "rb") as MyFile:
    ItemsInFile = pickle.load(MyFile)
    Deck = ItemsInFile[0]
    LastCard  = ItemsInFile[1]
    NextCard = ItemsInFile[2]
    NoOfCardsTurnedOver = ItemsInFile[3]
    return Deck, LastCard, NextCard, NoOfCardsTurnedOver



def PlayGame(Deck, RecentScores, AceHigh):
  Valid = "False"
  NoOfCardsTurnedOver = 1
  LastCard = TCard()
  NextCard = TCard()
  GameOver = False
  GetCard(LastCard, Deck, 0)
  while not Valid:
    if AvailibleFile:
      YesOrNo = input("There is a Saved File, Would you like to load it?").upper()
      if YesOrNo == "Y":
        Deck, LastCard, NextCard, NoOfCardsTurnedOver = LoadSavedGame()
        Valid = True
        DisplayCard(LastCard)
      else:
          DisplayCard(LastCard)
  else:
      DisplayCard(LastCard)
  while (NoOfCardsTurnedOver < 52) and (not GameOver):
    GetCard(NextCard, Deck, NoOfCardsTurnedOver)
    Choice = ''
    while (Choice != 'y') and (Choice != 'n') and (Choice != "s"):
      Choice = GetChoiceFromUser()
    DisplayCard(NextCard)
    NoOfCardsTurnedOver = NoOfCardsTurnedOver + 1
    Higher = IsNextCardHigher(LastCard, NextCard)
    if (Higher and Choice == 'y') or (not Higher and Choice == 'n') or (NextCard.Rank == LastCard.Rank and SameCard):
      DisplayCorrectGuessMessage(NoOfCardsTurnedOver - 1)
      LastCard.Rank = NextCard.Rank
      LastCard.Suit = NextCard.Suit
    elif Choice == "s":
      SaveDuringGame(LastCard, NextCard, NoOfCardsTurnedOver, Deck)
    else:
      GameOver = True
      if GameOver:
          DisplayEndOfGameMessage(NoOfCardsTurnedOver - 2)
          UpdateRecentScores(RecentScores, NoOfCardsTurnedOver - 2)
      else:
        DisplayEndOfGameMessage(51)
        UpdateRecentScores(RecentScores, 51)


def BubbleSortScores(RecentScores):
  swap = True
  while swap:
     swap = False
     for count in range(1,len(RecentScores)-1):
         if RecentScores[count].Score < RecentScores[count+1].Score:
           swap = True
           temp = RecentScores[count]
           RecentScores[count] = RecentScores[count+1]
           RecentScores[count+1] = temp
  return RecentScores
 
def OptionsMenu():
  print()
  print("Options Menu")
  print()
  print("1. Make Ace High Or Low...")
  print("2. Same Value Cards...")
  Option = int(input("Your Choice Please:  "))
  return Option
  
def GetOptionChoice(Option):
  if Option == 1:
    SetAceHighOrLow()
  if Option == 2:
    SameCardOptions()

def SameCardOptions():
  Valid = False
  while not Valid:
    ExceptDuplicates = input("Would you like duplicates to end the game(Y/N)?  " ).upper()
    if ExceptDuplicates == "N":
      SameCard = True
      Valid = True
    elif ExceptDuplicates == "Y":
      SameCard = False
      Valid = True
    else:
      print("Invalid Input! ")
  global SameCard
  
def SetAceHighOrLow():
  Valid = False
  while not Valid:
    HighOrLow = input("Would You Like Ace's to be HIGH or LOW?").upper()
    if HighOrLow == "H":
      AceHigh = True
      Valid = True
    elif HighOrLow == "L":
      Valid = True
      AceHigh = False
    else:
      print("Would You Like Ace's to be (H)IGH or (L)OW?").upper()
  global AceHigh


def SaveHighScores(RecentScores):
   with open("HighScores.dat", mode="wb") as my_file:
     pickle.dump(RecentScores, my_file)
 
def LoadScores():
  try:
   with open("HighScores.dat", mode="rb") as my_file:
       RecentScores = pickle.load(my_file)
       return RecentScores
  except IOError:
    pass
        
if __name__ == '__main__':
  for Count in range(1, 53):
    Deck.append(TCard())
  RecentScores = LoadScores()
  for Count in range(1, NO_OF_RECENT_SCORES + 1):
    RecentScores.append(TRecentScore())
  Choice = ''
  while Choice != 'q':
    DisplayMenu()
    Choice = GetMenuChoice()
    if Choice == '1':
      LoadDeck(Deck)
      ShuffleDeck(Deck)
      PlayGame(Deck, RecentScores, AceHigh)
    elif Choice == '2':
      LoadDeck(Deck)
      PlayGame(Deck, RecentScores, AceHigh)
    elif Choice == '3':
      RecentScores = BubbleSortScores(RecentScores)
      DisplayRecentScores(RecentScores)
    elif Choice == '4':
      ResetRecentScores(RecentScores)
    elif Choice == '5':
      Option = OptionsMenu()
      GetOptionChoice(Option)
    elif Choice == "6":
      SaveHighScores(RecentScores)
