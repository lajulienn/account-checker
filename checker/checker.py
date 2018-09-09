"""
    _header_for_request = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0)'
                      ' Gecko/20100101 Firefox/61.0'
    }

"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from checker.db import get_db

bp = Blueprint('checker', __name__)


def has_account(phone_or_email):
    pass


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
