'''
Equipo 5

    Moscoso Cedillo Edmundo Enrique
    Ornelas Durán Natalia Alessandra
    Paez Medrano Kevin Randú
    Quistian Arreguín Victor Daniel
    Rentería Xochipa Moisés Alejandro
    Sección D03 Calendario 2024B
'''
import psycopg2
from tkinter import messagebox

# Clase correspondiente con la conexión de la base de datos
class Conexion:
	# Constructor de la clase donde se genera la conexión utilizaond psycopg2
	def __init__(self):
		conexion=psycopg2.connect(
			#Datos de la conexión
			host='localhost',
			port=5434,
			user='admin',
			password='admin',
			database='proyectoFinal')
		self.cursor=conexion.cursor()
		self.datosUsuario=()
		print('Conexión exitosa')

	# Funición que valida las credenciales de los usuarios que quieren acceder a la base de datos
	def validarCredenciales(self, usuario, contrasena):
		encontrado=False
		self.cursor.execute(f'SELECT "Nombre", "Código", "Contraseña" FROM public."EMPLEADO" WHERE "Código"={usuario} UNION SELECT "Nombre", "Código", "Contraseña" FROM public."DOCTOR" WHERE "Código"={usuario}')
		self.datosUsuario=self.cursor.fetchall()
		if len(self.datosUsuario):
			for i in range(len(self.datosUsuario)):
				if contrasena==self.datosUsuario[i][2]:
					self.datosUsuario=self.datosUsuario[i]
					encontrado=True
					break
			if encontrado:
				return encontrado
			else:
				messagebox.showerror('Error', f'Contraseña incorrecta')
		else:
			messagebox.showerror('Error', f'Usuario no reconocido')
			return encontrado

	# Función que obtiene el nombre del usuario conectado a la base de datos
	def obtenerNombreUsuario(self):
		return self.datosUsuario[0]

	# Función que obtnene el código del usuario conectado a la base de datos	
	def obtenerCodigoUsuario(self):
		return self.datosUsuario[1]

	# Función que obtinene la profesión del usuario conectado a la base de datos
	def obtenerProfesion(self, nombre):
		self.cursor.execute(f'SELECT "Nombre" FROM public."EMPLEADO" WHERE "Nombre"='+f"'{nombre}'")
		empleado=self.cursor.fetchall()
		if len(empleado):
			return 'E'
		else:
			return 'D'

	# Función para insertar valores en una tabla.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla en la cual se quieren insertar los valores.
	# valores- Tupla con los valores que se quieren agregar a la tabla.
	def insertInto(self, tabla, valores):
		peticion='SELECT "column_name" FROM information_schema.columns'+f" WHERE table_schema='public' AND table_name='{tabla}'"
		self.cursor.execute(peticion)
		columnas=self.cursor.fetchall()
		insert='INSERT INTO public."'+tabla+'"('
		for i in range(len(columnas)):
			if i<len(columnas)-1:
				insert+=f'"{columnas[i][0]}", '
			else:
				insert+=f'"{columnas[i][0]}"'
		insert+=') VALUES ('
		for i in range(len(columnas)):
			if i<len(columnas)-1:
				insert+='%s, '
			else:
				insert+='%s)'
		self.cursor.execute(insert, valores)
		self.cursor.connection.commit()

	# Función para seleccionar todos los atributos de todos los registros de una tabla.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla que se quiere consultar.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección. Si se seleccionaron 0 registros,
	# la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectAllFromTable(self, tabla):
		select=f'SELECT * FROM public."{tabla}"'
		self.cursor.execute(select)
		return self.cursor.fetchall()

	# Función para seleccionar los atributos Código y Nombre de todos los registros de una tabla.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla que se quiere consultar.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección y cada tupla tendrá dos elementos. 
	# Si se seleccionaron 0 registros la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectNameAndCodeFromTable(self, tabla):
		select=f'SELECT "Código", "Nombre" FROM public."{tabla}"'
		self.cursor.execute(select)
		return self.cursor.fetchall()

	# Función para seleccionar los atributos CódigoDoctor, Fecha y Hora de todos los registros de la tabla CITA.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección y cada tupla tendrá tres elementos. 
	# Si se seleccionaron 0 registros la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectDataFromCita(self):
		select=f'SELECT "CódigoDoctor", TO_CHAR("Fecha", '+"'DD-MM-YYYY'"+'), TO_CHAR("Hora", '+"'HH24:MM'"+f') FROM public."CITA"'
		self.cursor.execute(select)
		return self.cursor.fetchall()

	# Función para actualizar los datos de una tabla con alguna condición.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla que se quiere consultar.
	# atributos - Los atributos con las modificaciones que se les tienen que hacer.
	# condiciones - Lista de condiciones que se tienen que respetar en formato de cadena de caracteres
	def updateSetWhere(self, tabla, atributos, condiciones):
		update=f'UPDATE public."{tabla}" SET {atributos} WHERE {condiciones}'
		self.cursor.execute(update)
		self.cursor.connection.commit()

	# Función para seleccionar todos los atributos de los registros cuyo atributo Nombre tenga un valor en especifico.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla que se quiere consultar.
	# nombre - Cadena de caracteres con el valor que tiene que tener el atributo Nombre para que un registro sea seleccionado.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección. 
	# Si se seleccionaron 0 registros la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectAllFromTableWhereName(self, tabla, nombre):
		select=f'SELECT * FROM public."{tabla}" WHERE "Nombre"='+f"'{nombre}'"
		self.cursor.execute(select)
		return self.cursor.fetchall()

	# Función para seleccionar todos los atributos de los registros cuyo atributo CódigoDoctor tenga un valor en especifico.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla que se quiere consultar.
	# codigo - Cadena de caracteres con el valor que tiene que tener el atributo CódigoDoctor para que un registro sea seleccionado.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección. 
	# Si se seleccionaron 0 registros la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectAllFromTableWhereDoctorCode(self, tabla, codigo):
		select=f'SELECT * FROM public."{tabla}" WHERE "CódigoDoctor"='+f"'{codigo}'"
		self.cursor.execute(select)
		return self.cursor.fetchall()

	# Función para seleccionar todos los atributos de los registros cuyo atributo Código tenga un valor en especifico.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla que se quiere consultar.
	# codigo - Cadena de caracteres con el valor que tiene que tener el atributo Código para que un registro sea seleccionado.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección. 
	# Si se seleccionaron 0 registros la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectAllFromTableWhereCode(self, tabla, codigo):
		select=f'SELECT * FROM public."{tabla}" WHERE "Código"='+f"'{codigo}'"
		self.cursor.execute(select)
		return self.cursor.fetchall() 
	
	# Función para seleccionar todos los atributos de los registros cuyo atributo CódigoDoctor tenga un valor en especifico.
	# Recibe:
	# tabla - Cadena de caracteres con el nombre de la tabla que se quiere consultar.
	# codigo - Cadena de caracteres con el valor que tiene que tener el atributo CódigoDoctor para que un registro sea seleccionado.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección. 
	# Si se seleccionaron 0 registros la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectAllFromTableWhereDateAndCode(self, tabla, fecha, codigo):
		select=f'SELECT * FROM public."{tabla}" WHERE "Fecha"='+f"'{fecha}' AND "+f'"CódigoDoctor"={codigo}'
		self.cursor.execute(select)
		return self.cursor.fetchall()

	# Función para seleccionar todos los atributos de los registros de la tabla CITA 
	# cuyos atributos Fecha y Código tengan un valor en especifico.
	# Recibe:
	# fecha1 - El valor mínimo que puede tener el atributo Fecha.
	# fecha2 - El valor máximo que puede tener al atributo Fecha.
	# codigo - El valor que debe tener el atributo Código de un registro para que éste sea seleccionado.
	# Retorna:
	# Una lista de tuplas, cada tupla representa un registro de la selección. 
	# Si se seleccionaron 0 registros la lista estará vacía. Si se seleccionarion N registros, la lista tendrá N tuplas.
	def selectAllFromCitaWhereDateBetweenAndCode(self, fecha1, fecha2, codigo):
		select=f'SELECT * FROM public."CITA" WHERE "CódigoDoctor"={codigo} AND "Fecha" BETWEEN '+f"'{fecha1}' AND '{fecha2}'"
		self.cursor.execute(select)
		return self.cursor.fetchall()

