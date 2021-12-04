conda run --no-capture-output -n est_comp python /app/app.py


docker exec web_miguel_adrian curl -X POST -H "Content-Type: application/json" -d @app/datos_json.txt 0.0.0.0:8080/users