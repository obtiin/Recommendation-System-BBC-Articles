# Recommendation-System-BBC-Articles

This project creates a simple article recommendation engine using word vectors, usingword vectors from [Stanford's GloVe project](https://nlp.stanford.edu/projects/glove/) trained on a dump of Wikipedia. 
Each word in our BBC article data can be represented by 300-dimensional vector, which was work done by Stanford. Here, we take all those vectors per document to compute the centroid of each of our BBC articles; the centroid is computed by taking the sum of the vectors and dividing that sum by the total number of 

To host the recommendation engine, I built a simple flask web app that displays a list of all the BBC articles on the landing page. After clicking on an article, we go to another page where we see the text of that article, alongside the top 5 recommended articles. 

When testing from your laptop, you would go to the following URL in your browser to get the list of articles:

And to get to a specific article you would go to:
