awk '!/N\/A/ && !/^$/ {print}' /app/healthcare-dataset-stroke-data.csv > /app/healthcare-dataset-stroke-data-new.csv

cut -d, -f2,3,4,5,6,8,9,10,11,12 /app/healthcare-dataset-stroke-data-new.csv > /app/healthcare-dataset-stroke-data-2.csv

sed -i 's/Other/0/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/Female/0/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/Male/1/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/Yes/1/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/No/0/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/Rural/0/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/Urban/1/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/never smoked/0/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/formerly smoked/1/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/smokes/2/g' /app/healthcare-dataset-stroke-data-2.csv
sed -i 's/Unknown/3/g' /app/healthcare-dataset-stroke-data-2.csv

