# Launch with
#
# python server.py

from flask import Flask, render_template
import sys
import pickle
import boto3
import os

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    return render_template('articles.html',articles = articles)  # Lets worry about formatting in the html


@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    checker = topic + '/' + filename
    artic_html = []
    for article_name in articles:
        parts = article_name[0].split("/")
        s = parts[-2] + "/" + parts[-1] 
        if s == checker:  # If found
            artic_html = article_name
            break  # Save data and break
    recs_html = recommended[(topic,filename)]  
    return render_template('article.html',title = artic_html[1],text = [artic_html[2]],recs = recs_html)


# f = open('articles.pkl', 'rb')
# articles = pickle.load(f)
# f.close()

# f = open('recommended.pkl', 'rb')
# recommended = pickle.load(f)
# f.close()


# for local debug
if __name__ == '__main__':
    aws_public = os.environ.get('aws_public')
    aws_secret = os.environ.get('aws_priv')
    name = "ob123"  # Can make these environment vars later
    bucket_name = "article-proj"  # Can make these environment vars later
    keys = ["pickles/articles.pkl", "pickles/recommended.pkl"]
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_public,
        aws_secret_access_key=aws_secret
    )
    data = {}
    for key_name in keys:
        object = s3.get_object(Bucket=bucket_name, Key=key_name)
        data[key_name] = pickle.loads(object['Body'].read())

    articles = data["pickles/articles.pkl"]
    recommended = data["pickles/recommended.pkl"]
    app.run(debug=False, host='0.0.0.0')




