from dbadmin.domain.validators import is_valid_ident, quote_ident, quote_string, is_valid_host


def test_is_valid_ident_ok():
    assert is_valid_ident('abc_123')


def test_is_valid_ident_fail():
    assert not is_valid_ident('abc-123')


def test_quote_ident():
    assert quote_ident('users') == '`users`'


def test_quote_string_escapes():
    assert quote_string("a'b") == "'a\\'b'"


def test_valid_host():
    assert is_valid_host('%')
