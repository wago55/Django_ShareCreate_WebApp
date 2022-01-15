from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm
)


from .models import User, Inquiry
from django.forms import ModelForm
from django.core.mail import EmailMessage


# カスタムユーザーを使っているためUserCreationFormをBaseUserCreationForm継承で書き換え
class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User


# カスタムユーザーを使っているためUserChangeFormをBaseUserChangeForm継承で書き換え
class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User


# プロフィールform
class UpdateUserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'last_name', 'first_name', 'sex', 'date_of_birth', 'old', 'username', 'profile_icon'
        )


# お問い合わせform
class InquiryForm(ModelForm):
    class Meta:
        model = Inquiry
        fields = (
            'name', 'title', 'email', 'message',
        )

    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = f'お問い合わせ {title}'
        message = f'送信者名: {name}\nメールアドレス: {email}\nメッセージ: {message}'
        from_email = 'admin@gmail.com'
        to_list = [
            'test@gmail.com'
        ]
        cc_list = [
            'email'
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email,
                               to=to_list, cc=cc_list)

        message.send()