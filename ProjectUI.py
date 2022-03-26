from tkinter import *

def resetWordsListBox(e):
    #when clicked on any word then reset the textbox and update that word in text box
	searchTextBox.delete(0, END)
	searchTextBox.insert(0, wordsList.get(ANCHOR))

def updateListBox(words):
    #adding each word from wordList to list box
	wordsList.delete(0, END)
	for i in words:
		wordsList.insert(END, i)
        
#checks for the similar letter in words as the texts are being typed ins search box
#and keeps relevent text
def findWordsFromListBox(e):
    searchText = searchTextBox.get()
    #prints the result to cmd as the user types the text in searchbox
    print(searchText)
    if searchText == '':
    	wordsFound = words
    else:
        wordsFound = []
        for i in words:
            if searchText.lower() in i.lower():
                wordsFound.append(i)
    updateListBox(wordsFound)               

#setting output ui's window size to middle by calculating the screenwidth and height
windowWidth = 400
windowHeight = 400
window = Tk(className = "Next Word Predictor")
screenWidth = window.winfo_screenwidth() 
screenHeight = window.winfo_screenheight() 

x = (screenWidth/2) - (windowWidth/2)
y = (screenHeight/2) - (windowHeight/2)

window.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))

#search label that shows "Search" in ui 
searchLabel = Label(window, text='Search:')
searchLabel.grid(row = 0,column=0,padx =10)

#textbox for tping text in ui, setting width,and padding and aligning
searchTextBox = Entry(window,  width = 30)
searchTextBox.grid(row = 0,column=1,pady=10,padx=10)

#list box that contains words 
wordsList = Listbox(window, height = 5)
wordsList.grid(row=1,column = 1)
words = ['Java', 'C#', 'C', 'C++', 'Python','Go', 'JavaScript', 'PHP', 'Swift']

updateListBox(words)
wordsList.bind("<<ListboxSelect>>",resetWordsListBox)
searchTextBox.bind("<KeyRelease>", findWordsFromListBox)

window.mainloop()


#References
#https://tkinter.com/basic-search-and-autofill-python-tkinter-gui-tutorial-162/