from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError('le de passe doit con tenir une lette', code='passeword_no_letters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'