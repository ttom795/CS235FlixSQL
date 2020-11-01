from datetime import date

import pytest

from CompSciFlix.authentication.services import AuthenticationException
from CompSciFlix.news import services as news_services
from CompSciFlix.authentication import services as auth_services
from CompSciFlix.news.services import NonExistentArticleException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    article_id = 3
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the comment.
    news_services.add_comment(article_id, comment_text, username, in_memory_repo, 3)

    # Retrieve the comments for the article from the repository.
    comments_as_dict = news_services.get_comments_for_article(article_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['comment_text'] for dictionary in comments_as_dict if dictionary['comment_text'] == comment_text),
        None) is not None


def test_cannot_add_comment_for_non_existent_article(in_memory_repo):
    article_id = 101
    comment_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(news_services.NonExistentArticleException):
        news_services.add_comment(article_id, comment_text, username, in_memory_repo, 3)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    article_id = 3
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(news_services.UnknownUserException):
        news_services.add_comment(article_id, comment_text, username, in_memory_repo, 3)


def test_can_get_article(in_memory_repo):
    article_id = 1

    article_as_dict = news_services.get_article(article_id, in_memory_repo)

    assert article_as_dict['id'] == article_id
    assert article_as_dict['date'] == 2014
    assert article_as_dict['title'] == 'Guardians of the Galaxy'
    assert len(article_as_dict['comments']) == 2

    tag_names = [dictionary['name'] for dictionary in article_as_dict['tags']]
    assert 'Action' in tag_names
    assert 'Adventure' in tag_names
    assert 'Sci-Fi' in tag_names


def test_cannot_get_article_with_non_existent_id(in_memory_repo):
    article_id = 101

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(news_services.NonExistentArticleException):
        news_services.get_article(article_id, in_memory_repo)


def test_get_first_article(in_memory_repo):
    article_as_dict = news_services.get_first_article(in_memory_repo)

    assert article_as_dict['id'] == 40


def test_get_last_article(in_memory_repo):
    article_as_dict = news_services.get_last_article(in_memory_repo)

    assert article_as_dict['id'] == 3


def test_get_articles_by_date_with_one_date(in_memory_repo):
    target_date = 2014

    articles_as_dict, prev_date, next_date = news_services.get_articles_by_date(target_date, in_memory_repo)

    assert len(articles_as_dict) == 2
    assert articles_as_dict[1]['id'] == 1

    assert prev_date == 2012
    assert next_date == 2015


def test_get_articles_by_date_with_multiple_dates(in_memory_repo):
    target_date = 2014

    articles_as_dict, prev_date, next_date = news_services.get_articles_by_date(target_date, in_memory_repo)

    # Check that there are 2 articles dated 2014.
    assert len(articles_as_dict) == 2

    # Check that the article ids for the the articles returned are 3, 4 and 5.
    article_ids = [article['id'] for article in articles_as_dict]
    assert article_ids == [37,1]

    # Check that the dates of articles surrounding the target_date are 2020-02-29 and 2020-03-05.
    assert prev_date == 2012
    assert next_date == 2015


def test_get_articles_by_date_with_non_existent_date(in_memory_repo):
    target_date = 2021

    articles_as_dict, prev_date, next_date = news_services.get_articles_by_date(target_date, in_memory_repo)

    # Check that there are no articles dated 2020-03-06.
    assert len(articles_as_dict) == 0


def test_get_articles_by_id(in_memory_repo):
    target_article_ids = [5, 6, 7, 8]
    articles_as_dict = news_services.get_articles_by_id(target_article_ids, in_memory_repo)

    # Check that 4 articles were returned from the query.
    assert len(articles_as_dict) == 4

    # Check that the article ids returned were 5 and 6.
    article_ids = [article['id'] for article in articles_as_dict]
    assert set([5, 6]).issubset(article_ids)


def test_get_comments_for_article(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_article(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(comments_as_dict) == 2

    # Check that the comments relate to the article whose id is 1.
    article_ids = [comment['article_id'] for comment in comments_as_dict]
    article_ids = set(article_ids)
    assert 1 in article_ids and len(article_ids) == 1


def test_get_comments_for_non_existent_article(in_memory_repo):
    with pytest.raises(NonExistentArticleException):
        comments_as_dict = news_services.get_comments_for_article(101, in_memory_repo)


def test_get_comments_for_article_without_comments(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_article(2, in_memory_repo)
    assert len(comments_as_dict) == 0

