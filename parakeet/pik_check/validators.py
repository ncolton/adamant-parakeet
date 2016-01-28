from django.core.exceptions import ValidationError
import string


def validate_uppercase(value):
    for character in value:
        if character in string.letters:
            if character not in string.uppercase:
                raise ValidationError('Not all letters are uppercase')
