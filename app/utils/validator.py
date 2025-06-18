from wtforms.validators import ValidationError
import re

def alphanumeric_only(form, field):
    if not re.match(r'^[a-zA-Z0-9]+$', field.data):
        raise ValidationError('用户名只能包含字母和数字')