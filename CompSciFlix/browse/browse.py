from flask import Blueprint, request, render_template, redirect, url_for, session

import CompSciFlix.utilities.utilities as utilities
from CompSciFlix.news import news
from flask import request


browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    return render_template('browse/browse.html',tag_urls=utilities.get_tags_and_urls())

@browse_blueprint.route('/browse/search_movie', methods=['GET', 'POST'])
def search_movie():
    input = request.form.get("search_term")
    term = input[0].upper()+input[1:]
    category = request.form.get("category")
    if category == "genre":
        return news.articles_by_tag(tag=term)
    if category == "title":
        return news.movies_by_title(title=term)
    if category == "director":
        return news.movies_by_director(director=term)
    if category == "actor":
        return news.articles_by_actor(actor=term)
