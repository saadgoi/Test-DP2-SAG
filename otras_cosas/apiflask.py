from flask import Flask
from flask import request
#from flask import jsonify

app = Flask(__name__)


#Ruta donde tenemos la carpeta , + el metódo de Get y Post
@app.route('/app/v1/Desktop/<id>', methods=["GET", "POST"])
# Defino una función donde quiero que me imprima de que metodo es esa request
def users_action(id):
    print(request.form)
    #print(request.form['temperatura'])
    #print(request.method)
    if( request.method == "POST") :
        print( " guardate en la base")
        return " guardado"
    else:
        print("recurso obtenido")
        return id
    
    # Todos los return nos los devuelve en Postman
    
#Corremos el código, nos dará una Url que introduciremos en Postman 
app.run(debug=True)
