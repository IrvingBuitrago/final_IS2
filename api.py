# Importaciones necesarias
from flask import Flask, request, render_template, redirect
from conex import myconex

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Cargar la configuración desde el archivo 'config.py'
app.config.from_pyfile('config.py')

# Instanciar la conexión a la base de datos
instancia = myconex
instancia.conectar()


@app.route('/', methods=["GET"])
def appointment_form():
    return render_template('appointment.html')


@app.route('/appointment/search', methods=["GET", "POST"])
def search_appointment():
    if request.method == 'POST':
        try:
            name_last_name = request.form['name_last_name']
            name, last_name = name_last_name.split()

            query = 'SELECT id FROM patient WHERE first_name = %s AND last_name = %s'
            review_id = instancia.consultar(query, (name, last_name))

            if review_id:
                id_patient = review_id[0]
                query = 'SELECT * FROM appointment WHERE id_patient = %s'
                appo_review = instancia.consultar(query, (id_patient,))

                if appo_review:
                    return render_template('appointment.html', name_last_name=name_last_name, appo_review=appo_review)
                else:
                    return render_template('appointment.html', error='No se encontraron citas agendadas')
            else:
                return render_template('appointment.html', error='Paciente no encontrado')
        except Exception as e:
            return render_template('appointment.html', error=str(e))
    return render_template('appointment.html')


def add_appointment_logic(name_last_name, dates, times, reason):
    try:
        name, last_name = name_last_name.split()
        query = 'SELECT id FROM patient WHERE first_name = %s AND last_name = %s'
        patient_id = instancia.consultar(query, (name, last_name))

        if patient_id:
            query = 'SELECT * FROM appointment WHERE dates = %s AND times = %s'
            exist_appo = instancia.consultar(query, (dates, times))

            if exist_appo:
                return 'Ya hay una cita registrada en ese horario', None
            else:
                query = 'INSERT INTO appointment (id_patient, dates, times, reason) VALUES (%s, %s, %s, %s)'
                instancia.insertar(query, (patient_id[0], dates, times, reason))
                return 'Cita agregada con éxito', None
        else:
            return 'Paciente no encontrado', None
    except Exception as e:
        return f'La cita no se agregó correctamente: {str(e)}', None


@app.route('/appointment/add', methods=["GET", "POST"])
def add_appointment():
    if request.method == 'POST':
        try:
            name_last_name = request.form['name_last_name']
            name, last_name = name_last_name.split()
            dates = request.form['dates']
            times = request.form['times']
            reason = request.form['reason']

            query = 'SELECT id FROM patient WHERE first_name = %s AND last_name = %s'
            patient_id = instancia.consultar(query, (name, last_name))
            if patient_id:
                query = 'SELECT * FROM appointment WHERE dates = %s AND times = %s'
                exist_appo = instancia.consultar(query, (dates, times))

                if exist_appo:
                    return render_template('add_appointment.html', msg='Ya hay una cita registrada en ese horario.')
                else:
                    query = 'INSERT INTO appointment (id_patient, dates, times, reason) VALUES (%s, %s, %s, %s)'
                    instancia.insertar(query, (patient_id[0], dates, times, reason))
                    return render_template('appointment.html', msg='Cita agregada con éxito')
            else:
                return render_template('add_appointment.html', msg='Paciente no encontrado')
        except Exception as e:
            return render_template('add_appointment.html', msg='La cita no se agregó correctamente: ' + str(e))
    return render_template('add_appointment.html')


@app.route('/appointment/edit', methods=["GET", "POST"])
def edit_appointment():
    if request.method == "POST":
        try:
            column_update = request.form['column_update']
            new_data = request.form['new_data']
            appo_date = request.form['appo_date']
            time = request.form['time']
            reason = request.form['reason']

            query = f'UPDATE appointment SET {column_update} = %s WHERE dates = %s AND times = %s AND reason = %s'
            instancia.actualizar(query, (new_data, appo_date, time, reason))
            return render_template('appointment.html', msg='Cita editada con éxito')
        except Exception as e:
            return render_template('appointment.html', error='No se editó la cita correctamente: ' + str(e))
    return render_template('appointment.html')


@app.route('/appointment/delete', methods=["POST"])
def delete_appointment():
    try:
        name_last_name = request.form['name_last_name']
        name, last_name = name_last_name.split()
        dates = request.form['dates']
        times = request.form['times']
        reason = request.form['reason']

        query = 'SELECT id FROM patient WHERE first_name = %s AND last_name = %s'
        patient_id = instancia.consultar(query, (name, last_name))

        if patient_id:
            id_patient = patient_id[0]
            query = 'DELETE FROM appointment WHERE id_patient = %s AND dates = %s AND times = %s AND reason = %s'
            instancia.eliminar(query, (id_patient, dates, times, reason))
            return render_template('appointment.html', msg='Cita eliminada con éxito')
        else:
            return render_template('appointment.html', error='Paciente no encontrado')
    except Exception as e:
        return render_template('appointment.html', error='Error durante la eliminación: ' + str(e))


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)


