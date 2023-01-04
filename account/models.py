from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin, UserManager
from django_boost.models.mixins import LogicalDeletionMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from stdimage.models import StdImageField
from django.conf import settings

from utilities.validators import ZIPCODE_VALIDATOR
from utilities.validators import TELEPHONE_VALIDATOR
from django.core.validators import MinLengthValidator

#
# ユーザータイプ定義
#
USER_TYPES = (
    (1, _("user_type_owner")),
    (2,_("user_type_administrator")),
    (3,_("user_type_user")),
    (10,_("user_type_guest")),
)

#
# 本アプリケーションのベースモデル
#
class BaseModel(LogicalDeletionMixin):
    """ accountアプリケーションのベースデータモデル

    Args:
        LogicalDeletionMixin (_type_): 論理削除のミックスインが入ってますよ
    """
    created_at = models.DateTimeField(verbose_name=_("created_at"),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"),auto_now=True)
    class Meta:
        abstract = True

#
# カスタムユーザーモデルクラス
#
class User(AbstractBaseUser, PermissionsMixin, LogicalDeletionMixin):
    """カスタムユーザーモデルクラス

    Args:
        AbstractBaseUser (_type_): 抽象ベースユーザクラスを拡張してますよ
        PermissionsMixin (_type_): 権限ミックスインが入ってますよ
        LogicalDeletionMixin (_type_): 論理削除のミックスインが入ってますよ
    """
    def get_profile_image_path(instance,filename):
        return 'profile/{}/main.{}'.format(str(instance.id).zfill(8),str(instance.user.id).zfill(8),filename.split('.')[-1])

    # ユーザー名バリデータ
    username_validator = UnicodeUsernameValidator()
    # ユーザー名（ログインID）
    username = models.CharField(verbose_name=_("username"),max_length=64,unique=True,validators=[username_validator])
    # 表示名
    viewname = models.CharField(_("viewname"), max_length=50, blank=True)
    # 名
    first_name = models.CharField(_("first_name"), max_length=50, blank=True)
    # 姓
    last_name = models.CharField(_("last_name"), max_length=50, blank=True)
    # メールアドレス
    email = models.EmailField(_("email"), blank=True)
    # プロフィール画像
    profile_image = StdImageField(verbose_name=_("profile_image"),null=True,blank=True,upload_to=get_profile_image_path,variations={
        "large":(600,600),
        "thumbnail":(100,100,True),
        'midium':(300,300),
    })
    # 参加日時
    date_joined = models.DateTimeField(_("date_joined"), default=timezone.now)
    # Django管理画面スタッフフラグ（デフォルトFalse）
    is_staff = models.BooleanField(
        _("staff_status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    # 有効無効フラグ（デフォルト有効）
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    # ログインに使うユーザー名フィールド名
    USERNAME_FIELD = "username"
    # メールアドレスフィールド
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")        
            
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_dict(self):
        data = {}
        data["id"] = self.id
        data['username'] = self.username
        data['viewname'] = self.viewname
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['profile_image'] = None
        if self.profile_image:
            data['profile_image'] = self.profile_image.thumbnail.url
        return data

#
# 組織データモデル
#
class Organization(BaseModel):
    """
    組織・会社を登録するデータモデル
    """
    code = models.CharField(max_length=255,validators=[MinLengthValidator(8),],verbose_name=_("organization_code"))
    # 組織名
    name = models.CharField(max_length=255,validators=[MinLengthValidator(6),],verbose_name=_("account_organization_name"))
    # 保有者
    owner  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,verbose_name=_("account_organization_owner"))
    # 郵便番号
    zipcode = models.CharField(max_length=8,null=True,blank=True,validators=[ZIPCODE_VALIDATOR],verbose_name=_("zipcode"))
    # 都道府県・州
    state = models.CharField(max_length=64,null=True,blank=True,verbose_name=_("state"))
    # 市区町村・町
    city = models.CharField(max_length=64,null=True,blank=True,verbose_name=_("city"))
    # 住所・番地
    street = models.CharField(max_length=255,null=True,blank=True,verbose_name=_("street"))
    # 建物・部屋番号
    address = models.CharField(max_length=255,null=True,blank=True,verbose_name=_("address"))
    # 代表メールアドレス
    email = models.CharField(max_length=255,null=True,blank=True,verbose_name=_("email"))
    # 電話番号
    telephone = models.CharField(max_length=16,null=True,blank=True,validators=[TELEPHONE_VALIDATOR],verbose_name=_("telephone"))
    # 概要
    description = models.TextField(null=True,blank=True,verbose_name=_("description"))
    # 業界
    industory = models.PositiveSmallIntegerField(verbose_name=_("industory"),choices=settings.INDUSTORIES,null=True,blank=True)
    # 文字列化
    def __str__(self):
        return self.name

#
# 組織ユーザー
#
class OrganizationUser(BaseModel):
    """組織ユーザー関連テーブルモデルクラス

    Args:
        BaseModel (_type_): _description_
    """
    # 組織
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT,verbose_name=_("organization"),related_name="users")
    # ユーザー
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,verbose_name=_("user"),related_name="organizations")
    # ユーザー種別
    user_type = models.PositiveSmallIntegerField(verbose_name=_("user_type"),choices=USER_TYPES,null=False,blank=False,default=3)
    # 部署
    department = models.CharField(verbose_name=_("department_name"),null=True,blank=True,max_length=255)
    # 役職
    position = models.CharField(verbose_name=_("position"),null=True,blank=True,max_length=255)
    # 役割
    role = models.CharField(verbose_name=_("role"),null=True,blank=True,max_length=255)
    # 有効フラグ
    is_active = models.BooleanField(_("active"), default=True)
    # 備考欄
    notes = models.TextField(verbose_name=_("notes"), null=True, blank=True, max_length=1000)
