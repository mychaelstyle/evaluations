from django.core.validators import RegexValidator
from string import ascii_uppercase, ascii_lowercase, digits
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# 郵便番号妥当性検査
ZIPCODE_VALIDATOR = RegexValidator(regex=r'^\d{3}-\d{4}$')
# 電話番号妥当性検査
TELEPHONE_VALIDATOR = RegexValidator(regex=r'^0\d{1,4}-\d{1,4}-\d{3,4}$')
# パスワードカスタム妥当性検査
def contain_any(target, condition_list):
    return any([i in target for i in condition_list])

class PasswordCustomValidator:
    message = _("password_must_include_upper_lower_symbol")
    
    symbols = ("@","-","_","#","=","(",")","$","%","!","[","]")

    def __init__(self,symbols=None):
        """init
        """
        if symbols is not None:
            self.symbols = symbols

    def validate(self, password, user=None):
        if not all([contain_any(password, ascii_lowercase),
                    contain_any(password, ascii_uppercase),
                    contain_any(password, digits),
                    contain_any(password, self.symbols)]):
            raise ValidationError(self.message)
        if len(password) < 8:
            raise ValidationError(_("password_must_be_more_than_8chars"))
        if len(password) > 36:
            raise ValidationError(_("password_must_be_less_than_36chars"))
        
    def get_help_text(self):
        return self.message