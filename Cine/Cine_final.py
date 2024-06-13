import tkinter as tk
from tkinter import Label, Button
from PIL import ImageTk, Image
import random

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Cine")
ventana.state('zoomed')  # Maximiza la ventana
ventana.config(bg="#0f1115")  # azulmarino

# Variables globales para el tamaño de la cuadrícula y los asientos
ROWS, COLS = 7, 7
asientos_ocupados = set()
asientos_seleccionados = []

# Función para limpiar los widgets anteriores
def vaciar_ventana(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

# Función para manejar el evento de clic en un botón
def cambiar_color(btn):
    if btn["bg"] == "#318ce7":
        btn.config(bg="#fbb018")  # amarillo
    else:
        btn.config(bg="#318ce7")

# Función para mostrar el mejor asiento disponible
def mejor_asiento(asientos):
    fila_media = ROWS // 2
    columna_media = COLS // 2

    # Buscar el primer asiento disponible comenzando desde el centro y expandiéndose hacia afuera
    for i in range(max(ROWS, COLS)):
        if (fila_media + i) < ROWS and asientos[fila_media + i][columna_media] != 'O':
            asiento_disponible = f"{chr(65 + fila_media + i)}{columna_media + 1}"
            break
        elif (fila_media - i) >= 0 and asientos[fila_media - i][columna_media] != 'O':
            asiento_disponible = f"{chr(65 + fila_media - i)}{columna_media + 1}"
            break
        elif (columna_media + i) < COLS and asientos[fila_media][columna_media + i] != 'O':
            asiento_disponible = f"{chr(65 + fila_media)}{columna_media + 1 + i}"
            break
        elif (columna_media - i) >= 0 and asientos[fila_media][columna_media - i] != 'O':
            asiento_disponible = f"{chr(65 + fila_media)}{columna_media + 1 - i}"
            break
    else:
        # Si no se encuentra ningún asiento disponible, mostrar un mensaje
        asiento_disponible = "No hay asientos disponibles"

    m_asiento = Label(ventana, bg="#0f1115", fg="#fbb018", text=f"Mejor asiento disponible: {asiento_disponible}", font=("Arial", 16))
    m_asiento.grid(row=ROWS + 2, column=1, columnspan=COLS , pady=10, sticky="nsew")

# Función para crear la cuadrícula de botones de asientos
def crear_asientos(ventana, asientos):
    def agregar_asiento(btn):
        if btn not in asientos_seleccionados:
            asientos_seleccionados.append(btn)
        cambiar_color(btn)

    def guardar_asientos(asientos_seleccionados):
        for btn in asientos_seleccionados:
            btn.config(bg="red", state="disabled")
            # Obtener la posición del botón en la cuadrícula
            fila, columna = btn.grid_info()["row"] - 1, btn.grid_info()["column"] - 1
            # Agregar la posición a los asientos ocupados
            asientos_ocupados.add((fila, columna))

        # Limpiar la lista de asientos seleccionados después de guardarlos
        asientos_seleccionados.clear()

    N = 65  # Código ASCII para 'A'
    for j in range(ROWS + 1):  # Se agrega una fila más para la pantalla
        if j == 0:
            # Etiquetas de la columna superior
            for b in range(COLS + 1):
                if b == 0:
                    # Esquina superior izquierda vacía
                    columnas = Label(ventana, text="", font=("Arial", 12), bg="#0f1115", fg="white")
                else:
                    columnas = Label(ventana, text=str(b), font=("Arial", 12), bg="#0f1115", fg="white")
                columnas.grid(row=j, column=b, padx=2, pady=2, sticky="nsew")
        else:
            L = chr(N)  # Convierte código ASCII a carácter
            columnas = Label(ventana, text=L, font=("Arial", 12), bg="#0f1115", fg="white")
            columnas.grid(row=j, column=0, padx=2, pady=2, sticky="nsew")
            N += 1
            for b in range(COLS):
                btn = Button(ventana, bg="#318ce7", fg="white", text=f"{L}{b + 1}", font=("Arial", 10))
                btn.grid(row=j, column=b + 1, padx=2, pady=2, sticky="nsew")
                if asientos[j - 1][b] == 'O':
                    btn.config(bg="red", state="disabled")
                btn.config(command=lambda current_btn=btn: agregar_asiento(current_btn))

    # Ajustar las proporciones de las columnas y filas para que se expandan con el tamaño de la ventana
    for i in range(ROWS + 2):
        ventana.grid_rowconfigure(i, weight=1)
    for i in range(COLS + 2):
        ventana.grid_columnconfigure(i, weight=1)
    
    # Agregar el botón para guardar los asientos seleccionados
    boton_guardar = Button(ventana, text="Guardar Asientos", font=("Arial", 16), bg="#fbb018", fg="black", command=lambda: guardar_asientos(asientos_seleccionados))
    boton_guardar.grid(row=ROWS + 3, column=1, columnspan=COLS , pady=10, sticky="nsew")

    # Agregar el rectángulo de la pantalla
    pantalla_label = Label(ventana, text="PANTALLA", font=("Arial", 16), bg="black", fg="white")
    pantalla_label.grid(row=ROWS+1 , column=1, columnspan=COLS, pady=10, sticky="nsew")

    # Botón para volver
    boton_volver = Button(ventana, text="Volver", font=("Arial", 16), bg="#fbb018", fg="black", command=pagina_principal)
    boton_volver.grid(row=ROWS + 4, column=1, columnspan=COLS , pady=10, sticky="nsew")

# Función para mostrar la cuadrícula de asientos
def botones(ventana, asientos):
    vaciar_ventana(ventana)
    crear_asientos(ventana, asientos)

# Función que muestra la cuadrícula en la misma ventana
def asientos_disponibles():
    asientos = sala()
    botones(ventana, asientos)
    mejor_asiento(asientos)

# Función para mostrar las salas disponibles y películas
def pagina_principal():
    vaciar_ventana(ventana)

    salas = [
        ("Deadpool & Wolverine", "#fbb018"),
        ("Venom: The Last Dance", "#fbb018"),
        ("Jurassic Park", "#fbb018")
    ]

    # Imagenes
    portada = ["deadpool-lobezno-poster-65cc8e2963707.jpg",
               "venom.jpg",
               "park.jpg"
               ]

    # Lista para mantener referencias de las imágenes
    imagenes_tk = []

    # Redimensionar las imágenes y agregar los elementos
    for i, (texto, color) in enumerate(salas):
        # Crear y posicionar el título de la sala
        sala_label = Label(ventana, text=texto, font=("Arial", 20), bg="#0f1115", fg="white")
        sala_label.grid(row=0, column=i, padx=40, pady=10)  # Ajustar padding horizontal

        # Cargar y redimensionar la imagen correspondiente
        imagen = Image.open(portada[i])
        imagen = imagen.resize((250, 375), Image.LANCZOS)  # Redimensionar la imagen
        imagen_tk = ImageTk.PhotoImage(imagen)
        imagenes_tk.append(imagen_tk)  # Mantener la referencia

        # Crear y posicionar la imagen
        label_imagen = tk.Label(ventana, image=imagen_tk)
        label_imagen.image = imagen_tk  # Asociar la imagen con el widget para evitar que sea recolectada por el recolector de basura
        label_imagen.grid(row=1, column=i, padx=40, pady=10)  # Ajustar padding horizontal

        # Crear y posicionar el botón correspondiente
        sala_boton = Button(ventana, bg=color, fg="black", text="Ver Funciones disponibles", font=("Arial", 20), command=funciones)
        sala_boton.grid(row=2, column=i, padx=40, pady=10)  # Ajustar padding horizontal

# Función para mostrar las funciones
def funciones():
    vaciar_ventana(ventana)

    peliculas = [
        ("Pelicula 1 hora: 14:30", "#fbb018"),
        ("Pelicula 2 hora: 16:00", "#fbb018"),
        ("Pelicula 3 hora: 18:00", "#fbb018")
    ]

    for i, (texto, color) in enumerate(peliculas):
        pelicula_label = Label(ventana, text=texto, font=("Arial", 20), bg="#0f1115", fg="white")
        pelicula_label.place(relx=0.1, rely=0.1 + i * 0.2)
        pelicula_boton = Button(ventana, bg=color, fg="black", text="Ingresar", font=("Arial", 20), command=asientos_disponibles)
        pelicula_boton.place(relx=0.5, rely=0.1 + i * 0.2)
    boton_volver = Button(ventana, text="Volver", font=("Arial", 20), bg="#fbb018", fg="black", command=pagina_principal)
    boton_volver.place(relx=0.45, rely=0.7)

# Función para mostrar la matriz de asientos
def sala():
    asientos = []
    N_Filas = ROWS
    N_Columnas = COLS
    for _ in range(N_Filas):
        fila = ["D"] * N_Columnas
        asientos.append(fila)
    # Verificar si hay asientos ocupados almacenados globalmente
    global asientos_ocupados
    if not asientos_ocupados:
        # Marcar asientos ocupados aleatoriamente si no hay asientos ocupados almacenados
        for _ in range(random.randint(5, 15)):
            fila = random.randint(0, N_Filas - 1)
            columna = random.randint(0, N_Columnas - 1)
            asientos[fila][columna] = 'O'
            asientos_ocupados.add((fila, columna))
    else:
        # Marcar los asientos ocupados almacenados globalmente
        for fila, columna in asientos_ocupados:
            asientos[fila][columna] = 'O'

    return asientos

# Mostrar la pantalla principal al iniciara
pagina_principal()

ventana.mainloop()

