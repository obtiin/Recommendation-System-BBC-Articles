# Launch with
#
# python app.py

from flask import Flask, render_template
import sys
import pickle

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


f = open('articles.pkl', 'rb')
articles = pickle.load(f)
f.close()

f = open('recommended.pkl', 'rb')
recommended = pickle.load(f)
f.close()


##Just a bunch of test code I needed to see what was going on.

# print((articles[0][1]))
# topic = "business"
# filename = "030.txt"
# article_object = []
# checker = topic + '/' + filename

# for article_name in articles:
#     parts = article_name[0].split("/")
#     s = parts[-2] + "/" + parts[-1] 
#     if s == checker:  # Seemingly because this part is messed up, meaning the pickle is messed up?
#         article_object = article_name
#         break
# print(len(article_object))  # This is always a empty list
# x = recommended[("business","353.txt")]
# for v in x:
#     print(v)  # v[0] is blank, v[2] is title.


# for local debug
if __name__ == '__main__':
    app.run(debug=True)