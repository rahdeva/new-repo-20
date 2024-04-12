from app.model.forecast_detail import ForecastDetail
from app.model.sale_forecast import SaleForecast
from app.model.sale import FactSale
from app.model.time import DimTime

from app import response, app, db
from flask import request, jsonify,abort
from sqlalchemy import text

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import root_mean_squared_error

from sklearn.model_selection import train_test_split

import math
import numpy as np
import pandas as pd

def getData():
    # Define the SQL query
    sql_query = """
        SELECT 
            ROW_NUMBER() OVER (ORDER BY dt.year, WEEKOFYEAR(dt.date)) AS week_id,
            WEEKOFYEAR(dt.date) AS week,
            CONCAT(
                DATE_FORMAT(MIN(dt.date), '%e'), ' - ', 
                DATE_FORMAT(DATE_ADD(MIN(dt.date), INTERVAL 6 DAY), '%e %b %Y')
            ) AS week_date,
            DATE_FORMAT(MIN(dt.date), '%e %b %Y') AS week_start_date,
            DATE_FORMAT(DATE_ADD(MIN(dt.date), INTERVAL 6 DAY), '%e %b %Y') AS week_last_date,
            COALESCE(COUNT(fs.sale_id), 0) AS total_transactions
        FROM 
            dim_time dt
        LEFT JOIN 
            fact_sale fs ON fs.time_id = dt.time_id
        WHERE 
            dt.date <= NOW()
        GROUP BY 
            dt.year,
            WEEKOFYEAR(dt.date)
        HAVING
            total_transactions > 0
        ORDER BY 
            dt.year,
            WEEKOFYEAR(dt.date);
    """

    # Execute the SQL query
    query_result = db.session.execute(text(sql_query))

    # Fetch the result
    result = [
        {
            'week_id': row[0],
            'week': row[1],
            'week_date': row[2],
            'week_start_date': row[3],
            'week_last_date': row[4],
            'total_transactions': row[5]
        }
        for row in query_result
    ]

    return result

def test():
    try:
        # Panggil fungsi untuk mendapatkan data
        result = getData()

        # Buat DataFrame dari hasil query
        result_df = pd.DataFrame(result)

        # Ambil kolom yang diperlukan
        data_transaksi_penjualan = result_df[['week_id', 'total_transactions']]

        # # Interpolasi week_id jika diperlukan
        # data_transaksi_penjualan['week_id'] = data_transaksi_penjualan['week_id'].interpolate()

        # Ambil nilai X dan y
        X = data_transaksi_penjualan[['week_id']].values
        y = data_transaksi_penjualan['total_transactions'].values

        # Lakukan sesuatu dengan X dan y
        # Misalnya, cetak X dan y
        print("X:", X)
        print("y:", y)

        return response.success(result, "success")
    except Exception as e:
        print(e)
    

# def predictData():
#     predict(data_transaksi_penjualan,12)


def trainSVR():
    data_transaksi_penjualan = pd.read_csv('Data_TPT_Forecasting_Terbaru.csv')
    data_transaksi_penjualan = data_transaksi_penjualan[["week_id","total_transactions"]]

    data_transaksi_penjualan['week_id'] = data_transaksi_penjualan['week_id'].interpolate()

    X = data_transaksi_penjualan[['week_id']].values
    y = data_transaksi_penjualan['total_transactions'].values

    svr_regressor = SVR(kernel="rbf", C=1000, gamma=0.9, epsilon=0.9)
    svr_regressor.fit(X, y)


# def predict(maxData=12):
#     lendf = len(data_transaksi_penjualan)
#     xData = np.array([[x] for x in range(lendf,lendf+maxData)])
#     y_pred = svr_regressor.predict(xData)

#     return pd.DataFrame.from_dict({"week_id":list(xData.flatten()),"predict_transaction":list(y_pred.flatten())})
