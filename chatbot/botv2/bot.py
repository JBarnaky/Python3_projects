import nltk
from nltk.chat.util import Chat
import csv

def load_pairs_and_reflections(filename):
    pairs = []
    reflections = {}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'pairs':
                pairs.append([row[1], row[2:]])
            elif row[0] =='reflections':
                reflections[row[1]] = row[2]
    return pairs, reflections

def chat():
    print("Hi! I am a chatbot created by Analytics Vidhya for your service")
    pairs, reflections = load_pairs_and_reflections('chatbot_data.csv')
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    chat()
