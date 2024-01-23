# app/views.py
from flask import Blueprint, render_template, request
from .model import probe_model_5l_profit
import json

page1_blueprint = Blueprint('page1', __name__)

@page1_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                content = file.read()
                print("JSON Data:", content)  # Print the JSON data for inspection
                data = json.loads(content)

                # Check if 'lineItems' key is present and is a list
                line_items = data.get('lineItems', [])
                if not isinstance(line_items, list):
                    raise ValueError("'lineItems' is not a list.")

                result = probe_model_5l_profit(data)
                return render_template('page1.html', result=result)
            except json.JSONDecodeError as json_error:
                error_message = f"Error decoding JSON data: {str(json_error)}"
                return render_template('page1.html', error_message=error_message)
            except ValueError as value_error:
                error_message = f"Error processing JSON data: {str(value_error)}"
                return render_template('page1.html', error_message=error_message)

    return render_template('page1.html')





