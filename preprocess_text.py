import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
import re


def initial_clean(text):
	'''
	Function to remove extra characters, convert to lowercase, and tokenize the sentence.
	Input: String
	Output: list of words
	'''
    text = re.sub("((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text)
    text = re.sub("[^a-zA-Z ]", "", text)
    text = text.lower()
    text = word_tokenize(text)
    return text

def pad_punctuation(text):
	'''
	Function to add extra spaces around punctuations for improved tokenization
	Input: String 
	Output: String
	'''
    PUNCTS = "!\"#$%'()*+,-./:;<=>?@[\]^_`{|}~"
    updated_list = []
    for i in range(len(text)):
        if text[i] in PUNCTS:
            updated_list.extend([" ", text[i], " "])
        else:
            updated_list.append(text[i])
    return ''.join(updated_list)

def stem_words(text):
	'''
	Function for stemming words.
	Input: List of words
	Output: List of words
	'''
  stemmer = PorterStemmer()
  try:
    text = [stemmer.stem(word) for word in text]
    text = [word for word in text if len(word) > 1]  
  except IndexError: 
    pass
  return text

def lem_words(text):
	'''
	Function for lemmatizing words.
	Input: List of words
	Output: List of words
	'''
  lemmatizer = WordNetLemmatizer()
  try:
    text = [lemmatizer.lemmatize(word) for word in text]
    text = [word for word in text if len(word) > 1]
  except IndexError:
    pass
  return text

def remove_stop_words(text):
	'''
	Function for removing stopwords words.
	Input: List of words
	Output: List of words
	'''
  stop_words = stopwords.words('english')
  return [word for word in text if word not in stop_words]

def apply_all(text):
	'''
	Function to apply all preprocessing techniques.
	Input: string
	Output: List of words
	'''
  summary = lem_words(stem_words(remove_stop_words(initial_clean(pad_punctuation(text)))))
  return summary