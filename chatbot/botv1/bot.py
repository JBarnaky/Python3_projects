import random
import string
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Downloading necessary packages
nltk.download('punkt')
nltk.download('wordnet')

class BiboChatbot:
    def __init__(self, filename):
        self.filename = filename
        self.lemmatizer = WordNetLemmatizer()
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        self.GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
        self.GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
        self.sent_tokens = self.load_data()

    def load_data(self):
        with open(self.filename, 'r', errors='ignore') as file:
            raw = file.read().lower()
            return sent_tokenize(raw)

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower().translate(self.remove_punct_dict))
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def greeting(self, sentence):
        for word in sentence.split():
            if word.lower() in self.GREETING_INPUTS:
                return random.choice(self.GREETING_RESPONSES)

    def response(self, user_response):
        tfidf_vec = TfidfVectorizer(tokenizer=self.preprocess_text, stop_words='english')
        tfidf = tfidf_vec.fit_transform(self.sent_tokens + [user_response])
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            return "I am sorry! I don't understand you"
        else:
            return self.sent_tokens[idx]

    def run(self):
        print("BIBO: My name is Bibo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
        while True:
            user_response = input().lower()
            if user_response == 'bye':
                print("BIBO: Bye! take care..")
                break
            elif user_response in ('thanks', 'thank you'):
                print("BIBO: You are welcome..")
                break
            elif self.greeting(user_response) is not None:
                print("BIBO: " + self.greeting(user_response))
            else:
                print("BIBO: " + self.response(user_response))

if __name__ == "__main__":
    chatbot = BiboChatbot('chatbot.txt')
    chatbot.run()
