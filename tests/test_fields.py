#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from src.app import api


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
        f.value = value
        assert f.value == value


class TestEmailField:
    @pytest.mark.parametrize(
        "value",
        [
            "mail@mail.com",
            "@",
        ],
    )
    def test_valid_EmailField(self, value):
        f = api.EmailField(required=False, nullable=True)
        f.value = value
        assert f.value == value
