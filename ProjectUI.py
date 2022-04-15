from tkinter import *
import nGram


threeGram = {}
twoGram = {}
oneGram = {}
window = Tk(className = "Next Word Predictor")


def resetWordsListBox(searchTextBox,wordsList,words,e):
    #when clicked on any word then reset the textbox and update that word in text box    
    serachTextLen = len(searchTextBox.get())
    searchTextBox.insert(serachTextLen, wordsList.get(ANCHOR) +" ")
    findWordsFromListBox(searchTextBox, wordsList, words, e)

def updateListBox(searchTextBox, wordsList,words):
    #adding each word from wordList to list box
    #print("pressed backspacce")
    if(type(searchTextBox) == str):
        if len(words) == 0 and (len(searchTextBox) > 0):
            notFoundLabel = Label(window,text="Words not found !!", justify="left", fg = "red")
            notFoundLabel.place(x=-50,y=160,width=600)  
        else:
            notFoundLabel = Label(window,text="", justify="left")
            notFoundLabel.place(x=-50,y=160,width=600) 
    elif (len(searchTextBox.get()) == 0):
        notFoundLabel = Label(window,text="", justify="left")
        notFoundLabel.place(x=-50,y=160,width=600) 

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
    manualLabel.place(x=20,y=210,width=60,height=15)
    
    #label to display manual text
    manualTextLabel = Label(window,text="Type text in textbox labeled 'Search', after typing text press the space bar and if there is any word that \ncan be resulted from prediction will be displayed in listbox, to select the word from listbox double \nclick on that word", justify="left")
    manualTextLabel.place(x=-5,y=230,width=600)
    
    #updating the search text

    updateListBox(searchTextBox, wordsList,words)
    wordsList.bind("<Double-Button-1>",lambda event : resetWordsListBox(searchTextBox,wordsList,words,event))
    searchTextBox.bind("<space>", lambda event : findWordsFromListBox(searchTextBox, wordsList,words,event))
    searchTextBox.bind("<BackSpace>", lambda event : findWordsFromListBox(searchTextBox, wordsList,words,event))

    window.mainloop()


# Returns a list of predicted word using first our 3-gram model, and if there aren't 6 predictions,
# we will check with our 2-gram model
def predictWord(searchText):
    prevWords = ""

    # start input command
    line = searchText.get()
    # Grab the last two words from line
    lastTwoWordsList = line.lower().split()[-2:]
    
    # Convert back to a single string
    for word in lastTwoWordsList:
        prevWords = prevWords + " " + word #nGram.removePunctuations(word)
    prevWords = prevWords.strip()
    
    # Get prediction of next word - if there is no prediction, will return an empty list
    prediction = nGram.generatePrediction(prevWords, threeGram, twoGram)

    # If it doesn't contain 6 predictions, we will check predictions with just the last word (i.e. with our 2-gram)
    if len(prediction) < 6 and len(lastTwoWordsList) > 0:
        lastword = lastTwoWordsList[-1].strip()
        morePrediction = nGram.generatePrediction(lastword, twoGram, oneGram)

        for word in morePrediction:
            if word not in prediction:
                prediction.append(word)
            if len(prediction) >= 6:
                break

    return prediction
    
def main():
    # Create our nGrams at the start of the app
    nGram.generateGrams(threeGram, 3)
    nGram.generateGrams(twoGram, 2)
    nGram.generateGrams(oneGram, 1)
    windowFun()
    
main()
#References
#https://tkinter.com/basic-search-and-autofill-python-tkinter-gui-tutorial-162/