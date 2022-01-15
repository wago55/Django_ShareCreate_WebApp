from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# ユーザーマネジャーの設定でUserからのデータを抜ける様にする
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        if not email:
            raise ValueError('Enter Email')

        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ユーザーモデル(AbstractBaseUserでカスタマイズ)
class User(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    profile_icon = models.ImageField(_('プロフィール画像'), upload_to='profile_icons/', null=True, blank=True)
    self_introduction = models.CharField(_('self introduction'), max_length=512, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    GENDER_CHOICES = (
        ('男性', '男性'),
        ('女性', '女性'),
        ('その他', 'その他'),
    )
    sex = models.CharField('性別', max_length=4, choices=GENDER_CHOICES, null=True)
    old = models.IntegerField('年齢', null=True)
    last_name = models.CharField('姓', max_length=30, null=True)
    first_name = models.CharField('名', max_length=30, null=True)
    date_of_birth = models.DateField('誕生日', blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


# お問い合わせ用のモデル
class Inquiry(models.Model):
    name = models.CharField('氏名', max_length=30)
    email = models.EmailField('お客様のメールアドレス')
    title = models.CharField('タイトル', max_length=30)
    message = models.TextField('お問い合わせ内容', max_length=100000)

    class Meta:
        db_table = 'inquiry'



