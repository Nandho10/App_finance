from django.db import models

class Sale(models.Model):
    paid_at = models.DateField("Data de Pagamento")
    product = models.CharField("Produto/Serviço", max_length=100)
    amount = models.DecimalField("Valor da Venda", max_digits=12, decimal_places=2)
    custo = models.DecimalField("Custo", max_digits=12, decimal_places=2)
    payment_method = models.CharField("Forma de Recebimento", max_length=50)
    observacoes = models.TextField("Observações", blank=True, null=True)
    delivery_date = models.DateField("Data de Entrega", blank=True, null=True)
    client = models.CharField("Cliente", max_length=100, blank=True, null=True)

    def lucro_bruto(self):
        return self.amount - self.custo

    def __str__(self):
        return f"{self.product} - {self.paid_at} - R$ {self.amount}" 