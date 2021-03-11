import codecs
import json

from flask import Blueprint, request, jsonify
import requests

from app.lib.parser import parse
import app.models.models as models

api = Blueprint('api', __name__)

@api.route('/', methods = ['GET', 'POST'])
def index():
    return jsonify({'status': 'ok', 'response' : {'message':'TODO document API calls available'},})


@api.route('/store-form', methods = ['GET'])
def store_form():
    form_id = request.args.get('form_id')
    url = f'http://s3.amazonaws.com/irs-form-990/{form_id}_public.xml'
    response = requests.get(url)

    # Remove the byte-order marker: AWS returns the XML with a BOM that confuses the XML parser (since it's not XML :) 
    data = response.content.decode("utf-8-sig").encode("utf-8")
        
    parsed_data = parse( data )
    parsed_data['form_id'] = form_id
    models.write_to_db( parsed_data )
    return jsonify({'status': 'ok', 'response': {'message': 'Stored form data.'},})


@api.route('/get-filings', methods = ['GET'])
def get_forms():
    args = request.args
    currency = args.get('currency')
    results = models.read_filings()
    if currency:
        currency_results = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
        currency_json = currency_results.json()
        rate = currency_json['rates'].get(currency)
        if rate:
            for result in results:
                for award in result['awards']:
                    amt = award['amount']
                    converted_amt = amt*rate
                    award['amount_converted'] = converted_amt
    return jsonify({'status': 'ok', 'response': {'filings': results},},)


@api.route('/get-receivers', methods = ['GET'])
def get_receivers():
    state = request.args.get('state')
    receivers = models.read_receivers( state )
    return jsonify({'status': 'ok', 'response': {'receivers': receivers,},},)
