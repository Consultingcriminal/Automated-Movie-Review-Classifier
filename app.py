from flask import Flask,request, url_for, redirect, render_template, jsonify
from ensemble_deployment import hard_voting,soft_voting 
import config
from text_cleaning import text_cleaner
import joblib
import numpy as np


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict',methods=['POST'])
def soft_voting_predict():
    text = request.form['Enter your review']
    text = text_cleaner(text)

    predictions = soft_voting([text])
    
    if predictions == 1:
        return render_template('home.html',pred='The sentiment of the review is POSITIVE.')

    else:
        return render_template('home.html',pred='The sentiment of the review is NEGATIVE.')
    
@app.route('/predict1',methods=['POST'])
def hard_voting_predict():
    text = request.form['Enter your review']
    text = text_cleaner(text)

    predictions = hard_voting([text])
    
    if predictions == 1:
        return render_template('home.html',pred='The sentiment of the review is POSITIVE.')

    else:
        return render_template('home.html',pred='The sentiment of the review is NEGATIVE.')    


@app.route('/predict_api',methods=['POST','GET'])
def predict_api():
    text = request.args.get('text')
    text = text_cleaner(str(text))
    predictions = soft_voting([text])
    #return '''<h1>The sentiment value is: {}</h1>'''.format(output)
    if predictions==1:
        return "POSITIVE"
    else:
        return "NEGATIVE"    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)    