import random
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Downloading necessary packages
nltk.download('punkt')
nltk.download('wordnet')


# Reading and preprocessing data
with open('chatbot.txt', 'r', errors='ignore') as file:
    raw = file.read().lower()
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)


# Text preprocessing functions
lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Chatbot response functions
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    bibo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        bibo_response = "I am sorry! I don't understand you"
    else:
        bibo_response = sent_tokens[idx]
    sent_tokens.remove(user_response)
    return bibo_response


# Chatbot initialization and main loop
print("BIBO: My name is Bibo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
while True:
    user_response = input().lower()
    if user_response == 'bye':
        print("BIBO: Bye! take care..")
        break
    elif user_response in ('thanks', 'thank you'):
        print("BIBO: You are welcome..")
        break
    elif greeting(user_response) is not None:
        print("BIBO: " + greeting(user_response))
    else:
        print("BIBO: " + response(user_response))
