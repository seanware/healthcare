#perfom textual analysis of the tweets

from sys import argv
from collections import Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt




def load_clean_text(tweet_file):
	""" This funcitons loads in a file from stdin, removes the 
	stopwords words from the text using nltk's stopwords corpus
	and outputs a filtered text file.
	"""
	
	stops = stopwords.words('english')
	stops.append('rt')#remove the rt from the language
		
	with open(tweet_file) as f:
		line = f.read()
		#populate the counter
		text = line.strip().lower().split()
	filtered_text = [ txt  for txt in text if txt not in stops]		
	return filtered_text
	

def frequency_distribution(text_list):
	"""  
	Takes in the filtered text data and returns a
	dictionary with the counts of the words
	"""
	return Counter(text_list)
	

def word_percentages(text_list):
	"""
	Takes in the filtered text data and returns a dictionary 
	with the percentage of the words in the text
	"""
	num_words = float(len(text_list))
	word_freq = Counter()
	for filtered_word in text_list:
		word_freq[filtered_word] += (1/num_words) * 100
	return word_freq		
	
	
	
def plot_frequency(counter_words):
	"""
	Create a LogLog plot from the text dictionaries
	"""
	word_counts = sorted(counter_words.values(), reverse=True)
	plt.loglog(word_counts)
	plt.ylabel("Freq")
	plt.xlabel("Word Rank")
	plt.show()
	
def plot_histogram(counter_words):
	""" 
	Creates a histogram of the word counts
	"""	
	plt.hist(counter_words.values(), bins = 25)
	plt.title("Histogram of Hashtags")
	plt.ylabel("Number of items in Bin")
	plt.xlabel("Bins")
	plt.show()	

	
	
if __name__ == "__main__":
	tweets = argv[1]
	words = load_clean_text(tweets)
	freq = word_percentages(words)
	plot_histogram(freq)
	
		