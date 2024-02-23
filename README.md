# Recommendation-System-BBC-Articles

This project hosts a simple article recommendation engine I built on a quick flask app I made. To build the recommendation system, I used word vectors from [Stanford's GloVe project](https://nlp.stanford.edu/projects/glove/) trained on a dump of Wikipedia. 
Each word in our BBC article data can be represented by 300-dimensional vector, which was work done by Stanford. Here, we take all those vectors per document to compute the centroid of each of our BBC articles; the centroid is computed by taking the sum of the vectors and dividing that sum by the total number of 

The flask web app displays a list of all the BBC articles on the landing page, and after clicking on an article, the user is directed to another page where we see the text of that article, alongside the top 5 recommended articles. 

Since the app is run locally, after running the orchestrator URL in your browser to get the list of articles:

And to get to a specific article you would go to:
