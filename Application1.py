
import pandas as pd
import numpy as np
from flask import Flask, request
from sklearn.linear_model import LogisticRegression
import joblib

app= Flask(__name__)
@app.route('/train')
def train_model():
    df= pd.read_excel('Historical Alarm Cases.xlsx')
    x = df.iloc[:, 1:7]
    y = df['Spuriosity Index(0/1)']
    logm = LogisticRegression()
    logm.fit(x, y)
    joblib.dump(logm, 'train.pkl')
    return 'model train successfully..'


@app.route('/test_model', methods=['POST'])
def test():
    pkl_file= joblib.load('train.pkl')
    test_data=request.get_json()
    f1= test_data['Ambient Temperature']
    f2 = test_data['Calibration']
    f3 = test_data['Unwanted substance deposition']
    f4 = test_data['Humidity']
    f5 = test_data['H2S Content']
    f6 = test_data['detected by']

    my_test_data = [f1, f2, f3, f4, f5, f6]
    my_data_array = np.array(my_test_data)
    test_array = my_data_array.reshape(1, 6)
    df_test = pd.DataFrame(test_array,
                           columns=['Ambient Temperature', 'Calibration', 'Unwanted substance deposition', 'Humidity',
                                    'H2S Content', 'detected by'])
    y_pred = pkl_file.predict(df_test)

    if y_pred == 1:
        return "False Alarm, No Danger"
    else:
        return "True Alarm, Danger "


app.run(port=5000)
