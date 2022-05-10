from django.forms import ValidationError


def validate_count_words(value: str):
    if len(value.split()) < 2:
        raise ValidationError('Необходимо минимум 2 слова. Убедитесь, что вы разделяете слова с помощью пробела " "')