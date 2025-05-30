# generar_token.py
import jwt

token = jwt.encode({"usuario": "juan.perez"}, "mi_clave_secreta", algorithm="HS256")
print(token)
