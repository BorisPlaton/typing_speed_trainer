import random

import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture(autouse=True)
def user(credentials):
    return User.objects.create_user(**credentials)


@pytest.fixture
def user_statistics_dict():
    return {
        'invalidKeystrokes': random.randint(5, 55),
        'correctKeystrokes': random.randint(5, 55),
        'summaryKeystrokes': random.randint(5, 55),
        'invalidWordsAmount': random.randint(5, 55),
        'correctWordsAmount': random.randint(5, 55),
        'totalWordsAmount': random.randint(5, 55),
        'typingAccuracy': random.randint(5, 55) + 0.1,
        'wpm': random.randint(5, 55),
        'dateEnd': '2022-07-03T16:07:32.225Z',
        'language': 'Ukrainian',
    }
