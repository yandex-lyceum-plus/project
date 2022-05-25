from django.forms import ValidationError


def validate_count_words(value: str):
    if len(value.split()) < 2:
        raise ValidationError('Необходимо минимум 2 слова. Убедитесь, что вы разделяете слова с помощью пробела " "')


def validate_rating(value):
    if value.isdigit():
        if 0 >= int(value) <= 10:
            pass
        else:
            raise ValidationError('Неверная оценка')
    else:
        raise ValidationError('Неверная оценка')
