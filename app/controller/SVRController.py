from app.model.forecast_detail import ForecastDetail
from app.model.sale_forecast import SaleForecast
from app.model.sale import FactSale
from app.model.time import DimTime

from app import response, app, db
from flask import request, jsonify,abort
from sqlalchemy import text
from datetime import datetime, timedelta

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import root_mean_squared_error

from sklearn.model_selection import train_test_split

import math
import numpy as np
import pandas as pd

def predict():
    try:
        # Panggil fungsi untuk mendapatkan data
        result = getData()

        # Buat DataFrame dari hasil query
        result_df = pd.DataFrame(result)

        # Ambil kolom yang diperlukan
        data_transaksi_penjualan = result_df[['week_id', 'total_transactions']]
        bottom_20_percent_length = int(len(result_df) * 0.2)
        weeks = result_df['week'].values[-bottom_20_percent_length - 1:]
        week_dates = result_df['week_date'].values[-bottom_20_percent_length - 1:]
        week_last_dates = result_df['week_last_date'].values[-bottom_20_percent_length - 1:]

        # # Interpolasi week_id jika diperlukan
        data_transaksi_penjualan['week_id'] = data_transaksi_penjualan['week_id'].interpolate()

        # Ambil nilai X dan y
        X = data_transaksi_penjualan[['week_id']].values
        y = data_transaksi_penjualan['total_transactions'].values

        # Cetak X dan y
        print("X:", X)
        print("y:", y)

        # Split Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

        print("X_test:", X_test)
        print("y_test:", y_test)

        # Setting SVR dengan hasil tuning terbaik
        svr_regressor = SVR(kernel="rbf", C=1000, gamma=0.9, epsilon=0.9)
        svr_regressor.fit(X_train, y_train)

        y_pred = svr_regressor.predict(X_test)
        print("y_pred:", y_pred)

        mae = mean_absolute_error(list(y_test), list(y_pred.flatten())),
        mse = mean_squared_error(list(y_test), list(y_pred.flatten())),
        rmse = root_mean_squared_error(list(y_test), list(y_pred.flatten()))

        print("mae:", mae)
        print("mse:", mse)
        print("rmse:", rmse)

        # Predict Data Testing dan Data Validasi
        maxData = 12 
        predictedData = predictData(X_train, len(y_test)+maxData, svr_regressor)
        print("predictedData:", predictedData)
        
        # Insert data forecast detail
        insertDataForecastDetail(
            method='Support Vector Regression (SVR)',
            last_week_date=week_dates[-1],
            last_week_transaction=y_test[-1],
            mae=mae,
            mse=mse,
            rsme=rmse
        )

        # Ambil ID forecast_detail yang baru saja dimasukkan
        forecast_detail_id = ForecastDetail.query.order_by(ForecastDetail.forecast_detail_id.desc()).first().forecast_detail_id

        actual_total_transaction = list(y_test)
        for _ in range(maxData):
            actual_total_transaction.append(0)

        print("actual_total_transaction:", actual_total_transaction)

        weeks_data = list(weeks)
        last_week = weeks_data[-1]
        for _ in range(maxData):
            last_week += 1
            weeks_data.append(last_week)

        print("weeks_data:", weeks_data)

        week_dates_data = list(week_dates)
        last_week_date = list(week_last_dates)[-1]
        new_week_date_data = generateWeekDates(last_week_date, maxData)
        week_dates_data.extend(new_week_date_data)
        print("week_dates_data:", week_dates_data)

        # Loop untuk memasukkan data sale forecast
        for i, row in predictedData.iterrows():
            insertDataSaleForecast(
                forecast_detail_id=forecast_detail_id,
                time_id=generate_time_id(),
                week=weeks_data[i], 
                week_date=week_dates_data[i],
                actual_total_transaction=actual_total_transaction[i],
                predict_total_transaction=row['predict_transaction']
            )
        
        return response.successMessage("success")
    except Exception as e:
        print(e)


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


def predictData(df, maxData, svr_regressor):
    lendf = len(df)
    xData = np.array([[x] for x in range(lendf,lendf+maxData)])
    y_pred = svr_regressor.predict(xData)

    return pd.DataFrame.from_dict({"week_id":list(xData.flatten()),"predict_transaction":list(y_pred.flatten())})


def insertDataForecastDetail(method, last_week_date, last_week_transaction, mae, mse, rsme):
    print("method:", method)
    print("last_week_date:", last_week_date)
    print("last_week_transaction:", last_week_transaction)
    print("mae:", mae)
    print("mse:", mse)
    print("rsme:", rsme)
    try:
        forecast_detail = ForecastDetail(
            method=method,
            last_week_date=last_week_date,
            last_week_transaction=last_week_transaction,
            mae=mae,
            mse=mse,
            rsme=rsme
        )
        
        # Tambahkan objek ke session
        db.session.add(forecast_detail)
        
        # Commit perubahan
        db.session.commit()
        
        return "Data dim_forecast_detail berhasil ditambahkan."
    except Exception as e:
        return "Gagal menambahkan data dim_forecast_detail:" + str(e)


def insertDataSaleForecast(forecast_detail_id, time_id, week, week_date, actual_total_transaction, predict_total_transaction):
    print("forecast_detail_id:", forecast_detail_id)
    print("time_id:", time_id)
    print("week:", week)
    print("week_date:", week_date)
    print("actual_total_transaction:", actual_total_transaction)
    print("predict_total_transaction:", predict_total_transaction)
    try:
        # Buat objek SaleForecast
        sale_forecast = SaleForecast(
            forecast_detail_id=forecast_detail_id,
            time_id=time_id,
            week=week,
            week_date=week_date,
            actual_total_transaction=actual_total_transaction,
            predict_total_transaction=predict_total_transaction
        )
        
        # Tambahkan objek ke session
        db.session.add(sale_forecast)
        
        # Commit perubahan
        db.session.commit()
        
        return "Data fact_sale_forecast berhasil ditambahkan."
    except Exception as e:
        return "Gagal menambahkan data fact_sale_forecast:" + str(e)

def generate_time_id():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    year_str = str(year)
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    time_id = int(year_str + month_str + day_str)
    return time_id

def generateWeekDates(last_week_date, maxData):
    # Parsing the last available week's end date
    end_date_last_week = datetime.strptime(last_week_date, "%d %b %Y")

    # Initialize lists to store next week numbers and dates
    list_next_week_date = []

    # Start generating data for the next 12 weeks
    for i in range(maxData):
        next_week_start_date = end_date_last_week + timedelta(days=1)
        next_week_end_date = next_week_start_date + timedelta(days=6)
        
        # Format dates
        formatted_start_date = next_week_start_date.strftime("%d")
        formatted_end_date = next_week_end_date.strftime("%d %b %Y")
        
        # Append data to the lists
        list_next_week_date.append(f"{formatted_start_date} - {formatted_end_date}")
        
        # Update end_date_last_week for the next iteration
        end_date_last_week = next_week_end_date

    print("list_next_week_date:", list_next_week_date)
    return list_next_week_date