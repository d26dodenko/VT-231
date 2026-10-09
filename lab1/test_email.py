
import pytest
from email_validator import validate_email, EmailNotValidError


def check_email(email):
    return validate_email(email, check_deliverability=False)


# 1. Проверка обычного корректного email
def test_valid_email():
    result = check_email("user@example.com")
    assert result.normalized == "user@example.com"


# 2. Проверка email с цифрами
def test_email_with_numbers():
    result = check_email("user123@example.com")
    assert result.normalized == "user123@example.com"


# 3. Проверка email с точкой в имени
def test_email_with_dot():
    result = check_email("first.last@example.com")
    assert result.normalized == "first.last@example.com"


# 4. Проверка email со знаком плюс
def test_email_with_plus():
    result = check_email("user+test@example.com")
    assert result.normalized == "user+test@example.com"


# 5. Проверка домена в верхнем регистре
def test_uppercase_domain():
    result = check_email("user@EXAMPLE.COM")
    assert result.normalized == "user@example.com"


# 6. Отсутствует символ @
def test_missing_at_symbol():
    with pytest.raises(EmailNotValidError):
        check_email("userexample.com")


# 7. Отсутствует имя пользователя
def test_missing_username():
    with pytest.raises(EmailNotValidError):
        check_email("@example.com")


# 8. Отсутствует домен
def test_missing_domain():
    with pytest.raises(EmailNotValidError):
        check_email("user@")


# 9. Пустая строка
def test_empty_email():
    with pytest.raises(EmailNotValidError):
        check_email("")


# 10. Пробел в имени пользователя
def test_space_in_username():
    with pytest.raises(EmailNotValidError):
        check_email("user name@example.com")


# 11. Двойной символ @
def test_double_at_symbol():
    with pytest.raises(EmailNotValidError):
        check_email("user@@example.com")


# 12. Две точки подряд в имени
def test_double_dot():
    with pytest.raises(EmailNotValidError):
        check_email("user..name@example.com")


# 13. Домен начинается с дефиса
def test_domain_starts_with_hyphen():
    with pytest.raises(EmailNotValidError):
        check_email("user@-example.com")



# 14. Превышение длины имени пользователя
def test_username_too_long():
    username = "a" * 65
    with pytest.raises(EmailNotValidError):
        validate_email(
            f"{username}@example.com",
            check_deliverability=False,
            strict=True
        )


# 15. Граничное значение длины имени пользователя
def test_username_max_length():
    username = "a" * 64
    result = check_email(f"{username}@example.com")
    assert result.local_part == username
