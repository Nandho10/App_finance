from django.db import models

class Venda(models.Model):
    DATA_CHOICES = [
        ("dinheiro", "Dinheiro"),
        ("cartao_credito", "Cartão de Crédito"),
        ("cartao_debito", "Cartão de Débito"),
        ("pix", "Pix"),
        ("boleto", "Boleto"),
        ("outro", "Outro"),
    ]

    data = models.DateField()
    produto_servico = models.CharField(max_length=100)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    forma_recebimento = models.CharField(max_length=20, choices=DATA_CHOICES)
    observacoes = models.TextField(blank=True, null=True)

    @property
    def lucro_bruto(self):
        return self.valor_venda - self.custo

    def __str__(self):
        return f"{self.data} - {self.produto_servico} - R${self.valor_venda}" 