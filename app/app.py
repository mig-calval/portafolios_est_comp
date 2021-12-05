from flask import Flask, request, jsonify, render_template, session, redirect, Response
import psycopg2
import psycopg2.extras
import json
import numpy as np
import pandas as pd
import time

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedKFold
import multiprocessing

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import io

import os
from datetime import datetime
from joblib import dump
from joblib import load

time.sleep(10)

database_uri = "postgresql://postgres:postgres@db:5432/postgres"

app = Flask(__name__)
conn = psycopg2.connect(database_uri)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/train_model")
def train_model():
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute("select * from users")
    results = cur.fetchall()
    cur.close()
    print("Data has been retreived. Model is being trained...")
    all_data = pd.DataFrame(results, columns = ['id', 'gender', 'age', 'hypertension', 'heart_disease', \
            'ever_married', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])
    all_data.drop('id', 1, inplace = True)

    X_train, X_test, y_train, y_test = train_test_split(all_data.drop(columns = "stroke"),
                                                        all_data['stroke'],
                                                        random_state = 203129)

    param_grid = {'n_estimators': [100, 120, 140],
                  'max_features': [5, 7, 9],
                 }

    grid = GridSearchCV(
            estimator  = RandomForestClassifier(random_state = 203129),
            param_grid = param_grid,
            scoring    = 'neg_log_loss',
            n_jobs     = multiprocessing.cpu_count() - 1,
            cv         = RepeatedKFold(n_splits=5, n_repeats=3, random_state=123), 
            refit      = True,
            verbose    = 0,
            return_train_score = True
        )

    grid.fit(X = X_train, y = y_train)

    modelo_final = grid.best_estimator_
    predicciones = modelo_final.predict(X = X_test)

    id_model = str(datetime.now())[:-7].replace('-', '_').replace(' ', '_').replace(':', '_')
    dump(modelo_final, filename = f"/app/modelos_locales/random_forest_{id_model}.joblib")    

    return json.dumps({"message": 'El modelo fue entrenado y guardado exitosamente.'})

@app.route("/predict")
def predict():
    aux = [file for file in os.listdir('/app/modelos_locales') if file[-6:] == 'joblib']
    if len(aux) > 0:
        modelo_actual = load('/app/modelos_locales/' + aux[-1])
        
        new_user_json = {
                        "gender": 1, 
                        "age": 67, 
                        "hypertension": 0, 
                        "heart_disease": 1, 
                        "ever_married": 1, 
                        "Residence_type": 1, 
                        "avg_glucose_level": "278.69", 
                        "bmi": "36.6",
                        "smoking_status": 2
                        }
        
        new_user = np.array([pd.Series(new_user_json)])
        
        if modelo_actual.predict(new_user) == 1:
            return json.dumps({"message": 'Tienes riesgo de sufrir un derrame.'})
        else:
            return json.dumps({"message": 'NO tienes riesgo de sufrir un derrame.'})
    else:
        return json.dumps({"message":'Se necesita un modelo. Prueba /train_model.'})

@app.route("/user", methods=["POST", "GET", "DELETE", "PATCH"])
def user():
    if request.method == "GET":
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        user_id = request.args.get("id")
        cur.execute(f"select * from users where id={user_id}")
        results = cur.fetchone()
        cur.close()

        return json.dumps(results._asdict(), default=str)

    if request.method == "POST":
        user = request.json
        cur = conn.cursor()
        cur.execute("insert into users (gender, age, hypertension, heart_disease, ever_married, Residence_type , avg_glucose_level, bmi, smoking_status, stroke) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" ,\
                   (user["gender"], user["age"], user["hypertension"], user["heart_disease"], user["ever_married"], user["Residence_type"], user["avg_glucose_level"], user["bmi"], user["smoking_status"], user["stroke"]),
                   )

        conn.commit()
        cur.execute("SELECT LASTVAL()")
        user_id = cur.fetchone()[0]
        cur.close()
        return json.dumps({"new_user": 'Se registro un nuevo usuario'})

    if request.method == "DELETE":
        cur = conn.cursor()
        user_id = request.args.get("id")
        cur.execute(f"delete from users where id={user_id}")
        conn.commit()
        cur.close()
        return json.dumps({"user_id": user_id})

    if request.method == "PATCH":
        user = request.json
        cur = conn.cursor()
        user_id = request.args.get("id")
        cur.execute("update users set (gender, age, hypertension, heart_disease, ever_married, Residence_type , avg_glucose_level, bmi, smoking_status, stroke) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) where id=%s" ,\
                   (user["gender"], user["age"], user["hypertension"], user["heart_disease"], user["ever_married"], user["Residence_type"], user["avg_glucose_level"], user["bmi"], user["smoking_status"], user["stroke"], user_id),
                   )
        conn.commit()
        cur.close()
        return json.dumps({"user_id": user_id})

@app.route("/users", methods=["POST", "GET", "DELETE"])
def users():
    if request.method == "GET":
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute("select * from users")
        results = cur.fetchall()
        cur.close()
        return json.dumps([x._asdict() for x in results], default=str)
    
    if request.method == "POST":
        cur = conn.cursor()
        users = request.json
        users_list = [(user["gender"], user["age"], user["hypertension"], user["heart_disease"], user["ever_married"], user["Residence_type"], user["avg_glucose_level"], user["bmi"], user["smoking_status"], user["stroke"]) for user in users]
        cur.executemany(
            "insert into users (gender, age, hypertension, heart_disease, ever_married, Residence_type , avg_glucose_level, bmi, smoking_status, stroke) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", users_list
        )
        conn.commit()
        cur.close()
        return "Correct!!"
    if request.method == "DELETE":
        users = request.json
        cur = conn.cursor()
        users_list = [(user,) for user in users["id"]]
        cur.executemany("delete from users where id=%s",  users_list)
        conn.commit()
        cur.close()
        return json.dumps({"mensaje": 'Se borraron correctamente'})

@app.route("/save_model")
def guardar():
    modelo = request.json

@app.route("/show_models")
def show_models():
    aux = [file for file in os.listdir('/app/modelos') if file[-6:] == 'joblib']
    if len(aux) == 0:
        return json.dumps({"message":'No hay modelos guardados'})
    else: 
        return json.dumps(dict(aux))

@app.route("/show_local_models")
def show_local_models():
    aux = [file for file in os.listdir('/app/modelos_locales') if file[-6:] == 'joblib']
    if len(aux) == 0:
        return json.dumps({"message":'No hay modelos locales guardados'})
    else: 
        return json.dumps([x._asdict() for x in aux], default=str)

@app.route("/tabla_usuarios")
def render_table():
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute("select * from users")
    results = cur.fetchall()
    cur.close()
    all_data = pd.DataFrame(results, columns = ['id', 'gender', 'age', 'hypertension', 'heart_disease', \
            'ever_married', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])

    return render_template('simple.html',  tables=[all_data.to_html(classes='data')], titles=all_data.columns.values)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == "__main__":
    try:
        os.mkdir('modelos')
    except FileExistsError:
        pass
    app.run(host="0.0.0.0", debug=True, port=8080)
