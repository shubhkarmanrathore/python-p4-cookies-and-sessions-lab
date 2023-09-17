#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    all_articles = Article.query.all()
    articles = []
    
    for article in all_articles:
        articles.append(article.to_dict())

    response = make_response(jsonify(articles), 200)

    return response

@app.route('/articles/<int:id>')
def show_article(id):
    article_by_id = Article.query.filter(Article.id==id).first()
    dict = article_by_id.to_dict()
    if session.get('page_views'):
        session['page_views']+=1
    else:
        session['page_views']=1
    
    if session.get('page_views')>3:
        response_body = {
            'message': 'Maximum pageview limit reached'
        }
        resonse = make_response(jsonify(response_body), 401)
        return resonse
    else:
        return make_response(jsonify(dict), 200)

if __name__ == '__main__':
    app.run(port=5555)
