FROM continuumio/miniconda3
EXPOSE 8080
COPY ./environment.yml /app/environment.yml
RUN conda env update -f /app/environment.yml
COPY . /app
RUN apt-get update && apt-get install -y jq curl
RUN chmod +x /app/limpieza/limpieza.sh
RUN /app/limpieza/limpieza.sh
RUN jq -R 'split(",")' /app/limpieza/healthcare-dataset-stroke-data-2.csv | jq -csf /app/limpieza/csv2json-helper.jq > /app/datos_json.txt
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "est_comp", "python", "/app/app.py"]
CMD ["curl","-X","POST","-H", "'Content-Type: application/json'","-d","@datos_json.txt","0.0.0.0:8080/users"]