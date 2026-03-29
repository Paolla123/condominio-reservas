from django import forms
from .models import Morador

class CadastroMoradorForm(forms.ModelForm):
    # Avisamos que o campo de senha não é um texto comum, é uma senha secreta
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Morador
        # Quais campos o usuário vai preencher na tela de cadastro?
        fields = ['first_name', 'email', 'bloco', 'apartamento', 'senha']

    def save(self, commit=True):
        # Pegamos os dados antes de salvar no banco
        user = super().save(commit=False)
        
        # Criptografa a senha (SUPER IMPORTANTE!)
        user.set_password(self.cleaned_data['senha'])
        
        # O Django nativo pede um 'username', então copiamos o email pra lá
        user.username = self.cleaned_data['email'] 
        
        # Regra de negócio: Nasce sempre como Pendente
        user.statusConta = 'Pendente' 
        
        if commit:
            user.save()
        return user