#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import pytest
from tests.log import get_logger
from src.app import api

logger = get_logger(__name__, 'logs', 'log_tests')
logger.info("\nProgram started")


class TestCharField:
    @pytest.mark.parametrize("value", [
        "99",
        "just string",
    ])
    def test_valid_CharField(self, value):
        logger.debug(f'1. {type(value)=}, {value=}')
        f = api.CharField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize('value, ex', [
        (None, ValueError),
        (1, ValueError),
        (('user',), ValueError),
        ({'user': 1}, ValueError),
    ])
    def test__invalid_CharField(self, value, ex):
        logger.debug(f'2. {type(value)=}, {value=}')
        f = api.CharField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)
            

class TestArgumentsField:
    @pytest.mark.parametrize("value", [
        {"arg": "arg"},
        {"arg": 1},
    ])
    def test_valid_ArgumentsField(self, value):
        logger.debug(f'3. {type(value)=}, {value=}')
        f = api.ArgumentsField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize("value, ex", [
        {1, ValueError},
        ("arg", ValueError),
        (("arg", 1), ValueError),
    ])
    def test_invalid_ArgumentsField(self, value, ex):
        logger.debug(f'4. {type(value)=}, {value=}')
        f = api.ArgumentsField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)

class TestEmailField:
    @pytest.mark.parametrize("value", [
        "mail@mail.com",
        "a@b.c",
    ])
    def test_valid_EmailField(self, value):
        logger.debug(f'5. {type(value)=}, {value=}')
        f = api.EmailField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize("value, ex", [
        (1, ValueError),
        ("1", ValueError),
        ("@", ValueError),
        ("1@1", ValueError),
    ])
    def test_invalid_EmailField(self, value, ex):
        logger.debug(f'6. {type(value)=}, {value=}')
        f = api.EmailField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)

class TestPhoneField:
    @pytest.mark.parametrize("value", [
        "71112223344",
    ])
    def test_valid_PhoneField(self, value):
        logger.debug(f'7. {type(value)=}, {value=}')
        f = api.PhoneField(required=False, nullable=True)
        assert f.validate(value) == value

    @pytest.mark.parametrize("value, ex", [
        ("81112223344", ValueError),
        ("+71112223344", ValueError),
        ("7333", ValueError),
    ])
    def test_invalid_PhoneField(self, value, ex):
        logger.debug(f'8. {type(value)=}, {value=}')
        f = api.PhoneField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)


class TestDateField:
    @pytest.mark.parametrize("value", [
        "01.01.1970",
    ])
    def test_valid_DateField(self, value):
        logger.debug(f'9. {type(value)=}, {value=}')
        f = api.DateField(required=False, nullable=True)
        assert f.validate(value) == datetime.datetime.strptime(value, "%d.%m.%Y")

    @pytest.mark.parametrize("value, ex", [
        ("1970.01.01", ValueError),
        ("20.20.20", ValueError),
        ("99.99.2000", ValueError),
        ("01.01.99", ValueError),
    ])
    def test_invalid_DateField(self, value, ex):
        logger.debug(f'10. {type(value)=}, {value=}')
        f = api.DateField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)

class TestBirthDayField:
    @pytest.mark.parametrize("value", [
        "01.01.1970",
    ])
    def test_valid_BirthDayField(self, value):
        logger.debug(f'11. {type(value)=}, {value=}')
        f = api.BirthDayField(required=False, nullable=True)
        assert f.validate(value) == datetime.datetime.strptime(value, "%d.%m.%Y")

    @pytest.mark.parametrize("value, ex", [
        ("01.01.1900", ValueError),
    ])
    def test_invalid_BirthDayField(self, value, ex):
        logger.debug(f'12. {type(value)=}, {value=}')
        f = api.BirthDayField(required=False, nullable=True)
        with pytest.raises(ex):
            f.validate(value)

# class Test:
#     @pytest.mark.parametrize("value", [
#         "01.01.1970",
#     ])
#     def test_valid_(self, value):
#         logger.debug(f'7. {type(value)=}, {value=}')
#         f = api.DateField(required=False, nullable=True)
#         assert f.validate(value) == value

#     @pytest.mark.parametrize("value, ex", [
#         ("1970.01.01", ValueError),
#     ])
#     def test_invalid_(self, value, ex):
#         logger.debug(f'8. {type(value)=}, {value=}')
#         f = api.DateField(required=False, nullable=True)
#         with pytest.raises(ex):
#             f.validate(value)
