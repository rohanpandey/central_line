from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

def initial_clean(text):
    text = re.sub("((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text)
    text = re.sub("[^a-zA-Z ]", "", text)
    text = text.lower() # lower case the text
    text = nltk.word_tokenize(text)
    return text

def pad_punctuation(note):
    PUNCTS = "!\"#$%'()*+,-./:;<=>?@[\]^_`{|}~"
    updated_list = []
    for i in range(len(note)):
        if note[i] in PUNCTS:
            updated_list.extend([" ", note[i], " "])
        else:
            updated_list.append(note[i])
    return ''.join(updated_list)

def stem_words(text):

	stemmer = PorterStemmer()
    try:
        text = [stemmer.stem(word) for word in text]
        text = [word for word in text if len(word) > 1]  # make sure we have no 1 letter words
    except IndexError:  # the word "oed" broke this, so needed try except
        pass
    return text

def lem_words(text):
    lemmatizer = WordNetLemmatizer()
    try:
        text = [lemmatizer.lemmatize(word) for word in text]
        text = [word for word in text if len(word) > 1]
    except IndexError:
        pass
    return text

def remove_stop_words(text):
	stop_words = stopwords.words('english')
    return [word for word in text if word not in stop_words]

def apply_all(text):
    summary = lem_words(stem_words(remove_stop_words(initial_clean(pad_punctuation(text)))))
    return summary 