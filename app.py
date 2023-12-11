import os
import pandas as pd
from flask import Flask, render_template, request
from src.ZillowHouseData.utils.common import load_pickle_object
from src.ZillowHouseData.pipeline.stage_05_user_predict_pipeline import UserPredictPipeline

app = Flask(__name__)
predict_pipeline = UserPredictPipeline()

def parse_form_data(request_form):
    """
    Parse and validate form data. Convert to appropriate types.
    """
    user_input = {}
    for key in ['encoded_indicator_id', 'region_id', 'year', 'month']:
        value = request_form.get(key)
        user_input[key] = int(value) if value.isdigit() else None

    for key in ['CRAM', 'IRAM', 'LRAM', 'MRAM', 'NRAM', 'SRAM']:
        value = request_form.get(key)
        user_input[key] = float(value) if value.replace('.', '', 1).isdigit() else None

    return user_input


FORM_FIELD_MAPPING = {
    "encoded_indicator_id": "Indicator ID",
    "region_id": "Region ID",
    "year": "Year",
    "month": "Month",
    "CRAM": "CRAM",
    "IRAM": "IRAM",
    "LRAM": "LRAM",
    "MRAM": "MRAM",
    "NRAM": "NRAM",
    "SRAM": "SRAM"
}

@app.route('/', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        user_input = None
        display_input = {}
        price = None
        if request.method == 'POST':
            user_input = parse_form_data(request.form)
            price = predict_pipeline.user_predict(user_input=user_input)

            for key, value in user_input.items():
                display_name = FORM_FIELD_MAPPING.get(key, key) 
                display_input[display_name] = value

        mapping = load_pickle_object("models", 'label')
        region_mapping = load_pickle_object("models", 'region_label')
        return render_template('index.html', 
                               label_to_category_mapping=mapping, region_label_mapping = region_mapping,
                               result=price, 
                               user_input=display_input)

    except Exception as e:
        app.logger.error(f"Error in prediction: {str(e)}")
        return render_template('index.html', error=str(e))

@app.route("/train", methods=['GET','POST'])
def trainRoute():
    os.system("python main.py")
    # os.system("dvc repro")
    return "Training done successfully!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
