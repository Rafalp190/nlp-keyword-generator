import pandas as pd
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
import multiprocessing

df = pd.read_pickle("./cured_data/train.pkl")

EMB_DIM = 300
w2v = Word2Vec(df.Abstract, size=EMB_DIM, window=5, min_count=5, negative=15, iter=10, workers=multiprocessing.cpu_count())
output_w2v = Word2Vec(df.Topics, size=EMB_DIM, window=5, min_count=5, negative=15, iter=10, workers=multiprocessing.cpu_count())
#Save the word vectors for later use
word_vectors_input = w2v.wv
fname = get_tmpfile("abstract_vectors.kv")
word_vectors_input.save(fname)

word_vectors_output = output_w2v.wv
fname_out = get_tmpfile("keywords_vectors.kv")
word_vectors_output.save(fname_out)

fname = get_tmpfile("abstract_vectors.kv")
fname_out = get_tmpfile("keywords_vectors.kv")
