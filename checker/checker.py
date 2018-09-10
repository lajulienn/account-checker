import requests

from bs4 import BeautifulSoup as bs
from checker.db import get_db

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)


bp = Blueprint('checker', __name__)


class PageTitleError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
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
            'account_not_exists': 'Mi аккаунт - Сбросить пароль',
        },
    }

    def __init__(self, url):
        self.url = url

    def account_exists(self, phone_or_email):
        """
        Checks is there an account for given phone or email on site or not

        Parameters
        ----------
        phone_or_email

        Returns
        -------
        bool
            True if exists, False otherwise
        """
        with requests.session() as session:
            post_response = session.post(self.url, data={'id': phone_or_email, })
            soup = bs(post_response.text, 'lxml')
            title = soup.find_all('title')[0]
            if title == self.XIAOMI_DATA.get('PAGE_TITLES').get('account_exists'):
                return True
            elif title == self.XIAOMI_DATA.get('PAGE_TITLES').get('account_not_exists'):
                return False
            else:
                raise PageTitleError('Page title at {url} is unknown: {title}.'.format(url=self.url, title=title))

    # url = r'https://account.xiaomi.com/pass/forgetPassword'


@bp.route('/check_user/<phone_or_email>', methods=['POST'])
def check_user(phone_or_email):
    users_db = get_db().db.users

    # Check if user info is already id DB
    user_entry = users_db.find_one({'login': phone_or_email})
    if user_entry:
        # Return result from DB
        output = {'Account exist': user_entry['Account exist']}
    else:
        # Send request and write to DB
        output = {'Account exist': False}
        phone_id = users_db.insert({'login': phone_or_email, 'Account exist': True})

    return jsonify({'result': output})
