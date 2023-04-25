from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-mail')

    # Metodo save para substituir o save do UserCreationForm
    def save(self, commit=True):
        #Passando commit False o save retorna o objeto user e não salva no banco
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe usuário com este e-mail')

        return email

class EditAccountForm(forms.ModelForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Já existe usuário com este e-mail')

        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
