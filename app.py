from flask import Flask, request, render_template
import joblib
import numpy as np
import os

app = Flask(__name__)


model = joblib.load('model.joblib')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:

            tv = float(request.form['tv_budget'])
            radio = float(request.form['radio_budget'])
            newspaper = float(request.form['newspaper_budget'])
                        
            if tv < 0 or radio < 0 or newspaper < 0:
                raise ValueError("Ad budgets cannot be negative.")


            input_data = np.array([[tv, radio, newspaper]])


            prediction = model.predict(input_data)[0]
            prediction = round(prediction, 2)
            prediction = "$" + str(prediction)

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template('index.html', prediction=prediction)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 5000 is the fallback for local
    app.run(host='0.0.0.0', port=port, debug=True)
