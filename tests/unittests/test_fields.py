#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

import pytest

from app import api


class TestCharField:
    @pytest.mark.parametrize(
        "value",
        [
            "99",
            "just string",
        ],
    )
    def test_valid_CharField(self, value):
        f = api.CharField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize(
        "value, ex",
        [
            (None, ValueError),
            (1, ValueError),
            (("user",), ValueError),
            ({"user": 1}, ValueError),
        ],
    )
    def test__invalid_CharField(self, value, ex):
        f = api.CharField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestArgumentsField:
    @pytest.mark.parametrize(
        "value",
        [
            {"arg": "arg"},
            {"arg": 1},
        ],
    )
    def test_valid_ArgumentsField(self, value):
        f = api.ArgumentsField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize(
        "value, ex",
        [
            {1, ValueError},
            ("arg", ValueError),
            (("arg", 1), ValueError),
        ],
    )
    def test_invalid_ArgumentsField(self, value, ex):
        f = api.ArgumentsField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestEmailField:
    @pytest.mark.parametrize(
        "value",
        [
            "mail@mail.com",
            "a@b.c",
        ],
    )
    def test_valid_EmailField(self, value):
        f = api.EmailField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize(
        "value, ex",
        [
            (1, ValueError),
            ("1", ValueError),
            ("@", ValueError),
            ("1@1", ValueError),
        ],
    )
    def test_invalid_EmailField(self, value, ex):
        f = api.EmailField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestPhoneField:
    @pytest.mark.parametrize(
        "value",
        [
            "71112223344",
        ],
    )
    def test_valid_PhoneField(self, value):
        f = api.PhoneField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize(
        "value, ex",
        [
            ("81112223344", ValueError),
            ("+71112223344", ValueError),
            ("7333", ValueError),
        ],
    )
    def test_invalid_PhoneField(self, value, ex):
        f = api.PhoneField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestDateField:
    @pytest.mark.parametrize(
        "value",
        [
            "01.01.1970",
        ],
    )
    def test_valid_DateField(self, value):
        f = api.DateField(required=False, nullable=True)
        assert f.validate(value) == datetime.datetime.strptime(value, "%d.%m.%Y")

    @pytest.mark.parametrize(
        "value, ex",
        [
            ("1970.01.01", ValueError),
            ("20.20.20", ValueError),
            ("99.99.2000", ValueError),
            ("01.01.99", ValueError),
        ],
    )
    def test_invalid_DateField(self, value, ex):
        f = api.DateField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestBirthDayField:
    @pytest.mark.parametrize(
        "value",
        [
            "01.01.1970",
        ],
    )
    def test_valid_BirthDayField(self, value):
        f = api.BirthDayField(required=False, nullable=True)
        assert f.validate(value) == datetime.datetime.strptime(value, "%d.%m.%Y")

    @pytest.mark.parametrize(
        "value, ex",
        [
            ("01.01.1900", ValueError),
        ],
    )
    def test_invalid_BirthDayField(self, value, ex):
        f = api.BirthDayField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestGenderField:
    @pytest.mark.parametrize("value", [0, 1, 2])
    def test_valid_GenderField(self, value):
        f = api.GenderField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize(
        "value, ex",
        [
            (-1, ValueError),
            (3, ValueError),
            ("1", ValueError),
            ((1,), ValueError),
        ],
    )
    def test_invalid_GenderField(self, value, ex):
        f = api.GenderField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestClientIDsField:
    @pytest.mark.parametrize(
        "value",
        [
            [-3, 2],
        ],
    )
    def test_valid_ClientIDsField(self, value):
        f = api.ClientIDsField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize(
        "value, ex",
        [
            (["1", "2"], ValueError),
            (("1", "2"), ValueError),
        ],
    )
    def test_invalid_ClientIDsField(self, value, ex):
        f = api.ClientIDsField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)
