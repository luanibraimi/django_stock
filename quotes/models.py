from django.db import models

# Create your models here.


class Stock(models.Model):
	ticker=models.CharField(max_length=10)
	shares = models.PositiveIntegerField(default=0)


	def __str__(self):
		return self.ticker