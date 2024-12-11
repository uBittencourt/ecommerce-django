from django import forms
from django.contrib.auth.models import User

from perfil import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.PerfilUsuario
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha' 
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmar Senha' 
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'confirm_password', 'email')

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        confirm_password_data = cleaned.get('confirm_password')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_short = 'Sua senha precisa ter pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório'

        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists
            
            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != confirm_password_data:
                    validation_error_msgs['password'] = error_msg_password_match 
                    validation_error_msgs['confirm_password'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short 
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists
            
            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field
            
            if not confirm_password_data:
                validation_error_msgs['confirm_password'] = error_msg_required_field
            
            if password_data != confirm_password_data:
                validation_error_msgs['password'] = error_msg_password_match 
                validation_error_msgs['confirm_password'] = error_msg_password_match

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short 

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))