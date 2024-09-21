import random
from tkinter import *
import requests

# List of words
'''M=["STUDENT", "MOM",
   "PENCILCASE", "HAIR",
   "LAPTOP", "BIOGRAPHY","UPPERCASE", "TELEPHONE"]'''

# Initialization of the alphabet list (contains the letters of the alphabet)
alphabet = [0] * 26
l = []

# Select a random word from a given list here M
def random_word():
    def word_list():
        # Query the website with a 10-second timeout:
        # If Python doesn't receive a response in 10 seconds, it interrupts the request
        response = requests.get(
            'http://www.ideal-group.org/dictionary/p-5_ok.txt',
            timeout=10
        )
        
        # Decode the content into a string
        chr_of_words = response.content.decode('utf-8')
        
        # Turn the string into a list of words
        # splitlines is used because words are on different lines
        word_list = chr_of_words.splitlines()
        
        for e in word_list:
            if ("'" or " ") in e:
                word_list.remove(e)
        
        return word_list
    
    def to_uppercase(word, m=''):
        for i in range (len(word)):
            if ord("a")<=ord(word[i])<=ord("z"):
                m += chr(ord(word[i]) - 32)
            else:
                m += word[i]
        return m

    words = word_list()

    m = random.choice(words)
    return to_uppercase(m)


# Create the list containing the "empty" spaces (underscores) to be replaced by letters
def create_blanks(word, l):
    # If l is empty, add underscores according to the length of the chosen word
    if not l: 
        for i in range (len(word)):
            l.append("__ ")
    # Otherwise, at least one letter has been placed (the user restarted the game)
    else:
        extra = len(l) - len(word)
        # All elements are replaced by "__ "
        for i in range(len(l)):
            l[i] = "__ "
        
        # If the old word is longer, the list is reduced
        # If it's the opposite, "__ " is added
        if extra > 0:
            for i in range(extra):
                l.pop()
        else:
            for i in range(-extra):
                l.append("__ ")

def create_alpha(scale=30, height=600, width=850):
    
    global c
    
    # Placement of x and y for the alphabet and the word underscores
    letter_x = int(width * 0.1)
    letter_y = int(height * 0.1)
    underscore_y = int(height * 0.3)
    underscore_x = int(width * 0.4)
    
    # Clear the canvas to prevent overlap
    canvas.delete("all") 
    
    # Placement of rectangles containing letters in a 13x2 grid
    letter_index = 0
    
    # Loop for the y-axis placement
    for j in range(letter_y, 2 * scale + letter_y, scale): 
        # Loop for the x-axis placement
        for i in range(letter_x, 13 * scale + letter_x, scale):
            # Color letters that are:
            # Not clicked (gray), clicked and correct (green), or clicked and wrong (red)
            if alphabet[letter_index][1] == 2:
                rect_color = "lightgrey"
            elif alphabet[letter_index][1] == 1:
                rect_color = "green"
            elif alphabet[letter_index][1] == 0:
                rect_color = "red"
            
            # Tags for identifying rectangles with their associated letter
            letter_tag = alphabet[letter_index][0]
            canvas.create_rectangle(i, j, i + scale, j + scale,
                                    fill=rect_color, 
                                    tags=letter_tag)
            canvas.create_text(i + 0.5 * (scale), j + 0.5 * (scale), 
                               text=letter_tag, 
                               fill="black", 
                               tags=letter_tag)
            letter_index += 1 
            
    # Place elements in list l (underscores and/or letters)
    j = 0
    for i in range(underscore_y, underscore_y + scale * len(l), scale):
        canvas.create_text(i + 0.5 * (scale), underscore_x + 0.5 * (scale), 
                           text= l[j], 
                           fill="black")
        j += 1
    
    # Text indicating how many chances are left, orange if less than 4 chances
    if c > 3:
        chances_color = "black"
    elif c <= 3:
        chances_color = "red"
    canvas.create_text(int(width * 0.8), int(height * 0.3), 
                       text= f"chances: {c}", 
                       fill=chances_color, 
                       font=("Arial",20))
    
    
    # Draw the hangman based on remaining chances
    #It is not working at the moment
    '''if c < 10:
        canvas.create_line(int(width * 0.7), int(height * 0.8), 
                           int(width * 0.7) + 3 * scale, int(height * 0.8))
        if c < 9:
            canvas.create_line(int(width * 0.7) + 1.5 * scale, int(height * 0.8), 
                               int(width * 0.7) + 1.5 * scale, int(height * 0.8) - 3 * scale)
            if c < 8:
                canvas.create_line(int(width * 0.7) + 1.5 * scale, int(height * 0.8) - 3 * scale, 
                                   int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 3 * scale)
                if c < 7:
                    canvas.create_line(int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 3 * scale, 
                                       int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 2.8 * scale)
                    if c < 6:
                        canvas.create_oval(int(width * 0.7) + 0.45 * scale, int(height * 0.8) - 2.8 * scale, 
                                           int(width * 0.7) + 1.05 * scale, int(height * 0.8) - 2.2 * scale)
                        if c < 5:
                            canvas.create_line(int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 2.2 * scale, 
                                               int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 1.2 * scale)
                            if c < 4:
                                canvas.create_line(int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 1.2 * scale, 
                                                   int(width * 0.7) + 0.5 * scale, int(height * 0.8) - 0.7 * scale)
                                if c < 3:
                                    canvas.create_line(int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 1.2 * scale, 
                                                       int(width * 0.7) + scale, int(height * 0.8) - 0.7 * scale)
                                    if c < 2:
                                        canvas.create_line(int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 1.9 * scale, 
                                                           int(width * 0.7) + 0.5 * scale, int(height * 0.8) - 1.4 * scale)
                                        canvas.create_line(int(width * 0.7) + 0.75 * scale, int(height * 0.8) - 1.9 * scale, 
                                                           int(width * 0.7) + scale, int(height * 0.8) - 1.4 * scale)'''
    
    # Placement of the restart button
    restart_x = int(width * 0.8)
    restart_y = int(height * 0.05)
    # Pass the initialization function to the callback, called when the button is clicked
    restart = Button(canvas, width= 12, text="Restart", command= lambda: initialization()) 
    # Place the button
    restart.place(x=restart_x, y=restart_y) 
    
    message(scale, height, width)

def message(scale, height, width):
    global c
    
    # If all underscores are replaced, the player wins
    if "__ " not in l:
        canvas.delete("all")
        canvas.create_text(int(width * 0.5), int(height * 0.5), 
                           text=f"You WON!!!!! The word was {m}", 
                           fill="green", font=15)
        # Draw a smiling face
        canvas.create_oval(int(width * 0.5) - scale, int(height * 0.6) - scale, 
                           int(width * 0.5) + scale, int(height * 0.6) + scale)
        canvas.create_text(int(width * 0.5) - 0.4 * scale, int(height * 0.6) - 0.4 * scale,
                           text="o")
        canvas.create_text(int(width * 0.5) + 0.4 * scale, int(height * 0.6) - 0.4 * scale,
                           text="o")
        canvas.create_arc(int(width * 0.5) - 0.4 * scale, int(height * 0.6),
                           int(width * 0.5) + 0.4 * scale, int(height * 0.6) + 0.6 * scale,
                           start=0 ,extent=-180)
    # If no chances are left, the player loses
    elif c == 0:
        canvas.delete("all")
        canvas.create_text(int(width * 0.5), int(height * 0.5), 
                           text=f"You LOST!!!!!!! The word was {m}", 
                           fill="red", font=15)
        # Draw a dead face
        canvas.create_oval(int(width * 0.5) - scale, int(height * 0.6) - scale, 
                           int(width * 0.5) + scale, int(height * 0.6) + scale)
        canvas.create_text(int(width * 0.5) - 0.4 * scale, int(height * 0.6) - 0.4 * scale,
                           text="x")
        canvas.create_text(int(width * 0.5) + 0.4 * scale, int(height * 0.6) - 0.4 * scale,
                           text="x")
        canvas.create_line(int(width * 0.5) - 0.4 * scale, int(height * 0.6) + 0.4 * scale,
                           int(width * 0.5) + 0.4 * scale, int(height * 0.6) + 0.4 * scale)

def initialization(event=None):
    global c
    global m
    
    m = random_word()
    
    create_blanks(m, l)
    
    # Place each letter of the alphabet in the alphabet list with a neutral state
    letter_tag = ord("A")
    for i in range(26):
        alphabet[i] = [chr(letter_tag), 2]
        letter_tag += 1 
    c = 10
    create_alpha()

def update(m, l, letter):
    global c
    letter_index_in_alphabet = ord(letter) - ord("A")
    if letter in m:
        # If the clicked letter is in the word, its state changes to correct
        alphabet[letter_index_in_alphabet][1] = 1
        for i in range(len(m)):
            if letter == m[i]:
                l[i] = letter + " "
    else:
        # Otherwise, its state changes to wrong and the number of remaining chances decreases if it hasn't been clicked yet
        if alphabet[letter_index_in_alphabet][1] != 0:
            alphabet[letter_index_in_alphabet][1] = 0
            c -= 1

def letter_clicked(rectangle, height=600):
    # If clicked below half the screen, do nothing
    y = rectangle.y
    if y < 0.5 * height:
        # Find the clicked object
        clicked = canvas.find_withtag("current")
        try:
            # The first tag is the letter
            letter = canvas.gettags(clicked)[0] 
        except IndexError:
            # No specific object was clicked
            return False 
        update(m, l, letter)
        create_alpha()
        return True   

def letter_typed(key):
    # Convert lowercase letter to uppercase
    if ord("a")<=ord(key.char)<=ord("z"):
        letter = chr(ord(key.char) - 32)
    else:
        letter = key.char
    update(m, l, letter)
    create_alpha()

width = 850
height = 600
scale = 30

root = Tk()
# Title of the window
root.title("Hangman") 
# Prevent resizing of the window in height and width (same as root.resizable(width=False, height=False))
root.resizable(False, False) 
# Definition of the canvas on which all objects are placed
canvas = Canvas(root, width=width, height=height, background="white") 
# Placement of the canvas
canvas.pack(fill="both", expand=True) 

# Create an event when a click occurs
# It contains the coordinates of the click and tags the clicked object as "current"
# Calls the letter_clicked function
canvas.bind('<Button-1>', letter_clicked) 

# Create an event when a letter is typed (uppercase or lowercase)
# Calls the letter_typed function
for i in range(ord("A"), ord("Z")+1, 1):
    root.bind(chr(i), letter_typed) 
    
for i in range(ord("a"), ord("z")+1, 1):
    root.bind(chr(i), letter_typed)

# When Enter is pressed, calls the initialization function
root.bind('<Return>', initialization)

# Call the initialization function to start the game
initialization()

root.mainloop()
