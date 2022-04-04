import numpy as np

# Constant variables
PUNCTUATIONS = "./\"',<>!?@#$%^&*()~`\\:;“”"
DATAPATH = 'COMP3106_Final_Project/dataset.txt'
N = 3

# Returns and removes all punctuation at the beginning and ending of word
def removePunctuations(word):
    # remove any punctuations from start or end of word
    while (word[0] in PUNCTUATIONS) or (word[-1] in PUNCTUATIONS):
        if word[0] in PUNCTUATIONS:
            word = word[1:]
        if word != '' and word[-1] in PUNCTUATIONS:
            word = word[:-1]
        if word == '':
            break

    return word


# Function to create our and count them n-gram and (n-1)-gram
def generateGrams(nGram, nMinusOneGram):
    nWords = ""
    nMinusOneWords = ""
    wordList = []

    # Read in our text file
    rawData = open(DATAPATH, 'r', encoding='utf8')

    # Add every word into our wordList from rawData
    for line in rawData:
        cleanedLine = line.lower().split()
        wordList = wordList + cleanedLine

    # Generate our n-gram/(n-1)-gram count
    for word in wordList:
        # if there are less than N words in nWords, we will add the current word to it
        if len(nWords.split()) < N:
            nWords = nWords + " " + removePunctuations(word)
            nWords = nWords.strip()
        # similarly, if there are less than (N - 1) words in nMinusOneWords, we will also add the current word to it
        if len(nMinusOneWords.split()) < N - 1:
            nMinusOneWords = nMinusOneWords + " " + removePunctuations(word)
            nMinusOneWords = nMinusOneWords.strip()
        
        # Add nWords to our count of n-grams
        if len(nWords.split()) == N:
            # check if this nWords has been added
            if nWords not in nGram:
                nGram[nWords] = 1
            # if not added, we increase count for occurrence of nWords
            else:
                nGram[nWords] = nGram[nWords] + 1
            
            # Remove first word from nWords
            nWords = nWords.split(' ', 1)[1]
        
        # Do the same with nMinusOneWords with nMinusOneGram
        if len(nMinusOneWords.split()) == N - 1:
            if nMinusOneWords not in nMinusOneGram:
                nMinusOneGram[nMinusOneWords] = 1
            else:
                nMinusOneGram[nMinusOneWords] = nMinusOneGram[nMinusOneWords] + 1
            if " " in nMinusOneWords:
                nMinusOneWords = nMinusOneWords.split(' ', 1)[1]
            else:
                nMinusOneWords = ""
        
        # Finally, current word is the end of a sentence/clause, then we will start a new set of strings to add
        if word[-1] in PUNCTUATIONS:
            # We create a new nGram section, this will make suggestions more human-like
            nWords = ""
            nMinusOneWords = ""


# Function to generate and return our top predicted next word as a list
def generatePrediction(nMinusWords, nGram, nMinusOneGram):
    maxNum = 3
    count = 0
    topNextWords = []
    potentialNextWords = {}
    nextWordfrequencies = {}

    if nMinusWords not in nMinusOneGram:
        return []
    nMinusOneGramCount = nMinusOneGram[nMinusWords]

    # First grab potential next word
    for nGramWords in nGram:
        if (nMinusWords + " ") in nGramWords[:len(nMinusWords)+1]:
            potentialNextWords[nGramWords] = nGram[nGramWords]
    
    # Calculate frequency of next word using the following equation: count(n-gram)/count((n-1)-gram)
    for nGramWords in potentialNextWords:
        nextWord = nGramWords[len(nMinusWords)+1:]
        nextWordfrequencies[nextWord] = potentialNextWords[nGramWords]/nMinusOneGramCount
    
    # Sort the frequency from highest to lowest
    sortedFreq = {k: v for k, v in sorted(nextWordfrequencies.items(), reverse=True, key=lambda item: item[1])}

    # Return back the top maxNum most probable next word
    for word in sortedFreq:
        count += 1
        if count > maxNum:
            break
        topNextWords.append(word)
        

    return topNextWords

'''
def main():
    # dictionary: keys are strings and is the n consecutive words, values is its count of occurences
    nGram = {}
    nMinusOneGram = {}
    nMinusWords = ""
    generateGrams(nGram, nMinusOneGram)

    # start input command
    line = input('> ')
    # Grab the last N - 1 words from line
    lastWords = line.lower().split()[-(N-1):]     

    # Convert back to a single string
    for word in lastWords:
        nMinusWords = nMinusWords + " " + removePunctuations(word)
    nMinusWords = nMinusWords.strip()

    # Get prediction of next word - if there is no prediction, will return an empty list
    prediction = generatePrediction(nMinusWords, nGram, nMinusOneGram)
    print(prediction)
    print()

main()
'''

# Some ways to get better accuracy: have a larger data set, but this will require larger cpu power
# another way for better accuracy is getting better data sets with more common every day phrases