curl -X POST -H "Content-Type: application/json"\
     -d '{"name":"Pedro", "lastname":"Pérez", "age":33}'\
     0.0.0.0:8080/user

curl -X DELETE '0.0.0.0:8080/user?id=2'

curl -X PATCH -H "Content-Type: application/json"\
     -d '{"name":"Pedru", "lastname":"Péres", "age":44}'\
     '0.0.0.0:8080/user?id=3'

curl -X POST -H "Content-Type: application/json"\
     -d '[{"name":"Pedro", "lastname":"Pérez", "age":33},
     	  {"name":"Lucía", "lastname":"Juarez", "age":23}]'\
     0.0.0.0:8080/users


# Ejemplo de POST para un solo user: 
curl -X POST -H "Content-Type: application/json"\
     -d '{"gender": 1, "age": 67, "hypertension": 0, "heart_disease": 1, "ever_married": 1, "Residence_type": 1, "avg_glucose_level": "228.69", "bmi": "36.6", "smoking_status": 2, "stroke": 1}'\
     0.0.0.0:8080/user

# Ejemplo de DELETE para user: 
curl -X DELETE '0.0.0.0:8080/user?id=2'

# Ejemplo de GET para user: 
curl '0.0.0.0:8080/user?id=3'

# Ejemplo de PATCH para user: 
curl -X PATCH -H "Content-Type: application/json"\
     -d '{"gender": 0, "age": 670, "hypertension": 0, "heart_disease": 1, "ever_married": 1, "Residence_type": 1, "avg_glucose_level": "228.69", "bmi": "36.6", "smoking_status": 2, "stroke": 1}'\
     '0.0.0.0:8080/user?id=4'

# Ejemplo de GET para users (regresa toda la base de datos): 
curl '0.0.0.0:8080/users'

# Ejemplo de POST para múltiples users: 
curl -X POST -H "Content-Type: application/json"\
     -d '[{"gender": 1, "age": 67, "hypertension": 0, "heart_disease": 1, "ever_married": 1, "Residence_type": 1, "avg_glucose_level": "228.69", "bmi": "36.6", "smoking_status": 2, "stroke": 1}, 
          {"gender": 0, "age": 64, "hypertension": 0, "heart_disease": 1, "ever_married": 1, "Residence_type": 1, "avg_glucose_level": "228.69", "bmi": "36.6", "smoking_status": 2, "stroke": 1}]' \
          0.0.0.0:8080/users
