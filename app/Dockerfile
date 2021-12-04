FROM continuumio/miniconda3
EXPOSE 8080
COPY ./environment.yml /app/environment.yml
RUN conda env update -f /app/environment.yml
COPY . /app
RUN apt-get update && apt-get install -y jq curl
RUN chmod +x /app/limpieza/limpieza.sh
RUN /app/limpieza/limpieza.sh
RUN jq -R 'split(",")' /app/limpieza/healthcare-dataset-stroke-data-2.csv | jq -csf /app/limpieza/csv2json-helper.jq > /app/datos_json.txt
RUN chmod +x /app/entrypoint.sh
RUN mkdir /app/modelos_locales
ENTRYPOINT /app/entrypoint.sh
