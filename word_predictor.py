import numpy as np
import re


# process data and initialize dataset with words and there possible predictions
def init_dataset(dataset):
    data_raw = open('COMP3106_Final_Project/dataset.txt', 'r', encoding='utf8')
    data_string = ""

    # convert data to single string
    for line in data_raw:
        data_string += line.strip().lower() + ' '
    
    # split into list of sentences and remove spaces on both sides
    data_list = re.split('[\.\?\!\:\;]\s*', data_string)
    
    # remove stuff in quotaions
    # remove single words/letters
    # remove special characters
    for line in data_list:
        if (len(line) < 10):
            data_list.remove(line)
        
        if ('(' in line and ')' in line):
            line = line[:line.index('(')] + line[line.index(')'):]

        words = line.strip().replace('\n', '').replace('\r', '').replace('\ufeff', '').replace('“','').replace('”','').replace(',', '').split(' ')

        for i in range(len(words) - 1):
            update_dataset(dataset, words[i], words[i+1])


# update dataset with word and possible prediction pair
def update_dataset(dataset, word, next_word):
    if word not in dataset:
        new = {word: {next_word: 1}}
        dataset.update(new)
        return

    other_words = dataset[word]

    if next_word not in other_words:
        other_words.update({next_word: 1})
    else:
        other_words.update({next_word: other_words[next_word] + 1})


# calculate probabillities of words following another
def calculate_probability(dataset):
    for word, other_words in dataset.items():
        temp = {}
        for key, value in other_words.items():
            word_probability = [(key, value / sum(other_words.values()))]
            temp.update(word_probability)

        other_words = temp
        dataset[word] = other_words


# predict word from user input
def predict_word(dataset):
    line = input('> ')
    word = line.strip().split(' ')[-1].lower()
    if word not in dataset:
        print('No predictions available...')
    else:     
        other_words = dataset[word]
        predictions = []
        for i in range(3):
            next_word = np.random.choice(list(other_words.keys()), p=list(other_words.values()))
            while next_word in predictions:
                next_word = np.random.choice(list(other_words.keys()), p=list(other_words.values()))
            predictions.append(next_word)

        print(predictions)


def main():
    dataset = {}

    init_dataset(dataset)
    calculate_probability(dataset)
    predict_word(dataset)


main()

# problem 1: only predicts from last word (not very accurate)
# problem 2: does not predict after punctuation (ex. "what is life?" = no predictions)