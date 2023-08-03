import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Tabla Clientes
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Clientes'")
        if self.cursor.fetchone() is None:
            self.conn.execute('''CREATE TABLE Clientes (
            ClienteID INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Direccion TEXT,
            Telefono TEXT
        )''')

        # Tabla Mascotas
        # agregar la edad de la mascota para saber cuando se tiene que vacunar y si puede vacunarse
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Mascotas'")
        if self.cursor.fetchone() is None:
            self.conn.execute(''' CREATE TABLE Mascotas (
            MascotaID INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Tipo TEXT NOT NULL,
            Edad INTEGER,
            PuedeVacunarse BOOLEAN NOT NULL,
            fechaVacunacion TEXT,
            ClienteID INTEGER,
            FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID))''')

        # Tabla Vacunas
        # se podria agregar dosis necesarias y fecha de vacunacion para saber cuando se tiene que vacunar
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Vacunas'")
        if self.cursor.fetchone() is None:
            self.conn.execute(''' CREATE TABLE Vacunas (
            VacunaID INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            CantDosis INTEGER,
            Descripcion TEXT)''')

        # Tabla VacunasMascotas
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='VacunasMascotas'")
        if self.cursor.fetchone() is None:
            self.conn.execute(''' CREATE TABLE VacunasMascotas(
            MascotaID INTEGER,
            VacunaID  INTEGER,
            FechaVacunacion TEXT,
            PRIMARY KEY(MascotaID, VacunaID),
            FOREIGN KEY(MascotaID) REFERENCES Mascotas(MascotaID),
            FOREIGN KEY(VacunaID) REFERENCES Vacunas(VacunaID))''')

        # Tabla Turnos que contiene la fecha y hora del turno con el nombre del cliente, nombre de su mascota y tipo
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Turnos'")
        if self.cursor.fetchone() is None:
            self.conn.execute(''' CREATE TABLE Turnos(
            TurnoID INTEGER PRIMARY KEY,
            Fecha DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            Hora TEXT NOT NULL,
            NombreCliente TEXT NOT NULL,
            MailCliente TEXT NOT NULL,
            NombreMascota TEXT NOT NULL,
            TipoMascota TEXT NOT NULL,
            MotivoConsulta TEXT NOT NULL,
            EdadMascota INTEGER,
            PesoMascota INTEGER,
            SexoMascota TEXT NOT NULL)''')

        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_turno(self, Fecha, Hora, NombreCliente, MailCliente, NombreMascota, TipoMascota, MotivoConsulta,
                     EdadMascota, PesoMascota, SexoMascota):
        self.cursor.execute('''INSERT INTO Turnos (Fecha, Hora, NombreCliente, MailCliente, NombreMascota, 
        TipoMascota, MotivoConsulta, EdadMascota, PesoMascota, SexoMascota) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                            (Fecha, Hora, NombreCliente, MailCliente, NombreMascota, TipoMascota, MotivoConsulta,
                             EdadMascota, PesoMascota, SexoMascota))
        self.conn.commit()

    def consulta_turnos(self):
        self.cursor.execute('''SELECT * FROM Turnos''')
        turnos = self.cursor.fetchall()
        return turnos

    # obtener usuario por turnoId
    def obtener_usuario(self, TurnoID):
        self.cursor.execute('''SELECT * FROM Turnos WHERE TurnoID = ?''', (TurnoID,))
        usuario = self.cursor.fetchone()
        return usuario

    def modificar_turno(self, TurnoID, Fecha, Hora, NombreCliente, MailCliente, NombreMascota, TipoMascota,
                        MotivoConsulta,
                        EdadMascota, PesoMascota, SexoMascota):
        self.cursor.execute('''UPDATE Turnos SET Fecha = ?, Hora = ?, NombreCliente = ?, MailCliente = ?, NombreMascota = ?, 
        TipoMascota = ?, MotivoConsulta = ?, EdadMascota = ?, PesoMascota = ?, SexoMascota = ? WHERE TurnoID = ?''',
                            (Fecha, Hora, NombreCliente, MailCliente, NombreMascota, TipoMascota, MotivoConsulta,
                             EdadMascota, PesoMascota, SexoMascota, TurnoID))
        self.conn.commit()

    def eliminar_turno(self, TurnoID):
        self.cursor.execute('''DELETE FROM Turnos WHERE TurnoID = ?''', (TurnoID,))
        self.conn.commit()
