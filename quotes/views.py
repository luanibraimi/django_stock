#Copyrights LuanIbraimi all rights reserved
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
# Create your views here.

def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker=request.POST['ticker']

		api_request=requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_fc2a82506a304894aa291aa4772106a8")

		try:
			api=json.loads(api_request.content)
		except Exception as e:
			api="Error..."
		return render(request, 'home.html', {'api':api})

	else:
		return render(request, 'home.html', {'ticker':"Enter a ticker symbol above"})
	# pk_fc2a82506a304894aa291aa4772106a8
	

def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests
	import json
	if request.method == 'POST':
		form=StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, "Stock has been added to the database")
			return redirect ('add_stock')

	else:
		ticker=Stock.objects.order_by('ticker')
		output=[]
		
		for ticker_item in ticker:
			api_request=requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_fc2a82506a304894aa291aa4772106a8")

			try:
				api=json.loads(api_request.content)

				api["id"]=ticker_item.id
				api["shares"]=ticker_item.shares
				api["value"]=api["shares"]*api["latestPrice"]
				output.append(api)
			except Exception as e:
				api="Error..."
		return render(request, 'add_stock.html', {'ticker':ticker, 'output':output})


def delete(request, stock_id):
	item=Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,"Stock has been deleted")
	return redirect(add_stock)


def stock_info(request, ticker):
	import requests
	import json


	api_request=requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_fc2a82506a304894aa291aa4772106a8")

	api=json.loads(api_request.content)
	history=json.loads(history_request.content)

	history_request=requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/chart/max?token=pk_fc2a82506a304894aa291aa4772106a8")

	list_date=[]
	list_close=[]


	stock_history={'date':[],'close': []}

	for item in history:
	  list_date.append(item['date'])
	  list_close.append(item['close'])
	  stock_history['date'].append(list_date)
	  stock_history['close'].append(list_close)


	return render(request, 'stock_info.html', {'api':api, 'history':stock_history})


def delete_stock(request):
	return render(request, 'delete_stock.html', {})

def chart(request):
	return render(request, 'chart.html', {})
