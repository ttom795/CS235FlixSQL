from flask import Blueprint, request, render_template, redirect, url_for, session

import CompSciFlix.adapters.repository as repo
import CompSciFlix.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint('utilities_bp', __name__)


def get_tags_and_urls():
    tag_names = services.get_tag_names(repo.repo_instance)
    tag_urls = dict()
    for tag_name in tag_names:
        tag_urls[tag_name] = url_for('news_bp.articles_by_tag', tag=tag_name)
    return tag_urls

def get_selected_articles(quantity=3):
    articles = services.get_random_articles(quantity, repo.repo_instance)
    for article in articles:
        article.hyperlink = url_for('news_bp.article_page', article_input=article.id)
    return articles
