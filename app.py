from flask import Flask, render_template, request, redirect
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
basedatos = client.tareas
mistareas = basedatos.lista

titulo = "Python y flask"
cabecera = "Gestion de tareas con Flask y MongoDB"

@app.route("/")
@app.route("/incompletas")
def lista_incompletas():
    incompletas = mistareas.find({"acabada": "no"})
    return render_template('index.html', a2="active", lista=incompletas, t=titulo, h=cabecera)

@app.route("/agregar", methods=['POST'])
def agregar_tarea():
    nom = request.values.get("nombre")
    desc = request.values.get("descripcion")
    fec = request.values.get("fecha")
    pr = request.values.get("prioridad")
    mistareas.insert({"nombre":nom, "descripcion":desc, "fecha":fec, "prioridad":pr, "acabada":"no"})
    return redirect("/")

@app.route("/todas")
def lista_todas():
    todas = mistareas.find()
    return render_template('index.html', a1="active", lista=todas, t=titulo, h=cabecera)

@app.route("/completadas")
def lista_completadas():
    completadas = mistareas.find({"acabada": "ok"})
    return render_template('index.html', a3="active", lista=completadas, t=titulo, h=cabecera)

@app.route("/cambiar")
def cambiar_estado():
    id=request.values.get("_id")
    tarea=mistareas.find_one({"_id": ObjectId(id)})
    if(tarea["acabada"]=="ok"):
        mistareas.update({"_id": ObjectId(id)}, {"$set": {"acabada": "no"}})
    else:
        mistareas.update({"_id": ObjectId(id)}, {"$set": {"acabada": "ok"}})
    return redirect("/")

@app.route("/buscar", methods=['GET'])
def buscar():
    c = request.values.get("campo")
    v = request.values.get("valor")
    encontradas = mistareas.find({c: v})
    return render_template('buscar.html', lista=encontradas, t=titulo, h=cabecera)

@app.route("/eliminar", methods=['GET'])
def eliminar():
    key = request.values.get("_id")
    mistareas.remove({"_id": ObjectId(key)})
    return redirect("/")

@app.route("/editar", methods=['GET'])
def pag_editar():
    id=request.values.get("_id")
    tarea=mistareas.find_one({"_id": ObjectId(id)})
    return render_template('editar.html', tarea=tarea, t=titulo, h=cabecera)

@app.route("/actualizar", methods=['POST'])
def efectuar_actualizar():
    id = request.values.get("_id")
    nom=request.values.get("nombre")
    desc=request.values.get("descripcion")
    fec=request.values.get("fecha")
    pr=request.values.get("prioridad")
    mistareas.update({"_id": ObjectId(id)}, {'$set':{"nombre":nom, "descripcion":desc, "fecha":fec, "prioridad":pr}})

if __name__ == "__main__":
    app.run()