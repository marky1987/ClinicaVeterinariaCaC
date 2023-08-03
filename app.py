from flask import Flask, request, redirect, url_for, render_template, g, jsonify

from createTableAndDB import Database

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = Database('veterinaria.db')


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Contacto')
def contacto():
    return render_template('Contacto.html')


@app.route('/Peluqueria')
def peluqueria():
    return render_template('Peluqueria.html')


@app.route('/Consultorio')
def consultorio():
    turnos = g.db.consulta_turnos()
    turnos_list = []
    for turno in turnos:
        turno_dict = {
            'id': turno[0],
            'fecha': turno[1],
            'hora': turno[2],
            'nombre': turno[3],
            'mail': turno[4],
            'mascota': turno[5],
            'tipo': turno[6],
            'motivo': turno[7],
            'edad': turno[8],
            'peso': turno[9],
            'sexo': turno[10]
        }
        turnos_list.append(turno_dict)
    return render_template('Consultorio.html', turnos=turnos_list)


@app.route('/Consultorio/<int:turno_id>', methods=['GET'])
def consultorio_id(turno_id):
    turno = g.db.obtener_usuario(turno_id)
    turno_dict = {
        'id': turno[0],
        'fecha': turno[1],
        'hora': turno[2],
        'nombre': turno[3],
        'mail': turno[4],
        'mascota': turno[5],
        'tipo': turno[6],
        'motivo': turno[7],
        'edad': turno[8],
        'peso': turno[9],
        'sexo': turno[10]
    }
    return jsonify(turno_dict)


@app.route('/turno', methods=['POST'])
def turno():
    data = request.get_json()
    nombreCliente = data['name'] + " " + data['lastName']
    nombreMascota = data['petName']
    tipoMascota = data['petType']
    fecha = data['date']
    hora = data['time']
    sexoMascota = data['animalSex']
    pesoMascota = data['weight']
    edadMascota = data['age']
    motivoConsulta = data['motConsulta']
    mailCliente = data['email']

    g.db.insert_turno(fecha, hora, nombreCliente, mailCliente, nombreMascota, tipoMascota, motivoConsulta, edadMascota,
                      pesoMascota, sexoMascota)
    return jsonify({"message": "success"})


@app.route('/consultaTurnos', methods=['GET'])
def consultaTurnos():
    return g.db.consulta_turnos()


@app.route('/turno/editar/<int:turno_id>', methods=['POST'])
def editar_turno(turno_id):
    data = request.get_json()
    nombreCliente = data['name']
    nombreMascota = data['petName']
    tipoMascota = data['petType']
    fecha = data['date']
    hora = data['time']
    sexoMascota = data['animalSex']
    pesoMascota = data['weight']
    edadMascota = data['age']
    motivoConsulta = data['motConsulta']
    mailCliente = data['email']

    g.db.modificar_turno(turno_id, fecha, hora, nombreCliente, mailCliente, nombreMascota, tipoMascota, motivoConsulta,
                         edadMascota,
                         pesoMascota, sexoMascota)
    return jsonify({"message": "success"})


@app.route('/turno/eliminar/<int:turno_id>', methods=['DELETE'])
def eliminar_turno(turno_id):
    g.db.eliminar_turno(turno_id)
    return jsonify({"message": "success"})


if __name__ == '__main__':
    app.run(port=5000)  # run app in debug mode on port 5000
