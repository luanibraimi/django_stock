from django.db import models

# Create your models here.


class Stock(models.Model):
	ticker=models.CharField(max_length=10)
	shares = models.PositiveIntegerField(default=0)


	def __str__(self):
		return self.ticker


class Stock_History2(models.Model):
	Date= models.DateField( db_index=True)
	Open=models.DecimalField(decimal_places=2, max_digits=10)
	High=models.DecimalField(decimal_places=2,max_digits=10)
	Low=models.DecimalField(decimal_places=2,max_digits=10)
	Close=models.DecimalField(decimal_places=2,max_digits=10)
	Volume=models.DecimalField(decimal_places=2,max_digits=10)
	Counter=models.DecimalField(decimal_places=2,max_digits=10)
	
	Ticker=models.CharField(max_length=10)

	def __str__(self):
		return self.Ticker