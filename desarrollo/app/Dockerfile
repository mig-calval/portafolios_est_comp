FROM continuumio/miniconda3
EXPOSE 8080
COPY ./environment.yml /app/environment.yml
RUN conda env update -f /app/environment.yml
COPY . /app
RUN apt-get update && apt-get install -y jq curl
RUN jq -R 'split(",")' healthcare-dataset-stroke-data.csv | jq -csf /app/csv2json-helper.jq > /app/datos_json.json
RUN 
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "est_comp", "python", "/app/app.py"]

