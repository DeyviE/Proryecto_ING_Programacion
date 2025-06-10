from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['DATABASE'] = 'biblioteca.db'

def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Tabla de autores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                nacionalidad TEXT,
                fecha_nacimiento DATE
            )
        ''')
        
        # Tabla de libros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                id_autor INTEGER,
                genero TEXT,
                año_publicacion INTEGER,
                isbn TEXT UNIQUE,
                disponible BOOLEAN DEFAULT 1,
                FOREIGN KEY(id_autor) REFERENCES autores(id)
            )
        ''')
        
        # Tabla de préstamos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_libro INTEGER,
                nombre_usuario TEXT,
                fecha_prestamo DATE,
                fecha_devolucion DATE,
                devuelto BOOLEAN DEFAULT 0,
                FOREIGN KEY(id_libro) REFERENCES libros(id)
            )
        ''')
        
        # Datos de prueba
        if cursor.execute('SELECT COUNT(*) FROM autores').fetchone()[0] == 0:
            cursor.executemany('INSERT INTO autores (nombre, nacionalidad, fecha_nacimiento) VALUES (?, ?, ?)', [
                ('Gabriel García Márquez', 'Colombiano', '1927-03-06'),
                ('J.K. Rowling', 'Británica', '1965-07-31'),
                ('Mario Vargas Llosa', 'Peruano', '1936-03-28')
            ])
        
        if cursor.execute('SELECT COUNT(*) FROM libros').fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO libros (titulo, id_autor, genero, año_publicacion, isbn, disponible) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', [
                ('Cien años de soledad', 1, 'Realismo mágico', 1967, '9780307474728', 1),
                ('Harry Potter y la piedra filosofal', 2, 'Fantasía', 1997, '9788478884456', 1),
                ('La ciudad y los perros', 3, 'Literatura contemporánea', 1963, '9788420471839', 1)
            ])
        
        db.commit()
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    mensaje = None
    
    if request.method == 'POST':
        if 'crear_tabla' in request.form:
            nombre_tabla = secure_filename(request.form['nombre_tabla'])
            campos = request.form['campos']
            
            try:
                db.execute(f'CREATE TABLE {nombre_tabla} ({campos})')
                db.commit()
                mensaje = {'tipo': 'exito', 'texto': f'Tabla {nombre_tabla} creada exitosamente'}
            except sqlite3.Error as e:
                mensaje = {'tipo': 'error', 'texto': f'Error creando tabla: {str(e)}'}
        
        elif 'insertar_datos' in request.form:
            tabla = request.form['tabla_seleccionada']
            valores = request.form['valores']
            
            try:
                db.execute(f'INSERT INTO {tabla} VALUES ({valores})')
                db.commit()
                mensaje = {'tipo': 'exito', 'texto': f'Datos insertados en {tabla} exitosamente'}
            except sqlite3.Error as e:
                mensaje = {'tipo': 'error', 'texto': f'Error insertando datos: {str(e)}'}
    
    # Obtener datos para mostrar
    tablas = ['autores', 'libros', 'prestamos']
    datos_tablas = {}
    
    for tabla in tablas:
        cursor = db.execute(f'SELECT * FROM {tabla} LIMIT 10')
        datos_tablas[tabla] = {
            'encabezados': [desc[0] for desc in cursor.description],
            'filas': cursor.fetchall()
        }
    
    # Consulta especial para mostrar libros con nombres de autores
    cursor = db.execute('''
        SELECT l.id, l.titulo, a.nombre as autor, l.genero, l.año_publicacion, l.isbn, l.disponible 
        FROM libros l JOIN autores a ON l.id_autor = a.id
    ''')
    datos_tablas['libros_completos'] = {
        'encabezados': [desc[0] for desc in cursor.description],
        'filas': cursor.fetchall()
    }
    
    db.close()
    return render_template('index.html', tablas=tablas, datos_tablas=datos_tablas, mensaje=mensaje)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)