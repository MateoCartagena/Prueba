# generar_token.py
import jwt

payload = {
    "name": "Juan Perez",
    "iss": "sKYih2eqdxdhLbK5AdzXmbovEH5Y21EJ"  # key de Kong
}

token = jwt.encode(payload, "RJkvfT6wGkPVEki8zwPBT8scLfl4qNOs", algorithm="HS256")
print(token)
