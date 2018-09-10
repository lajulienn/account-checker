import requests

from bs4 import BeautifulSoup as bs
from checker.db import get_db

from flask import Blueprint, jsonify


bp = Blueprint('checker', __name__)


class PageTitleError(Exception):
    """
    Exception raised for errors in the page title processing.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class SiteAnalyser:
    REQUEST_HEADER = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0)'
                      ' Gecko/20100101 Firefox/61.0'
    }

    XIAOMI_DATA = {
        'PAGE_TITLES': {
            'account_exists': 'Mi аккаунт - Проверка подлинности Аккаунта',
            'account_not_exists': 'Mi аккаунт -  Сбросить пароль ',
        },
    }

    def __init__(self, url):
        self.url = url

    def account_exists(self, phone_or_email):
        """
        Checks is there an account for given phone or email on site or not.

        Parameters
        ----------
        phone_or_email

        Returns
        -------
        bool
            True if exists, False otherwise

        Raises
        ------
        PageTitleError
            If processed title is unknown
        """
        with requests.session() as session:
            post_response = session.post(self.url, data={'id': phone_or_email, })
            soup = bs(post_response.text, 'lxml')
            title = soup.find_all('title')[0].string
            if title == self.XIAOMI_DATA.get('PAGE_TITLES').get('account_exists'):
                return True
            elif title == self.XIAOMI_DATA.get('PAGE_TITLES').get('account_not_exists'):
                return False
            else:
                raise PageTitleError('Page title at {url} is unknown: {title}.'.format(url=self.url, title=title))


@bp.route('/check_user/<phone_or_email>', methods=['POST'])
def check_user(phone_or_email):
    """
    Checks account existence and updates data in DB.

    Parameters
    ----------
    phone_or_email

    Returns
    -------
    json
    """
    xiaomi = SiteAnalyser('https://account.xiaomi.com/pass/forgetPassword')

    try:
        account_exists = xiaomi.account_exists(phone_or_email)
    except PageTitleError as e:
        return jsonify({'result': e.message})

    if account_exists:
        account_info = {'Account exists': True}
    else:
        account_info = {'Account exists': False}

    users_db = get_db().db.users
    users_db.update_one({'login': phone_or_email}, {"$set": account_info, }, upsert=True)

    return jsonify({'result': account_info})


@bp.route('/check_user/<phone_or_email>', methods=['GET'])
def check_user_from_db(phone_or_email):
    """
    Checks account existence only according to archived in DB data.

    Parameters
    ----------
    phone_or_email

    Returns
    -------
    json
    """
    users_db = get_db().db.users

    # Check if user info is already id DB
    user_entry = users_db.find_one({'login': phone_or_email})
    if user_entry:
        # Return result from DB
        account_info = {'Account exists': user_entry['Account exists']}
    else:
        account_info = 'No such user in the database. Use POST request instead.'

    return jsonify({'result': account_info})
