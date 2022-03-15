from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto_herramientas'
mysql = MySQL(app)

#sesion
app.secret_key = 'mysecretkey'

@app.route('/')
def inicio():
    cur = mysql.connection.cursor()
    cur.execute('Select * from tipo_pago' )
    datos = cur.fetchall()
    return render_template('index.html',tipos=datos)

@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        codigo = request.form['codigoTipo']
        descripcion = request.form['descripcion']
        print(codigo)
        print(descripcion)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tipo_pago VALUES (%s,%s)', (codigo,descripcion) )
        mysql.connection.commit()
        flash('Se agrego satisfactoriamente')
        return redirect(url_for('inicio'))

@app.route('/editar/<id>')
def asignarEdicion(id):
    cur = mysql.connection.cursor()
    cur.execute('Select * from tipo_pago where codigo = %s',(id) )
    datos = cur.fetchall()
    return render_template('editarTipo.html', tipo = datos[0])

@app.route('/editar/<id>', methods=['POST'])
def editar(id):
    if request.method == 'POST':
        codigo = request.form['codigo']
        descripcion = request.form['descrip']
        cur = mysql.get_db().cursor()
        cur.execute('UPDATE tipo_pago SET descripcion =%s where codigo = %s',(descripcion,id) )
        mysql.get_db().commit()
        return redirect(url_for('inicio'))

@app.route('/eliminar/<string:cod>') 
def eliminar(cod):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tipo_pago WHERE codigo = %s',(cod))
    mysql.connection.commit()
    flash('Se elimino satisfactoriamente')
    return redirect(url_for('inicio'))




if __name__ == '__main__':
    app.run(port=3000, debug=True)