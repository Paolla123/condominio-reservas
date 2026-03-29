from django.db import models
from django.contrib.auth.models import AbstractUser

# A Classe Usuario agora herda do sistema de segurança nativo do Django
class Usuario(AbstractUser):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado'),
    ]
    
    # Vamos forçar o e-mail a ser o campo principal, em vez de um "username" qualquer
    email = models.EmailField(unique=True)
    
    statusConta = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pendente' # Todo mundo nasce pendente, até o admin aprovar!
    )

    # Dizemos ao Django que o login será feito pelo EMAIL e não pelo username padrão
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# O Morador continua herdando de Usuario, ganhando automaticamente login e senha
class Morador(Usuario):
    bloco = models.CharField(max_length=10)
    apartamento = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"

class Administrador(Usuario):
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

class Sindico(Administrador):
    class Meta:
        verbose_name = "Síndico"
        verbose_name_plural = "Síndicos"

class AreaComum(models.Model):
    STATUS_CHOICES = [
        ('Disponivel', 'Disponível'),
        ('EmManutencao', 'Em Manutenção'),
    ]
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    prazoCancelamentoDias = models.IntegerField()
    tempoDaReserva = models.IntegerField(help_text="Tempo em horas")
    statusLocal = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponivel')

class Reserva(models.Model):
    dataReserva = models.DateField()
    horarioInicio = models.TimeField()
    horarioFim = models.TimeField()
    status = models.CharField(max_length=50, default="Pendente")
    
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    areaComum = models.ForeignKey(AreaComum, on_delete=models.CASCADE)