from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import warnings
warnings.filterwarnings("ignore")

nltk.download("punkt", quiet = True)

article = Article ("https://m.economictimes.com/markets/cryptocurrency/top-cryptocurrency-prices-today-bitcoin-ethereum-solana-add-up-to-3/articleshow/87708694.cms")
article.download()
article.parse()
article.nlp()
corpus = article.text

text = corpus
sentence_list = nltk.sent_tokenize(text)

def greeting_response(text):
  text = text.lower()
  bot_greetings = ["hi", "hey", "hello"]
  user_greetings = ["hi", "hey", "hello", "greetings"]

  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)

def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:

        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp

  return list_index

def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response = ""
  cm = CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1], cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)
  index = index[1:]
  response_flag = 0

  j = 0
  for i in range(len(index)):

    if similarity_scores_list[index[i]] > 0.0:
      bot_response = bot_response+" "+sentence_list[index[i]]
      response_flag = 1
      j = j+1
    if j > 2:
      break

  if response_flag == 0:
    bot_response = bot_response+" "+"I apologize, I don't understand"

  sentence_list.remove(user_input)

  return bot_response

print ("Bot: I am Bot. I will answer your queries about site. If you want to exit, type bye.")

exit_list = ["bye", "exit", "quit", "see you later", "break"]

while (True):
  user_input = input("User: ")
  if user_input.lower() in exit_list:
    print ("Bot: Chat with you later!")
    break
  else:
    if greeting_response(user_input) != None:
      print ("Bot: " + greeting_response(user_input))
    else:
      print ("Bot: " + bot_response(user_input))
