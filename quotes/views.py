#Copyrights LuanIbraimi all rights reserved
from django.shortcuts import render, redirect
from .models import Stock, Stock_History2
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
			except:
				api2={}
				api2["shares"]=ticker_item.shares
				api2["companyName"]=ticker_item.ticker
				api2["symbol"]=ticker_item.ticker
				api2["id"]=ticker_item.id
				api2["latestPrice"]=0
				api2["previousClose"]=0
				api2["marketCap"]=0
				api2["ytdChange"]=0
				api2["week52High"]=0
				api2["week52Low"]=0
				output.append(api2)
		return render(request, 'add_stock.html', {'ticker':ticker, 'output':output})


def delete(request, stock_id):
	item=Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,"Stock has been deleted")
	return redirect(add_stock)


def stock_info(request, ticker):

	api=Stock_History2.objects.filter(Ticker=ticker).order_by('-Date')

	list_date=[]
	list_close=[]


	new_dictionary={'date':[],'close': []}

	for item in api:
	  list_date.append(item.Date)
	  list_close.append(item.Close)
	new_dictionary['date'].append(list_date)
	new_dictionary['close'].append(list_close)

	  
	return render(request, 'stock_info.html', {'api':api, 'ticker':ticker, 'new_dictionary':new_dictionary})


def delete_stock(request):
	return render(request, 'delete_stock.html', {})

def chart(request):
	return render(request, 'chart.html', {})
	


def stock_history(request):
		import yfinance as yf
		import pandas as pd
		import numpy as np
		from django.shortcuts import HttpResponse
		from django.conf import settings 
		from sqlalchemy import create_engine

		data = pd.read_csv('C:/Users/Luan Ibraimi/Desktop/Tickers.txt', sep='\t',error_bad_lines=False, encoding = "ISO-8859-1")
		
		stock_info=data['Symbol'].apply(yf.Ticker)

		df=pd.DataFrame([])
		counter=0
		for i,val in stock_info.items():
			counter=counter+1
			values=val.history(period='1y')
			values['Ticker']=val.ticker
			values['Counter']=counter  
			df=pd.concat([df, values], axis=0)
		
		#df['Date']=df.index
		
		df['id']=range(len(df))

		df=df[['id','Counter','Open','High','Low','Close','Volume','Ticker']]



		engine=create_engine('sqlite:///db.sqlite3')
		#ls=engine.table_names() , {'ls':ls}

		df.to_sql('quotes_stock_history2', con=engine, if_exists="replace")


		return render(request, 'stock_history.html')	
		#return render(request, 'chart.html', {'df':df })





