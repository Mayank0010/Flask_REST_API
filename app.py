from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

# DB Model


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64))
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)

    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content

    def __repr__(self):
        return '< Article %r >' % self.title

# Schema


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'title', 'content')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

# Default route


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello World', 'status': 'OK 200'})

# Get all articles


@app.route('/articles', methods=['GET'])
def get_articles():
    all_articles = Article.query.all()
    result = articles_schema.dump(all_articles)

    return jsonify(result)

# Get articles by id


@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.filter_by(id=id).first_or_404()
    return article_schema.jsonify(article)

# Get articles by title


@app.route('/articles/<title>', methods=['GET'])
def get_article_by_title(title):
    article = Article.query.filter_by(title=title).first_or_404()
    return article_schema.jsonify(article)

# Add article


@app.route('/articles', methods=['POST'])
def add_article():
    author = request.json['author']
    title = request.json['title']
    content = request.json['content']

    new_article = Article(author, title, content)
    db.session.add(new_article)
    db.session.commit()
    return article_schema.jsonify(new_article)

# Update an article


@app.route('/articles/<int:id>', methods=['PUT'])
def update_article(id):
    article = Article.query.get(id)

    author = request.json['author']
    title = request.json['title']
    content = request.json['content']

    article.author = author
    article.title = title
    article.content = content

    db.session.commit()
    return article_schema.jsonify(article)

# Delete a single article


@app.route('/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


# main
if __name__ == '__main__':
    app.run(debug=True)
