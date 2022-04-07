from tkinter import *
import nGram as nGramFile
N = 3
nGram = {}
nMinusOneGram = {}

def resetWordsListBox(searchTextBox,wordsList,words,e):
    #when clicked on any word then reset the textbox and update that word in text box
	#searchTextBox.delete(0, END)
    
    serachTextLen = len(searchTextBox.get())
    searchTextBox.insert(serachTextLen, wordsList.get(ANCHOR) +" ")
    findWordsFromListBox(searchTextBox, wordsList, words, e)

def updateListBox(searchTextBox, wordsList,words):
    #adding each word from wordList to list box
    #predictWord(searchTextBox)
    line = searchTextBox
    wordsList.delete(0, END)
    for i in words:
        wordsList.insert(END, i)
        
#checks for the similar letter in words as the texts are being typed ins search box
#and keeps relevent text
def findWordsFromListBox(searchTextBox,wordsList,words,e):
    searchText = searchTextBox.get()
    #prints the result to cmd as the user types the text in searchbox
    #print(searchText)
    predictedWords = predictWord(searchTextBox)
    
    words = []
    for k in predictedWords:
        words.append(k)
    if searchText == '':
        wordsFound = words
    else:
        wordsFound = []
        for i in words:
            wordsFound.append(i)
    updateListBox(searchText,wordsList, wordsFound)               


def windowFun():
    #setting output ui's window size to middle by calculating the screenwidth and height
    windowWidth = 600
    windowHeight = 300
    window = Tk(className = "Next Word Predictor")
    screenWidth = window.winfo_screenwidth() 
    screenHeight = window.winfo_screenheight() 
    
    x = (screenWidth/2) - (windowWidth/2)
    y = (screenHeight/2) - (windowHeight/2)
    
    window.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
    
    #search label that shows "Search" in ui 
    searchLabel = Label(window, text='Search :')
    searchLabel.place(x=20,y=30,width=60,height=25)
    
    #textbox for tping text in ui, setting width,and padding and aligning
    searchTextBox = Entry(window,  width = 30)
    searchTextBox.place(x=200,y=30,width=305,height=20)
    
    #label for predicted words list
    listLabel = Label(window,text ="List of predicted words : ")
    listLabel.place(x=20,y=80,width=150,height=25)

    #list box that contains predicted words 
    wordsList = Listbox(window, height = 5)
    wordsList.place(x=200,y=80,width=305,height=72)
    words = []
    
    #label for manual
    manualLabel = Label(window, text = "Manual : ", anchor="e",justify="left")
    manualLabel.place(x=20,y=190,width=60,height=15)
    
    #label to display manual text
    manualTextLabel = Label(window,text="Type text in textbox labeled 'Search', after typing text press the space bar and if there is any word that \ncan be resulted from prediction will be displayed in listbox, to select the word from listbox double \nclick on that word", justify="left")
    manualTextLabel.place(x=-5,y=210,width=600)
    
    #updating the search text
    updateListBox(searchTextBox, wordsList,words)
    wordsList.bind("<Double-Button-1>",lambda event : resetWordsListBox(searchTextBox,wordsList,words,event))
    searchTextBox.bind("<space>", lambda event : findWordsFromListBox(searchTextBox, wordsList,words,event))

    window.mainloop()

def predictWord(searchText):
    nMinusWords = ""

    # start input command
    line = searchText.get()
    # Grab the last N - 1 words from line
    lastWords = line.lower().split()[-(N-1):]
    
    # Convert back to a single string
    for word in lastWords:
        nMinusWords = nMinusWords + " " + nGramFile.removePunctuations(word)
    nMinusWords = nMinusWords.strip()
    
    # Get prediction of next word - if there is no prediction, will return an empty list
    prediction = nGramFile.generatePrediction(nMinusWords, nGram, nMinusOneGram)

    
    return prediction
    
def main():
    nGramFile.generateGrams(nGram, nMinusOneGram)
    windowFun()
    
main()
#References
#https://tkinter.com/basic-search-and-autofill-python-tkinter-gui-tutorial-162/