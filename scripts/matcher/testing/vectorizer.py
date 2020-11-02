# importing all necessary modules
import warnings

warnings.filterwarnings(action = 'ignore')

import gensim
from gensim.models import Word2Vec

def word_model(data):
	# # Create CBOW model
	# cbow = gensim.models.Word2Vec(data, min_count = 1, size = 100, window = 5)

	# Create Skip Gram model
	skipgram = gensim.models.Word2Vec(data, min_count = 1, size = 100, window = 5, sg = 1)

	return skipgram

def sentence_model(data):
	wm = word_model(data)



from nltk import corpus
skipgram_model = model(corpus.gutenberg.words())

from sklearn.cluster import MiniBatchKmeans, Kmeans

clust = KMeans(init="k-means++", n_clusters=5, n_init=10)
clust.fit(features)
