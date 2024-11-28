'''
Equipo 5
    Moscoso Cedillo Edmundo Enrique
    Ornelas Durán Natalia Alessandra
    Paez Medrano Kevin Randú
    Quistian Arreguín Victor Daniel
    Rentería Xochipa Moisés Alejandro
    Sección D03 Calendario 2024B
'''
import tkinter as tk
import connection as dataBase
import tkcalendar as tkc
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DB_MASTER_USUARIO='admin'
DB_MASTER_CONTRASENA='1234'

# Clase para la vetana de Login
class VentanaLogin:
    # Constructor de la clase
    def __init__(self, root, conexion):
        self.root=root
        self.root.title('Inicio de sesión')
        self.root.geometry('300x300')
        self.conexion=conexion

        # Elementos de la ventana de login
        labelTitulo=ttk.Label(root, text='Inicio de Sesión', font=('Helvetica', 16))
        labelTitulo.pack(pady=10)

        labelUsuario=ttk.Label(root, text='Usuario:')
        labelUsuario.pack(pady=5)
        self.usuarioVar=tk.StringVar()
        entryUsuario=ttk.Entry(root, textvariable=self.usuarioVar)
        entryUsuario.pack(pady=5)

        labelContrasena=ttk.Label(root, text='Contraseña:')
        labelContrasena.pack(pady=5)
        self.contrasenaVar=tk.StringVar()
        entryContrasena=ttk.Entry(root, show='*', textvariable=self.contrasenaVar)
        entryContrasena.pack(pady=5)

        btnAceptar=ttk.Button(root, text='Aceptar', command=self.iniciarSesion)
        btnAceptar.pack(pady=5)

        btnCerrar=ttk.Button(root, text='Cerrar', command=self.root.quit)
        btnCerrar.pack(pady=5)

    # Función llamada al presionar el botón Iniciar sesión
    def iniciarSesion(self):
        # Validación de usuario y contraseña
        usuario=self.usuarioVar.get()
        contrasena=self.contrasenaVar.get()
        
        if usuario==DB_MASTER_USUARIO and contrasena==DB_MASTER_CONTRASENA:
            self.root.withdraw()
            self.usuarioVar.set('')
            self.contrasenaVar.set('')
            VentanaSistema(self.root, self.conexion, usuario)
        else:
            try:
                if conexion.validarCredenciales(usuario, contrasena)==True:
                    self.root.withdraw()
                    self.usuarioVar.set('')
                    self.contrasenaVar.set('')
                    VentanaSistema(self.root, self.conexion, self.conexion.obtenerNombreUsuario())
            except Exception as ex:
                messagebox.showerror('Error', f'Error de conexión con la base de datos: {ex}')

# Clase principal de Mi Núcleo de Diagnóstico
class VentanaSistema:
    #Constructor de la clase
    def __init__(self, root, conexion, nombreCompletoUsuario):
        self.root=root
        self.ventanaSistema=tk.Toplevel(root)
        self.ventanaSistema.title("Mi Nucleo de Diagnóstico")
        self.conexion=conexion

        # Elementos de la ventana del sistema
        frameVentanaSistema=ttk.Frame(self.ventanaSistema)
        frameVentanaSistema.pack(fill='both', expand=True)

        nombreUsuario=''
        for i in range(len(nombreCompletoUsuario)):
            c=nombreCompletoUsuario[i]
            if c==' ':
                break
            nombreUsuario+=c
        labelUsuario=ttk.Label(frameVentanaSistema, text=f'Hola, {nombreUsuario}', font=('Helvetica', 13))
        labelUsuario.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        labelTitulo=ttk.Label(frameVentanaSistema, text="Mi Nucleo de Diagnóstico", font=('Helvetica', 16))
        labelTitulo.grid(row=1, column=0, pady=10) 

        menu=tk.Menu(self.ventanaSistema, tearoff=False)

        menuEmpleados=tk.Menu(menu, tearoff=False)
        menuDoctores=tk.Menu(menu, tearoff=False)
        menuPacientes=tk.Menu(menu, tearoff=False)
        menuCitas=tk.Menu(menu, tearoff=False)
        menuMedicamentos=tk.Menu(menu, tearoff=False)
        menuDiagnostico=tk.Menu(menu, tearoff=False)

        menuEmpleados.add_command(label='Agregar empleado', command=self.agregarEmpleado)
        menuEmpleados.add_command(label='Consulta general', command=self.mostrarEmpleados)

        menuDoctores.add_command(label='Agregar doctor', command=self.agregarDoctor)
        menuDoctores.add_command(label='Consulta general', command=self.mostrarDoctores)
        
        menuMedicamentos.add_command(label='Agregar medicamento', command=self.agregarMedicamento)
        menuMedicamentos.add_command(label='Consulta general', command=self.mostrarMedicamentos)

        menu.add_cascade(label='Empleados', menu=menuEmpleados)
        menu.add_cascade(label='Doctores', menu=menuDoctores)
        menu.add_cascade(label='Pacientes', menu=menuPacientes)
        menu.add_cascade(label='Citas', menu=menuCitas)
        menu.add_cascade(label='Medicamentos', menu=menuMedicamentos)
        menu.add_cascade(label='Diagnóstico', menu=menuDiagnostico)

        if nombreUsuario!=DB_MASTER_USUARIO:
            menu.entryconfig('Empleados', state='disabled')
            menu.entryconfig('Doctores', state='disabled')
            menu.entryconfig('Medicamentos', state='disabled')

        if nombreUsuario==DB_MASTER_USUARIO:
            menuPacientes.add_command(label='Agregar paciente', command=self.agregarPaciente)
            menuPacientes.add_command(label='Consulta general', command=self.mostrarPacientes)

            menuCitas.add_command(label='Agregar cita', command=self.agregarCita)
            menuCitas.add_command(label='Modificar cita', command=self.modificarCita)

            menuPacientes.add_command(label='Ver informacion paciente', command=self.mostrarInformacionPaciente)

            menuDiagnostico.add_command(label='Generar diagnóstico', command=self.generarDiagnostico)
        elif self.conexion.obtenerProfesion(self.conexion.obtenerNombreUsuario())=='E':
            menu.entryconfig('Diagnóstico', state='disabled')

            menuPacientes.add_command(label='Agregar paciente', command=self.agregarPaciente)
            menuPacientes.add_command(label='Consulta general', command=self.mostrarPacientes)

            menuCitas.add_command(label='Agregar cita', command=self.agregarCita)
            menuCitas.add_command(label='Modificar cita', command=self.modificarCita)
        else:
            menuPacientes.add_command(label='Ver informacion paciente', command=self.mostrarInformacionPaciente)

            menuCitas.add_command(label='Ver cita (día específico)', command=self.verCitaDia)
            menuCitas.add_command(label='Ver citas (por semana)', command=self.verCitasSemana)
            menuCitas.add_command(label='Ver citas (por mes)', command=self.verCitasMes)

            menuDiagnostico.add_command(label='Generar diagnóstico', command=self.generarDiagnostico)

        self.ventanaSistema.configure(menu=menu)

        imagen=Image.open('images/salud1.png')
        self.imagen=ImageTk.PhotoImage(imagen)
        labelImagen=ttk.Label(frameVentanaSistema, image=self.imagen)
        labelImagen.grid(row=2, column=0, pady=10)

        botonCerrarSesión=ttk.Button(frameVentanaSistema, text="Cerrar sesión", command=self.cerrarSesión)
        botonCerrarSesión.grid(row=3, column=0, pady=5)

    # Función llamada al presionar el botón Cerrar sesión
    def cerrarSesión(self):
        self.ventanaSistema.destroy()
        self.root.deiconify()

    # Función llamada al presionar el botón Agregar en la ventana empleado
    def agregarEmpleado(self):
    
        # Enviar la petición para insertar un empleado a la base de datos
        def enviarPeticionBD():
            try:
                valores=(codigo.get(), nombre.get(), direccion.get(), telefono.get(), fechaNac.get(), sexo.get(), sueldo.get(), turno.get(), contrasena.get())
                self.conexion.insertInto('EMPLEADO', valores)
                ventanaEmpleado.destroy()
                messagebox.showinfo('Éxito', 'Empleado agregado correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al agregar el empleado: {ex}')

        ventanaEmpleado=tk.Toplevel()
        ventanaEmpleado.title('Agregar empleado')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaEmpleado, text='Ingresa los datos para el empleado:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameFormularioEmpleado=ttk.Frame(ventanaEmpleado)
        frameFormularioEmpleado.pack(pady=10)

        codigo=tk.StringVar()
        labelCodigo=ttk.Label(frameFormularioEmpleado, text='Código:', font=('Helvetica', 12))
        entryCodigo=ttk.Entry(frameFormularioEmpleado, textvariable=codigo)
        labelCodigo.pack(pady=10)
        entryCodigo.pack()

        nombre=tk.StringVar()
        labelNombre=ttk.Label(frameFormularioEmpleado, text='Nombre:', font=('Helvetica', 12))
        entryNombre=ttk.Entry(frameFormularioEmpleado, textvariable=nombre)
        labelNombre.pack(pady=10)
        entryNombre.pack()

        direccion=tk.StringVar()
        labelDireccion=ttk.Label(frameFormularioEmpleado, text='Dirección:', font=('Helvetica', 12))
        entryDireccion=ttk.Entry(frameFormularioEmpleado, textvariable=direccion)
        labelDireccion.pack(pady=10)
        entryDireccion.pack()

        telefono=tk.StringVar()
        labelTeléfono=ttk.Label(frameFormularioEmpleado, text='Teléfono:', font=('Helvetica', 12))
        entryTeléfono=ttk.Entry(frameFormularioEmpleado, textvariable=telefono)
        labelTeléfono.pack(pady=10)
        entryTeléfono.pack()

        fechaNac=tk.StringVar()
        labelFechaNac=ttk.Label(frameFormularioEmpleado, text='Fecha de nacimiento:', font=('Helvetica', 12))
        entryFechaNac=ttk.Entry(frameFormularioEmpleado, textvariable=fechaNac)
        labelFechaNac.pack(pady=10)
        entryFechaNac.pack()

        sexo=tk.StringVar()
        labelSexo=ttk.Label(frameFormularioEmpleado, text='Sexo:', font=('Helvetica', 12))
        entrySexo=ttk.Entry(frameFormularioEmpleado, textvariable=sexo)
        labelSexo.pack(pady=10)
        entrySexo.pack()

        sueldo=tk.DoubleVar()
        labelSueldo=ttk.Label(frameFormularioEmpleado, text='Sueldo:', font=('Helvetica', 12))
        entrySueldo=ttk.Entry(frameFormularioEmpleado, textvariable=sueldo)
        labelSueldo.pack(pady=10)
        entrySueldo.pack()

        turno=tk.StringVar()
        labelTurno=ttk.Label(frameFormularioEmpleado, text='Turno:', font=('Helvetica', 12))
        entryTurno=ttk.Entry(frameFormularioEmpleado, textvariable=turno)
        labelTurno.pack(pady=10)
        entryTurno.pack()

        contrasena=tk.StringVar()
        labelContrasena=ttk.Label(frameFormularioEmpleado, text='Contraseña:', font=('Helvetica', 12))
        entryContrasena=ttk.Entry(frameFormularioEmpleado, textvariable=contrasena)
        labelContrasena.pack(pady=10)
        entryContrasena.pack()

        botonAgregar=ttk.Button(frameFormularioEmpleado, text='Agregar', command=enviarPeticionBD)
        botonAgregar.pack(pady=10)

    # Función llamada al presionar el botón Agregar en la ventana el doctor
    def agregarDoctor(self):

        # Enviar la petición para insertar un doctor a la base de datos
        def enviarPeticionBD():
            try:
                valores=(codigo.get(), nombre.get(), direccion.get(), telefono.get(), fechaNac.get(), sexo.get(), especialidad.get(), contrasena.get())
                self.conexion.insertInto('DOCTOR', valores)
                ventanaDoctor.destroy()
                messagebox.showinfo('Éxito', 'Doctor agregado correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al agregar el doctor: {ex}')

        ventanaDoctor=tk.Toplevel()
        ventanaDoctor.title('Agregar doctor')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaDoctor, text='Ingresa los datos para el doctor:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameFormularioDoctor=ttk.Frame(ventanaDoctor)
        frameFormularioDoctor.pack(pady=10)

        codigo=tk.StringVar()
        labelCodigo=ttk.Label(frameFormularioDoctor, text='Código:', font=('Helvetica', 12))
        entryCodigo=ttk.Entry(frameFormularioDoctor, textvariable=codigo)
        labelCodigo.pack(pady=10)
        entryCodigo.pack()

        nombre=tk.StringVar()
        labelNombre=ttk.Label(frameFormularioDoctor, text='Nombre:', font=('Helvetica', 12))
        entryNombre=ttk.Entry(frameFormularioDoctor, textvariable=nombre)
        labelNombre.pack(pady=10)
        entryNombre.pack()

        direccion=tk.StringVar()
        labelDireccion=ttk.Label(frameFormularioDoctor, text='Dirección:', font=('Helvetica', 12))
        entryDireccion=ttk.Entry(frameFormularioDoctor, textvariable=direccion)
        labelDireccion.pack(pady=10)
        entryDireccion.pack()

        telefono=tk.StringVar()
        labelTeléfono=ttk.Label(frameFormularioDoctor, text='Teléfono:', font=('Helvetica', 12))
        entryTeléfono=ttk.Entry(frameFormularioDoctor, textvariable=telefono)
        labelTeléfono.pack(pady=10)
        entryTeléfono.pack()

        fechaNac=tk.StringVar()
        labelFechaNac=ttk.Label(frameFormularioDoctor, text='Fecha de nacimiento:', font=('Helvetica', 12))
        entryFechaNac=ttk.Entry(frameFormularioDoctor, textvariable=fechaNac)
        labelFechaNac.pack(pady=10)
        entryFechaNac.pack()

        sexo=tk.StringVar()
        labelSexo=ttk.Label(frameFormularioDoctor, text='Sexo:', font=('Helvetica', 12))
        entrySexo=ttk.Entry(frameFormularioDoctor, textvariable=sexo)
        labelSexo.pack(pady=10)
        entrySexo.pack()

        especialidad=tk.StringVar()
        labelSueldo=ttk.Label(frameFormularioDoctor, text='Especialidad:', font=('Helvetica', 12))
        entrySueldo=ttk.Entry(frameFormularioDoctor, textvariable=especialidad)
        labelSueldo.pack(pady=10)
        entrySueldo.pack()

        contrasena=tk.StringVar()
        labelContrasena=ttk.Label(frameFormularioDoctor, text='Contraseña:', font=('Helvetica', 12))
        entryContrasena=ttk.Entry(frameFormularioDoctor, textvariable=contrasena)
        labelContrasena.pack(pady=10)
        entryContrasena.pack()

        botonAgregar=ttk.Button(frameFormularioDoctor, text='Agregar', command=enviarPeticionBD)
        botonAgregar.pack(pady=10)

    # Función llamada al presionar el botón Agregar en la ventana paciente
    def agregarPaciente(self):

        # Enviar la petición para insertar un paciente a la base de datos
        def enviarPeticionBD():
            try:
                valores=(codigo.get(), nombre.get(), direccion.get(), telefono.get(), fechaNac.get(), sexo.get(), edad.get(), estatura.get())
                self.conexion.insertInto('PACIENTE', valores)
                ventanaPaciente.destroy()
                messagebox.showinfo('Éxito', 'Paciente agregado correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al agregar el paciente: {ex}')

        ventanaPaciente=tk.Toplevel()
        ventanaPaciente.title('Agregar paciente')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaPaciente, text='Ingresa los datos para el paciente:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameFormularioPaciente=ttk.Frame(ventanaPaciente)
        frameFormularioPaciente.pack(pady=10)

        codigo=tk.StringVar()
        labelCodigo=ttk.Label(frameFormularioPaciente, text='Código:', font=('Helvetica', 12))
        entryCodigo=ttk.Entry(frameFormularioPaciente, textvariable=codigo)
        labelCodigo.pack(pady=10)
        entryCodigo.pack()

        nombre=tk.StringVar()
        labelNombre=ttk.Label(frameFormularioPaciente, text='Nombre:', font=('Helvetica', 12))
        entryNombre=ttk.Entry(frameFormularioPaciente, textvariable=nombre)
        labelNombre.pack(pady=10)
        entryNombre.pack()

        direccion=tk.StringVar()
        labelDireccion=ttk.Label(frameFormularioPaciente, text='Dirección:', font=('Helvetica', 12))
        entryDireccion=ttk.Entry(frameFormularioPaciente, textvariable=direccion)
        labelDireccion.pack(pady=10)
        entryDireccion.pack()

        telefono=tk.StringVar()
        labelTeléfono=ttk.Label(frameFormularioPaciente, text='Teléfono:', font=('Helvetica', 12))
        entryTeléfono=ttk.Entry(frameFormularioPaciente, textvariable=telefono)
        labelTeléfono.pack(pady=10)
        entryTeléfono.pack()

        fechaNac=tk.StringVar()
        labelFechaNac=ttk.Label(frameFormularioPaciente, text='Fecha de nacimiento:', font=('Helvetica', 12))
        entryFechaNac=ttk.Entry(frameFormularioPaciente, textvariable=fechaNac)
        labelFechaNac.pack(pady=10)
        entryFechaNac.pack()

        sexo=tk.StringVar()
        labelSexo=ttk.Label(frameFormularioPaciente, text='Sexo:', font=('Helvetica', 12))
        entrySexo=ttk.Entry(frameFormularioPaciente, textvariable=sexo)
        labelSexo.pack(pady=10)
        entrySexo.pack()

        edad=tk.StringVar()
        labelSueldo=ttk.Label(frameFormularioPaciente, text='Edad:', font=('Helvetica', 12))
        entrySueldo=ttk.Entry(frameFormularioPaciente, textvariable=edad)
        labelSueldo.pack(pady=10)
        entrySueldo.pack()

        estatura=tk.StringVar()
        labelContrasena=ttk.Label(frameFormularioPaciente, text='Estatura:', font=('Helvetica', 12))
        entryContrasena=ttk.Entry(frameFormularioPaciente, textvariable=estatura)
        labelContrasena.pack(pady=10)
        entryContrasena.pack()

        botonAgregar=ttk.Button(frameFormularioPaciente, text='Agregar', command=enviarPeticionBD)
        botonAgregar.pack(pady=10)

    # Función llamada al presionar el botón Agregar en la ventana cita
    def agregarCita(self):

        # Enviar la petición para insertar una cita a la base de datos
        def enviarPeticionBD():
            try:
                valores=(codigo.get(), codigosPacientes[comboNombrePaciente.current()], codigosDoctores[comboNombreDoctor.current()], fecha.get(), hora.get())
                self.conexion.insertInto('CITA', valores)
                ventanaCita.destroy()
                messagebox.showinfo('Éxito', 'Cita agregada correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al agregar la cita: {ex}')

        def mostrarCalendario(event):
            labelFecha.pack(pady=10)
            calendario.pack()
            actualizarHoras()

        def mostrarHoras(event):
            labelHora.pack(pady=10)
            comboHora.pack()

            fechaData=datetime.strptime(fecha.get(), '%d-%m-%Y')
            if fechaData.weekday()!=5 and fechaData.weekday()!=6:
                comboHora.configure(state='normal')
                hora.set('')
                botonAgregar.pack(pady=10)
                actualizarHoras()
            else:
                comboHora.configure(state='disabled')
                hora.set('FIN DE SEMANA')
                botonAgregar.pack_forget()

        def actualizarHoras():
            horas.clear()

            horaActual=datetime.strptime('09:00', '%H:%M')
            horaFinal=datetime.strptime('20:00', '%H:%M')
            while horaActual<=horaFinal:
                horas.append(horaActual.strftime('%H:%M'))
                horaActual+=timedelta(hours=1)

            citasData=conexion.selectDataFromCita()

            for i in range(len(citasData)):
                if codigosDoctores[comboNombreDoctor.current()]==citasData[i][0] and fecha.get()==citasData[i][1]:
                    if horas.count(citasData[i][2]):
                        horas.remove(citasData[i][2])

            comboHora.configure(values=horas)

        ventanaCita=tk.Toplevel()
        ventanaCita.title('Agregar cita')

        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaCita, text='Ingresa los datos para la cita:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameFormularioCita=ttk.Frame(ventanaCita)
        frameFormularioCita.pack(pady=10)

        codigo=tk.StringVar()
        labelCodigo=ttk.Label(frameFormularioCita, text='Código:', font=('Helvetica', 12))
        entryCodigo=ttk.Entry(frameFormularioCita, textvariable=codigo)
        labelCodigo.pack(pady=10)
        entryCodigo.pack()

        pacientes=conexion.selectNameAndCodeFromTable('PACIENTE')
        codigosPacientes=[]
        nombresPacientes=[]
        for i in range(len(pacientes)):
            codigosPacientes.append(pacientes[i][0])
            nombresPacientes.append(pacientes[i][1])

        nombrePaciente=tk.StringVar()
        labelNombrePaciente=ttk.Label(frameFormularioCita, text='Nombre del paciente: ', font=('Helvetica', 12))
        comboNombrePaciente=ttk.Combobox(frameFormularioCita, textvariable=nombrePaciente)
        comboNombrePaciente.configure(values=nombresPacientes, width=30)
        labelNombrePaciente.pack(pady=10)
        comboNombrePaciente.pack()

        doctores=conexion.selectNameAndCodeFromTable('DOCTOR')
        codigosDoctores=[]
        nombresDoctores=[]
        for i in range(len(doctores)):
            codigosDoctores.append(doctores[i][0])
            nombresDoctores.append(doctores[i][1])

        nombreDoctor=tk.StringVar()
        labelNombreDoctor=ttk.Label(frameFormularioCita, text='Nombre del doctor: ', font=('Helvetica', 12))
        comboNombreDoctor=ttk.Combobox(frameFormularioCita, textvariable=nombreDoctor)
        comboNombreDoctor.configure(values=nombresDoctores, width=30)
        labelNombreDoctor.pack(pady=10)
        comboNombreDoctor.pack()
        comboNombreDoctor.bind('<<ComboboxSelected>>', mostrarCalendario)
        
        fecha=tk.StringVar()
        labelFecha=ttk.Label(frameFormularioCita, text='Fecha: ', font=('Helvetica', 12))
        calendario=tkc.DateEntry(frameFormularioCita, textvariable=fecha, selectmode='day', date_pattern='dd-mm-yyyy', day=1, month=11, year=2024)
        calendario.bind('<<DateEntrySelected>>', mostrarHoras)

        horas=[]
        hora=tk.StringVar()
        labelHora=ttk.Label(frameFormularioCita, text='Hora: ', font=('Helvetica', 12))
        comboHora=ttk.Combobox(frameFormularioCita, textvariable=hora)
        comboHora.configure(values=horas, width=30)

        botonAgregar=ttk.Button(frameFormularioCita, text='Agregar', command=enviarPeticionBD)

    # Función llamada al presionar el botón Agregar en la ventana medicamento
    def agregarMedicamento(self):
    
        # Enviar la petición para insertar un medicamento a la base de datos
        def enviarPeticionBD():
            try:
                valores=(codigo.get(), nombre.get(), viaAdm.get(), presentacion.get(), fechaCad.get())
                self.conexion.insertInto('MEDICAMENTO', valores)
                ventanaMedicamento.destroy()
                messagebox.showinfo('Éxito', 'Medicamento agregado correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al agregar el medicamento: {ex}')

        ventanaMedicamento=tk.Toplevel()
        ventanaMedicamento.title('Agregar medicamento')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaMedicamento, text='Ingresa los datos para el medicamento:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameFormularioMedicamento=ttk.Frame(ventanaMedicamento)
        frameFormularioMedicamento.pack(pady=10)

        codigo=tk.IntVar()
        labelCodigo=ttk.Label(frameFormularioMedicamento, text='Código:', font=('Helvetica', 12))
        entryCodigo=ttk.Entry(frameFormularioMedicamento, textvariable=codigo)
        labelCodigo.pack(pady=10)
        entryCodigo.pack()

        nombre=tk.StringVar()
        labelNombre=ttk.Label(frameFormularioMedicamento, text='Nombre:', font=('Helvetica', 12))
        entryNombre=ttk.Entry(frameFormularioMedicamento, textvariable=nombre)
        labelNombre.pack(pady=10)
        entryNombre.pack()

        viaAdm=tk.StringVar()
        labelViaAdm=ttk.Label(frameFormularioMedicamento, text='Via de administración:', font=('Helvetica', 12))
        entryViaAdm=ttk.Entry(frameFormularioMedicamento, textvariable=viaAdm)
        labelViaAdm.pack(pady=10)
        entryViaAdm.pack()

        presentacion=tk.StringVar()
        labelPresentacion=ttk.Label(frameFormularioMedicamento, text='Presentación:', font=('Helvetica', 12))
        entryPresentacion=ttk.Entry(frameFormularioMedicamento, textvariable=presentacion)
        labelPresentacion.pack(pady=10)
        entryPresentacion.pack()

        fechaCad=tk.StringVar()
        labelFechaCad=ttk.Label(frameFormularioMedicamento, text='Fecha de caducidad:', font=('Helvetica', 12))
        entryFechaCad=ttk.Entry(frameFormularioMedicamento, textvariable=fechaCad)
        labelFechaCad.pack(pady=10)
        entryFechaCad.pack()

        botonAgregar=ttk.Button(frameFormularioMedicamento, text='Agregar', command=enviarPeticionBD)
        botonAgregar.pack(pady=10)

    # Función llamada al presionar el menú de consulta de Empleados
    def mostrarEmpleados(self):

        # Enviar la petición para obtener todos los empleados a la base de datos
        try:
            empleados=conexion.selectAllFromTable('EMPLEADO')

            ventanaEmpleado=tk.Toplevel()
            ventanaEmpleado.title('Consulta general')

            tablaEmpleado=ttk.Treeview(ventanaEmpleado,
                columns=('codigo', 
                         'nombre', 
                         'direccion', 
                         'telefono', 
                         'fecha_nac', 
                         'sexo', 
                         'sueldo', 
                         'turno', 
                         'contrasena'), show='headings')
            tablaEmpleado.heading('codigo', text='Código')
            tablaEmpleado.column('codigo', width=60)
            tablaEmpleado.heading('nombre', text='Nombre')
            tablaEmpleado.column('nombre', width=300)
            tablaEmpleado.heading('direccion', text='Dirección')
            tablaEmpleado.heading('telefono', text='Teléfono')
            tablaEmpleado.column('telefono', width=70)
            tablaEmpleado.heading('fecha_nac', text='Fecha_Nac')
            tablaEmpleado.column('fecha_nac', width=90)
            tablaEmpleado.heading('sexo', text='Sexo')
            tablaEmpleado.column('sexo', width=90)
            tablaEmpleado.heading('sueldo', text='Sueldo')
            tablaEmpleado.column('sueldo', width=90)
            tablaEmpleado.heading('turno', text='Turno')
            tablaEmpleado.column('turno', width=90)
            tablaEmpleado.heading('contrasena', text='Contraseña')
            tablaEmpleado.column('contrasena', width=90)
            tablaEmpleado.pack()

            for empleado in range(len(empleados)):
                tablaEmpleado.insert(
                    parent='',
                    index=tk.END,
                    values=empleados[empleado])
        except Exception as ex:
            messagebox.showerror('Error', f'Error al mostrar los empleados: {ex}')

    # Función llamada al presionar el menú de consulta de Doctores
    def mostrarDoctores(self):

        # Enviar la petición para obtener todos los doctores a la base de datos
        try:
            doctores=conexion.selectAllFromTable('DOCTOR')

            ventanaDoctores=tk.Toplevel()
            ventanaDoctores.title('Consulta general')

            tablaDoctor=ttk.Treeview(
                ventanaDoctores,
                columns=('codigo', 
                         'nombre', 
                         'direccion', 
                         'telefono', 
                         'fecha_nac', 
                         'sexo', 
                         'especialidad',
                         'contrasena'),
                show='headings')
            tablaDoctor.heading('codigo', text='Código')
            tablaDoctor.column('codigo', width=60)
            tablaDoctor.heading('nombre', text='Nombre')
            tablaDoctor.column('nombre', width=300)
            tablaDoctor.heading('direccion', text='Dirección')
            tablaDoctor.heading('telefono', text='Teléfono')
            tablaDoctor.column('telefono', width=70)
            tablaDoctor.heading('fecha_nac', text='Fecha_Nac')
            tablaDoctor.column('fecha_nac', width=90)
            tablaDoctor.heading('sexo', text='Sexo')
            tablaDoctor.column('sexo', width=90)
            tablaDoctor.heading('especialidad', text='Especialidad')
            tablaDoctor.column('especialidad', width=200)
            tablaDoctor.heading('contrasena', text='Contraseña')
            tablaDoctor.column('contrasena', width=90)
            tablaDoctor.pack()

            for doctor in range(len(doctores)):
                tablaDoctor.insert(
                    parent='',
                    index=tk.END,
                    values=doctores[doctor])
        except Exception as ex:
            messagebox.showerror('Error', f'Error al mostrar los doctores: {ex}')

    # Función llamada al presionar el menú de consulta de Pacientes
    def mostrarPacientes(self):
        # Enviar la petición para obtener todos los pacientes a la base de datos
        try:
            pacientes=conexion.selectAllFromTable('PACIENTE')

            ventanaPacientes=tk.Toplevel()
            ventanaPacientes.title('Consulta general')

            tablaPaciente=ttk.Treeview(
                ventanaPacientes,
                columns=('codigo', 
                         'nombre', 
                         'direccion', 
                         'telefono', 
                         'fecha_nac', 
                         'sexo', 
                         'edad',
                         'estatura'),
                show='headings')
            tablaPaciente.heading('codigo', text='Código')
            tablaPaciente.column('codigo', width=60)
            tablaPaciente.heading('nombre', text='Nombre')
            tablaPaciente.column('nombre', width=300)
            tablaPaciente.heading('direccion', text='Dirección')
            tablaPaciente.heading('telefono', text='Teléfono')
            tablaPaciente.column('telefono', width=70)
            tablaPaciente.heading('fecha_nac', text='Fecha_Nac')
            tablaPaciente.column('fecha_nac', width=90)
            tablaPaciente.heading('sexo', text='Sexo')
            tablaPaciente.column('sexo', width=90)
            tablaPaciente.heading('edad', text='Edad')
            tablaPaciente.column('edad', width=60)
            tablaPaciente.heading('estatura', text='Estatura')
            tablaPaciente.column('estatura', width=60)
            tablaPaciente.pack()

            for paciente in range(len(pacientes)):
                tablaPaciente.insert(
                    parent='',
                    index=tk.END,
                    values=pacientes[paciente])
        except Exception as ex:
            messagebox.showerror('Error', f'Error al mostrar los pacientes: {ex}')

    # Función llamada al presionar el menú de consulta de Medicamentos
    def mostrarMedicamentos(self):
        # Enviar la petición para obtener todos los Medicamentos a la base de datos
        try:
            medicamentos=conexion.selectAllFromTable('MEDICAMENTO')

            ventanaMedicamento=tk.Toplevel()
            ventanaMedicamento.title('Consulta general')

            tablaPaciente=ttk.Treeview(
                ventanaMedicamento,
                columns=('codigo', 
                         'nombre', 
                         'via_adm', 
                         'presentacion', 
                         'fecha_cad'),
                show='headings')
            tablaPaciente.heading('codigo', text='Código')
            tablaPaciente.column('codigo', width=60)
            tablaPaciente.heading('nombre', text='Nombre')
            tablaPaciente.column('nombre', width=300)
            tablaPaciente.heading('via_adm', text='Via_adm')
            tablaPaciente.heading('presentacion', text='Presentacion')
            tablaPaciente.heading('fecha_cad', text='Fecha_cad')
            tablaPaciente.column('fecha_cad', width=90)
            tablaPaciente.pack()

            for medicamento in range(len(medicamentos)):
                tablaPaciente.insert(
                    parent='',
                    index=tk.END,
                    values=medicamentos[medicamento])
        except Exception as ex:
            messagebox.showerror('Error', f'Error al mostrar los medicamentos: {ex}')

    # Función llamada al presionar el menú de modificación de Citas
    def modificarCita(self):

        # Enviar la petición para modificar una cita de la base de datos
        def enviarPeticionBD():
            try:
                atributos=f'"Código"={codigo.get()}, "CódigoPaciente"={codigosPacientes[comboNombrePaciente.current()]}, "CódigoDoctor"={codigosDoctores[comboNombreDoctor.current()]}, "Fecha"='+f"'{fecha.get()}', "+'"Hora"='+f"'{hora.get()}'"
                condicion=f'"Código"={codigoActual.get()}'
                self.conexion.updateSetWhere('CITA', atributos, condicion)
                ventanaCita.destroy()
                messagebox.showinfo('Éxito', 'Cita modificada correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al modificar la cita: {ex}')

        def mostrarCalendario(event):
            labelFecha.pack(pady=10)
            calendario.pack()
            actualizarHoras()

        def mostrarHoras(event):
            labelHora.pack(pady=10)
            comboHora.pack()

            fechaData=datetime.strptime(fecha.get(), '%d-%m-%Y')
            if fechaData.weekday()!=5 and fechaData.weekday()!=6:
                comboHora.configure(state='normal')
                hora.set('')
                botonModificar.pack(pady=10)
                actualizarHoras()
            else:
                comboHora.configure(state='disabled')
                hora.set('FIN DE SEMANA')
                botonModificar.pack_forget()

        def actualizarHoras():
            horas.clear()

            horaActual=datetime.strptime('09:00', '%H:%M')
            horaFinal=datetime.strptime('20:00', '%H:%M')
            while horaActual<=horaFinal:
                horas.append(horaActual.strftime('%H:%M'))
                horaActual+=timedelta(hours=1)

            citasData=conexion.selectDataFromCita()

            for i in range(len(citasData)):
                if codigosDoctores[comboNombreDoctor.current()]==citasData[i][0] and fecha.get()==citasData[i][1]:
                    if horas.count(citasData[i][2]):
                        horas.remove(citasData[i][2])

            comboHora.configure(values=horas)

        def mostrarDatosActuales(event):
            labelCodigoActual.pack_forget()
            comboCodigoActual.pack_forget()

            datosActuales='Los datos actuales de la cita son:\n'
            datosActuales+='Código: '+codigoActual.get()+'\n'
            datosActuales+='Código paciente: '+str(citas[comboCodigoActual.current()][1])+'\n'
            datosActuales+='Código doctor: '+str(citas[comboCodigoActual.current()][2])+'\n'
            datosActuales+='Fecha: '+citas[comboCodigoActual.current()][3].strftime('%d-%m-%Y')+'\n'
            datosActuales+='Hora: '+citas[comboCodigoActual.current()][4].strftime('%H:%M')
            labelDatosActuales.configure(text=datosActuales)
            labelDatosActuales.pack(pady=10)
            mostrarFormulario()

        def mostrarFormulario():
            labelCodigo.pack(pady=10)
            entryCodigo.pack()

            labelNombrePaciente.pack(pady=10)
            comboNombrePaciente.pack()

            labelNombreDoctor.pack(pady=10)
            comboNombreDoctor.pack()

        ventanaCita=tk.Toplevel()
        ventanaCita.title('Modificar cita')

        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaCita, text='Ingresa los datos para la cita a modificar:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameFormularioCita=ttk.Frame(ventanaCita)
        frameFormularioCita.pack(pady=10)

        codigos=[]
        citas=conexion.selectAllFromTable('CITA')
        for i in range(len(citas)):
            codigos.append(citas[i][0])

        codigoActual=tk.StringVar()
        labelCodigoActual=ttk.Label(frameFormularioCita, text='Código actual:', font=('Helvetica', 12))
        comboCodigoActual=ttk.Combobox(frameFormularioCita, textvariable=codigoActual, values=codigos)
        labelCodigoActual.pack(pady=10)
        comboCodigoActual.pack()
        comboCodigoActual.bind('<<ComboboxSelected>>', mostrarDatosActuales)

        labelDatosActuales=ttk.Label(frameFormularioCita, text='', font=('Helvetica', 12))
    
        codigo=tk.StringVar()
        labelCodigo=ttk.Label(frameFormularioCita, text='Código:', font=('Helvetica', 12))
        entryCodigo=ttk.Entry(frameFormularioCita, textvariable=codigo)

        pacientes=conexion.selectNameAndCodeFromTable('PACIENTE')
        codigosPacientes=[]
        nombresPacientes=[]
        for i in range(len(pacientes)):
            codigosPacientes.append(pacientes[i][0])
            nombresPacientes.append(pacientes[i][1])

        nombrePaciente=tk.StringVar()
        labelNombrePaciente=ttk.Label(frameFormularioCita, text='Nombre del paciente: ', font=('Helvetica', 12))
        comboNombrePaciente=ttk.Combobox(frameFormularioCita, textvariable=nombrePaciente)
        comboNombrePaciente.configure(values=nombresPacientes, width=30)

        doctores=conexion.selectNameAndCodeFromTable('DOCTOR')
        codigosDoctores=[]
        nombresDoctores=[]
        for i in range(len(doctores)):
            codigosDoctores.append(doctores[i][0])
            nombresDoctores.append(doctores[i][1])

        nombreDoctor=tk.StringVar()
        labelNombreDoctor=ttk.Label(frameFormularioCita, text='Nombre del doctor: ', font=('Helvetica', 12))
        comboNombreDoctor=ttk.Combobox(frameFormularioCita, textvariable=nombreDoctor)
        comboNombreDoctor.configure(values=nombresDoctores, width=30)
        comboNombreDoctor.bind('<<ComboboxSelected>>', mostrarCalendario)
        
        fecha=tk.StringVar()
        labelFecha=ttk.Label(frameFormularioCita, text='Fecha: ', font=('Helvetica', 12))
        calendario=tkc.DateEntry(frameFormularioCita, textvariable=fecha, selectmode='day', date_pattern='dd-mm-yyyy', day=1, month=11, year=2024)
        calendario.bind('<<DateEntrySelected>>', mostrarHoras)

        horas=[]
        hora=tk.StringVar()
        labelHora=ttk.Label(frameFormularioCita, text='Hora: ', font=('Helvetica', 12))
        comboHora=ttk.Combobox(frameFormularioCita, textvariable=hora)
        comboHora.configure(values=horas, width=30)

        botonModificar=ttk.Button(frameFormularioCita, text='Modificar', command=enviarPeticionBD)

    # Función llamada al presionar el menú de mostrar información del Paciente
    def mostrarInformacionPaciente(self):
        # Enviar la petición para mostrar la información del empleado
        def enviarPeticionBD():
            try:
                atributos=f'"Código"={codigo.get()}, "CódigoPaciente"={codigosPacientes[comboNombrePaciente.current()]}, "CódigoDoctor"={codigosDoctores[comboNombreDoctor.current()]}, "Fecha"='+f"'{fecha.get()}', "+'"Hora"='+f"'{hora.get()}'"
                condicion=f'"Código"={codigoActual.get()}'
                self.conexion.updateSetWhere('CITA', atributos, condicion)
                ventanaCita.destroy()
                messagebox.showinfo('Éxito', 'Cita modificada correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al modificar la cita: {ex}')

        def mostrarDatos(event):
            datosPaciente=self.conexion.selectAllFromTableWhereName('PACIENTE', nombrePaciente.get())[0]
            data='Los datos del paciente son:\n'
            data+='Código: '+str(datosPaciente[0])+'\n'
            data+='Nombre: '+datosPaciente[1]+'\n'
            data+='Dirección '+datosPaciente[2]+'\n'
            data+='Teléfono: '+datosPaciente[3]+'\n'
            data+='Fecha de nacimiento: '+datosPaciente[4].strftime('%d-%m-%Y')+'\n'
            data+='Sexo: '+datosPaciente[5]+'\n'
            data+='Edad: '+str(datosPaciente[6])+'\n'
            data+='Estatura: '+str(datosPaciente[7])
            labelDatosPaciente.configure(text=data)
            labelDatosPaciente.pack(pady=10)

        ventanaPaciente=tk.Toplevel()
        ventanaPaciente.title('Mostrar informacion paciente')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaPaciente, text='Ver informacion del paciente:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameInformacionPaciente=ttk.Frame(ventanaPaciente)
        frameInformacionPaciente.pack(pady=10)

        nombresPacientes=[]
        pacientes=self.conexion.selectAllFromTable('PACIENTE');
        for i in range(len(pacientes)):
            nombresPacientes.append(pacientes[i][1])

        nombrePaciente=tk.StringVar()
        labelNombrePaciente=ttk.Label(frameInformacionPaciente, text='Nombre del paciente: ', font=('Helvetica', 12))
        comboNombrePaciente=ttk.Combobox(frameInformacionPaciente, textvariable=nombrePaciente)
        comboNombrePaciente.configure(values=nombresPacientes, width=30)
        comboNombrePaciente.pack()
        comboNombrePaciente.bind('<<ComboboxSelected>>', mostrarDatos)

        labelDatosPaciente=ttk.Label(frameInformacionPaciente, text="", font=('Helvetica', 12))

    # Función llamada al presionar el menú de consulta de Citas por día
    def verCitaDia(self):

        def mostrarCitas(event):
            citasDia=self.conexion.selectAllFromTableWhereDateAndCode('CITA', datetime.strptime(fecha.get(), '%d-%m-%Y'), self.conexion.obtenerCodigoUsuario())
            labelDatosCita.pack(pady=10)
            data=''
            if len(citasDia):
                for i in range(len(citasDia)):
                    data+="Código paciente: "+str(citasDia[i][1])+" | Hora: "+citasDia[i][4].strftime('%H:%M')+'\n'
                labelDatosCita.configure(text=data)
            else:
                labelDatosCita.configure(text='El día de hoy no hay citas') 

        ventanaCita=tk.Toplevel()
        ventanaCita.title('Mostrar citas del día')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaCita, text='Citas del día:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameCitasDia=ttk.Frame(ventanaCita)
        frameCitasDia.pack(pady=10)

        labelFecha=ttk.Label(frameCitasDia, text='Selecciona una fecha: ', font=('Helvetica', 12))
        labelFecha.pack(pady=10)

        fecha=tk.StringVar()
        labelFecha=ttk.Label(frameCitasDia, text='Fecha: ', font=('Helvetica', 12))
        calendario=tkc.DateEntry(frameCitasDia, textvariable=fecha, selectmode='day', date_pattern='dd-mm-yyyy', day=1, month=11, year=2024)
        calendario.bind('<<DateEntrySelected>>', mostrarCitas)
        calendario.pack(pady=10)
        
        labelDatosCita=ttk.Label(frameCitasDia, text="", font=('Helvetica', 12))       

    # Función llamada al presionar el menú de consulta de Citas por semana
    def verCitasSemana(self):
        ventanaCita=tk.Toplevel()
        ventanaCita.title('Mostrar citas de la semana')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaCita, text='Citas de la semana:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)
        
        frameCitasSemana=ttk.Frame(ventanaCita)
        frameCitasSemana.pack(pady=10)

        hoy=datetime.now()
        inicioSemana=hoy-timedelta(days=hoy.weekday())
        finSemana=inicioSemana+timedelta(days=6)

        citasSemana=self.conexion.selectAllFromCitaWhereDateBetweenAndCode(inicioSemana.strftime('%d-%m-%Y'), finSemana.strftime('%d-%m-%Y'), self.conexion.obtenerCodigoUsuario())
        
        labelDatosCita=ttk.Label(frameCitasSemana, text="", font=('Helvetica', 12))
        labelDatosCita.pack()

        if len(citasSemana):
            data=""
            for i in range(len(citasSemana)):
                data+="Código paciente: "+str(citasSemana[i][1])+" | Fecha: "+citasSemana[i][3].strftime('%d-%m-%Y')+" | Hora: "+citasSemana[i][4].strftime('%H:%M')+'\n'
            labelDatosCita.configure(text=data)
        else:
            labelDatosCita.configure(text='No hay citas esta semana')

    # Función llamada al presionar el menú de consulta de Citas por mes
    def verCitasMes(self):    
        ventanaCita=tk.Toplevel()
        ventanaCita.title('Mostrar citas del mes')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaCita, text='Citas del mes:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameCitasMes=ttk.Frame(ventanaCita)
        frameCitasMes.pack(pady=10)

        hoy=datetime.now()
        inicioMes=hoy.replace(day=1)

        if hoy.month==12:
            finMes=hoy.replace(year=hoy.year+1, month=1, day=1)-timedelta(days=1)
        else:
            finMes=hoy.replace(month=hoy.month+1, day=1)-timedelta(days=1)

        citasMes=self.conexion.selectAllFromCitaWhereDateBetweenAndCode(inicioMes.strftime('%d-%m-%Y'), finMes.strftime('%d-%m-%Y'), self.conexion.obtenerCodigoUsuario())

        labelDatosCita=ttk.Label(frameCitasMes, text="", font=('Helvetica', 12))
        labelDatosCita.pack()

        if len(citasMes):
            data=""
            for i in range(len(citasMes)):
                data+="Código paciente: "+str(citasMes[i][1])+" | Fecha: "+citasMes[i][3].strftime('%d-%m-%Y')+" | Hora: "+citasMes[i][4].strftime('%H:%M')+'\n'
            labelDatosCita.configure(text=data)
        else:
            labelDatosCita.configure(text='No hay citas este mes')

    # Función llamada al presionar el menú de Generar diagnóstico
    def generarDiagnostico(self):
        def mostrarDatosCita(event):
            global cita, datosPaciente;

            labelCodigoCita.pack_forget()
            comboCodigoCita.pack_forget()

            cita=citas[comboCodigoCita.current()]
            datosPaciente=self.conexion.selectAllFromTableWhereCode('PACIENTE', cita[1])

            data='Fecha de la consulta: '+cita[3].strftime('%d-%m-%Y')+' | Hora: '+cita[4].strftime('%H:%M')+'\n'
            data+='Nombre del paciente: '+datosPaciente[0][1]+'\n'
            labelDatosCita.configure(text=data)
            labelDatosCita.pack(pady=10)

            labelCodigo.pack(pady=10)
            entryCodigo.pack(pady=10)

            labelDiagnostico.pack(pady=10)
            entryDiagnostico.pack(pady=10)

            labelMedicamento.pack(pady=10)
            comboMedicamento.pack(pady=10)

            labelAtendido.pack(pady=10)
            comboAtendido.pack(pady=10)    

            botonGenerarDiagnostico.pack(pady=10)
            botonGenerarReceta.pack(pady=10)

        def generarDiagnostico():
            try:
                valores=(codigo.get(), cita[0], diagnostico.get(), medicamentos[comboMedicamento.current()][0], atendido.get())
                self.conexion.insertInto('CONSULTA', valores)
                ventanaDiagnostico.destroy()
                messagebox.showinfo('Éxito', 'Diagnóstico generado correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al generar el diagnóstico: {ex}')

        def generarReceta():
            try:
                # Dimensiones del archivo
                ancho, alto = letter
                # Generar archivo
                nombreArchivo='receta.pdf'
                pdf=canvas.Canvas(nombreArchivo, pagesize=letter)
                # Título
                pdf.setFont('Helvetica-Bold', 18)
                pdf.drawString(100, 750, 'Receta médica')
                # Logo
                pdf.drawImage('images/salud1.png', 392, 592, width=180, height=180)
                # Información del paciente
                infoPaciente='Información del paciente'+'\n'
                infoPaciente+='Código: '+str(datosPaciente[0][0])+'\n'
                infoPaciente+='Nombre: '+datosPaciente[0][1]+'\n'
                infoPaciente+='Dirección: '+datosPaciente[0][2]+'\n'
                infoPaciente+='Teléfono: '+datosPaciente[0][3]+'\n'
                infoPaciente+='Fecha de nacimiento: '+datosPaciente[0][4].strftime("%d-%m-%Y")+'\n'
                infoPaciente+='Sexo: '+datosPaciente[0][5]+'\n'
                infoPaciente+='Edad: '+str(datosPaciente[0][6])+'\n'
                infoPaciente+='Estatura: '+str(datosPaciente[0][7])+'\n'
                pdf.setFont('Helvetica', 12)
                text = pdf.beginText(100, alto - 100)
                text.setLeading(15)
                text.textLines(infoPaciente.strip())
                pdf.drawText(text)
                # Medicamento
                pdf.drawString(100, 372, 'Medicamento: '+nombresMedicamentos[comboMedicamento.current()])
                # Doctor
                pdf.drawString(100, 345, 'Doctor: '+self.conexion.obtenerNombreUsuario())
                pdf.save()
                messagebox.showinfo('Éxito', 'Receta generada correctamente.')
            except Exception as ex:
                messagebox.showerror('Error', f'Error al generar la receta: {ex}')

        ventanaDiagnostico=tk.Toplevel()
        ventanaDiagnostico.title('Generar diagnóstico')
        
        # Elementos de la ventana
        labelTitulo=ttk.Label(ventanaDiagnostico, text='Realizar diagnóstico:', font=('Helvetica', 16))
        labelTitulo.pack(padx=10, pady=10)

        frameDiagnostico=ttk.Frame(ventanaDiagnostico)
        frameDiagnostico.pack(pady=10)

        codigosCitas=[]
        citas=self.conexion.selectAllFromTableWhereDoctorCode('CITA', self.conexion.obtenerCodigoUsuario());
        for i in range(len(citas)):
            codigosCitas.append(citas[i][0])

        labelCodigoCita=ttk.Label(frameDiagnostico, text='Seleccione una cita: ', font=('Helvetica', 12))
        labelCodigoCita.pack(pady=10)
        codigoCita=tk.StringVar()
        comboCodigoCita=ttk.Combobox(frameDiagnostico, textvariable=codigoCita)
        comboCodigoCita.configure(values=codigosCitas, width=30)
        comboCodigoCita.pack()
        comboCodigoCita.bind('<<ComboboxSelected>>', mostrarDatosCita)

        labelDatosCita=ttk.Label(frameDiagnostico, text='Código:', font=('Helvetica', 12))

        labelCodigo=ttk.Label(frameDiagnostico, text='Ingresa el código de la consulta: ', font=('Helvetica', 12))
        codigo=tk.IntVar()
        entryCodigo=ttk.Entry(frameDiagnostico, textvariable=codigo)

        labelDiagnostico=ttk.Label(frameDiagnostico, text='Ingresa el diagnóstico: ', font=('Helvetica', 12))
        diagnostico=tk.StringVar()
        entryDiagnostico=ttk.Entry(frameDiagnostico, textvariable=diagnostico)

        medicamentos=self.conexion.selectAllFromTable('MEDICAMENTO')
        nombresMedicamentos=[]
        for medicamento in range(len(medicamentos)):
            nombresMedicamentos.append(medicamentos[medicamento][1])

        labelMedicamento=ttk.Label(frameDiagnostico, text='Seleccione un medicamento: ', font=('Helvetica', 12))
        medicamento=tk.StringVar()
        comboMedicamento=ttk.Combobox(frameDiagnostico, textvariable=medicamento)
        comboMedicamento.configure(values=nombresMedicamentos, width=30)
        comboMedicamento.bind('<<ComboboxSelected>>', mostrarDatosCita)

        opcionesAtendido=['Sí', 'No']
        labelAtendido=ttk.Label(frameDiagnostico, text='¿El paciente fue atendido?', font=('Helvetica', 12))
        atendido=tk.StringVar()
        comboAtendido=ttk.Combobox(frameDiagnostico, textvariable=atendido)
        comboAtendido.configure(values=opcionesAtendido)

        botonGenerarDiagnostico=ttk.Button(frameDiagnostico, text='Generar diagnóstico', command=generarDiagnostico)
        botonGenerarReceta=ttk.Button(frameDiagnostico, text='Generar receta', command=generarReceta)

# Flujo inicial del programa
# Si el nombre de la función en ejecución es __main__, se ejecuta el programa.
if __name__=='__main__':
    # Conexión con la base de datos
    try:
        conexion=dataBase.Conexion()
    except Exception as ex:
        messagebox.showerror('Error', f'Error de conexión con la base de datos: {ex}')

    # Configuración inicial de la aplicación
    root=tk.Tk()
    app=VentanaLogin(root, conexion)
    root.mainloop()