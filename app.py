from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_MYSQL_DB'] = 'proyectopython'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template('home.html')

@app.route('/verProducto')
def verProducto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectopython.productos')
    data = cur.fetchall()
    print(data)
    return render_template('productos.html', productos = data)

@app.route('/verClient')
def verClient():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectopython.clientes')
    data = cur.fetchall()
    print(data)
    return render_template('clientes.html', clientes = data)

## Todo sobre clientes

@app.route('/addClient', methods = ['POST'])
def addClient():
    if request.method == 'POST':
        nombreCompleto = request.form['nombreCompleto']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO proyectopython.clientes (nombreCompleto, telefono, email) VALUES (%s, %s, %s)', (nombreCompleto, telefono, email))
        mysql.connection.commit()
        flash('Cliente agregado satisfactoriamente')
        return redirect(url_for('verClient'))

@app.route('/edit/<id>')
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectopython.clientes WHERE id ={0}'.format(id))
    data = cur.fetchall()
    print(data[0])
    return render_template('editarCliente.html', cliente = data[0])

@app.route('/update/<id>', methods = ['POST'])
def updateCliente(id):
    if request.method == 'POST':
        nombreCompleto = request.form['nombreCompleto']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE proyectopython.clientes
        SET nombreCompleto = %s,
            telefono = %s,
            email = %s
        WHERE id = %s
        """, (nombreCompleto, telefono, email, id))
        mysql.connection.commit()
        flash('Cliente actualizado satisfactoriamente')
        return redirect(url_for('verClient'))

@app.route('/delete/<string:id>')
def deleteClient(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM proyectopython.clientes WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Cliente removido satisfactoriamente')
    return redirect(url_for('verClient'))

## Todo sobre productos

@app.route('/addProducto', methods = ['POST'])
def addProducto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO proyectopython.productos (nombre, descripcion, stock, precio) VALUES (%s, %s, %s, %s)', (nombre, descripcion, stock, precio))
        mysql.connection.commit()
        flash('Producto agregado satisfactoriamente')
        return redirect(url_for('verProducto'))


@app.route('/editProd/<string:id>')
def get_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectopython.productos WHERE id = {0}'.format(id))
    data = cur.fetchall()
    print(data)
    return render_template('editarProducto.html', producto = data[0])


@app.route('/updateProd/<id>', methods = ['POST'])
def updateProducto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE proyectopython.productos SET nombre = %s, descripcion = %s, stock = %s, precio = %s WHERE id = %s', (nombre, descripcion, stock, precio, int(id)))
        mysql.connection.commit()
        flash('Producto actualizado satisfactoriamente')
        return redirect(url_for('verProducto'))


@app.route('/deleteProd/<id>')
def deleteProducto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM proyectopython.productos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto removido satisfactoriamente')
    return redirect(url_for('verProducto'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)


