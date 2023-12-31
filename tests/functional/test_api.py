# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import datetime
import hashlib
import json
import random

import pytest

from app import api
from app.db import Store

pytest.context = {}
pytest.headers = {}
pytest.settings = Store("store")


def get_response(request):
    return api.method_handler({"body": request, "headers": pytest.headers}, pytest.context, pytest.settings)


def set_valid_auth(request):
    if request.get("login") == api.ADMIN_LOGIN:
        msg = datetime.datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT
    else:
        msg = request.get("account", "") + request.get("login", "") + api.SALT
    request["token"] = hashlib.sha512(msg.encode("utf-8")).hexdigest()


def test_empty_request():
    _, code = get_response({})
    assert api.INVALID_REQUEST == code


@pytest.mark.parametrize(
    "r",
    [
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "sdd", "arguments": {}},
        {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": "", "arguments": {}},
    ],
)
def test_bad_auth(r):
    _, code = get_response(r)
    assert api.FORBIDDEN == code


@pytest.mark.parametrize(
    "r",
    [
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score"},
        {"account": "horns&hoofs", "login": "h&f", "arguments": {}},
        {"account": "horns&hoofs", "method": "online_score", "arguments": {}},
    ],
)
def test_invalid_method_request(r):
    set_valid_auth(r)
    response, code = get_response(r)
    assert api.INVALID_REQUEST == code
    assert len(response)


class TestScoreRequest:
    @pytest.mark.parametrize(
        "arguments",
        [
            {},
            {"phone": "79175002040"},
            {"phone": "89175002040", "email": "stupnikov@otus.ru"},
            {"phone": "79175002040", "email": "stupnikovotus.ru"},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": -1},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": "1"},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.1890"},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "XXX"},
            {
                "phone": "79175002040",
                "email": "stupnikov@otus.ru",
                "gender": 1,
                "birthday": "01.01.2000",
                "first_name": 1,
            },
            {
                "phone": "79175002040",
                "email": "stupnikov@otus.ru",
                "gender": 1,
                "birthday": "01.01.2000",
                "first_name": "s",
                "last_name": 2,
            },
            {"phone": "79175002040", "birthday": "01.01.2000", "first_name": "s"},
            {"email": "stupnikov@otus.ru", "gender": 1, "last_name": 2},
        ],
    )
    def test_invalid_score_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        set_valid_auth(request)
        response, code = get_response(request)
        assert api.INVALID_REQUEST == code
        assert len(response)

    @pytest.mark.parametrize(
        "arguments",
        [
            {"phone": "79175002040", "email": "stupnikov@otus.ru"},
            {"phone": 79175002040, "email": "stupnikov@otus.ru"},
            {"gender": 1, "birthday": "01.01.2000", "first_name": "a", "last_name": "b"},
            {"gender": 0, "birthday": "01.01.2000"},
            {"gender": 2, "birthday": "01.01.2000"},
            {"first_name": "a", "last_name": "b"},
            {
                "phone": "79175002040",
                "email": "stupnikov@otus.ru",
                "gender": 1,
                "birthday": "01.01.2000",
                "first_name": "a",
                "last_name": "b",
            },
        ],
    )
    def test_ok_score_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        set_valid_auth(request)
        response, code = get_response(request)
        assert api.OK == code
        score = response.get("score")
        assert isinstance(score, (int, float))
        assert score >= 0
        assert arguments
        assert sorted(pytest.context["has"]) == sorted(arguments.keys())

    def test_ok_score_admin_request(self):
        arguments = {"phone": "79175002040", "email": "stupnikov@otus.ru"}
        request = {"account": "horns&hoofs", "login": "admin", "method": "online_score", "arguments": arguments}
        set_valid_auth(request)
        response, code = get_response(request)
        assert api.OK == code
        score = response.get("score")
        assert score == 42


class MockStore:
    def get(self, key):
        interests = ["cars", "pets", "travel", "hi-tech", "sport", "music", "books", "tv", "cinema", "geek", "otus"]
        return json.dumps(random.sample(interests, 2))


@pytest.fixture
def mock_store():
    pytest.settings = MockStore()


class TestInterestsRequest:
    @pytest.mark.parametrize(
        "arguments",
        [
            {},
            {"date": "20.07.2017"},
            {"client_ids": [], "date": "20.07.2017"},
            {"client_ids": {1: 2}, "date": "20.07.2017"},
            {"client_ids": ["1", "2"], "date": "20.07.2017"},
            {"client_ids": [1, 2], "date": "XXX"},
        ],
    )
    def test_invalid_interests_request(self, arguments, mock_store):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        set_valid_auth(request)
        response, code = get_response(request)
        assert api.INVALID_REQUEST == code
        assert len(response)

    @pytest.mark.parametrize(
        "arguments",
        [
            {"client_ids": [1, 2, 3], "date": datetime.datetime.today().strftime("%d.%m.%Y")},
            {"client_ids": [1, 2], "date": "19.07.2017"},
            {"client_ids": [0]},
        ],
    )
    def test_ok_interests_request(self, arguments, mock_store):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        set_valid_auth(request)
        response, code = get_response(request)
        assert api.OK == code
        assert len(arguments["client_ids"]) == len(response)
        assert all(v and isinstance(v, list) and all(isinstance(i, (bytes, str)) for i in v) for v in response.values())
        assert pytest.context.get("nclients") == len(arguments["client_ids"])
