# Recommendation-System-BBC-Articles

This project is an article recommendation engine I built on a flask app I made, hosted on the web via an AWS EC2 instance. To build the recommendation system, I used word vectors from [Stanford's GloVe project](https://nlp.stanford.edu/projects/glove/) trained on a dump of Wikipedia. Each word in our BBC article data can be represented by 300-dimensional vector, which was work done by Stanford. Here, we take all those vectors per document to compute the centroid of each of our BBC articles; the centroid is computed by taking the average of all the word vectors in a document, giving us one 300-entry vector to represent our entire document. Two documents are considered similar if those 2 document vectors are close in the 300-dimension space. Thus, by calculating the distance between the cetroid of a given article and the centroids of all other articles in the dataset, we can determine the articles most similar to the one the user clicked on. 

The flask web app displays a list of all the BBC articles on the landing page, and after clicking on an article, the user is directed to another page where we see the text of that article, alongside the top 5 similar articles. 


- http://13.57.19.113/
- To get to another article, you can click on any hyperlink on the homepage, for example:
[`http://127.0.0.1/:5000/article/entertainment/303.txt`](http://13.57.19.113/article/entertainment/074.txt)

# Files:
- Dockerfile:
    - The Dockerfile is used to build a Docker image for the project.
    - It specifies the environment and dependencies required to run the application, and actually runs the application.
- requirements.txt
    - The requirements.txt file lists all the Python dependencies required for the project to be installed by pip.
- doc2vec.py:
    - The doc2vec.py file contains code for generating document embeddings using the Doc2Vec algorithm.
    - These embeddings are used to calculate article similarity for recommendation.
- server.py
    - The server.py file contains the Flask application code.
    - It defines the routesfor serving the web application, including displaying articles and generating recommendations.
- article.html & articles.html:
    - These two html files are the html templates for displaying the landing page (a list of all the articles), and the page     
      displaying the article content and its similar articles.
