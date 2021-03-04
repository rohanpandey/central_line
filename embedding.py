from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors

Dimension=100

def embed_column(dataframe,column,model):
	value_array=[]
		for index,row in dataframe.iterrows():
			note_as_vec=[]
			preprocessed_text=apply_all(dataframe[column])
			for word in preprocessed_text:
				try:
				    vec_word = model[word]
				except:
					vec_word = [0.0]*Dimension
        		note_as_vec.append(biowordvec_word)
        	value=np.average(note_as_vec, axis=0)
        	value_array.append(value)
	dataframe[column+'_avg']=value_array
	return dataframe

def load_glove()
	Word2vecpath = os.path.expanduser("insert location of downloaded file here") 
	word2vec = gensim.models.KeyedVectors.load_word2vec_format(word2vecpath, binary=True)
	return word2vec

def load_w2v()
	glovepath = os.path.expanduser("insert location of downloaded file here")
	temp_file = "/tmp/glove.840B.300d.w2v.txt"
	glove2word2vec(glovepath, temp_file)
	glove = gensim.models.KeyedVectors.load_word2vec_format(tmp_file)
	return glove