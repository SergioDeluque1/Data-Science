from tkinter import *
from tkinter import ttk
import mysql.connector 
from tkinter import messagebox

class Ventana(Frame):    
    def __init__(self, master):
        super().__init__(master, width=880, height=650)
        self.master = master
        self.db_config = {
            'host': '',
            'user': '',
            'password': '',
            'database': ''
        }
        self.conn = None  # Conexión persistente
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            messagebox.showinfo("Conexión Exitosa", "Conexión exitosa a la base de datos.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", 
                               f"Error al conectar a la base de datos: {str(err)}\n"
                               f"Por favor verifica tus credenciales:\n"
                               f"Host: {self.db_config['host']}\n"
                               f"Usuario: {self.db_config['user']}\n"
                               f"Base de datos: {self.db_config['database']}")
        self.pack()
        self.create_frames()
        self.show_welcome()
        
    def test_connection(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            conn.close()
            messagebox.showinfo("Conexión Exitosa", "Conexión exitosa a la base de datos.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", 
                               f"Error al conectar a la base de datos: {str(err)}\n"
                               f"Por favor verifica tus credenciales:\n"
                               f"Host: {self.db_config['host']}\n"
                               f"Usuario: {self.db_config['user']}\n"
                               f"Base de datos: {self.db_config['database']}")

    def create_frames(self):
        # Frame de bienvenida
        self.frame_welcome = Frame(self, bg="#117ba5", width=880, height=650)
        self.lbl_bienvenido = Label(self.frame_welcome, text="Bienvenido", font=("Arial", 28), bg="#117ba5", fg="white")
        self.lbl_bienvenido.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.btn_cliente = Button(self.frame_welcome, text="Cliente", width=15, height=2, command=self.show_busqueda)
        self.btn_cliente.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.btn_inventario = Button(self.frame_welcome, text="Inventario", width=15, height=2, command=self.show_inventario)
        self.btn_inventario.place(relx=0.6, rely=0.5, anchor=CENTER)

        # Frame principal
        self.frame_main = Frame(self, bg="#d3dde3", width=880, height=650)
        self.lbl_empresa = Label(self.frame_main, text="video-games", font=("Arial", 22, "bold"), bg="#d3dde3", fg="#117ba5")
        self.lbl_empresa.place(x=0, y=10, width=880)
        
        # Botones laterales
        self.btn_cliente_main = Button(self.frame_main, text="Cliente", width=15, height=2, command=self.show_busqueda)
        self.btn_cliente_main.place(x=10, y=70)
        self.btn_inventario_main = Button(self.frame_main, text="Inventario", width=15, height=2, command=self.show_inventario)
        self.btn_inventario_main.place(x=10, y=130)
        
        # Frame CRUD
        self.frame_crud = Frame(self.frame_main, bg="#d3dde3")
        self.frame_crud.place(x=200, y=60, width=500, height=50)
        
        # Botones CRUD SOLO Inserción y Búsqueda debajo de 'video-games'
        self.btn_insercion = Button(self.frame_crud, text="Inserción", width=12, command=self.mostrar_formulario_cliente)
        self.btn_insercion.pack(side=LEFT, padx=5)
        self.btn_busqueda = Button(self.frame_crud, text="Búsqueda", width=12, command=self.mostrar_busqueda)
        self.btn_busqueda.pack(side=LEFT, padx=5)
        # Los botones de borrado y edición ya no se crean aquí

        # Frame contenido
        self.frame_contenido = Frame(self.frame_main, bg="#f5f5f5", width=600, height=500, relief=RIDGE, borderwidth=2)
        self.frame_contenido.place(x=200, y=120, width=650, height=500)

        # Treeview para mostrar usuarios
        self.tree = ttk.Treeview(self.frame_contenido, columns=("ID", "Nombre", "Email", "Dirección", "Teléfonos"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Teléfonos", text="Teléfonos")
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=150)
        self.tree.column("Email", width=150)
        self.tree.column("Dirección", width=150)
        self.tree.column("Teléfonos", width=150)
        self.tree.place(x=20, y=60, width=600, height=400)

    def show_welcome(self):
        self.frame_main.place_forget()
        self.frame_welcome.place(x=0, y=0, width=880, height=650)

    def show_cliente(self):
        self.frame_welcome.place_forget()
        self.frame_main.place(x=0, y=0, width=880, height=650)
        self.clear_contenido()
        self.mostrar_busqueda()

    def show_busqueda(self):
        self.frame_welcome.place_forget()
        self.frame_main.place(x=0, y=0, width=880, height=650)
        self.clear_contenido()
        # Restaurar botones CRUD de cliente
        for widget in self.frame_crud.winfo_children():
            widget.destroy()
        self.btn_insercion = Button(self.frame_crud, text="Inserción", width=12, command=self.mostrar_formulario_cliente)
        self.btn_insercion.pack(side=LEFT, padx=5)
        self.btn_busqueda = Button(self.frame_crud, text="Búsqueda", width=12, command=self.mostrar_busqueda)
        self.btn_busqueda.pack(side=LEFT, padx=5)
        self.mostrar_busqueda()

    def show_inventario(self):
        self.frame_welcome.place_forget()
        self.frame_main.place(x=0, y=0, width=880, height=650)
        self.clear_contenido()
        # Cambiar botones CRUD a los de inventario
        for widget in self.frame_crud.winfo_children():
            widget.destroy()
        self.btn_insercion_inventario = Button(self.frame_crud, text="Inserción", width=12, command=self.mostrar_formulario_inventario)
        self.btn_insercion_inventario.pack(side=LEFT, padx=5)
        self.btn_busqueda_inventario = Button(self.frame_crud, text="Búsqueda", width=12, command=self.mostrar_busqueda_inventario)
        self.btn_busqueda_inventario.pack(side=LEFT, padx=5)
        self.mostrar_busqueda_inventario()

    def clear_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()    
            

    def mostrar_formulario_cliente(self):
        self.clear_contenido()
        # Título
        lbl = Label(self.frame_contenido, text="Formulario Cliente", font=("Arial", 16), bg="#f5f5f5")
        lbl.place(x=20, y=10)
        
        # Campos
        Label(self.frame_contenido, text="Nombre:", bg="#f5f5f5").place(x=20, y=60)
        self.entry_nombre = Entry(self.frame_contenido, width=40)
        self.entry_nombre.place(x=120, y=60)
        
        Label(self.frame_contenido, text="Correo Electrónico:", bg="#f5f5f5").place(x=20, y=100)
        self.entry_correo = Entry(self.frame_contenido, width=40)
        self.entry_correo.place(x=120, y=100)
        
        Label(self.frame_contenido, text="Teléfono:", bg="#f5f5f5").place(x=20, y=140)
        self.entry_telefono = Entry(self.frame_contenido, width=40)
        self.entry_telefono.place(x=120, y=140)
        
        # Descuento (derivado, siempre 0)
        Label(self.frame_contenido, text="Descuento:", bg="#f5f5f5").place(x=20, y=180)
        self.lbl_descuento = Label(self.frame_contenido, text="0", bg="#f5f5f5")
        self.lbl_descuento.place(x=120, y=180)
        
        # Botón Guardar
        self.btn_guardar_cliente = Button(self.frame_contenido, text="Guardar", bg="green", fg="white", width=12, command=self.guardar_cliente)
        self.btn_guardar_cliente.place(x=500, y=400)

    def guardar_cliente(self):
        # Obtener los valores del formulario
        nombre = self.entry_nombre.get().strip()
        email = self.entry_correo.get().strip()
        telefono = self.entry_telefono.get().strip()

        # Validación de campos obligatorios
        if not nombre or not email:
            messagebox.showerror("Error", "Los campos nombre y email son obligatorios")
            return

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            conn.start_transaction()

            # Insertar en tabla usuario
            cursor.execute("""
                INSERT INTO usuario (idUsuario, Nombre, Email)
                VALUES (NULL, %s, %s)
            """, (nombre, email))
            id_usuario = cursor.lastrowid

            # Insertar en tabla cliente
            cursor.execute("""
                INSERT INTO cliente (idCliente, idUsuario, disc)
                VALUES (NULL, %s, 0)
            """, (id_usuario,))
            id_cliente = cursor.lastrowid

            # Insertar teléfono si se proporcionó
            if telefono:
                cursor.execute("""
                    INSERT INTO telefono_cliente (idCliente, Tel)
                    VALUES (%s, %s)
                """, (id_cliente, telefono))

            conn.commit()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")

            # Limpiar formulario
            self.entry_nombre.delete(0, END)
            self.entry_correo.delete(0, END)
            self.entry_telefono.delete(0, END)

            # Actualizar lista de usuarios si el widget aún existe
            try:
                if hasattr(self, 'tree') and self.tree.winfo_exists():
                    self.buscar_usuarios()
            except TclError:
                pass

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Error al guardar cliente: {str(err)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mostrar_busqueda(self):
        # Limpiar el frame de contenido
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        # Barra de búsqueda
        Label(self.frame_contenido, text="Buscar:", bg="#f5f5f5").place(x=20, y=10)
        self.entry_busqueda = Entry(self.frame_contenido, width=40)
        self.entry_busqueda.place(x=80, y=10)
        self.btn_buscar = Button(self.frame_contenido, text="Buscar", command=self.buscar_usuarios)
        self.btn_buscar.place(x=400, y=7)
        
        # Crear tabla
        self.tree = ttk.Treeview(self.frame_contenido, columns=("ID", "Nombre", "Email", "Teléfonos"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Teléfonos", text="Teléfonos")
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Teléfonos", width=200)
        self.tree.place(x=20, y=50, width=750, height=370)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_contenido, orient=VERTICAL, command=self.tree.yview)
        scrollbar.place(x=770, y=50, height=370)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Botones de edición y borrado en la parte inferior izquierda
        self.btn_editar = Button(self.frame_contenido, text="Editar", width=12, command=self.iniciar_edicion)
        self.btn_editar.place(x=20, y=440)
        self.btn_borrado = Button(self.frame_contenido, text="Borrado", width=12, command=self.borrar_cliente)
        self.btn_borrado.place(x=150, y=440)
        
        # Mostrar todos al cargar
        self.buscar_usuarios(mostrar_todos=True)

    def buscar_usuarios(self, mostrar_todos=False):
        texto = self.entry_busqueda.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            if mostrar_todos or not texto:
                consulta = '''
                    SELECT c.idCliente, u.Nombre, u.Email, GROUP_CONCAT(IFNULL(t.Tel, '')) as telefonos
                    FROM cliente c
                    JOIN usuario u ON c.idUsuario = u.idUsuario
                    LEFT JOIN telefono_cliente t ON c.idCliente = t.idCliente
                    GROUP BY c.idCliente, u.Nombre, u.Email
                '''
                cursor.execute(consulta)
            else:
                like = f"%{texto}%"
                consulta = '''
                    SELECT c.idCliente, u.Nombre, u.Email, GROUP_CONCAT(IFNULL(t.Tel, '')) as telefonos
                    FROM cliente c
                    JOIN usuario u ON c.idUsuario = u.idUsuario
                    LEFT JOIN telefono_cliente t ON c.idCliente = t.idCliente
                    WHERE c.idCliente LIKE %s OR u.Nombre LIKE %s OR u.Email LIKE %s OR t.Tel LIKE %s
                    GROUP BY c.idCliente, u.Nombre, u.Email
                '''
                cursor.execute(consulta, (like, like, like, like))
            for row in cursor.fetchall():
                row_list = list(row)
                row_list[3] = row_list[3] if row_list[3] else ""
                self.tree.insert("", "end", values=row_list)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al buscar usuarios: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mostrar_todos_usuarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            consulta = '''
                SELECT c.idCliente, u.Nombre, u.Email, GROUP_CONCAT(IFNULL(t.Tel, '')) as telefonos
                FROM cliente c
                JOIN usuario u ON c.idUsuario = u.idUsuario
                LEFT JOIN telefono_cliente t ON c.idCliente = t.idCliente
                GROUP BY c.idCliente, u.Nombre, u.Email
            '''
            cursor.execute(consulta)
            for row in cursor.fetchall():
                row_list = list(row)
                row_list[3] = row_list[3] if row_list[3] else ""
                self.tree.insert("", "end", values=row_list)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al mostrar usuarios: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mostrar_formulario_inventario(self):
        self.clear_contenido()
        # Título
        lbl = Label(self.frame_contenido, text="Formulario Inventario", font=("Arial", 16), bg="#f5f5f5")
        lbl.place(x=20, y=10)
        # Campos
        Label(self.frame_contenido, text="Nombre del Producto:", bg="#f5f5f5").place(x=20, y=60)
        self.entry_nombre_juego = Entry(self.frame_contenido, width=40)
        self.entry_nombre_juego.place(x=180, y=60)
        Label(self.frame_contenido, text="Categoría:", bg="#f5f5f5").place(x=20, y=100)
        self.entry_categoria = Entry(self.frame_contenido, width=40)
        self.entry_categoria.place(x=180, y=100)
        Label(self.frame_contenido, text="Precio:", bg="#f5f5f5").place(x=20, y=140)
        self.entry_precio = Entry(self.frame_contenido, width=20)
        self.entry_precio.place(x=180, y=140)
        Label(self.frame_contenido, text="Cantidad:", bg="#f5f5f5").place(x=20, y=180)
        self.entry_cantidad = Entry(self.frame_contenido, width=20)
        self.entry_cantidad.place(x=180, y=180)
        # Botón Guardar
        self.btn_guardar_inventario = Button(self.frame_contenido, text="Guardar", bg="green", fg="white", width=12, command=self.guardar_inventario)
        self.btn_guardar_inventario.place(x=500, y=400)

    def guardar_inventario(self):
        # Obtener valores del formulario
        nombre = self.entry_nombre_juego.get().strip()
        categoria = self.entry_categoria.get().strip()
        precio = self.entry_precio.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        
        # Validación de campos
        if not all([nombre, categoria, precio, cantidad]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            precio = float(precio)
            cantidad = int(cantidad)
            if precio < 0 or cantidad < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número positivo y la cantidad un número entero positivo")
            return
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            # Insertar en producto
            cursor.execute("""
                INSERT INTO producto (Nombre, categoria, precio)
                VALUES (%s, %s, %s)
            """, (nombre, categoria, precio))
            id_producto = cursor.lastrowid
            # Insertar en inventario
            cursor.execute("""
                INSERT INTO inventario (idProducto, Cantidad)
                VALUES (%s, %s)
            """, (id_producto, cantidad))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado al inventario correctamente")
            # Limpiar formulario
            self.entry_nombre_juego.delete(0, END)
            self.entry_categoria.delete(0, END)
            self.entry_precio.delete(0, END)
            self.entry_cantidad.delete(0, END)
            # Actualizar lista si el widget aún existe
            try:
                if hasattr(self, 'tree_inventario') and self.tree_inventario.winfo_exists():
                    self.buscar_inventario(mostrar_todos=True)
            except:
                pass
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Error al guardar en inventario: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def borrar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para borrar.")
            return

        item = seleccion[0]
        datos = self.tree.item(item, 'values')
        id_cliente = datos[0]
        nombre = datos[1]

        respuesta = messagebox.askyesno("Confirmar borrado", f"¿Deseas borrar al cliente '{nombre}' (ID: {id_cliente})?")
        if not respuesta:
            return

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Llamar al procedimiento almacenado que elimina balance y cliente
            cursor.callproc("eliminar_cliente", (id_cliente,))

            conn.commit()
            messagebox.showinfo("Éxito", "Cliente borrado correctamente")
            self.buscar_usuarios()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al borrar cliente: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def iniciar_edicion(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un cliente para editar.")
            return

        # Ocultar botones de editar y borrar
        self.btn_editar.place_forget()
        self.btn_borrado.place_forget()

        # Mostrar botones de guardar y cancelar
        self.btn_cancelar = Button(self.frame_contenido, text="Cancelar", width=12, command=self.cancelar_edicion)
        self.btn_guardar = Button(self.frame_contenido, text="Guardar", width=12, bg="green", fg="white", command=self.guardar_edicion)
        self.btn_cancelar.place(x=20, y=440)
        self.btn_guardar.place(x=150, y=440)

        # Obtener datos del cliente seleccionado
        item = seleccion[0]
        valores = self.tree.item(item)['values']
        
        # Crear entries para edición
        self.entries_edicion = {}
        campos = [("Nombre", valores[1]), ("Email", valores[2]), ("Teléfonos", valores[3] if valores[3] else "")]
        y_pos = 50
        
        for campo, valor in campos:
            Label(self.frame_contenido, text=f"{campo}:", bg="#f5f5f5").place(x=400, y=y_pos)
            entry = Entry(self.frame_contenido, width=30)
            entry.insert(0, valor)
            entry.place(x=470, y=y_pos)
            self.entries_edicion[campo.lower()] = entry
            y_pos += 30
            
        # Guardar el ID del cliente que se está editando
        self.cliente_editando_id = valores[0]

    def cancelar_edicion(self):
        # Eliminar entries de edición
        for entry in self.entries_edicion.values():
            entry.destroy()
            
        # Eliminar labels de edición
        for widget in self.frame_contenido.winfo_children():
            if isinstance(widget, Label) and widget.cget("text").endswith(":"):
                widget.destroy()
        
        self.entries_edicion = {}
        
        # Restaurar botones originales
        self.btn_guardar.destroy()
        self.btn_cancelar.destroy()
        self.btn_editar.place(x=20, y=440)
        self.btn_borrado.place(x=150, y=440)    
    def guardar_edicion(self):
        # Validar que ningún campo esté vacío
        for campo, entry in self.entries_edicion.items():
            if not entry.get().strip():
                messagebox.showerror("Error", f"El campo {campo} no puede estar vacío")
                return

        nombre = self.entries_edicion['nombre'].get().strip()
        email = self.entries_edicion['email'].get().strip()
        telefono = self.entries_edicion['teléfonos'].get().strip()

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(buffered=True)

            # Verificar si el email ya existe para otro usuario
            cursor.execute("""
                SELECT u.idUsuario 
                FROM usuario u
                JOIN cliente c ON u.idUsuario = c.idUsuario
                WHERE u.Email = %s AND c.idCliente != %s
            """, (email, self.cliente_editando_id))
            
            existe_email = cursor.fetchone()
            if existe_email:
                messagebox.showerror("Error", "Ya existe otro usuario con ese correo electrónico")
                return

            # Actualizar usuario
            cursor.execute("""
                UPDATE usuario u
                JOIN cliente c ON u.idUsuario = c.idUsuario
                SET u.Nombre = %s, u.Email = %s
                WHERE c.idCliente = %s
            """, (nombre, email, self.cliente_editando_id))

            # Actualizar teléfono
            cursor.execute("DELETE FROM telefono_cliente WHERE idCliente = %s", (self.cliente_editando_id,))
            if telefono:
                cursor.execute("""
                    INSERT INTO telefono_cliente (idCliente, Tel)
                    VALUES (%s, %s)
                """, (self.cliente_editando_id, telefono))

            conn.commit()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            
            # Actualizar la vista y restaurar botones
            self.buscar_usuarios()
            self.cancelar_edicion()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(err)}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def mostrar_busqueda_inventario(self):
        self.clear_contenido()
        Label(self.frame_contenido, text="Buscar:", bg="#f5f5f5").place(x=20, y=10)
        self.entry_busqueda_inventario = Entry(self.frame_contenido, width=40)
        self.entry_busqueda_inventario.place(x=80, y=10)
        self.btn_buscar_inventario = Button(self.frame_contenido, text="Buscar", command=self.buscar_inventario)
        self.btn_buscar_inventario.place(x=400, y=7)
        # Crear tabla de inventario
        self.tree_inventario = ttk.Treeview(self.frame_contenido, columns=("ID", "Nombre", "Categoría", "Precio", "Cantidad"), show="headings")
        self.tree_inventario.heading("ID", text="ID Inventario")
        self.tree_inventario.heading("Nombre", text="Nombre")
        self.tree_inventario.heading("Categoría", text="Categoría")
        self.tree_inventario.heading("Precio", text="Precio")
        self.tree_inventario.heading("Cantidad", text="Cantidad")
        self.tree_inventario.column("ID", width=80)
        self.tree_inventario.column("Nombre", width=200)
        self.tree_inventario.column("Categoría", width=120)
        self.tree_inventario.column("Precio", width=100)
        self.tree_inventario.column("Cantidad", width=100)
        self.tree_inventario.place(x=20, y=50, width=700, height=370)
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_contenido, orient=VERTICAL, command=self.tree_inventario.yview)
        scrollbar.place(x=720, y=50, height=370)
        self.tree_inventario.configure(yscrollcommand=scrollbar.set)
        # Botones Editar y Borrar
        self.btn_editar_inventario = Button(self.frame_contenido, text="Editar", width=12, command=self.iniciar_edicion_inventario)
        self.btn_editar_inventario.place(x=20, y=440)
        self.btn_borrar_inventario = Button(self.frame_contenido, text="Borrar", width=12, command=self.borrar_inventario)
        self.btn_borrar_inventario.place(x=150, y=440)
        self.buscar_inventario(mostrar_todos=True)

    def buscar_inventario(self, mostrar_todos=False):
        texto = self.entry_busqueda_inventario.get().strip()
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            if mostrar_todos or not texto:
                consulta = '''
                    SELECT i.idInventario, p.Nombre, p.categoria, p.precio, i.Cantidad
                    FROM inventario i
                    JOIN producto p ON i.idProducto = p.idProducto
                '''
                cursor.execute(consulta)
            else:
                like = f"%{texto}%"
                consulta = '''
                    SELECT i.idInventario, p.Nombre, p.categoria, p.precio, i.Cantidad
                    FROM inventario i
                    JOIN producto p ON i.idProducto = p.idProducto
                    WHERE p.Nombre LIKE %s OR p.categoria LIKE %s
                '''
                cursor.execute(consulta, (like, like))
            for row in cursor.fetchall():
                self.tree_inventario.insert("", "end", values=list(row))
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al buscar inventario: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def borrar_inventario(self):
        seleccion = self.tree_inventario.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un producto para borrar.")
            return
        item = seleccion[0]
        datos = self.tree_inventario.item(item, 'values')
        id_inventario = datos[0]
        nombre = datos[1]
        respuesta = messagebox.askyesno("Confirmar borrado", f"¿Deseas borrar el producto '{nombre}' (ID: {id_inventario})?")
        if not respuesta:
            return
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.callproc("eliminar_inventario", (id_inventario,))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            self.buscar_inventario(mostrar_todos=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al borrar producto: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def iniciar_edicion_inventario(self):
        seleccion = self.tree_inventario.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para editar.")
            return
        self.btn_editar_inventario.place_forget()
        if hasattr(self, 'btn_borrar_inventario'):
            self.btn_borrar_inventario.place_forget()
        self.btn_cancelar_inventario = Button(self.frame_contenido, text="Cancelar", width=12, command=self.cancelar_edicion_inventario)
        self.btn_guardar_inventario_edit = Button(self.frame_contenido, text="Guardar", width=12, bg="green", fg="white", command=self.guardar_edicion_inventario)
        self.btn_cancelar_inventario.place(x=20, y=440)
        self.btn_guardar_inventario_edit.place(x=150, y=440)
        item = seleccion[0]
        valores = self.tree_inventario.item(item)['values']
        self.entries_edicion_inventario = {}
        campos = [("Nombre", valores[1]), ("Categoría", valores[2]), ("Precio", valores[3]), ("Cantidad", valores[4])]
        y_pos = 50
        for campo, valor in campos:
            Label(self.frame_contenido, text=f"{campo}:", bg="#f5f5f5").place(x=400, y=y_pos)
            entry = Entry(self.frame_contenido, width=30)
            entry.insert(0, valor)
            entry.place(x=500, y=y_pos)
            self.entries_edicion_inventario[campo.lower()] = entry
            y_pos += 30
        self.inventario_editando_id = int(valores[0])
        # Obtener idProducto para edición
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT idProducto FROM inventario WHERE idInventario = %s", (self.inventario_editando_id,))
            res = cursor.fetchone()
            if res and (isinstance(res, tuple) or isinstance(res, list)):
                try:
                    self.producto_editando_id = int(str(res[0]))
                except Exception:
                    self.producto_editando_id = None
            else:
                self.producto_editando_id = None
        except:
            self.producto_editando_id = None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def cancelar_edicion_inventario(self):
        for entry in self.entries_edicion_inventario.values():
            entry.destroy()
        for widget in self.frame_contenido.winfo_children():
            if isinstance(widget, Label) and widget.cget("text").endswith(":"):
                widget.destroy()
        self.entries_edicion_inventario = {}
        self.btn_guardar_inventario_edit.destroy()
        self.btn_cancelar_inventario.destroy()
        self.btn_editar_inventario.place(x=20, y=440)
        self.btn_borrar_inventario.place(x=150, y=440)

    def guardar_edicion_inventario(self):
        # Validar que ningún campo esté vacío
        for campo, entry in self.entries_edicion_inventario.items():
            if not entry.get().strip():
                messagebox.showerror("Error", f"El campo {campo} no puede estar vacío")
                return
        nombre = self.entries_edicion_inventario['nombre'].get().strip()
        categoria = self.entries_edicion_inventario['categoría'].get().strip()
        precio = self.entries_edicion_inventario['precio'].get().strip()
        cantidad = self.entries_edicion_inventario['cantidad'].get().strip()
        try:
            precio = float(precio)
            cantidad = int(cantidad)
            if precio < 0 or cantidad < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número positivo y la cantidad un número entero positivo")
            return
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            # Actualizar producto
            cursor.execute("""
                UPDATE producto SET Nombre=%s, categoria=%s, precio=%s WHERE idProducto=%s
            """, (nombre, categoria, precio, self.producto_editando_id))
            # Actualizar inventario
            cursor.execute("""
                UPDATE inventario SET Cantidad=%s WHERE idInventario=%s
            """, (cantidad, self.inventario_editando_id))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.buscar_inventario(mostrar_todos=True)
            self.cancelar_edicion_inventario()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Error al actualizar producto: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



