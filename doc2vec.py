import sys
import re
import string
import os
import numpy as np
import codecs
import pickle

# From scikit learn that got words from:
# http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words
ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"])


def load_glove(filename):
    """
    Read all lines from the indicated file and return a dictionary
    mapping word:vector where vectors are of numpy `array` type.
    GloVe file lines are of the form:

    the 0.418 0.24968 -0.41242 0.1217 ...

    So split each line on spaces into a list; the first element is the word
    and the remaining elements represent factor components. The length of the vector
    should not matter; read vectors of any length.

    ignore stopwords
    """

    output = {}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:  # Iterate through each line
            parts = line.split(" ")
            word = parts[0]  # First element is word
            vals = np.array([float(val) for val in parts[1:]])

            # Check if the word is not a stopword
            if word not in ENGLISH_STOP_WORDS:
                output[word] = vals

    return output

def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    allfiles = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            allfiles.append(os.path.join(path, name))
    return allfiles


def get_text(filename):
    """
    Load and return the text of a text file, assuming latin-1 encoding as that
    is what the BBC corpus uses.  Use codecs.open() function not open().
    """
    f = codecs.open(filename, encoding='latin-1', mode='r')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    
        1. Lowercase all words
        2. Use re.sub function and string.punctuation + '0-9\\r\\t\\n]'
            to replace all those char with a space character.
        3. Split on space to get word list.
        4. Ignore words < 3 char long.
        5. Remove English stop words
    Don't use Spacy.
    """
    text = text.lower()
    text = re.sub("[" + string.punctuation + '0-9\\r\\t\\n]', ' ', text)
    words = text.split(" ")
    output = []
    for w in words:
        if len(w) >= 3:
            if w not in ENGLISH_STOP_WORDS:
                output.append(w)

    return output


def split_title(text):
    """
    Given text returns title and the rest of the article.

    Split the test by "\n" and assume that the first element is the title
    """
    parts = text.split("\n")
    title = parts[0]
    content = "\n".join(parts[1:])
    return title, content



def load_articles(articles_dirname, gloves):
    """
    Load all .txt files under articles_dirname and return a table (list of lists/tuples)
    where each record is a list of:

      [filename, title, article-text-minus-title, wordvec-centroid-for-article-text]

    We use gloves parameter to compute the word vectors and centroid.

    The filename is fully-qualified name of the text file including
    the path to the root of the corpus passed in on the command line.

    When computing the vector for each document, use just the text, not the text and title.
    """

    output = []

    for root, dirs, files in os.walk(articles_dirname):
        for file in files:
            if file.endswith(".txt"):  # Check to ensure textfile
                filename = os.path.join(root, file)
                with open(filename, "r", encoding="latin-1") as f:
                    content = f.read()
                title, article_text = split_title(content)  # Use splittitle() for title vs content
                word_vectors = [gloves[word] for word in words(article_text) if word in gloves]  # Centroid, use if word in gloves like on slack
                if word_vectors:
                    centroid = np.mean(word_vectors, axis=0)
                else:
                    centroid = None  # Weird nonetype error fix

                # Create a record and add it to the list
                article_record = [filename, title, article_text, centroid]
                output.append(article_record)

    return output


def doc2vec(text, gloves):
    """
    Return the word vector centroid for the text. Sum the word vectors
    for each word and then divide by the number of words. Ignore words
    not in gloves.
    """
    g_keys = gloves.keys() 
    vector = [gloves[key] for key in text if key in g_keys]
    np_arr = np.array(vector, dtype=float)
    return np_arr.mean(axis = 0)  


def distances(article, articles):
    """
    Compute the euclidean distance from article to every other article.

    Inputs:
        article = [filename, title, text-minus-title, wordvec-centroid]
        articles is a list of [filename, title, text-minus-title, wordvec-centroid]

    Output:
        list of (distance, a) for a in articles
        where a is a list [filename, title, text-minus-title, wordvec-centroid]
    """
    # Calculate the Euclidean distance between the article and all other articles
    output = []
    for x in articles:
        if x[0] != article[0]:  #  If not the same article
            distance = np.linalg.norm(article[3] - x[3])  # Euclidian dist
            output.append((distance, [x[0], x[1], x[2],x[3]]))
        else:
            output.append((0, [x[0], x[1], x[2], x[3]]))  # If it is the same, just say dist=0
    return output


def recommended(article, articles, n):
    """ Return top n articles closest to article.

    Inputs:
        article: list [filename, title, text-minus-title, wordvec-centroid]
        articles: list of list [filename, title, text-minus-title, wordvec-centroid]

    Output:
         list of [topic, filename, title]
    """
    d = distances(article, articles)
    artic_sort = sorted(d, key=lambda x: x[0])
    top_n = artic_sort[1:n+1]  # Do it from 1 to n+1 to remove the article itself (dist=0)
    output = [[a[1][0].split("/")[-2], a[1][0].split("/")[-1], a[1][1]] for a in top_n]
    return output


def main():
    glove_filename = sys.argv[1]
    articles_dirname = sys.argv[2]
    gloves = load_glove(glove_filename)
    articles = load_articles(articles_dirname, gloves)  
    with open("articles.pkl", "wb") as articles_file:  # Topic, filename, title, text
        pickle.dump(articles, articles_file)
    # Loop through articles to generate recommendations for each article
    recommendations = {}
    for article in articles:
        if len(article) >= 2:
            path = article[0]  # Extract the file path
            title = article[1]  # Extract the title
            key = (path.split("/")[-2], path.split("/")[-1])  # Split the path to get topic and filename --> Keys are fine
            recommended_articles = recommended(article, articles, 5) # Returning 0 ='', 1 = Users
            recommendations[key] = recommended_articles
    with open("recommended.pkl", "wb") as recommended_file:
        pickle.dump(recommendations, recommended_file)

if __name__ == '__main__':
    main()

