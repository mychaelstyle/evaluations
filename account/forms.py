from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
  """ログイン用フォームクラス
  """
  organiztion_code = forms.CharField(max_length=128,required=False)
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for key in self.fields:
      self.fields[key].widget.attrs['class'] = 'form-control'

  def is_valid(self):
    return super().is_valid()

  def clean_username(self):
    organiztion_code = self.data.get('organiztion_code',None)
    username = self.data.get('username',None)
    if organiztion_code is not None and len(organiztion_code) > 0:
      return organiztion_code + "-" + username
    else:
      return username
