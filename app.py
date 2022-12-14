from flask import Flask, request, render_template, jsonify
import pymongo
from bson import json_util
import pandas as pd
from import_data import import_data
from import_data import updated_data
import json
from datetime import date, timedelta
import requests

app=Flask(__name__)
app.register_blueprint(import_data, url_prefix="")

#updated_data()

#Import data from MongoDB
myclient = pymongo.MongoClient("mongodb+srv://Hoanglong_Pham:Long1989@cluster0.j3atpvd.mongodb.net/?retryWrites=true&w=majority")



@app.route('/')
def index():
	return render_template('index.html')


@app.route('/history')
def display_data():
  symbol = request.args.get('symbol', default="AMZN")
  period = request.args.get('period', default=360)
  mydb = myclient['StockMarket']
  mycol = mydb[symbol]
  mydoc = mycol.find_one({})
  data_display = mydoc['Time Series']
  df = pd.DataFrame(data_display).T.iloc[:, ::-1]
  data = df.iloc[0:4,0:period].iloc[:, ::-1].T.to_json(date_format ='iso')
  return data

@app.route("/quote")
def display_info():
  symbol = request.args.get('symbol', default="AMZN")
  mydb = myclient['StockMarket']
  mycol = mydb[symbol]
  mydoc = mycol.find_one({})
  quote = mydoc['Meta data']
  return jsonify(quote)

@app.route("/chart")
def chart():
    return render_template("chart.html")

@app.route('/team')
def OurTeam():
	return render_template('OurTeam.html')

if __name__ == "__main__":
  app.run()