from dotenv import load_dotenv
import os
from pprint import pprint
import requests

load_dotenv()

def gen_product(product = "productos"):
   status_id = os.getenv("STATUS_ID")
   site_id = os.getenv("SITE_ID")
   product_identifier = os.getenv("PRODUCT_IDENTIFIER")
   api_key = os.getenv("API_KEY")
    
    # URL con los parámetros de consulta
   url = f"https://api.mercadolibre.com/sites/MLA/search?q={product}"

    # Encabezado de autorización con API_KEY
   try:
          # Realizamos la solicitud a la API
          response = requests.get(url)
          response.raise_for_status()  # Lanza un error si la solicitud no es exitosa (código 4xx o 5xx)
          data = response.json()  # Con
     
          if data and "results" in data and len(data["results"]) > 0:
            # Extraemos los detalles del primer producto encontrado
            product_info = data["results"][0]
            return {
                "nombre": product_info["title"],    # Título del producto
                "precio": product_info["price"],    # Precio del producto
                "imagen": product_info["thumbnail"],  # URL de la imagen del producto
                "product": data["results"]          # Lista completa de productos (opcional)
            }
          else:
            return {}  # Si no hay resultados, dev

     # Llamar a la función

   except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a la API: {e}")
        return {}  # Si ha
