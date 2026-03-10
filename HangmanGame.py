from tkinter import *
import tkinter.messagebox
import random
import tkinter.simpledialog
window = Tk()
class HangmanGame:
    def __init__(self):
        window.title("Hangman Game")
        #creates the lists for the categories of words
        self.sports = ["basketball", "baseball", "football", "soccer", "tennis"]
        self.celebs = ["Kim K", "Jim Carrey", "Peyton Manning", "Taylor Swift", "Justin Bieber"]
        self.animals = ["dog", "cat", "moose", "snake", "tiger"]
        self.food = ["hamburger", "chicken wings", "pizza", "taco", "french fries"]

        #creates a frame where the categories will be displayed
        frame1 = Frame(window)
        frame1.pack()

        #creates a label to tell user to pick a category
        categoryLabel = Label(frame1, text= "Pick a category:")

        #creates the variable to be used with the radio buttons
        self.v1 = IntVar()

        #creates the radio buttons for the categories
        rbSport = Radiobutton(frame1, text = "Sports", variable = self.v1, value = 1, command = self.processRadioButton)
        rbCelebrities = Radiobutton(frame1, text = "Celebrities", variable = self.v1, value = 2, command = self.processRadioButton)
        rbAnimals = Radiobutton(frame1, text = "Animals", variable = self.v1, value = 3, command = self.processRadioButton)
        rbFood = Radiobutton(frame1, text = "Food", variable = self.v1, value = 4, command = self.processRadioButton)
        
        #creates a radiobutton for the user to enter their own custom word
        rbCustom = Radiobutton(frame1, text = "Custom", variable = self.v1, value = 5, command = self.processRadioButton)
        
        #creates a button that will start the game
        startButton = Button(frame1, text = "Start Game", command = self.startGame)
        

        #places the items in the frame
        categoryLabel.grid(row = 1, column = 1)
        rbSport.grid(row = 1, column = 2)
        rbCelebrities.grid(row = 1, column = 3)
        rbAnimals.grid(row = 1, column = 4)
        rbFood.grid(row = 1, column = 5)
        rbCustom.grid(row = 1, column = 6)
        startButton.grid(row = 1, column = 7)

        #creates a frame for the canvas
        frame2 = Frame(window)
        frame2.pack()

        #creates the canvas
        self.canvas = Canvas(frame2, width = 400, height = 200, bg = "white")
        self.canvas.pack()

        #writes category at the top and will show user the category they selected
        self.canvas.create_text(160,20, text = "Category: ")

        #draws the different part of hanging post
        self.canvas.create_line(140, 40, 210, 40) #top horizontal line for hanging post
        self.canvas.create_line(210, 40, 210, 50) #vertical line for part that connects to person
        self.canvas.create_line(140, 40, 140, 100) #vertical line for hanging post
        self.canvas.create_line(140, 100, 120, 120) #left leg of hanging post
        self.canvas.create_line(140, 100, 160, 120) #right leg of hanging post

        #creates a frame for the guess entry and make a guess button
        frame3 = Frame(window)
        frame3.pack()
        #creates a label to tell user what to do
        guessLabel = Label(frame3, text = "Guess a letter:")

        #creates a variable to be used in the entry
        self.guessVar = StringVar()

        #creates an entry for the guess
        guessEntry = Entry(frame3, textvariable = self.guessVar)

        #creates a make guess button so user can sumbit a guess with it
        guessButton = Button(frame3, text = "Make Guess", command = self.makeGuess)

        #allows the use of the enter button to submit a guess
        guessEntry.bind("<Return>", self.enterButtonMakeGuess)
        guessEntry.focus_set()

        #places the guess items in the frame
        guessLabel.grid(row = 1, column = 1)
        guessEntry.grid(row = 1, column = 2)
        guessButton.grid(row = 1, column = 3)
        
        window.mainloop()
    #method to process radio button and set the category a user picked
    def processRadioButton(self):
        
        if self.v1.get() == 1:
            self.category = "Sports"
        elif self.v1.get() == 2:
            self.category = "Celebs"
        elif self.v1.get() == 3:
            self.category = "Animals"
        elif self.v1.get() == 4:
            self.category = "Food"
        elif self.v1.get() == 5:
            self.category = "Custom"
        
        

    #called when startGame button is clicked
    def startGame(self):
        self.lineNum = 0
        self.correct = 0
        self.wrongGuess = 0
        self.guesses = []
        self.posX = 260
        self.posY = 90
        #assigns a value to self.word by calling the self.getWord method
        self.word = self.getWord()

        #clears anything that may of been present before and set background back to white
        self.canvas.delete("category","body", "guess", "wrong", "line", "letter")
        self.canvas["bg"] = "white"

        #writes the category the user chose to the canvas
        self.canvas.create_text(205, 20, text = self.category, tags = "category")

        #determines if the word has a space in it
        self.space = self.ifSpace()
       
        #depending on whether the word has a space or not it draws the lines for the word
        if self.space:
            self.spaceInt = self.word.find(" ")
            #draws the lines for a word with a space
            self.drawLinesWithSpace()
        else:
            #draws the lines for a word with no spaces
            self.drawLinesNoSpace()

    #this method is for if the user uses the enter key instead of clicking the make guess button
    def enterButtonMakeGuess(self, event):
        self.makeGuess()
    #this method is used to sumbit a guess
    def makeGuess(self):
        #checks the length and whether the character is alphabetic
        if self.guessVar.get().isalpha() and len(self.guessVar.get()) == 1:
            #makes the guess always lowercase
            guess = self.guessVar.get().lower()
            #checks to see if user has previously guessed the letter, if not adds to the guesses list and checks guess
            if guess in self.guesses:
                tkinter.messagebox.showwarning("Attention", "Already guessed that letter")
            else:
                self.guesses.append(guess)
                self.checkGuess(guess)
        else:
            tkinter.messagebox.showwarning("Attention!", "Guess must be a single alphabetic character")
        
    #picks the word randomly depending on what category was picked by the user
    def getWord(self):
        num = random.randint(0,4)
        if self.category == "Sports":
            word = self.sports[num]
        elif self.category == "Celebs":
            word = self.celebs[num]
        elif self.category == "Animals":
            word = self.animals[num]
        elif self.category == "Food":
            word = self.food[num]
        #Allows the user to enter a custom word
        elif self.category == "Custom:
            word = tkinter.simpledialog.askstring("Custom word", "Enter your custom word", parent=window)
      
        return word

    #determines whether or not the word has a space in it
    def ifSpace(self):
        if self.word.find(" ") != -1:
            space = True
        else:
            space = False

        return space
    
    #method draws the lines for a word that has a space
    def drawLinesWithSpace(self):
        #deletes any lines if there are any from previous game
        self.canvas.delete("line")
        #sets default values for the lines depending on length of word
        if len(self.word) < 9:
            a = 160
            b = 160
            c = 170
            d = 160
        else:
            a = 80 
            b = 160
            c = 90
            d = 160
        #a default value to be used to move the lines
        move = 20
        x = 0
        #loop used to draw the lines
        while x < len(self.word):
            #draws the lines but skips when the space is encountered
            if x != self.spaceInt:
                self.canvas.create_line(a, b, c, d, tags = "line")
                self.lineNum += 1
            #adds on to the position variables to move the lines over
            a += move           
            c += move
            #loop control variable
            x += 1

    def drawLinesNoSpace(self):
        #deletes any lines if there are any from previous game
        self.canvas.delete("line")
        #sets default values for the lines depending on length of word
        if len(self.word) < 9:
            a = 140
            b = 160
            c = 150
            d = 160
        else:
            a = 80 
            b = 160
            c = 90
            d = 160
        #a default value to be used to move the lines
        move = 20
        x = 0
        while x < len(self.word):
            #draws the lines
            self.canvas.create_line(a, b, c, d, tags = "line")
            self.lineNum += 1
            
            #adds to the position variables of the lines
            a += move           
            c += move
            #loop control variable
            x += 1
    
    #method used to check to see if the guess is present in the word
    def checkGuess(self, guess):
        maxWrong = 5
        
        if self.word.lower().find(guess) == -1:
            #user guessed a letter not in the word
            self.wrongGuess += 1
            self.canvas.create_text(self.posX + 10*(self.wrongGuess), self.posY, text = guess, tags= "guess")
            if self.wrongGuess == 1:
                self.canvas.create_text(300, 70, text= "Incorrect Guesses", tags="wrong")
                #draw head
                self.canvas.create_oval(200, 50, 220, 70, tags ="body")
            elif self.wrongGuess == 2:
                #draw torso
                self.canvas.create_line(210,70, 210, 100, tags = "body")
            elif self.wrongGuess == 3:
                #draw left leg
                self.canvas.create_line(210, 100, 200, 110, tags = "body")
            elif self.wrongGuess == 4:
                #draw right leg
                self.canvas.create_line(210,100, 220, 110, tags = "body")
            elif self.wrongGuess == 5:
                #draw left arm
                self.canvas.create_line(210, 80, 200, 90, tags = "body" )
            elif self.wrongGuess == 6:
                #draw right arm
                self.canvas.create_line(210, 80, 220, 90, tags = "body")
            
            #way to end the game if the user got to many wrong guesses
            if self.wrongGuess > maxWrong:
                self.canvas["bg"] = "red"
                #calls method to write the full word on the blanks
                self.writeFullWord()
                #dialog box to ask if they want to play again
                isYes = tkinter.messagebox.askyesno("Game Over", "You lost.\nPlay Again?")
                if isYes:
                    #if the user clicks yes the background is reset and things are deleted from the canvas
                    self.canvas["bg"] = "white"
                    self.canvas.delete("body", "guess", "wrong", "line", "letter")
        else:
            #user guessed a correct letter
            #method for writing the letter they guessed on a blank
            self.writeCorrectLetter(guess)
            #way to show the user has won when they guess all the letters
            if self.correct == self.lineNum:
                self.canvas["bg"] = "green"
                #dialog to ask to tell them they won and to ask if they want to play again
                isYes = tkinter.messagebox.askyesno("WINNER!", "You have won!\nPlayAgain?")
                #if user clicks yes background will reset and items will be cleared from canvas
                if isYes:
                    self.canvas["bg"] = "white"
                    self.canvas.delete("body", "guess", "wrong", "line", "letter")
    
    #method to show the full word on the blanks
    def writeFullWord(self):
        #asks if word has a space
        if self.space:
            #determines the default position values based on length of word
            if len(self.word) < 9:
                a = 164
                b = 154
            else:
                a = 84 
                b = 154
            move = 20
            x = 0
            #loop that writes the letters on the lines and skips the space
            while x < len(self.word):
                if x != self.spaceInt:
                    self.canvas.create_text(a, b, text = self.word[x], tags = "letter")
                #adds to the position variable
                a += move
                x += 1
        else:
            #word with no space
            #determines default position variables for the word based on length
            if len(self.word) < 9:
                a = 144
                b = 154
            else:
                a = 84 
                b = 154
            move = 20
            x = 0
            #loop to write the letters on the lines
            while x < len(self.word):
                self.canvas.create_text(a,b, text = self.word[x], tags = "letter")
                #adds to the position variable
                a += move           
                
                x+= 1
    #method for writing a correctly guessed letter onto the blank it belongs
    def writeCorrectLetter(self, guess):
        #check to see if word has a space, if yes
        if self.space:
            #sets default values for position of letters based on length of word
            if len(self.word) < 9:
                a = 164
                b = 154
            else:
                a = 84 
                b = 154
            move = 20
            x = 0
            #loop to find the placing of the letter on the blanks
            while x < len(self.word):
                if guess == self.word[x].lower():
                    self.canvas.create_text(a, b, text = self.word[x], tags = "letter")
                    self.correct += 1
                
                a += move           
                
                x += 1
        else:
            #word with no space
            #sets the default position values based on length of word
            if len(self.word) < 9:
                a = 144
                b = 154
            else:
                a = 84 
                b = 154
            move = 20
            x = 0
            #loop for finding the position of the letter
            while x < len(self.word):
                if guess == self.word[x].lower():
                    self.canvas.create_text(a,b, text = self.word[x], tags = "letter")
                    self.correct += 1
            
                a += move           
                x+= 1





HangmanGame()
