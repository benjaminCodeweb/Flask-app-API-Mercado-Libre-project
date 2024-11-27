import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from config import gen_product
from pydantic import EmailStr, BaseModel, ValidationError 
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = os.urandom(24) 




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/productos')
def buscar_productos():
 product = request.args.get('product')
    
    # Si no se proporciona un producto, retornamos un mensaje de error
 if not product:
        return "No se ha proporcionado un nombre de producto", 400
    
    # Llamamos a gen_product con el nombre del producto
 products_data = gen_product(product)
    
    # Si no obtenemos productos o los datos no son válidos, retornamos un error
 if not products_data or "nombre" not in products_data or "product" not in products_data:
        return "No se encontraron productos o hubo un error al obtener los datos", 404
    
 precio = products_data.get("precio", "precio no disponible")
 imagen = products_data.get("imagen", "")   
 nombre = products_data.get("nombre", "Nombre no disponible")
 description = products_data.get("product", [{}])[0].get("description", "Descripción no disponible").capitalize()       
    
 return render_template('productos.html', nombre=nombre, status=description, precio= precio, imagen=imagen)



@app.route('/agregar_al_carrito', methods = ['POST'])
def agregar_al_carrito():
    # Crear un diccionario con los detalles del producto recibido desde el formulario
    producto = {
        "nombre": request.form['nombre'],
        "precio": float(request.form['precio']),
        "imagen": request.form['imagen'],
    }

    # Si el carrito no existe en la sesión, se crea como una lista vacía
    if 'carrito' not in session:
        session['carrito'] = []

    # Agregar el producto al carrito en la sesión
    session['carrito'].append(producto)
    session.modified = True  # Marca la sesión como modificada para asegurar que se actualice

    return redirect(url_for('ver_carrito')) 

@app.route('/ver_carrito')
def ver_carrito():
  carrito = session.get('carrito', [])
  return render_template('carrito.html', carrito = carrito)  

@app.route('/eliminar_carrito')
def eliminar_carrito():
    nombre_producto = request.form['nombre']

    if 'carrito' in session:
        session['carrito'] = [producto for producto in session['carrito'] if producto['nombre'] != nombre_producto]
        session.modified = True

    return redirect(url_for('ver_carrito'))


@app.route('/contacto', methods= ['GET', 'POST'])
def contacto():

 if request.method == 'POST':
  nombre = request.form.get('nombre')
  gmail = request.form.get('Gmail')
  fecha_str = request.form.get('fecha')
  descrip = request.form.get('descrip')

  try: 
      fecha = datetime.strptime(fecha_str, '%Y-%m-%d' ).date()
  except ValueError:
      flash ('formulario incorrecto de fecha. use yyyy- MM- DD.')
      return redirect(url_for('contacto'))
  
  if fecha < datetime.today().date():
      flash("la fecha ingresada no puede ser anterior a la fecha actual")
      return redirect(url_for('contacto'))
  
  return render_template('info.html', gmail=gmail, nombre=nombre, fecha=fecha, descrip=descrip)

 return render_template('contactos.html')

  

if __name__ == '__main__':
    app.run(debug=True)
    