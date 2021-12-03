from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import json
import pandas as pd
import time

time.sleep(15)

# cur.execute('insert into users (gender,\
#                                 age,\
#                                 hypertension,\
#                                 heart_disease,\
#                                 ever_married,\
#                                 Residence_type ,\
#                                 avg_glucose_level,\
#                                 bmi,\
#                                 smoking_status,\
#                                 stroke) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
#                                 (1, \
#                                  1, \
#                                  67, \
#                                  0, \
#                                  1, \
#                                  1, \
#                                  1, \
#                                  228.69, \
#                                  36.6, \
#                                  2)'
#                                 )

database_uri = "postgresql://postgres:postgres@db:5432/postgres"

app = Flask(__name__)
conn = psycopg2.connect(database_uri)

@app.route("/")
def home():
    return "Hello lkfahslfhsalfdh!"

@app.route("/user", methods=["POST", "GET", "DELETE", "PATCH"])
def user():
    if request.method == "GET":
        # cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # # user_id = request.args.get("id")
        # user_id = 1
        # cur.execute(f"select * from users where id={user_id}")
        # results = cur.fetchone()
        # cur.close()
        # return json.dumps(results._asdict(), default=str)
        return 'Hola'

    if request.method == "POST":
        user = request.json
        cur = conn.cursor()
        cur.execute("insert into users (gender, age, hypertension, heart_disease, ever_married, Residence_type , avg_glucose_level, bmi, smoking_status, stroke) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" ,\
                   (user["gender"], user["age"], user["hypertension"], user["heart_disease"], user["ever_married"], user["Residence_type"], user["avg_glucose_level"], user["bmi"], user["smoking_status"], user["stroke"]),
                   )

        conn.commit()
        # cur.execute("SELECT LASTVAL()")
        # user_id = cur.fetchone()[0]
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
        cur.execute(
            "update users set (name, lastname, age) = (%s,%s,%s) where id=%s ",
            (user["name"], user["lastname"], user["age"], user_id),
        )
        conn.commit()
        cur.close()
        return json.dumps({"user_id": user_id})


@app.route("/users", methods=["POST", "GET", "DELETE", "PATCH"])
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
        users_list = [(user["name"], user["lastname"], user["age"]) for user in users]
        cur.executemany(
            "insert into users (name, lastname, age) values (%s, %s, %s)", users_list
        )
        conn.commit()
        cur.close()
        return "Correct!!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)