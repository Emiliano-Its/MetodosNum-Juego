import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import random
import math
import os
from metodos import MetodosCalculo
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
class DesactivacionTotal:
    def __init__(self, root):
        self.tolerancia = 0.0001  
        self.tiempo_limite = 0
        self.tiempo_restante = 0
        self.temporizador_activo = False
        self.lbl_tiempo = None
        self.temporizador_id = None  
        self.animacion_id = None
        self.root = root
        self.metodos_por_tema = {
            "Interpolación": ["Interpolación lineal", "Lagrange", "Newton hacia adelante", "Newton hacia atrás", "Newton con diferencias divididas"],
            "Ecuaciones No Lineales": ["Bisección","Falsa posición","Newton Raphson","Punto fijo","Secante"],
            "Ecuaciones Lineales": ["Montante","Gauss-Jordan","Eliminación Gaussiana","Gauss-Seidel","Jacobi"],
            "Mínimos Cuadrados": ["Línea recta","Cuadrática y Cúbica","Lineal y Cuadrática con función"],
            "Integración": ["Regla trapezoidal","Regla de un tercio Simpson","Regla de tres octavos Simpson","Newton-Cotes cerradas y abiertas", "Newton-Cotes tablas"],
            "Ecuaciones Diferenciales Ordinarias (EDO)": ["Euler Modificado","Runge-Kutta de 2° orden","Runge-Kutta de 3° orden","Runge-Kutta de 4° orden por un tercio Simpson ","Runge-Kutta de 4° orden por tres octavos Simpson","Runge-Kutta de orden superior"]
        }
        self.metodos_desactivacion = []
        for tema, lista in self.metodos_por_tema.items():
            if tema != "Interpolación":
                self.metodos_desactivacion.extend(lista)
        metodos_fase1_puros = self.metodos_por_tema["Interpolación"].copy()
        if "Interpolación lineal" in metodos_fase1_puros:
            metodos_fase1_puros.remove("Interpolación lineal") 
        self.metodos_interpolacion = metodos_fase1_puros 
        # Aseguramos que 'Interpolación lineal' esté en la lista de Desactivación si no lo estaba
        if "Interpolación lineal" not in self.metodos_desactivacion:
            self.metodos_desactivacion.append("Interpolación lineal") 
        self.metodos_seleccionados_interpolacion = self.metodos_interpolacion.copy()
        self.metodos_seleccionados_desactivacion = self.metodos_desactivacion.copy()
        self.metodos_calculo = MetodosCalculo()
        self.root.title("💣 Desactivacíon Total - INTERPOLACIÓN DE BOMBAS")
        self.root.state("zoomed")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)
        # Configuración de colores
        self.colors = {
            'dark_bg': '#1a1a2e',
            'medium_bg': '#16213e',
            'light_bg': '#0f3460',
            'accent_red': '#e94560',
            'accent_green': '#2ecc71',
            'accent_yellow': '#f39c12',
            'accent_blue': '#3498db',
            'text_white': '#ffffff',
            'text_gray': '#bdc3c7'
        }
        # Métodos de interpolación disponibles
        self.metodos_interpolacion = [
            "Newton hacia adelante",
            "Newton hacia atrás", 
            "Newton con diferencias divididas",
            "Lagrange"
        ]
        # Métodos de desactivación disponibles
        self.metodos_desactivacion = [
            "Interpolación lineal",
            "Montante",
            "Gauss-Jordan",
            "Eliminación Gaussiana",
            "Gauss-Seidel",
            "Jacobi",
            "Bisectriz",
            "Falsa Posición",
            "Punto Fijo",
            "Newton-Raphson",
            "Secante",
            "Euler modificado",
            "Runge-Kutta de 2° orden",
            "Runge-Kutta de 3° orden",
            "Runge-Kutta 4° orden 1/3 Simpson",
            "Runge-Kutta 4° orden 3/8 Simpson",
            "Runge-Kutta de orden superior",
            "Linea Recta (Minimos cuadrados)",
            "Lineal con funcion(MC)",
            "Cuadratica con funcion(MC)",
            "Cuadratica(MC)",
            "Cubica(MC)",
            "Regla Trapezoidal",
            "Regla de 1/3 Simpson",
            "Regla de 3/8 Simpson",
            "Newton-Cotes Cerradas",
            "Newton-Cotes Abiertas"
        ]
        # Métodos de integración disponibles
        self.metodos_integracion = [
            "Regla Trapezoidal",
            "Regla de 1/3 Simpson",
            "Regla de 3/8 Simpson",
            "Newton-Cotes Cerradas",
            "Newton-Cotes Abiertas"
        ]
        # Tablas de constantes para Newton-Cotes
        self.constantes_newton_cotes_cerradas = {
            1: {"alpha": 1/2, "coef": [1, 1]},
            2: {"alpha": 1/3, "coef": [1, 4, 1]},
            3: {"alpha": 3/8, "coef": [1, 3, 3, 1]},
            4: {"alpha": 2/45, "coef": [7, 32, 12, 32, 7]},
            5: {"alpha": 5/288, "coef": [19, 75, 50, 50, 75, 19]},
            6: {"alpha": 1/140, "coef": [41, 216, 27, 272, 27, 216, 41]},
            7: {"alpha": 7/17280, "coef": [751, 3577, 1323, 2989, 2989, 1323, 3577, 751]},
            8: {"alpha": 14/14175, "coef": [989, 5888, -928, 10946, -4540, 10946, -928, 5888, 989]},
            9: {"alpha": 9/89600, "coef": [2857, 15741, 1080, 19344, 5788, 5788, 19344, 1080, 15741, 2857]},
            10: {"alpha": 5/299376, "coef": [16067, 106300, -48525, 272400, -260550, 427368, -260550, 272400, -48525, 106300, 16067]}
        }
        self.constantes_newton_cotes_abiertas = {
            1: {"alpha": 3/2, "coef": [0, 1, 1, 0]},
            2: {"alpha": 4/3, "coef": [0, 2, -1, 2, 0]},
            3: {"alpha": 5/24, "coef": [0, 11, 1, 1, 11, 0]},
            4: {"alpha": 6/20, "coef": [0, 11, -14, 26, -14, 11, 0]},
            5: {"alpha": 7/1440, "coef": [0, 611, -453, 562, 562, -453, 611, 0]},
            6: {"alpha": 8/945, "coef": [0, 460, -954, 2196, -2459, 2196, -954, 460, 0]}
        }
        # Estado del juego
        self.nivel_actual = 1
        self.vidas = 3
        self.puntos = 0
        self.metodo_actual = None
        self.fase_actual = "interpolacion"
        self.mostrar_problema_integracion = False
        # Datos del problema actual
        self.puntos_detonados = []
        self.bombas_ocultas = []  # Lista de tuplas (x, y_real)
        self.x_objetivo = []      # Valores X que el usuario debe encontrar
        self.funcion_real = None
        self.respuestas_correctas = {}
        # Datos para la fase de desactivación
        self.problemas_desactivacion = []
        self.respuestas_desactivacion = []
        self.metodos_desactivacion_asignados = []
        self.problema_actual_desactivacion = 0
        # Datos para problemas de integración
        self.problema_integracion_actual = None
        self.respuesta_integracion_correcta = None
        self.metodo_integracion_actual = None
        # Instancia de métodos de cálculo
        self.metodos_calculo = MetodosCalculo()
        # Mostrar menú principal al iniciar
        self.crear_menu_principal()
    def normalizar(self, texto):
        return texto.lower()\
            .replace("°", "")\
            .replace("á", "a")\
            .replace("é", "e")\
            .replace("í", "i")\
            .replace("ó", "o")\
            .replace("ú", "u")\
            .replace("ñ", "n")\
            .replace("(", "")\
            .replace(")", "")\
            .replace(".", "")\
            .replace("-", "_")\
            .replace(" ", "_")
    def limpiar_interfaz(self):
        """Elimina todos los widgets de la ventana principal y detiene temporizadores/animaciones.
        Esta función se usa cada vez que cambiamos de 'pantalla' (menú principal,
        selección de nivel, fase de interpolación, fase de desactivación, etc.).
        """
        # Detener temporizador principal si está activo
        if hasattr(self, 'temporizador_id') and self.temporizador_id:
            try:
                self.root.after_cancel(self.temporizador_id)
            except Exception:
                pass
            self.temporizador_id = None
        # Detener animaciones de títulos u otros efectos
        if hasattr(self, 'animacion_id') and self.animacion_id:
            try:
                self.root.after_cancel(self.animacion_id)
            except Exception:
                pass
            self.animacion_id = None
        # Resetear bandera de temporizador
        if hasattr(self, 'temporizador_activo'):
            self.temporizador_activo = False
        # Limpiar referencia de etiqueta de tiempo
        if hasattr(self, 'lbl_tiempo'):
            self.lbl_tiempo = None
        # Destruir todos los widgets de la ventana raíz
        for widget in self.root.winfo_children():
            try:
                widget.destroy()
            except Exception:
                # En caso de que algún widget ya esté destruido
                pass
    # =========================
    # MENÚ PRINCIPAL Y NIVELES
    # =========================
    def crear_menu_principal(self):
        """Muestra un menú principal profesional estilo 'desactivación de minas'."""
        self.limpiar_interfaz()
        self.fase_actual = "menu"
        # ===== Fondo táctico con radar =====
        try:
            bg = tk.PhotoImage(file="assets/fondo.png")
            bg_label = tk.Label(self.root, image=bg)
            bg_label.image = bg
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except:        
            self.root.configure(bg="#0a0f0a")
        # ===== Panel central tipo pantalla holográfica =====
        panel = tk.Frame(
            self.root,
            bg="#0f1f0f",  # verde militar oscuro
            bd=3,
            relief="ridge",
            highlightbackground="#2ecc71",
            highlightthickness=2)
        panel.place(relx=0.5, rely=0.5, anchor="center", width=950, height=720)
        # ===== Logo de minas (dos iconos side-by-side) =====
        logo_frame = tk.Frame(panel, bg="#0f1f0f")
        logo_frame.pack(pady=5)
        def cargar_icono(ruta, size):
            img = Image.open(ruta)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        try:
            # Icono 1: mina normal
            icon1 = cargar_icono("assets/icono_mina.png", (110, 110))
            lbl1 = tk.Label(logo_frame, image=icon1, bg="#0f1f0f")
            lbl1.image = icon1
            lbl1.pack(side="left", padx=8)  # poco espacio entre iconos
            # Icono 2: mina pixel art (más grande)
            icon2 = cargar_icono("assets/mina.png", (110, 110))
            lbl2 = tk.Label(logo_frame, image=icon2, bg="#0f1f0f")
            lbl2.image = icon2
            lbl2.pack(side="left", padx=8)
        except Exception as e:
            print("Error cargando iconos:", e)
            tk.Label(logo_frame, text="💣 💣", font=("Arial", 40), bg="#0f1f0f", fg="#2ecc71").pack()
        # ===== Título principal con estilo digital =====
        titulo = tk.Label(
            panel,
            text="Desactivacíon Total",
            font=("Consolas", 36, "bold"),
            fg="#145a32",  # glow oscuro
            bg="#0f1f0f"
            )
        titulo.pack()
        # Animación leve estilo terminal
        def animar(i=0):
            colores = ["#2ecc71", "#25a65a", "#1e8c4e"]
            titulo.config(fg=colores[i])
            self.animacion_id = self.root.after(180, lambda: animar((i + 1) % 3))
        animar()
        # ===== Subtítulo =====
        tk.Label(
            panel,
            text="Localiza minas ocultas y desactívalas usando métodos numéricos.",
            font=("Consolas", 15, "bold"),
            fg="#a8e6a1",
            bg="#0f1f0f").pack(pady=(0, 12))
        # ===== Cuadro descriptivo =====
        descripcion_frame = tk.Frame(panel, bg="#a8e6a1", bd=2, relief="solid")
        descripcion_frame.pack(pady=5, padx=40, fill="x")
        desc = (
            "• Fase 1: Escanea el campo minado e identifica la posición exacta de cada mina\n"
            "  usando interpolación (Newton, Lagrange).\n"
            "• Fase 2: Desactiva minas resolviendo problemas numéricos:\n"
            "  bisección, falsa posición, Newton-Raphson, métodos de Gauss,\n"
            "  Jacobi, Gauss-Seidel, Montante, interpolación lineal e integración, etc.")
        tk.Label(
            descripcion_frame,
            text=desc,
            font=("Consolas", 13, "bold"),
            fg="#020202",
            justify="left",
            bg="#a8e6a1"
            ).pack(padx=10, pady=10)
        # ===== Botones estilo terminal militar =====
        botones_frame = tk.Frame(panel, bg="#0f1f0f")
        botones_frame.pack(pady=20)
        def crear_boton(texto, color_base, color_hover, comando):
            btn = tk.Button(
                botones_frame,
                text=texto,
                font=("Consolas", 14, "bold"),
                fg="black",
                bg=color_base,
                activebackground=color_base,
                activeforeground="black",
                relief="flat",
                padx=30,
                pady=12,
                command=comando
            ) 
            btn.pack(fill="x", pady=8)
            # Hover personalizado para cada botón
            def on_enter(e):
                btn["bg"] = color_hover
            def on_leave(e):
                btn["bg"] = color_base
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            return btn
        crear_boton("▶ INICIAR MISIÓN", "#2ecc71","#32fc86", self.crear_pantalla_niveles)
        crear_boton("📘 ENTRENAMIENTO (MÉTODOS)", "#f4d03f","#f1c40f", self.crear_pantalla_ayuda_general)
        crear_boton("⛔ SALIR",  "#e74c3c","#f93b26", self.root.quit)
        # ===== Footer =====
        tk.Label(
            panel,
            text="Sistema de Desactivación Táctica · Equipo 4 · FIME",
            font=("Consolas", 12),
            fg="#a8e6a1",
            bg="#0f1f0f"
            ).pack(side="bottom", pady=30)
    def crear_pantalla_niveles(self):
        """Pantalla para seleccionar nivel de dificultad"""
        self.limpiar_interfaz()
        self.fase_actual = "seleccion_nivel"
        try:
            if not hasattr(self, 'bg_niveles'):
                self.bg_niveles = tk.PhotoImage(file="assets/fondo.png")
            bg_label = tk.Label(self.root, image=self.bg_niveles)
            bg_label.image = self.bg_niveles 
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except:     
            self.root.configure(bg="#0a0f0a")
        main_frame = tk.Frame(self.root, bg="#0f1f0f", bd=3,
            relief="ridge",
            highlightbackground="#2ecc71",
            highlightthickness=2)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1200, height=750)
        try:
            if not hasattr(self, 'icon_normal'):
                self.icon_normal = tk.PhotoImage(file="assets/facil.png")
                self.icon_dificil = tk.PhotoImage(file="assets/medio.png")
                self.icon_expert = tk.PhotoImage(file="assets/dificil.png")
        except:
            self.icon_normal = self.icon_dificil = self.icon_expert = None
        titulo = tk.Label(
            main_frame,
            text="Selecciona el nivel de dificultad",
            font=("Consolas", 24, "bold"),
            fg="#145a32",
            bg="#0f1f0f"
        )
        titulo.pack(pady=20)
        def animar(i=0):
            colores = ["#2ecc71", "#25a65a", "#1e8c4e"]
            titulo.config(fg=colores[i])
            self.animacion_id = self.root.after(180, lambda: animar((i + 1) % 3))
        animar()
        tk.Label(
            main_frame,
            text=(
                "Cada nivel define cuántos explosivos debes localizar y cuántas vidas tienes.\n"
                "\t\t     ¡Selecciona con cuidado y prepárate!"), font=("Consolas", 14), fg="#a8e6a1", bg="#0f1f0f", justify="left").pack(pady=10)
        botones_frame = tk.Frame(main_frame, bg="#0f1f0f")
        botones_frame.pack(pady=20)
        def seleccionar_nivel(nivel, vidas):
            if self.animacion_id:
                try:
                    self.root.after_cancel(self.animacion_id)
                except ValueError:
                    pass
            self.animacion_id = None
            self.nivel_actual = nivel
            self.vidas = vidas
            self.puntos = 0
            # Obtener métodos seleccionados
            self.metodos_seleccionados_interpolacion = [
                metodo for metodo, var in self.metodos_vars_fase1.items() if var.get() == 1
            ]
            self.metodos_seleccionados_desactivacion = [
                metodo for metodo, var in self.metodos_vars_fase2.items() if var.get() == 1
            ]
            if not self.metodos_seleccionados_interpolacion:
                messagebox.showerror("Error", "Debes seleccionar al menos un método de Interpolación (Fase 1).")
                return
            if not self.metodos_seleccionados_desactivacion:
                messagebox.showerror("Error", "Debes seleccionar al menos un método de Desactivación (Fase 2).")
                return
            # ================================
            #  ASIGNAR TIEMPOS EN MINUTOS
            # ================================
            if nivel == 1:        # Normal (90 min)
                self.tiempo_limite = 90 * 60
            elif nivel == 2:      # Difícil (60 min)
                self.tiempo_limite = 60 * 60
            elif nivel == 3:      # Experimentado (30 min)
                self.tiempo_limite = 30 * 60
            # Tiempo restante = tiempo límite
            self.tiempo_restante = self.tiempo_limite
            # Iniciar fase de interpolación
            self.crear_interfaz_interpolacion()
        # Botón nivel Normal
        btn_normal = tk.Button(
            botones_frame,
            text="Nivel Normal\n3 explosivos · 3 vidas",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.colors["accent_blue"],
            activebackground=self.colors["accent_blue"],
            activeforeground="white",
            relief="flat",
            image=self.icon_normal,
            compound="top",
            command=lambda: seleccionar_nivel(1, 3)
        )
        def on_enter_normal(e):
             btn_normal["bg"] = "#1b3dd4" # Color de resaltado (hover
        def on_leave_normal(e):
             btn_normal["bg"] = self.colors["accent_blue"] # Color base
        btn_normal.bind("<Enter>", on_enter_normal)
        btn_normal.bind("<Leave>", on_leave_normal)
        btn_normal.grid(row=0, column=0, padx=15, pady=10)
        # Botón nivel Difícil
        btn_dificil = tk.Button(
            botones_frame,
            text="Nivel Difícil\n4 explosivos · 2 vidas",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.colors["accent_red"],
            activebackground=self.colors["accent_red"],
            activeforeground="white",
            relief="flat",
            image=self.icon_dificil,
            compound="top",
            command=lambda: seleccionar_nivel(2, 2)
        )
        def on_enter_dificil(e):
            btn_dificil["bg"] = "#f93b26" # Ejemplo de color hover (rojo intenso)
        def on_leave_dificil(e):
            btn_dificil["bg"] = self.colors["accent_red"] # Color base
        btn_dificil.bind("<Enter>", on_enter_dificil)
        btn_dificil.bind("<Leave>", on_leave_dificil)
        btn_dificil.grid(row=0, column=1, padx=15, pady=10)
        # Botón nivel Experimentado
        btn_expert = tk.Button(
            botones_frame,
            text="Nivel Experimentado\n5 explosivos · 1 vida",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#222222",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            image=self.icon_expert,
            compound="top",
            command=lambda: seleccionar_nivel(3, 1)
        )
        def on_enter_expert(e):
            btn_expert["bg"] = "#cccccc" # Ejemplo de color hover (gris más claro)
        def on_leave_expert(e):
            btn_expert["bg"] = "#222222" # Color base
        btn_expert.bind("<Enter>", on_enter_expert)
        btn_expert.bind("<Leave>", on_leave_expert)
        btn_expert.grid(row=0, column=2, padx=15, pady=10)
        tk.Label(
            main_frame,
            text="🛠 PERSONALIZA LOS MÉTODOS A ENFRENTAR 🛠",
            font=("Consolas", 18, "bold"),
            fg="#f1c40f",
            bg="#0f1f0f"
        ).pack(pady=(15, 5))
        # Marco principal para las dos columnas de métodos
        metodos_contenedor_frame = tk.Frame(main_frame, bg="#0f1f0f")
        metodos_contenedor_frame.pack(padx=20, pady=10, fill="x", expand=True)
        # ----------------------------------------------------
        # COLUMNA 1: MÉTODOS DE FASE 1 (INTERPOLACIÓN)
        # ----------------------------------------------------
        col1_frame = tk.LabelFrame(
            metodos_contenedor_frame,
            text="FASE 1: LOCALIZACIÓN (Interpolación)",
            font=("Consolas", 12, "bold"),
            fg="#2ecc71",
            bg="#0f1f0f",
            padx=10,
            pady=10
        )
        col1_frame.pack(side="left", padx=15, pady=5, fill="both", expand=True)
        # Diccionario para guardar variables de control (solo Fase 1)
        self.metodos_vars_fase1 = {} 
        # Crear Checkboxes para Interpolación
        for metodo in self.metodos_interpolacion:
            var = tk.IntVar(value=1) # Por defecto, todos activados
            self.metodos_vars_fase1[metodo] = var
            tk.Checkbutton(
                col1_frame,
                text=metodo,
                variable=var,
                onvalue=1,
                offvalue=0,
                fg="#ffffff",
                bg="#0f1f0f",
                selectcolor="#1a1a2e",
                activebackground="#0f1f0f",
                activeforeground="#2ecc71",
                font=("Consolas", 11)
            ).pack(anchor="w", pady=2)
        col1_frame.config(height=165)
        col1_frame.pack_propagate(False)
        # ----------------------------------------------------
        # COLUMNA 2: MÉTODOS DE FASE 2 (DESACTIVACIÓN)
        # ----------------------------------------------------
        col2_container = tk.LabelFrame(
            metodos_contenedor_frame,
            text="FASE 2: DESACTIVACIÓN (Ecs. Lineales/No Lineales, etc.)",
            font=("Consolas", 12, "bold"),
            fg="#e74c3c",
            bg="#0f1f0f",
            padx=5,
            pady=5
        )
        col2_container.pack(side="right", padx=15, pady=5, fill="both", expand=True)
        # === Scrollbar + Canvas ===
        canvas = tk.Canvas(
             col2_container,
             bg="#0f1f0f",
             highlightthickness=0,
        ) 
        canvas.pack(side="left", fill="both", expand=False)
        canvas.config(height=200)
        scrollbar = tk.Scrollbar(    
            col2_container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        # === Frame interno donde van los checkboxes ===
        inner_frame = tk.Frame(canvas, bg="#0f1f0f")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        def actualizar_scroll(event=None):
             canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", actualizar_scroll)
        # === Crear checkboxes de Fase 2 ===
        self.metodos_vars_fase2 = {}
        for metodo in self.metodos_desactivacion:
             var = tk.IntVar(value=1)
             self.metodos_vars_fase2[metodo] = var
             tk.Checkbutton(
                inner_frame,
                text=metodo,    
                variable=var,
                onvalue=1,
                offvalue=0,
                fg="#ffffff",
                bg="#0f1f0f",
                selectcolor="#1a1a2e",
                activebackground="#0f1f0f",
                activeforeground="#2ecc71",
                font=("Consolas", 11)
                ).pack(anchor="w", pady=2)        
        col2_container.config(height=165)
        col2_container.pack_propagate(False)
        btn_volver = tk.Button(
            main_frame,
            text="🏠 Volver al menú principal",
            font=("Consolas", 12, "bold"),
            fg="white",
            bg=self.colors["medium_bg"],
            activebackground=self.colors["medium_bg"],
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            command=self.crear_menu_principal
        )
        btn_volver.pack(pady=20)
    def crear_pantalla_ayuda_general(self):
        self.limpiar_interfaz()
        self.fase_actual = "ayuda"
        main_frame = tk.Frame(self.root, bg="#0f1f0f")
        main_frame.pack(expand=True, fill="both")
        # ===== Título =====
        tk.Label(
            main_frame, 
            text="📘 CENTRO DE APRENDIZAJE", 
            font=("Consolas", 26, "bold"),
            fg="#2ecc71",
            bg="#0f1f0f"
        ).pack(pady=(20, 15))
        # ===== Frame con scroll =====
        scroll_frame = self.crear_frame_scroll(main_frame)
        # ===== Contenido =====
        for tema, lista_metodos in self.metodos_por_tema.items():
            # ----- Contenedor del tema -----
            contenedor = tk.Frame(
                scroll_frame,
                bg="#e8f5e9",
                bd=2,
                relief="solid",
                highlightbackground="#2ecc71",
                highlightthickness=2
            )
            contenedor.pack(pady=15, padx=20, fill="x")
            # Título del tema
            tk.Label(
                contenedor,
                text=tema,
                font=("Consolas", 18, "bold"),
                bg="#e8f5e9",
                fg="black",
                anchor="w"
            ).pack(pady=10, padx=15)
            # ----- Grid de tarjetas -----
            tarjetas_frame = tk.Frame(contenedor, bg="#e8f5e9")
            tarjetas_frame.pack(pady=10)
            # ===== Crear tarjeta por cada método =====
            for i, metodo in enumerate(lista_metodos):
                tarjeta = tk.Frame(
                    tarjetas_frame,
                    bg="#ffffff",
                    bd=2,
                    relief="ridge",
                    highlightbackground="#2ecc71",
                    highlightthickness=1,
                    width=210,
                    height=290
                )
                tarjeta.pack_propagate(False)
                tarjeta.grid(row=0, column=i, padx=15, pady=15)
                # ===== Imagen del método =====
                nombre_img = self.normalizar(metodo) + ".png"
                ruta_img = f"assets/metodos/{self.normalizar(tema)}/{nombre_img}"
                try:
                    img = Image.open(ruta_img)
                    img = img.resize((200, 170), Image.LANCZOS)
                    img = ImageTk.PhotoImage(img)
                    lbl_img = tk.Label(tarjeta, image=img, bg="white")
                    lbl_img.image = img
                except:
                    lbl_img = tk.Label(
                        tarjeta, text="Sin imagen",
                        bg="#d0f0d0", font=("Consolas", 10, "bold"),
                        width=20, height=5
                    )
                lbl_img.pack(pady=10)
                # ===== Texto del método =====
                tk.Label(
                    tarjeta,
                    text=metodo,
                    font=("Consolas", 11, "bold"),
                    bg="#ffffff",
                    fg="black",
                    wraplength=200,
                    justify="center"
                ).pack(pady=5)
                # ===== Botón PDF =====
                nombre_pdf = self.normalizar(metodo) + ".pdf"
                # 1. Obtener el directorio del script actual (interfaz.py)
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # 2. Construir la ruta absoluta: script_dir/pdfs/nombre_tema/nombre_pdf
                ruta_pdf = os.path.join(script_dir, "pdfs", self.normalizar(tema), nombre_pdf)
                def abrir_pdf(ruta=ruta_pdf):
                    try:
                        os.startfile(ruta)
                    except:
                        messagebox.showerror("Error", f"No se encontró:\n{ruta}")
                btn = tk.Button(
                    tarjeta,
                    text="Ver PDF",
                    font=("Consolas", 10, "bold"),
                    bg="#f1c40f",
                    fg="black",
                    relief="flat",
                    padx=10,
                    pady=5,
                    command=abrir_pdf
                )
                btn.pack(pady=5)
                # Hover
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#d4ac0d"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#f1c40f"))
        # ===== Botón Volver =====
        btn_volver = tk.Button(
            main_frame, 
            text="🏠 Volver al menú", 
            font=("Consolas", 12, "bold"), 
            bg="#2ecc71", 
            fg="black", 
            relief="flat", 
            padx=20, 
            pady=10, 
            command=self.crear_menu_principal
        )
        btn_volver.place(relx=0.98, rely=0.02, anchor="ne")
    def crear_frame_scroll(self, parent):
        canvas = tk.Canvas(parent, bg="#0f1f0f", highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#0f1f0f")
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return scroll_frame
    def generar_problema_aleatorio(self):
        """Genera un nuevo problema de interpolación con puntos enteros y adecuados para el método"""
        # Determinar complejidad según nivel
        if self.nivel_actual <= 2:
            grado = random.randint(2, 3)
            num_puntos = grado + 2
        else:
            grado = random.randint(3, 4)
            num_puntos = grado + 3
        # Generar función polinómica realista con coeficientes que den valores razonables
        if grado == 2:
            coef = [random.uniform(-2, 2), random.uniform(-5, 5), random.uniform(-10, 10)]
        elif grado == 3:
            coef = [random.uniform(-1, 1), random.uniform(-3, 3), random.uniform(-5, 5), random.uniform(-10, 10)]
        else:
            coef = [random.uniform(-0.5, 0.5), random.uniform(-2, 2), random.uniform(-3, 3), 
                    random.uniform(-5, 5), random.uniform(-10, 10)]
        self.funcion_real = np.poly1d(coef)
        # Seleccionar método de interpolación ANTES de generar puntos
        self.metodo_actual = random.choice(self.metodos_seleccionados_interpolacion)
        # Generar puntos según el método seleccionado (siempre enteros)
        if self.metodo_actual == "Newton hacia adelante":
            self.puntos_detonados = self.generar_puntos_equiespaciados_enteros(num_puntos)
        elif self.metodo_actual == "Newton hacia atrás":
            self.puntos_detonados = self.generar_puntos_equiespaciados_enteros(num_puntos)
        elif self.metodo_actual == "Newton con diferencias divididas":
            self.puntos_detonados = self.generar_puntos_no_equiespaciados_enteros(num_puntos)
        else:  # Lagrange
            self.puntos_detonados = self.generar_puntos_mixtos_enteros(num_puntos)
        # Generar bombas objetivo (siempre enteras y dentro del rango)
        self.generar_bombas_objetivo_enteras()
        # Calcular respuestas correctas
        self.calcular_respuestas_correctas()
        # Debug information
        print(f"\n=== PROBLEMA GENERADO (Nivel {self.nivel_actual}) ===")
        print(f"Función: {self.funcion_real}")
        print(f"Método: {self.metodo_actual}")
        print(f"Bombas explotadas: {self.puntos_detonados}")
        print(f"Bombas objetivo (X): {self.x_objetivo}")
        print(f"Bombas ocultas: {self.bombas_ocultas}")
        print(f"Respuestas correctas: {self.respuestas_correctas}")
    def generar_puntos_equiespaciados_enteros(self, num_puntos):
        """Genera puntos equiespaciados enteros para Newton hacia adelante/atrás"""
        puntos = []
        # Definir rango base
        x_min = 0
        x_max = num_puntos * 3  # Espacio suficiente para seleccionar puntos equiespaciados
        # Generar puntos equiespaciados con paso entero
        paso = random.choice([2, 3, 4])  # Pasos de 2, 3 o 4 metros
        max_inicio = x_max - (num_puntos - 1) * paso
        if max_inicio < x_min:
             max_inicio = x_min  # corregimos para evitar rango negativo
        inicio = random.randint(x_min, max_inicio)
        for i in range(num_puntos):
            x = inicio + i * paso
            y = float(self.funcion_real(x))
            puntos.append((x, y))
        # Ordenar por X
        puntos.sort(key=lambda p: p[0])
        return puntos
    def generar_puntos_no_equiespaciados_enteros(self, num_puntos):
        """Genera puntos no equiespaciados enteros para Newton con diferencias divididas"""
        puntos = []
        # Definir rango base
        x_min = 0
        x_max = num_puntos * 3
        # Generar puntos no equiespaciados (todos enteros)
        x_vals = set()
        # Asegurar al menos un punto en los extremos
        x_vals.add(x_min)
        x_vals.add(x_max)
        # Generar puntos internos con espaciado irregular pero enteros
        while len(x_vals) < num_puntos:
            # Generar puntos enteros con diferentes espaciados
            x_candidato = random.randint(x_min + 1, x_max - 1)
            # Verificar que no esté demasiado cerca de puntos existentes
            demasiado_cerca = any(abs(x_candidato - x) < 2 for x in x_vals)
            if not demasiado_cerca:
                x_vals.add(x_candidato)
            else:
                # Si está demasiado cerca, agregar un punto con espaciado diferente
                x_vals.add(random.choice([x_min + 1, x_max - 1, 
                                        (x_min + x_max) // 2 + random.choice([-2, -1, 1, 2])]))
        # Convertir a lista y calcular Y
        x_lista = sorted(list(x_vals))[:num_puntos]  # Tomar solo los necesarios
        for x in x_lista:
            y = float(self.funcion_real(x))
            puntos.append((x, y))
        return puntos
    def generar_puntos_mixtos_enteros(self, num_puntos):
        """Genera puntos mixtos enteros (pueden ser equiespaciados o no) para Lagrange"""
        if random.choice([True, False]):
            return self.generar_puntos_equiespaciados_enteros(num_puntos)
        else:
            return self.generar_puntos_no_equiespaciados_enteros(num_puntos)
    def generar_bombas_objetivo_enteras(self):
        """Genera las bombas objetivo basándose en los puntos detonados (siempre enteras)"""
        self.x_objetivo = []
        self.bombas_ocultas = []
        # Encontrar rango de X de puntos detonados
        x_detonadas = [p[0] for p in self.puntos_detonados]
        x_min_detonado = min(x_detonadas)
        x_max_detonado = max(x_detonadas)
        # Generar bombas objetivo en función del nivel seleccionado
        # Nivel 1 (Normal): 3 bombas
        # Nivel 2 (Difícil): 4 bombas
        # Nivel 3 (Experimentado): 5 bombas
        if self.nivel_actual == 1:
            num_objetivos = 3
        elif self.nivel_actual == 2:
            num_objetivos = 4
        else:
            num_objetivos = 5
        # Crear lista de posibles X objetivo (enteras dentro del rango pero no en puntos detonados)
        posibles_x = [x for x in range(x_min_detonado + 1, x_max_detonado) 
                     if x not in x_detonadas and x not in self.x_objetivo]
        # Si no hay suficientes puntos posibles, extender el rango
        if len(posibles_x) < num_objetivos:
            # Agregar puntos justo fuera del rango
            for x in [x_min_detonado - 1, x_max_detonado + 1]:
                if x not in x_detonadas and x not in self.x_objetivo:
                    posibles_x.append(x)
        # Seleccionar aleatoriamente de los posibles
        if len(posibles_x) >= num_objetivos:
            self.x_objetivo = random.sample(posibles_x, num_objetivos)
        else:
            # Si aún no hay suficientes, usar los que haya
            self.x_objetivo = posibles_x[:num_objetivos]
            # Completar con valores únicos si es necesario
            while len(self.x_objetivo) < num_objetivos:
                nuevo_x = x_max_detonado + len(self.x_objetivo) + 1
                self.x_objetivo.append(nuevo_x)
        # Ordenar y calcular Y real
        self.x_objetivo.sort()
        self.bombas_ocultas = [(x, float(self.funcion_real(x))) for x in self.x_objetivo]
    def calcular_respuestas_correctas(self):
        """Calcula las respuestas correctas usando el método de interpolación asignado"""
        self.respuestas_correctas = {}
        # Ordenar puntos por X para los métodos que lo requieren
        puntos_ordenados = sorted(self.puntos_detonados, key=lambda p: p[0])
        for x_objetivo, y_real in self.bombas_ocultas:
            if self.metodo_actual == "Lagrange":
                y_calculado = self.metodos_calculo.interpolacion_lagrange(x_objetivo, puntos_ordenados)
            elif self.metodo_actual == "Newton hacia adelante":
                y_calculado = self.metodos_calculo.interpolacion_newton_adelante(x_objetivo, puntos_ordenados)
            elif self.metodo_actual == "Newton hacia atrás":
                y_calculado = self.metodos_calculo.interpolacion_newton_atras(x_objetivo, puntos_ordenados)
            else:  # Newton con diferencias divididas
                y_calculado = self.metodos_calculo.interpolacion_diferencias_divididas(x_objetivo, puntos_ordenados)
            self.respuestas_correctas[x_objetivo] = y_calculado
    def iniciar_temporizador(self, parent_header):
        # Cancelar temporizador previo
        if hasattr(self, 'temporizador_id') and self.temporizador_id:
            self.root.after_cancel(self.temporizador_id)
            self.temporizador_id = None
        # Mantener tiempo restante
        self.temporizador_activo = True
        # Crear etiqueta si no existe
        if self.lbl_tiempo is None or not self.lbl_tiempo.winfo_exists():
            self.lbl_tiempo = tk.Label(
                parent_header,
                text="",
                font=("Arial", 16, "bold"),
                fg="yellow",
                bg="#0f1f0f"
            )
            for widget in parent_header.winfo_children():
                if isinstance(widget, tk.Frame):
                    self.lbl_tiempo.pack(side='left', padx=20)
                    break
            else:
                self.lbl_tiempo.pack(side='left', padx=200)
        # Mostrar tiempo actual
        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        self.lbl_tiempo.config(text=f"⏳ Tiempo: {minutos:02d}:{segundos:02d}")
        # Iniciar cuenta regresiva
        self.temporizador_id = self.root.after(1000, self.actualizar_temporizador)
    def actualizar_temporizador(self):
        if not self.temporizador_activo:
            return
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            self.lbl_tiempo.config(text=f"⏳ Tiempo: {minutos:02d}:{segundos:02d}")
            self.temporizador_id = self.root.after(1000, self.actualizar_temporizador)
        else:
            # ======== TIEMPO AGOTADO ========
            self.temporizador_activo = False
            if self.fase_actual == "desactivacion":  
                # FALLÓ AL DESACTIVAR EL EXPLOSIVO POR TIEMPO
                self.vidas -= 1
                if self.vidas <= 0:
                    self.mostrar_interfaz_derrota()  # Usar la nueva función
                else:
                    # Manda a resolver interpolación (fase 1)
                    self.crear_interfaz_interpolacion()
            else:
                # Tiempo agotado en fase de interpolación
                self.vidas -= 1
                if self.vidas <= 0:
                    self.mostrar_interfaz_derrota()  # Usar la nueva función
                else:
                    self.crear_interfaz_interpolacion()
    def crear_interfaz_interpolacion(self, regenerar_problema=True):
        """Crea la interfaz para la fase de interpolación"""
        self.limpiar_interfaz()
        self.fase_actual = "interpolacion"
        try:
            # Reutilizar el objeto de imagen si ya existe, si no, cargarlo
            if not hasattr(self, 'bg_juego'): # Podría ser 'bg_niveles' o 'bg_menu'
                self.bg_juego = tk.PhotoImage(file="assets/fondo.png")
            bg_label = tk.Label(self.root, image=self.bg_juego)
            bg_label.image = self.bg_juego 
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            self.root.configure(bg="#1a1a2e")
        # Generar nuevo problema solo si se solicita
        if regenerar_problema:
            self.generar_problema_aleatorio()
        # Frame principal
        borde_principal = tk.Frame(
            self.root,
            bg="#0f1f0f",    # color del borde    
            relief="ridge",  # estilos: ridge / groove / solid / raised
            bd=8             # grosor del borde
        )
        borde_principal.pack(expand=True, fill="both", padx=20, pady=20)
        main_frame = tk.Frame(borde_principal, bg="#0b2c0b")
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        # Header informativo
        header_frame = tk.Frame(main_frame, bg="#0f1f0f", relief='raised', bd=2)
        header_frame.pack(pady=20)
        btn_menu = tk.Button(
            main_frame,
            text="🏠 Menú principal",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg=self.colors['dark_bg'],
            activebackground=self.colors['dark_bg'],
            activeforeground='white',
            relief='flat',
            command=self.crear_menu_principal
        )
        btn_menu.place(relx=1.0, rely=0.0, x=-140, y=110, anchor='ne')
        tk.Label(header_frame, 
                text=f"💣 NIVEL {self.nivel_actual} - INTERPOLACIÓN DE BOMBAS",
                font=('Arial', 20, 'bold'),
                fg=self.colors['accent_yellow'],
                bg="#0f1f0f").pack(pady=15)
        # Información del método
        metodo_frame = tk.Frame(header_frame, bg="#0f1f0f")
        metodo_frame.pack(pady=10)
        tk.Label(metodo_frame,
                text="MÉTODO ASIGNADO:",
                font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(side='left', padx=10)
        tk.Label(metodo_frame,
                text=self.metodo_actual,
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_green'],
                bg="#0f1f0f").pack(side='left', padx=10)
        # Información adicional sobre el tipo de puntos
        info_puntos_frame = tk.Frame(header_frame, bg="#0f1f0f")
        info_puntos_frame.pack(pady=5)
        if self.metodo_actual in ["Newton hacia adelante", "Newton hacia atrás"]:
            puntos_info = "Puntos equiespaciados (enteros)"
            color_info = self.colors['accent_blue']
        elif self.metodo_actual == "Newton con diferencias divididas":
            puntos_info = "Puntos no equiespaciados (enteros)"
            color_info = self.colors['accent_yellow']
        else:  # Lagrange
            puntos_info = "Puntos mixtos (enteros)"
            color_info = self.colors['accent_green']
        tk.Label(info_puntos_frame,
                text=f"Tipo de puntos: {puntos_info}",
                font=('Arial', 10, 'italic'),
                fg=color_info,
                bg="#0f1f0f").pack()
        # Información de estado
        estado_frame = tk.Frame(header_frame, bg="#0f1f0f")
        estado_frame.pack(pady=10)
        tk.Label(estado_frame,
                text=f"VIDAS: {'❤️' * self.vidas}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_red'],
                bg="#0f1f0f").pack(side='left', padx=20)
        tk.Label(estado_frame,
                text=f"PUNTOS: {self.puntos}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_yellow'],
                bg="#0f1f0f").pack(side='left', padx=20)
        tk.Label(estado_frame,
                text=f"BOMBAS A ENCONTRAR: {len(self.x_objetivo)}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_blue'],
                bg="#0f1f0f").pack(side='left', padx=20)
        # Contenedor de dos columnas
        content_frame = tk.Frame(main_frame, bg="#0b2c0b")
        content_frame.pack(expand=True, fill='both', pady=20)
        # Columna izquierda - Campo de batalla
        left_frame = tk.Frame(content_frame, bg="#0b2c0b")
        left_frame.config(width=700)
        left_frame.pack(side='left', fill='both', expand=False, padx=10)
        self.crear_campo_batalla(left_frame)
        # Columna derecha - Panel de control
        right_frame = tk.Frame(content_frame, bg=self.colors['medium_bg'], relief='sunken', bd=2)
        right_frame.config(width=850, height=550)
        right_frame.pack_propagate(False)
        right_frame.pack(side='right', fill='y', expand=False, padx= 10, pady=10)
        self.crear_panel_control(right_frame)
        self.iniciar_temporizador(header_frame)
    def crear_campo_batalla(self, parent):
        """Crea la visualización del campo de batalla"""
        campo_frame = tk.Frame(parent, bg="#0f1f0f", relief='raised', bd=3)
        campo_frame.config(width=800, height=550)
        campo_frame.pack_propagate(False)
        campo_frame.pack(fill='both',padx=25, pady=10)
        # Título del campo
        tk.Label(campo_frame,
                text="CAMPO DE BATALLA - DISTRIBUCIÓN DE BOMBAS",
                font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(pady=10)
        # Canvas para dibujar el campo
        self.canvas = tk.Canvas(campo_frame,
                               highlightthickness=0)
        self.canvas.pack(expand=True, fill='both', padx=20, pady=20)
        self.bg_batalla_original = Image.open("assets/campo.png")
        # Actualizar el canvas después de que se haya renderizado
        self.root.after(100, self.dibujar_campo_batalla)
    def dibujar_campo_batalla(self):
        """Dibuja las bombas en el campo de batalla"""
        self.canvas.delete("all")
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()
        if ancho <= 1 or alto <= 1:
            self.root.after(300, self.dibujar_campo_batalla)
            return
        img_resized = self.bg_batalla_original.resize((ancho, alto), Image.Resampling.LANCZOS)
        self.bg_batalla = ImageTk.PhotoImage(img_resized)
        self.canvas.create_image(0, 0, image=self.bg_batalla, anchor="nw")
        # Encontrar rango de coordenadas
        todas_x = [p[0] for p in self.puntos_detonados] + [x for x, y in self.bombas_ocultas]
        todas_y = [p[1] for p in self.puntos_detonados] + [y for x, y in self.bombas_ocultas]
        x_min, x_max = min(todas_x), max(todas_x)
        y_min, y_max = min(todas_y), max(todas_y)
        # Agregar márgenes
        x_min -= 1
        x_max += 1
        y_min -= 1
        y_max += 1
       
        if x_max - x_min == 0:
            x_max += 1
        if y_max - y_min == 0:
            y_max += 1
        # Función para convertir coordenadas reales a píxeles
        def a_pixel(x, y):
            x_pixel = ((x - x_min) / (x_max - x_min)) * (ancho - 100) + 50
            y_pixel = alto - (((y - y_min) / (y_max - y_min)) * (alto - 100) + 50)
            return x_pixel, y_pixel
        # Dibujar grid
        for x in range(int(x_min), int(x_max) + 1):
            x_pixel, _ = a_pixel(x, 0)
            self.canvas.create_line(x_pixel, 50, x_pixel, alto - 50, 
                                  fill="#000000", width=1, dash=(2, 4))
            self.canvas.create_text(x_pixel, alto - 30, text=f"{x}m", 
                                  fill="#000000", font=('Arial', 10))
        # Dibujar bombas explotadas
        for x, y in self.puntos_detonados:
            x_pixel, y_pixel = a_pixel(x, y)
            # Círculo de explosión
            self.canvas.create_oval(x_pixel-15, y_pixel-15, x_pixel+15, y_pixel+15,
                                  fill=self.colors['accent_red'], outline='white', width=2)
            # Efecto de explosión
            for i in range(8):
                angulo = math.radians(i * 45)
                dx = math.cos(angulo) * 25
                dy = math.sin(angulo) * 25
                self.canvas.create_line(x_pixel, y_pixel, x_pixel+dx, y_pixel+dy,
                                      fill="#000000", width=2)
            # Coordenadas
            self.canvas.create_text(x_pixel, y_pixel-30, 
                                  text=f"({x}, {y:.1f})", 
                                  fill="#000000", font=('Arial', 8, 'bold'))
        # Dibujar bombas objetivo (las que el usuario debe encontrar)
        for x, y_real in self.bombas_ocultas:
            x_pixel, y_pixel = a_pixel(x, y_real)
            # Círculo de bomba oculta
            self.canvas.create_oval(x_pixel-12, y_pixel-12, x_pixel+12, y_pixel+12,
                                  fill='#7f8c8d', outline='white', width=2)
            # Signo de interrogación
            self.canvas.create_text(x_pixel, y_pixel, text="?", 
                                  fill=self.colors['text_white'], font=('Arial', 12, 'bold'))
            # Coordenada X conocida (objetivo)
            self.canvas.create_text(x_pixel, y_pixel-25, text=f"X = {x}", 
                                  fill=self.colors['accent_blue'], font=('Arial', 10, 'bold'))
        # Dibujar línea de interpolación
        if len(self.puntos_detonados) >= 2:
            puntos_ordenados = sorted(self.puntos_detonados, key=lambda p: p[0])
            puntos_linea = []
            for i in range(100):
                x = x_min + (x_max - x_min) * (i / 99)
                if self.metodo_actual == "Lagrange":
                    y = self.metodos_calculo.interpolacion_lagrange(x, puntos_ordenados)
                elif self.metodo_actual in ["Newton hacia adelante", "Newton hacia atrás"]:
                    # Para métodos que requieren equiespaciados, verificar si podemos usarlos
                    diferencias = [puntos_ordenados[i+1][0] - puntos_ordenados[i][0] for i in range(len(puntos_ordenados)-1)]
                    if len(set(diferencias)) <= 1:
                        if self.metodo_actual == "Newton hacia adelante":
                            y = self.metodos_calculo.interpolacion_newton_adelante(x, puntos_ordenados)
                        else:
                            y = self.metodos_calculo.interpolacion_newton_atras(x, puntos_ordenados)
                    else:
                        y = self.metodos_calculo.interpolacion_diferencias_divididas(x, puntos_ordenados)
                else:  # Newton con diferencias divididas
                    y = self.metodos_calculo.interpolacion_diferencias_divididas(x, puntos_ordenados)
                puntos_linea.append((x, y))
            # Dibujar línea
            puntos_pixel = [a_pixel(x, y) for x, y in puntos_linea]
            for i in range(len(puntos_pixel) - 1):
                x1, y1 = puntos_pixel[i]
                x2, y2 = puntos_pixel[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, 
                                      fill=self.colors['accent_green'], width=2, dash=(5, 5))
    def crear_panel_control(self, parent):
        """Crea el panel de control para ingresar respuestas con scrollbar"""
        # Frame principal que contendrá el canvas y scrollbar
        main_container = tk.Frame(parent, bg="#0f1f0f")
        main_container.pack(fill='both', expand=True)
        # Crear canvas y scrollbar
        canvas = tk.Canvas(main_container, bg="#0f1f0f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(canvas, bg="#0f1f0f")
        # Configurar el scroll region cuando el frame se expanda
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        # Crear ventana en el canvas para el frame scrollable
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        # Configurar el canvas para usar el scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Ajustar el ancho del frame interno cuando cambie el tamaño del canvas
        def configurar_ancho_frame(event):
            canvas.itemconfig(1, width=event.width)  # 1 es el ID del window creado
        canvas.bind("<Configure>", configurar_ancho_frame)
        # Contenido del panel (todo dentro de scrollable_frame)
        tk.Label(scrollable_frame,
                text="PANEL DE INTERPOLACIÓN",
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_yellow'],
                bg="#0f1f0f").pack(pady=20)
        # Información de bombas explotadas
        info_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        info_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(info_frame,
                text="BOMBAS EXPLOTADAS (Puntos conocidos):",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(anchor='w')
        puntos_text = "\n".join([f"• ({x}, {y:.4f})" for x, y in sorted(self.puntos_detonados)])
        puntos_label = tk.Label(info_frame,
                            text=puntos_text,
                            font=('Arial', 10),
                            fg=self.colors['text_gray'],
                            bg="#0f1f0f",
                            justify='left')
        puntos_label.pack(anchor='w', pady=5)
        # Información de bombas a encontrar
        objetivo_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        objetivo_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(objetivo_frame,
                text="BOMBAS A ENCONTRAR (Coordenadas X):",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(anchor='w')
        objetivo_text = ", ".join([f"X = {x}" for x in self.x_objetivo])
        objetivo_label = tk.Label(objetivo_frame,
                                text=objetivo_text,
                                font=('Arial', 12, 'bold'),
                                fg=self.colors['accent_blue'],
                                bg="#0f1f0f")
        objetivo_label.pack(anchor='w', pady=5)
        # Instrucciones
        instrucciones_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        instrucciones_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(instrucciones_frame,
                text="INSTRUCCIONES:",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(anchor='w')
        instrucciones_text = f"Usa el método {self.metodo_actual} para calcular las coordenadas Y de las bombas en las posiciones X dadas."
        instrucciones_label = tk.Label(instrucciones_frame,
                                    text=instrucciones_text,
                                    font=('Arial', 10),
                                    fg=self.colors['text_gray'],
                                    bg="#0f1f0f",
                                    wraplength=350,
                                    justify='left')
        instrucciones_label.pack(anchor='w', pady=5)
        # Información sobre tolerancia
        tolerancia_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        tolerancia_frame.pack(fill='x', padx=20, pady=5)
        tolerancia_text = "💡 NOTA: Se acepta un margen de error del 0.5% + 0.01 unidades para cálculos manuales"
        tolerancia_label = tk.Label(tolerancia_frame,
                                text=tolerancia_text,
                                font=('Arial', 9, 'italic'),
                                fg=self.colors['accent_yellow'],
                                bg="#0f1f0f",
                                wraplength=350,
                                justify='left')
        tolerancia_label.pack(anchor='w', pady=5)
        # Entradas para las bombas objetivo
        self.entradas = {}
        entradas_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        entradas_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(entradas_frame,
                text="INGRESA LAS COORDENADAS Y CALCULADAS:",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(anchor='w', pady=10)
        for x in self.x_objetivo:
            entrada_frame = tk.Frame(entradas_frame, bg="#0f1f0f")
            entrada_frame.pack(fill='x', pady=5)
            tk.Label(entrada_frame,
                    text=f"Para X = {x} | Y =",
                    font=('Arial', 10),
                    fg=self.colors['text_white'],
                    bg="#0f1f0f").pack(side='left')
            entry = tk.Entry(entrada_frame,
                        font=('Arial', 10),
                        width=15,
                        justify='center')
            entry.pack(side='left', padx=5)
            if hasattr(self, "respuestas_guardadas") and x in self.respuestas_guardadas:
                entry.insert(0, str(self.respuestas_guardadas[x]))
            self.entradas[x] = entry
        # Botones de acción
        botones_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        botones_frame.pack(fill='x', padx=20, pady=20)
        tk.Button(botones_frame,
                text="🧮 VERIFICAR INTERPOLACIÓN",
                font=('Arial', 12, 'bold'),
                fg='white',
                bg=self.colors['accent_green'],
                relief='raised',
                bd=3,
                command=self.verificar_interpolacion).pack(fill='x', pady=5)
        tk.Button(botones_frame,
                text="📚 AYUDA DEL MÉTODO",
                font=('Arial', 12, 'bold'),
                fg='white',
                bg=self.colors['accent_blue'],
                relief='raised',
                bd=3,
                command=self.mostrar_ayuda_metodo).pack(fill='x', pady=5)
    def parsear_entrada(self, entrada):
            """Convierte diferentes formatos de entrada a float"""
            # Eliminar espacios
            entrada = entrada.strip()
            # Manejar comas como separadores decimales
            entrada = entrada.replace(',', '.')
            # Manejar notación científica básica
            if 'e' in entrada.lower():
                parte, exponente = entrada.lower().split('e')
                return float(parte) * (10 ** float(exponente))
            # Manejar el símbolo × para multiplicación (común en calculadoras)
            if '×' in entrada:
                partes = entrada.split('×')
                resultado = 1.0
                for parte in partes:
                    resultado *= float(parte.strip())
                return resultado
            # Conversión directa
            return float(entrada)
    def verificar_interpolacion(self):
        """Verifica las respuestas del usuario y RESTA tiempo multiplicado por los errores"""
        correctas = 0
        total = len(self.x_objetivo)
        resultados = []
        errores = 0  # <-- Contador de errores
        self.respuestas_guardadas = getattr(self, "respuestas_guardadas", {})
        for x in self.x_objetivo:
            entrada = self.entradas[x].get().strip()
            y_correcta = self.respuestas_correctas[x]
            if y_correcta == 0:
                tolerancia = 0.01
            else:
                tolerancia = abs(y_correcta) * 0.005 + 0.01
            try:
                y_usuario = self.parsear_entrada(entrada)
                if abs(y_usuario - y_correcta) <= tolerancia:
                    correctas += 1
                    self.respuestas_guardadas[x] = y_usuario
                    resultados.append((x, y_correcta, y_usuario, True, tolerancia))
                else:
                    errores += 1  
                    self.entradas[x].delete(0, "end")
                    resultados.append((x, y_correcta, y_usuario, False, tolerancia))
            except (ValueError, TypeError):
                errores += 1  
                self.entradas[x].delete(0, "end")
                resultados.append((x, y_correcta, "ENTRADA INVÁLIDA", False, tolerancia))
        if errores > 0 and self.vidas > 0:
            if self.nivel_actual == 1:       # Normal
                penalizacion = 30
            elif self.nivel_actual == 2:     # Difícil
                penalizacion = 45
            else:                            # Experto
                penalizacion = 60
            penalizacion_total = penalizacion * errores  # <-- Multiplicar por errores
            self.tiempo_restante += penalizacion_total
            # Actualizar label
            if self.lbl_tiempo and self.lbl_tiempo.winfo_exists():
                minutos = self.tiempo_restante // 60
                segundos = self.tiempo_restante % 60
                self.lbl_tiempo.config(text=f"⏳ Tiempo: {minutos:02d}:{segundos:02d}")
        self.mostrar_resultados(resultados, correctas, total)    
    def mostrar_resultados(self, resultados, correctas, total):
        """Muestra los resultados de la verificación con información de tolerancia"""
        # Crear ventana de resultados
        resultados_window = tk.Toplevel(self.root)
        resultados_window.title("RESULTADOS DE INTERPOLACIÓN")
        resultados_window.geometry("800x600")
        resultados_window.configure(bg=self.colors['dark_bg'])
        resultados_window.protocol("WM_DELETE_WINDOW", lambda: None)
        resultados_window.grab_set()
        resultados_window.transient(self.root)
        # Centrar ventana
        resultados_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - resultados_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - resultados_window.winfo_height()) // 2
        resultados_window.geometry(f"+{x}+{y}")
        # Frame principal
        main_frame = tk.Frame(resultados_window, bg=self.colors['dark_bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        # Título
        if correctas == total:
            titulo = "🎯 ¡INTERPOLACIÓN EXITOSA!"
            color_titulo = self.colors['accent_green']
            self.puntos += total * 10
        else:
            titulo = "⚠️ INTERPOLACIÓN CON ERRORES"
            color_titulo = self.colors['accent_yellow']
            self.vidas -= 1
        tk.Label(main_frame,
                text=titulo,
                font=('Arial', 16, 'bold'),
                fg=color_titulo,
                bg=self.colors['dark_bg']).pack(pady=10)
        # Resumen
        tk.Label(main_frame,
                text=f"Correctas: {correctas}/{total}",
                font=('Arial', 14),
                fg=self.colors['text_white'],
                bg=self.colors['dark_bg']).pack(pady=5)
        # Tabla de resultados
        tabla_frame = tk.Frame(main_frame, bg=self.colors['medium_bg'], relief='sunken', bd=2)
        tabla_frame.pack(expand=True, fill='both', pady=10)
        # Encabezados de la tabla
        encabezados = ["X", "Y Ingresada", "Tolerancia", "Resultado"]
        for i, texto in enumerate(encabezados):
            tk.Label(tabla_frame,
                    text=texto,
                    font=('Arial', 10, 'bold'),
                    fg=self.colors['accent_yellow'],
                    bg=self.colors['medium_bg']).grid(row=0, column=i, padx=5, pady=5, sticky='ew')
        # Datos de la tabla
        for i, (x, y_correcta, y_usuario, correcto, tolerancia) in enumerate(resultados, 1):
            # X
            tk.Label(tabla_frame,
                    text=str(x),
                    font=('Arial', 9),
                    fg=self.colors['text_white'],
                    bg=self.colors['medium_bg']).grid(row=i, column=0, padx=5, pady=2)
            # Y Ingresada
            color_ingresado = self.colors['accent_green'] if correcto else self.colors['accent_red']
            texto_ingresado = str(y_usuario) if isinstance(y_usuario, (int, float)) else y_usuario
            tk.Label(tabla_frame,
                    text=texto_ingresado,
                    font=('Arial', 9),
                    fg=color_ingresado,
                    bg=self.colors['medium_bg']).grid(row=i, column=1, padx=5, pady=2)
            # Tolerancia usada
            tk.Label(tabla_frame,
                    text=f"±{tolerancia:.4f}",
                    font=('Arial', 8),
                    fg=self.colors['text_gray'],
                    bg=self.colors['medium_bg']).grid(row=i, column=2, padx=5, pady=2)
            # Resultado
            resultado_texto = "✅ CORRECTO" if correcto else "❌ INCORRECTO"
            color_resultado = self.colors['accent_green'] if correcto else self.colors['accent_red']
            tk.Label(tabla_frame,
                    text=resultado_texto,
                    font=('Arial', 9, 'bold'),
                    fg=color_resultado,
                    bg=self.colors['medium_bg']).grid(row=i, column=3, padx=5, pady=2)
        # Configurar grid weights
        for i in range(4):
            tabla_frame.columnconfigure(i, weight=1)
        # Botones
        botones_frame = tk.Frame(main_frame, bg=self.colors['dark_bg'])
        botones_frame.pack(fill='x', pady=10)
        if correctas == total:
            tk.Button(botones_frame,
                    text="💣 DESACTIVAR BOMBAS",
                    font=('Arial', 12, 'bold'),
                    fg='white',
                    bg=self.colors['accent_red'],
                    command=lambda: [resultados_window.destroy(), self.fase_desactivacion()]).pack(fill='x', pady=5)
        elif self.vidas > 0:
            # Guardar la fase actual para poder volver
            self.fase_anterior = "interpolacion"
            # Mostrar problema de integración
            tk.Button(botones_frame,
                    text="🧮 RESOLVER PROBLEMA DE INTEGRACIÓN",
                    font=('Arial', 12, 'bold'),
                    fg='white',
                    bg=self.colors['accent_blue'],
                    command=lambda: [resultados_window.destroy(), 
                                self.seleccionar_problema_integracion(),
                                self.crear_interfaz_integracion_emergencia()]).pack(fill='x', pady=5)
        else:
            # SE QUEDÓ SIN VIDAS - GAME OVER
            tk.Button(botones_frame,
                    text="💀 GAME OVER - VER RESULTADO",
                    font=('Arial', 12, 'bold'),
                    fg='white',
                    bg=self.colors['accent_red'],
                    command=lambda: [resultados_window.destroy(), self.mostrar_interfaz_derrota()]).pack(fill='x', pady=5)
    def fase_desactivacion(self):
        """Inicia la fase de desactivación de bombas"""
        self.fase_actual = "desactivacion"
        self.generar_problemas_desactivacion()
        self.problema_actual_desactivacion = 0
        self.crear_interfaz_desactivacion()
        
    def generar_problemas_desactivacion(self):
        """Genera múltiples problemas para la fase de desactivación (uno por bomba encontrada)"""
        self.problemas_desactivacion = []
        self.respuestas_desactivacion = []
        self.metodos_desactivacion_asignados = []
        num_bombas = len(self.x_objetivo)
        # Seleccionar métodos aleatorios diferentes para cada bomba
        metodos_disponibles = self.metodos_seleccionados_desactivacion.copy()
        random.shuffle(metodos_disponibles)
        # Si hay más bombas que métodos, repetimos algunos métodos
        while len(metodos_disponibles) < num_bombas:
            metodos_disponibles.extend(self.metodos_seleccionados_desactivacion)
        for i in range(num_bombas):
            metodo = metodos_disponibles[i]
            if metodo in self.metodos_integracion:
                # Lógica específica para Integración (copiada de tu lógica de penalización)
                if metodo == "Regla de 1/3 Simpson":
                    n = random.choice([2, 4, 6, 8]) # n debe ser par
                    problema, respuesta = self.metodos_calculo.generar_problema_simpson13(n)
                elif metodo == "Regla de 3/8 Simpson":
                    n = random.choice([3, 6, 9])    # n debe ser múltiplo de 3
                    problema, respuesta = self.metodos_calculo.generar_problema_simpson38(n)
                elif metodo == "Newton-Cotes Cerradas":
                    n = random.choice([4, 5, 6, 7])
                    problema, respuesta = self.metodos_calculo.generar_problema_newton_cotes_cerradas(n, self.constantes_newton_cotes_cerradas)
                elif metodo == "Newton-Cotes Abiertas":
                    n = random.choice([2, 3, 4, 5])
                    problema, respuesta = self.metodos_calculo.generar_problema_newton_cotes_abiertas(n, self.constantes_newton_cotes_abiertas)
                else:  # Regla Trapezoidal
                    n = random.choice([1, 2, 3, 4, 5])
                    problema, respuesta = self.metodos_calculo.generar_problema_trapezoidal(n)
            else:
                # Lógica estándar para el resto de métodos (Ecuaciones, EDOs, etc.)
                problema, respuesta = self.metodos_calculo.generar_problema_por_metodo(metodo)
            
            self.problemas_desactivacion.append(problema)
            self.respuestas_desactivacion.append(respuesta)
            self.metodos_desactivacion_asignados.append(metodo)
        # Imprimir en terminal las respuestas correctas para facilitar pruebas
        print(f"\n=== PROBLEMAS DE DESACTIVACIÓN ({num_bombas} bombas) ===")
        for i in range(num_bombas):
            print(f"Bomba {i+1}: {self.metodos_desactivacion_asignados[i]}")
            print(f"Problema: {self.problemas_desactivacion[i]}")
            print(f"Respuesta correcta: {self.respuestas_desactivacion[i]}")
            print("---")

    def crear_interfaz_desactivacion(self):
        self.limpiar_interfaz()
        self.fase_actual = "desactivacion"
        # 1. Fondo
        try:
            if not hasattr(self, 'bg_juego'):
                self.bg_juego = tk.PhotoImage(file="assets/fondo.png")
            bg_label = tk.Label(self.root, image=self.bg_juego)
            bg_label.image = self.bg_juego
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            self.root.configure(bg="#1a1a2e")
        frame_principal = tk.Frame(self.root, bg="#0f1f0f", relief="ridge", bd=8)
        frame_principal.pack(expand=True, fill='both', padx=20, pady=20)
        title = tk.Label(frame_principal, 
                        text=f"💣 DESACTIVACIÓN DEL EXPLOSIVO #{self.problema_actual_desactivacion + 1}", 
                        font=("Consolas", 26, "bold"), 
                        fg="red", 
                        bg="#0f1f0f")
        title.pack(pady=20)

        if self.nivel_actual == 1:  # Normal
            tiempo_base = 30 * 60
        elif self.nivel_actual == 2:  # Difícil
            tiempo_base = 25 * 60
        elif self.nivel_actual == 3:  # Experimentado
            tiempo_base = 20 * 60
        # Solo mantiene el tiempo si se está volviendo de una penalización de integración
        if self.temporizador_activo and self.tiempo_restante > 0 and (hasattr(self, 'volviendo_de_integracion') and self.volviendo_de_integracion):
            # Mantener el tiempo restante
            self.volviendo_de_integracion = False # Resetear bandera
        else:
            self.tiempo_restante = tiempo_base
        # ================================
        # Mostrar encabezado y temporizador
        # ================================
        header_frame = tk.Frame(frame_principal, bg="#0f1f0f")
        header_frame.pack(pady=10, fill='x')
        self.lbl_nivel = tk.Label(header_frame, 
                                text=f"Nivel {self.nivel_actual} | Bomba: {self.problema_actual_desactivacion + 1}/{len(self.problemas_desactivacion)}", 
                                font=("Consolas", 14, "bold"), 
                                fg=self.colors['accent_blue'], 
                                bg="#0f1f0f")
        self.lbl_nivel.pack(side='left', padx=140)
        self.lbl_vidas = tk.Label(header_frame, 
                                text=f"VIDAS: {'❤️' * self.vidas}", 
                                font=('Consolas', 14, 'bold'), 
                                fg=self.colors['accent_red'], 
                                bg="#0f1f0f")
        self.lbl_vidas.pack(side='right', padx=20)
        # Iniciar/Actualizar temporizador
        self.iniciar_temporizador(header_frame)
        # ================================
        # Panel con scrollbar para contenido
        # ================================
        main_container = tk.Frame(frame_principal, bg="#0f1f0f")
        main_container.pack(expand=True, fill='both', padx=20, pady=10)
        canvas = tk.Canvas(main_container, bg="#0f1f0f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f1f0f")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def configurar_ancho_frame(event):
            canvas.itemconfig(1, width=event.width)
        canvas.bind("<Configure>", configurar_ancho_frame)
        # ================================
        # Panel del Problema (Muestra el texto del problema)
        # ================================
        problema_actual = self.problemas_desactivacion[self.problema_actual_desactivacion]
        problema_frame = tk.Frame(scrollable_frame, bg="#0b2c0b", relief='raised', bd=3)
        problema_frame.pack(expand=True, fill='x', padx=20, pady=10)
        tk.Label(problema_frame, 
                text="EXPLOSIVO DETECTADO - CÓDIGO DE DESACTIVACIÓN:", 
                font=('Consolas', 14, 'bold'), 
                fg=self.colors['accent_yellow'], 
                bg="#0b2c0b").pack(pady=(10, 5))
        tk.Label(problema_frame, 
                text=problema_actual, 
                font=('Consolas', 12), 
                fg=self.colors['text_white'], 
                bg="#0b2c0b", 
                justify='left', 
                wraplength=700).pack(padx=10, pady=10, anchor='w')
        # ================================
        # Panel de Instrucciones y Respuesta
        # ================================
        tk.Label(scrollable_frame, 
                text="INGRESA TU RESPUESTA", 
                font=('Arial', 16, 'bold'), 
                fg=self.colors['accent_yellow'], 
                bg="#0f1f0f").pack(pady=20)
        # Instrucciones
        instrucciones_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        instrucciones_frame.pack(fill='x', padx=20, pady=10)
        metodo_actual = self.metodos_desactivacion_asignados[self.problema_actual_desactivacion]
        respuesta_actual = self.respuestas_desactivacion[self.problema_actual_desactivacion]
        # Lógica de instrucciones para diferentes tipos de problemas
        if isinstance(respuesta_actual, list) and len(respuesta_actual) > 1:
            instrucciones_text = f"Resuelve el problema usando el método de **{metodo_actual}**.\nLa función tiene {len(respuesta_actual)} raíces válidas. Cualquiera de ellas es aceptable."
        elif isinstance(respuesta_actual, tuple):
            instrucciones_text = f"Resuelve el problema usando el método de **{metodo_actual}**.\nIngresa los valores de x, y, z en los campos correspondientes:"
        else:
            instrucciones_text = f"Resuelve el problema usando el método de **{metodo_actual}**.\nIngresa el valor numérico resultante:"
        instrucciones_label = tk.Label(instrucciones_frame, 
                                    text=instrucciones_text, 
                                    font=('Consolas', 12), 
                                    fg=self.colors['text_white'], 
                                    bg="#0f1f0f", 
                                    wraplength=800, 
                                    justify='left')
        instrucciones_label.pack(fill='x', padx=10, pady=10)
        # Campo de entrada
        entrada_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        entrada_frame.pack(padx=20, pady=10)
        tk.Label(entrada_frame, 
                text="Resultado:", 
                font=('Consolas', 12, 'bold'), 
                fg=self.colors['text_white'], 
                bg="#0f1f0f").pack(side='left', padx=10)
        # ESTO CREA self.entradas_sistema, NECESARIO PARA verificar_desactivacion
        if isinstance(respuesta_actual, tuple):
            self.entradas_sistema = {} # Inicializa el diccionario de entradas
            variables = ['x', 'y', 'z']
            for var in variables[:len(respuesta_actual)]:
                self.entradas_sistema[var] = tk.StringVar()
                tk.Label(entrada_frame, 
                        text=f"{var} =", 
                        font=('Consolas', 12), 
                        fg=self.colors['text_white'], 
                        bg="#0f1f0f").pack(side='left', padx=(20, 5))
                entry = tk.Entry(entrada_frame, 
                                textvariable=self.entradas_sistema[var], 
                                width=10, 
                                font=('Consolas', 12), 
                                justify='center', 
                                bg=self.colors['text_white'], 
                                fg='black')
                entry.pack(side='left')
                if var == 'x':
                    entry.focus_set()
        else:
            self.entrada_desactivacion = tk.StringVar()
            self.entrada_desactivacion_widget = tk.Entry(entrada_frame, 
                                                        textvariable=self.entrada_desactivacion, 
                                                        width=25, 
                                                        font=('Consolas', 12), 
                                                        justify='center', 
                                                        bg=self.colors['text_white'], 
                                                        fg='black')
            self.entrada_desactivacion_widget.pack(side='left', padx=10)
            self.entrada_desactivacion_widget.focus_set()
        # Botón de verificación
        btn_verificar = tk.Button(
            scrollable_frame, 
            text="✅ CORTAR CABLE", 
            font=('Consolas', 14, 'bold'), 
            fg="black", 
            bg=self.colors['accent_green'], 
            activebackground="#20b968",
            relief="flat", 
            padx=20, 
            pady=10,
            command=self.verificar_desactivacion
        )
        btn_verificar.pack(pady=30)
        # Botón de ayuda 
        btn_ayuda = tk.Button(
            scrollable_frame, 
            text=f"❓ Ayuda: {metodo_actual}", 
            font=('Consolas', 13, 'bold'), 
            fg="white", 
            bg=self.colors['accent_blue'], 
            activebackground="#2a77b3",
            relief="flat", 
            padx=10, 
            pady=5,
            command=self.mostrar_ayuda_desactivacion
        )
        btn_ayuda.pack(pady=(0, 20))
    def crear_panel_problema(self, parent):
        """Crea el panel que muestra el problema de desactivación"""
        problema_frame = tk.Frame(parent, bg=self.colors['light_bg'], relief='raised', bd=3)
        problema_frame.pack(expand=True, fill='both', pady=10)
        # Título del problema
        tk.Label(problema_frame,
                text=f"BOMBA {self.problema_actual_desactivacion + 1} - PROBLEMA DE DESACTIVACIÓN",
                font=('Arial', 16, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['light_bg']).pack(pady=15)
        # Descripción del problema
        descripcion_frame = tk.Frame(problema_frame, bg=self.colors['light_bg'])
        descripcion_frame.pack(expand=True, fill='both', padx=20, pady=10)
        problema_text = tk.Text(descripcion_frame,
                               font=('Arial', 12),
                               fg=self.colors['text_white'],
                               bg=self.colors['light_bg'],
                               wrap='word',
                               width=60,
                               height=15)
        problema_text.pack(expand=True, fill='both')
        problema_actual = self.problemas_desactivacion[self.problema_actual_desactivacion]
        problema_text.insert('1.0', problema_actual)
        problema_text.config(state='disabled')
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(descripcion_frame, orient='vertical', command=problema_text.yview)
        scrollbar.pack(side='right', fill='y')
        problema_text.config(yscrollcommand=scrollbar.set)
    def crear_panel_respuesta(self, parent):
        """Crea el panel para ingresar la respuesta con scroll"""
        # Frame principal que contendrá el canvas y scrollbar
        main_container = tk.Frame(parent, bg=self.colors['medium_bg'])
        main_container.pack(expand=True, fill='both')
        # Crear canvas y scrollbar
        canvas = tk.Canvas(main_container, bg=self.colors['medium_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(canvas, bg=self.colors['medium_bg'])
        # Configurar el scroll region cuando el frame se expanda
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        # Crear ventana en el canvas para el frame scrollable
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        # Configurar el canvas para usar el scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Ajustar el ancho del frame interno cuando cambie el tamaño del canvas
        def configurar_ancho_frame(event):
            canvas.itemconfig(1, width=event.width)  # 1 es el ID del window creado
        canvas.bind("<Configure>", configurar_ancho_frame)
        # ===== CONTENIDO DEL PANEL (dentro de scrollable_frame) =====
        tk.Label(scrollable_frame,
                text="INGRESA TU RESPUESTA",
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['medium_bg']).pack(pady=20)
        # Instrucciones
        instrucciones_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        instrucciones_frame.pack(fill='x', padx=20, pady=10)
        metodo_actual = self.metodos_desactivacion_asignados[self.problema_actual_desactivacion]
        respuesta_actual = self.respuestas_desactivacion[self.problema_actual_desactivacion]
        # Para ecuaciones no lineales con múltiples raíces válidas
        if isinstance(respuesta_actual, list) and len(respuesta_actual) > 1:
            instrucciones_text = f"Resuelve el problema usando el método de {metodo_actual}.\nLa función tiene {len(respuesta_actual)} raíces válidas. Cualquiera de ellas es aceptable."
        elif isinstance(respuesta_actual, tuple):
            instrucciones_text = f"Resuelve el problema usando el método de {metodo_actual}.\nIngresa los valores de x, y, z en los campos correspondientes:"
        else:
            instrucciones_text = f"Resuelve el problema usando el método de {metodo_actual}.\nIngresa el valor numérico resultante:"
        instrucciones_label = tk.Label(instrucciones_frame,
                                    text=instrucciones_text,
                                    font=('Arial', 10),
                                    fg=self.colors['text_gray'],
                                    bg=self.colors['medium_bg'],
                                    wraplength=300,
                                    justify='left')
        instrucciones_label.pack(anchor='w', pady=5)
        # Entrada de respuesta
        entrada_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        entrada_frame.pack(fill='x', padx=20, pady=20)
        # Si es un sistema de ecuaciones, creamos tres entradas, sino una
        if isinstance(respuesta_actual, tuple):
            self.entradas_desactivacion = []
            variables_frame = tk.Frame(entrada_frame, bg=self.colors['medium_bg'])
            variables_frame.pack(fill='x', pady=10)
            for i, variable in enumerate(['x', 'y', 'z']):
                sub_frame = tk.Frame(variables_frame, bg=self.colors['medium_bg'])
                sub_frame.pack(fill='x', pady=5)
                tk.Label(sub_frame, 
                        text=f"{variable}:", 
                        font=('Arial', 12), 
                        fg=self.colors['text_white'], 
                        bg=self.colors['medium_bg'],
                        width=5).pack(side='left')
                entry = tk.Entry(sub_frame, 
                            font=('Arial', 12), 
                            width=15, 
                            justify='center')
                entry.pack(side='left', padx=5, fill='x', expand=True)
                self.entradas_desactivacion.append(entry)
                # Enfocar el primer campo
                if i == 0:
                    entry.focus()
        else:
            self.entrada_desactivacion = tk.Entry(entrada_frame,
                                                font=('Arial', 14),
                                                width=20,
                                                justify='center')
            self.entrada_desactivacion.pack(fill='x', pady=10)
            self.entrada_desactivacion.focus()
        # Botones de acción
        botones_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        botones_frame.pack(fill='x', padx=20, pady=20)
        tk.Button(botones_frame,
                text="💣 VERIFICAR DESACTIVACIÓN",
                font=('Arial', 12, 'bold'),
                fg='white',
                bg=self.colors['accent_red'],
                relief='raised',
                bd=3,
                command=self.verificar_desactivacion).pack(fill='x', pady=5)
        tk.Button(botones_frame,
                text="📚 AYUDA DEL MÉTODO",
                font=('Arial', 12, 'bold'),
                fg='white',
                bg=self.colors['accent_blue'],
                relief='raised',
                bd=3,
                command=self.mostrar_ayuda_desactivacion).pack(fill='x', pady=5)
    def mostrar_interfaz_derrota(self):
        """Muestra la interfaz de game over cuando el jugador se queda sin vidas"""
        self.limpiar_interfaz()
        # Detener temporizador
        if hasattr(self, 'temporizador_id') and self.temporizador_id:
            try:
                self.root.after_cancel(self.temporizador_id)
            except:
                pass
            self.temporizador_id = None
        self.temporizador_activo = False
        # Fondo
        try:
            if not hasattr(self, 'bg_derrota'):
                self.bg_derrota = tk.PhotoImage(file="assets/fondo.png")
            bg_label = tk.Label(self.root, image=self.bg_derrota)
            bg_label.image = self.bg_derrota
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except:
            self.root.configure(bg="#1a0000")  # Rojo oscuro para derrota
        # Frame principal
        main_frame = tk.Frame(
            self.root,
            bg="#400000",
            bd=5,
            relief="ridge",
            highlightbackground="#ff0000",
            highlightthickness=3
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=850, height=700)
        # Icono de derrota
        try:
            if not hasattr(self, 'icon_derrota'):
                self.icon_derrota = tk.PhotoImage(file="assets/derrota.png")
            lbl_icono = tk.Label(main_frame, image=self.icon_derrota, bg="#400000")
            lbl_icono.image = self.icon_derrota
            lbl_icono.pack(pady=20)
        except:
            tk.Label(main_frame, text="💀", font=("Arial", 80), bg="#400000", fg="#ff0000").pack(pady=20)
        # Título
        tk.Label(
            main_frame,
            text="GAME OVER",
            font=("Consolas", 36, "bold"),
            fg="#ff0000",
            bg="#400000"
        ).pack(pady=10)
        # Mensaje
        tk.Label(
            main_frame,
            text="¡Te has quedado sin vidas!",
            font=("Consolas", 18, "bold"),
            fg="#ff6b6b",
            bg="#400000"
        ).pack(pady=10)
        # Estadísticas
        stats_frame = tk.Frame(main_frame, bg="#400000")
        stats_frame.pack(pady=20)
        tk.Label(
            stats_frame,
            text=f"Nivel alcanzado: {self.nivel_actual}",
            font=("Consolas", 14),
            fg="#ffffff",
            bg="#400000"
        ).pack(pady=5)
        tk.Label(
            stats_frame,
            text=f"Puntos totales: {self.puntos}",
            font=("Consolas", 14),
            fg="#ffffff",
            bg="#400000"
        ).pack(pady=5)
        # Botones
        botones_frame = tk.Frame(main_frame, bg="#400000")
        botones_frame.pack(pady=30)
        def reiniciar():
            self.reiniciar_juego()
        def volver_menu():
            self.crear_menu_principal()
        # Botón Reiniciar
        btn_reiniciar = tk.Button(
            botones_frame,
            text="🔄 REINICIAR",
            font=("Consolas", 14, "bold"),
            fg="white",
            bg="#e74c3c",
            activebackground="#c0392b",
            relief="flat",
            padx=20,
            pady=10,
            command=reiniciar
        )
        btn_reiniciar.pack(fill="x", pady=10)
        # Botón Menú Principal
        btn_menu = tk.Button(
            botones_frame,
            text="🏠 MENÚ PRINCIPAL",
            font=("Consolas", 14, "bold"),
            fg="white",
            bg="#34495e",
            activebackground="#2c3e50",
            relief="flat",
            padx=20,
            pady=10,
            command=volver_menu
        )
        btn_menu.pack(fill="x", pady=10)
    def verificar_desactivacion(self):
        # Asumiendo que self.tolerancia está definido en __init__ (ej: self.tolerancia = 0.0001)
        if not hasattr(self, 'tolerancia'):
            self.tolerancia = 0.0001
        respuesta_correcta = self.respuestas_desactivacion[self.problema_actual_desactivacion]
        es_sistema = isinstance(respuesta_correcta, tuple)
        respuesta_usuario_formateada = None
        # 1. Obtener la respuesta(s) del usuario
        if es_sistema:
            # Lógica para sistemas de ecuaciones (Montante, Gauss-Jordan, etc.)
            respuestas_usuario = []
            try:
                # Recorre los campos de entrada de las variables (x, y, z)
                for var in self.entradas_sistema:
                    valor_str = self.entradas_sistema[var].get().replace(',', '.')
                    respuestas_usuario.append(float(valor_str))
                respuesta_usuario_formateada = tuple(respuestas_usuario)
            except ValueError:
                messagebox.showerror("Error de entrada", "Asegúrate de ingresar solo números válidos en todos los campos (x, y, z).")
                return
        else:
            # Lógica para respuesta única (raíz, integral, etc.)
            try:
                valor_str = self.entrada_desactivacion.get().replace(',', '.')
                respuesta_usuario_formateada = float(valor_str)
            except AttributeError:
                messagebox.showerror("Error", "Problema interno: La interfaz no coincide con el tipo de respuesta esperado.")
                return
            except ValueError:
                messagebox.showerror("Error de entrada", "Asegúrate de ingresar un valor numérico válido.")
                return
        # 2. Verificar la respuesta
        acierto = False
        # 2.1. Comparación para sistemas (tupla)
        if es_sistema:
            if respuesta_usuario_formateada and len(respuesta_usuario_formateada) == len(respuesta_correcta):
                # Compara cada componente con la tolerancia
                acierto = all(abs(u - c) <= self.tolerancia for u, c in zip(respuesta_usuario_formateada, respuesta_correcta))
        # 2.2. Comparación para respuesta única (float o lista de floats)
        else:
            if isinstance(respuesta_correcta, list):
                # Ecuaciones no lineales con múltiples raíces válidas
                for raiz in respuesta_correcta:
                    if abs(respuesta_usuario_formateada - raiz) <= self.tolerancia:
                        acierto = True
                        break
            elif respuesta_usuario_formateada is not None:
                # Respuesta única estándar
                if abs(respuesta_usuario_formateada - respuesta_correcta) <= self.tolerancia:
                    acierto = True
        # 3. Manejo de resultado
        if acierto:
            messagebox.showinfo("¡Éxito!", "Cable cortado. ¡Explosivo desactivado!")
            self.problema_actual_desactivacion += 1
            if self.problema_actual_desactivacion < len(self.problemas_desactivacion):
                # Eliminar la bandera si el jugador ha acertado (para que el siguiente problema sea tiempo base)
                if hasattr(self, 'volviendo_de_integracion'):
                    del self.volviendo_de_integracion
                self.crear_interfaz_desactivacion()  # Siguiente explosivo
            else:
                self.siguiente_nivel() 
        else:
            self.vidas -= 1
            messagebox.showerror("¡ERROR!", f"Respuesta Incorrecta. Vidas restantes: {self.vidas}")
            # VERIFICAR SI SE QUEDÓ SIN VIDAS INMEDIATAMENTE
            if self.vidas <= 0:
                self.mostrar_interfaz_derrota()
                return
            # ==================================================
            # LÓGICA DE PENALIZACIÓN DE TIEMPO (Integración)
            # ==================================================
            if self.nivel_actual == 1:
                penalizacion_minutos = 30
            elif self.nivel_actual == 2:
                penalizacion_minutos = 25
            elif self.nivel_actual == 3:
                penalizacion_minutos = 20
            # Sumar la penalización de tiempo al tiempo restante
            self.tiempo_restante += penalizacion_minutos * 60
            # GUARDAR LA FASE ACTUAL PARA PODER VOLVER AL MISMO PROBLEMA
            self.fase_anterior = "desactivacion"
            # Establecer la bandera para que crear_interfaz_desactivacion mantenga el tiempo al volver
            self.volviendo_de_integracion = True 
            # Llamar a la fase de penalización (Integración)
            self.seleccionar_problema_integracion()
            self.crear_interfaz_integracion_emergencia()
    def seleccionar_problema_integracion(self):
            """Selecciona y genera un problema de integración para la penalización"""
            self.metodo_integracion_actual = random.choice(self.metodos_integracion)
            # Seleccionar función y límites según el método
            if self.metodo_integracion_actual == "Regla de 1/3 Simpson":
                # n debe ser par
                n = random.choice([2, 4, 6, 8])
                problema, respuesta = self.metodos_calculo.generar_problema_simpson13(n)
            elif self.metodo_integracion_actual == "Regla de 3/8 Simpson":
                # n debe ser múltiplo de 3
                n = random.choice([3, 6, 9])
                problema, respuesta = self.metodos_calculo.generar_problema_simpson38(n)
            elif self.metodo_integracion_actual == "Newton-Cotes Cerradas":
                n = random.choice([4, 5, 6, 7])
                problema, respuesta = self.metodos_calculo.generar_problema_newton_cotes_cerradas(n, self.constantes_newton_cotes_cerradas)
            elif self.metodo_integracion_actual == "Newton-Cotes Abiertas":
                n = random.choice([2, 3, 4, 5])
                problema, respuesta = self.metodos_calculo.generar_problema_newton_cotes_abiertas(n, self.constantes_newton_cotes_abiertas)
            else:  # Regla Trapezoidal
                n = random.choice([1, 2, 3, 4, 5])
                problema, respuesta = self.metodos_calculo.generar_problema_trapezoidal(n)
            self.problema_integracion_actual = problema
            self.respuesta_integracion_correcta = respuesta
            print(f"\n=== PROBLEMA DE INTEGRACIÓN (PENALIZACIÓN) ===")
            print(f"Método: {self.metodo_integracion_actual}")
            print(f"Problema: {problema}")
            print(f"Respuesta correcta: {respuesta}")

    def mostrar_resultado_desactivacion(self, exitoso):
        """Muestra el resultado de la desactivación"""
        if exitoso:
            # Bomba desactivada correctamente
            self.problema_actual_desactivacion += 1
            if self.problema_actual_desactivacion < len(self.problemas_desactivacion):
                # Hay más bombas por desactivar
                mensaje = f"🎉 ¡BOMBA {self.problema_actual_desactivacion} DESACTIVADA!"
                detalle = f"Pasando a la siguiente bomba...\n{self.problema_actual_desactivacion + 1}/{len(self.problemas_desactivacion)}"
                color = self.colors['accent_green']
                # Continuar con la siguiente bomba después de un breve retraso
                self.root.after(2000, self.crear_interfaz_desactivacion)
            else:
                # Todas las bombas desactivadas
                puntos_ganados = len(self.problemas_desactivacion) * 50
                self.puntos += puntos_ganados
                mensaje = "🎉 ¡TODAS LAS BOMBAS DESACTIVADAS!"
                detalle = f"Has ganado {puntos_ganados} puntos.\nPuntos totales: {self.puntos}"
                color = self.colors['accent_green']
                # Avanzar al siguiente nivel después de un breve retraso
                self.root.after(2000, self.siguiente_nivel)
        else:
            # Fallo en la desactivación
            mensaje = "💥 ¡BOMBA EXPLOTADA!"
            detalle = f"Has perdido una vida.\nVidas restantes: {self.vidas}"
            color = self.colors['accent_red']
            if self.vidas <= 0:
                detalle += "\n\n💀 GAME OVER"
                self.root.after(3000, self.reiniciar_juego)
            else:
                # Volver a interpolación después de un breve retraso
                self.root.after(3000, self.crear_interfaz_interpolacion)
        resultado_window = tk.Toplevel(self.root)
        resultado_window.title("RESULTADO DE DESACTIVACIÓN")
        resultado_window.geometry("400x200")
        resultado_window.configure(bg=self.colors['dark_bg'])
        resultado_window.transient(self.root)
        resultado_window.grab_set()
        # Centrar ventana
        resultado_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - resultado_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - resultado_window.winfo_height()) // 2
        resultado_window.geometry(f"+{x}+{y}")
        # Contenido
        tk.Label(resultado_window,
                text=mensaje,
                font=('Arial', 18, 'bold'),
                fg=color,
                bg=self.colors['dark_bg']).pack(expand=True, pady=20)
        tk.Label(resultado_window,
                text=detalle,
                font=('Arial', 12),
                fg=self.colors['text_white'],
                bg=self.colors['dark_bg']).pack(pady=10)
    def mostrar_ayuda_desactivacion(self):
        """Muestra ayuda sobre el método de desactivación actual"""
        metodo_actual = self.metodos_desactivacion_asignados[self.problema_actual_desactivacion]
        ayuda_textos = {
            "Interpolación lineal": """
INTERPOLACIÓN LINEAL
Fórmula:
y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
Donde:
- (x1, y1) y (x2, y2) son puntos conocidos
- x es el punto donde queremos interpolar
- y es el valor interpolado
Es el método más simple de interpolación.
""",
            "Montante": """
MÉTODO DE MONTANTE
Características:
- Método para resolver sistemas de ecuaciones lineales
- Similar a eliminación gaussiana pero sin división
- Utiliza determinantes
- Evita errores de redondeo al evitar divisiones
Para sistemas 3x3, ingresa los valores de x, y, z en los campos correspondientes.
""",
            "Gauss-Jordan": """
MÉTODO DE GAUSS-JORDAN
Pasos:
1. Escribir la matriz aumentada del sistema
2. Convertir la matriz a forma escalonada reducida
3. Leer las soluciones directamente
Ventajas:
- Proporciona la solución directamente
- No requiere sustitución hacia atrás
Para sistemas 3x3, ingresa los valores de x, y, z en los campos correspondientes.
""",
            "Eliminación Gaussiana": """
ELIMINACIÓN GAUSSIANA
Pasos:
1. Escribir la matriz aumentada
2. Convertir a forma escalonada
3. Realizar sustitución hacia atrás
Es el método más común para resolver sistemas lineales.
Para sistemas 3x3, ingresa los valores de x, y, z en los campos correspondientes.
""",
            "Gauss-Seidel": """
MÉTODO DE GAUSS-SEIDEL
Características:
- Método iterativo para sistemas lineales
- Actualiza variables una por una
- Converge más rápido que Jacobi
- Requiere matriz diagonalmente dominante para convergencia garantizada
Para sistemas 3x3, ingresa los valores de x, y, z en los campos correspondientes.
""",
            "Jacobi": """
MÉTODO DE JACOBI
Características:
- Método iterativo para sistemas lineales
- Actualiza todas las variables simultáneamente
- Más lento que Gauss-Seidel
- Fácil de paralelizar
Para sistemas 3x3, ingresa los valores de x, y, z en los campos correspondientes.
""",
            "Bisección": """
MÉTODO DE LA BISECCIÓN
Pasos:
1. Encontrar intervalo [a,b] donde f(a)*f(b) < 0
2. Calcular punto medio c = (a+b)/2
3. Reemplazar a o b con c según el signo de f(c)
4. Repetir hasta alcanzar la precisión deseada
Ventajas:
- Garantiza convergencia
- Simple de implementar
Desventajas:
- Convergencia lenta
- Necesita intervalo con cambio de signo
""",
            "Falsa Posición": """
MÉTODO DE LA FALSA POSICIÓN (Regula Falsi)
Similar a bisección pero usa interpolación lineal:
c = (a*f(b) - b*f(a)) / (f(b) - f(a))
Ventajas:
- Generalmente converge más rápido que bisección
- Garantiza convergencia
Desventajas:
- Puede ser lento para algunas funciones
- Necesita intervalo con cambio de signo
""",
            "Punto Fijo": """
MÉTODO DEL PUNTO FIJO
Transforma f(x)=0 en x = g(x)
Iteración: x_{n+1} = g(x_n)
Condiciones de convergencia:
- |g'(x)| < 1 en la región de interés
- g(x) continua
Ventajas:
- Simple de implementar
- No necesita derivadas
Desventajas:
- No siempre converge
- La elección de g(x) es crítica
""",
            "Newton-Raphson": """
MÉTODO DE NEWTON-RAPHSON
Iteración: x_{n+1} = x_n - f(x_n)/f'(x_n)
Características:
- Convergencia cuadrática (muy rápida)
- Requiere cálculo de derivada
- Puede divergir si el valor inicial es malo
Ventajas:
- Muy rápido cuando converge
- Preciso
Desventajas:
- Necesita derivada de la función
- Sensible al valor inicial
""",
            "Secante": """
MÉTODO DE LA SECANTE
Similar a Newton-Raphson pero usa aproximación de la derivada:
x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
Ventajas:
- No requiere cálculo de derivada
- Convergencia superlineal
Desventajas:
- Necesita dos puntos iniciales
- Más lento que Newton-Raphson
- Puede divergir
""",
            "Euler modificado": """
MÉTODO DE EULER MODIFICADO
MÉTODO: Euler Modificado
Fórmula:
y_{n+1} = y_n + h * ( f(y_n, t_n) + f(y_{n+1}, t_{n+1}) ) / 2
Ventajas:
- Más exacto que Euler hacia adelante.
- Excelente estabilidad.
- Fácil de implementar.
Desventajas:
- Método implícito: a veces requiere despejar y_{n+1}.
- Puede necesitar iteraciones internas.
""",
            "Runge-Kutta de 2° orden": """
MÉTODO DE RUNGE-KUTTA DE 2° ORDEN (RK2)
Fórmulas:
k1 = h * f(y_n, t_n)
k2 = h * f(y_n + k1, t_n + h)
y_{n+1} = y_n + 0.5 * (k1 + k2)
Ventajas:
- Más exacto que Euler y Euler modificado.
- Fácil de programar.
- Requiere poca memoria.
Desventajas:
- Menos preciso que RK3 y RK4.
- Puede requerir pasos pequeños para estabilidad.
""",
            "Runge-Kutta de 3° orden": """
MÉTODO DE RUNGE-KUTTA DE 3° ORDEN (RK3)
Fórmulas:
k1 = h * f(y_n, t_n)
k2 = h * f(y_n + k1/2, t_n + h/2)
k3 = h * f(y_n - k1 + 2*k2, t_n + h)
y_{n+1} = y_n + (1/6) * (k1 + 4*k2 + k3)
Ventajas:
- Buen equilibrio entre precisión y costo.
- Más preciso que RK2.
Desventajas:
- Menos utilizado que RK4.
- No tan estable ni preciso como RK4.
""",
            "Runge-Kutta de 4° orden": """
MÉTODO DE RUNGE-KUTTA DE 4° ORDEN (RK4)- 1/3 DE SIMPSON
Fórmulas:
k1 = h * f(y_n, t_n)
k2 = h * f(y_n + k1/2, t_n + h/2)
k3 = h * f(y_n + k2/2, t_n + h/2)
k4 = h * f(y_n + k3, t_n + h)
y_{n+1} = y_n + (1/6)*(k1 + 2*k2 + 2*k3 + k4)
Ventajas:
- Muy exacto.
- Alta estabilidad.
- Es el estándar en ingeniería.
Desventajas:
- Requiere 4 evaluaciones de f por iteración.
- Más lento que métodos simples como Euler.
""",
            "Runge-Kutta de 4° orden": """
MÉTODO DE RUNGE-KUTTA DE 4° ORDEN (RK4)- 3/8 DE SIMPSON
Fórmulas:
k1 = h * f(y_n, t_n)
k2 = h * f(y_n + k1/3, t_n + h/3)
k3 = h * f(y_n + k1/3 + k2/3, t_n + 2h/3)
k4 = h * f(y_n + k1 - k2 + k3, t_n + h)
y_{n+1} = y_n + (1/8)*(k1 + 3*k2 + 3*k3 + k4)
Ventajas:
- Misma precisión que RK4.
- Puede ser útil en funciones con comportamientos especiales.
Desventajas:
- Menos conocido.
- En algunos casos menos estable que RK4 clásico.
""",
            "Runge-Kutta de orden superior": """
MÉTODO DE RUNGE-KUTTA DE ORDEN SUPERIOR
Fórmulas generales:
k1 = h * V_n
m1 = h * (a*V_n + b*U_n)
k2 = h * (V_n + m1)
m2 = h * (a*(V_n + m1) + b*(U_n + k1))
y_{n+1} = y_n + 0.5 * (k1 + k2)
y'_{n+1} = y'_n + 0.5 * (m1 + m2)
Ventajas:
- Mucha exactitud para ecuaciones de orden 2.
- Útil en problemas físicos avanzados.
Desventajas:
- Extenso y costoso computacionalmente.
- Más difícil de implementar.
""",
    "Linea Recta (Minimos cuadrados)": """
REGRESIÓN LINEAL (MC)
Ajusta una recta y = a0 + a1*x.
Minimiza la suma de los errores al cuadrado entre los datos reales y la recta.
Sistema:
n*a0 + Σx*a1 = Σy
Σx*a0 + Σx²*a1 = Σxy
""",
            "Lineal con funcion(MC)": """
MC CON FUNCIÓN (LINEAL)
Ajusta modelos como y = a*e^x o y = a*x^b linealizándolos primero (usando logaritmos) para aplicar mínimos cuadrados estándar.
""",
            "Cuadratica con funcion(MC)": """
MC CON FUNCIÓN (CUADRÁTICA)
Similar al lineal con función, pero se usa cuando la relación transformada requiere un polinomio de segundo grado para ajustarse bien a los datos transformados.
""",
            "Cuadratica(MC)": """
REGRESIÓN CUADRÁTICA (POLINOMIAL)
Ajusta una parábola: y = a0 + a1*x + a2*x².
Se genera un sistema de 3x3 ecuaciones normales (sumatorias de x, x², x³, x⁴).
""",
            "Cubica(MC)": """
REGRESIÓN CÚBICA (POLINOMIAL)
Ajusta un polinomio de grado 3: y = a0 + a1*x + a2*x² + a3*x³.
Permite modelar curvas con cambios de concavidad (punto de inflexión).
Requiere resolver un sistema de 4x4.
""",
"Regla Trapezoidal": """
REGLA TRAPEZOIDAL
Fórmula: ∫f(x)dx ≈ (h/2) * [f(x₀) + 2f(x₁) + ... + f(xₙ)]
Aproxima el área bajo la curva usando trapecios.
""",
            "Regla de 1/3 Simpson": """
REGLA DE 1/3 DE SIMPSON
Fórmula: ∫f(x)dx ≈ (h/3) * [f(x₀) + 4f(x₁) + 2f(x₂) + ... + f(xₙ)]
Requiere que 'n' sea PAR. Usa parábolas para aproximar.
""",
            "Regla de 3/8 Simpson": """
REGLA DE 3/8 DE SIMPSON
Fórmula: ∫f(x)dx ≈ (3h/8) * [f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + ... + f(xₙ)]
Requiere que 'n' sea MÚLTIPLO DE 3.
""",
            "Newton-Cotes Cerradas": """
NEWTON-COTES CERRADAS
Usa puntos equiespaciados INCLUYENDO los extremos.
Los coeficientes dependen del grado 'n'.
""",
            "Newton-Cotes Abiertas": """
NEWTON-COTES ABIERTAS
Usa puntos equiespaciados EXCLUYENDO los extremos.
Útil cuando la función no está definida en los límites.
"""
        }
        ayuda = ayuda_textos.get(metodo_actual, "Información no disponible para este método.")
        messagebox.showinfo(f"Ayuda - {metodo_actual}", ayuda)
    def siguiente_nivel(self):
        # Mostrar pantalla de victoria
        self.limpiar_interfaz()
        def go_menu():
            self.crear_menu_principal()
        def go_next():
            self.limpiar_interfaz()
            self.nivel_actual += 1
            if self.nivel_actual == 1:        # Normal (90 min)
                self.tiempo_limite = 90 * 60
            elif self.nivel_actual == 2:      # Difícil (60 min)
                self.tiempo_limite = 60 * 60
            elif self.nivel_actual >= 3:      # Experimentado (30 min)
                self.tiempo_limite = 30 * 60
            self.tiempo_restante = self.tiempo_limite
            self.crear_interfaz_interpolacion()

        vista = PantallaVictoria(self.root, go_menu, go_next,self.nivel_actual)
        vista.pack(fill="both", expand=True)
    def reiniciar_juego(self):
        # Detener temporizador si existe
        if hasattr(self, 'temporizador_id') and self.temporizador_id:
            try:
                self.root.after_cancel(self.temporizador_id)
            except:
                pass
            self.temporizador_id = None
        self.temporizador_activo = False
        self.nivel_actual = 1
        self.vidas = 3
        self.puntos = 0
        # Reiniciar tiempo a 90 minutos por defecto (nivel 1)
        self.tiempo_limite = 90 * 60
        self.tiempo_restante = self.tiempo_limite
        # Crear interfaz de inicio del juego
        self.crear_interfaz_interpolacion()
    def mostrar_ayuda_metodo(self):
        """Muestra ayuda sobre el método de interpolación actual"""
        ayuda_textos = {
            "Lagrange": """
INTERPOLACIÓN DE LAGRANGE
Fórmula:
P(x) = Σ [y_i * L_i(x)]
donde L_i(x) = Π (x - x_j) / (xi - x_j) para j ≠ i
Características:
- Fórmula directa y explícita
- Fácil de programar
- No requiere puntos equiespaciados
- Computacionalmente costosa para muchos puntos
""",
            "Newton hacia adelante": """
INTERPOLACIÓN DE NEWTON HACIA ADELANTE
Fórmula:
P(x) = f[x0] + f[x0,x1](x-x0) + f[x0,x1,x2](x-x0)(x-x1) + ...
Características:
- Usa diferencias finitas hacia adelante
- Ideal para puntos equiespaciados
- Fácil de actualizar agregando nuevos puntos
- Eficiente computacionalmente
""",
            "Newton hacia atrás": """
INTERPOLACIÓN DE NEWTON HACIA ATRÁS
Fórmula:
P(x) = f[xn] + f[xn-1,xn](x-xn) + f[xn-2,xn-1,xn](x-xn)(x-xn-1) + ...
Características:
- Usa diferencias finitas hacia atrás
- Ideal para puntos cerca del final del intervalo
- Similar eficiencia a Newton hacia adelante
- Útil para extrapolación
""",
            "Newton con diferencias divididas": """
INTERPOLACIÓN DE NEWTON CON DIFERENCIAS DIVIDIDAS
Fórmula:
P(x) = f[x0] + f[x0,x1](x-x0) + f[x0,x1,x2](x-x0)(x-x1) + ...
Características:
- Versión general del método de Newton
- Funciona con puntos no equiespaciados
- Construye tabla de diferencias divididas
- Muy versátil y ampliamente usado
"""
        }
        ayuda = ayuda_textos.get(self.metodo_actual, "Método no reconocido")
        messagebox.showinfo(f"Ayuda - {self.metodo_actual}", ayuda)
    def limpiar_interfaz(self):
        """Limpia toda la interfaz y detiene animaciones/temporizadores"""
        # Detener animación del título si existe
        if self.animacion_id:
            try:
                self.root.after_cancel(self.animacion_id)
            except:
                pass
            self.animacion_id = None
        # Detener temporizador si está activo
        if hasattr(self, 'temporizador_id') and self.temporizador_id:
            try:
                self.root.after_cancel(self.temporizador_id)
            except:
                pass
            self.temporizador_id = None
        self.temporizador_activo = False
        # Limpiar widgets
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def mostrar_problema_integracion_emergencia(self):
            """Muestra un problema de integración como última oportunidad para evitar perder el nivel"""
            # Guardar la fase actual para poder volver
            self.fase_anterior = self.fase_actual
            self.mostrar_problema_integracion = True
            self.generar_problema_integracion()
            self.crear_interfaz_integracion_emergencia()
    def generar_problema_integracion(self):
        """Genera un problema de integración con método específico"""
        self.metodo_integracion_actual = random.choice(self.metodos_integracion)
        # Seleccionar función y límites según el método
        if self.metodo_integracion_actual == "Regla de 1/3 Simpson":
            # n debe ser par
            n = random.choice([2, 4, 6, 8])
            problema, respuesta = self.metodos_calculo.generar_problema_simpson13(n)
        elif self.metodo_integracion_actual == "Regla de 3/8 Simpson":
            # n debe ser múltiplo de 3
            n = random.choice([3, 6, 9])
            problema, respuesta = self.metodos_calculo.generar_problema_simpson38(n)
        elif self.metodo_integracion_actual == "Newton-Cotes Cerradas":
            n = random.choice([4, 5, 6, 7])
            problema, respuesta = self.metodos_calculo.generar_problema_newton_cotes_cerradas(n, self.constantes_newton_cotes_cerradas)
        elif self.metodo_integracion_actual == "Newton-Cotes Abiertas":
            n = random.choice([2, 3, 4, 5])
            problema, respuesta = self.metodos_calculo.generar_problema_newton_cotes_abiertas(n, self.constantes_newton_cotes_abiertas)
        else:  # Regla Trapezoidal
            n = random.choice([1, 2, 3, 4, 5])
            problema, respuesta = self.metodos_calculo.generar_problema_trapezoidal(n)
        self.problema_integracion_actual = problema
        self.respuesta_integracion_correcta = respuesta
        print(f"\n=== PROBLEMA DE INTEGRACIÓN ===")
        print(f"Método: {self.metodo_integracion_actual}")
        print(f"Problema: {problema}")
        print(f"Respuesta correcta: {respuesta}")
    def crear_interfaz_integracion_emergencia(self):
        """Crea la interfaz completa para el problema de integración de emergencia"""
        self.limpiar_interfaz()
        self.fase_actual = "integracion_emergencia"
        # Fondo estilo militar
        try:
            if not hasattr(self, 'bg_juego'):
                self.bg_juego = tk.PhotoImage(file="assets/fondo.png")
            bg_label = tk.Label(self.root, image=self.bg_juego)
            bg_label.image = self.bg_juego 
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            self.root.configure(bg="#1a1a2e")
        # Frame principal con borde
        borde_principal = tk.Frame(
            self.root,
            bg="#0f1f0f",
            relief="ridge",
            bd=8
        )
        borde_principal.pack(expand=True, fill="both", padx=20, pady=20)
        main_frame = tk.Frame(borde_principal, bg="#0b2c0b")
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        # Header de emergencia
        header_frame = tk.Frame(main_frame, bg="#0f1f0f", relief='raised', bd=3)
        header_frame.pack(fill='x', pady=20, padx=20)
        # Botón de menú principal
        btn_menu = tk.Button(
            header_frame,
            text="🏠 Menú principal",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg=self.colors['dark_bg'],
            activebackground=self.colors['dark_bg'],
            activeforeground='white',
            relief='flat',
            command=self.crear_menu_principal
        )
        btn_menu.pack(side='right', padx=20, pady=10)
        # Título de emergencia - DIFERENTE SEGÚN LA FASE
        if hasattr(self, 'fase_anterior') and self.fase_anterior == "interpolacion":
            titulo_texto = "🚨 EMERGENCIA - FALLASTE EN INTERPOLACIÓN"
            instruccion_texto = "Has fallado en la interpolación. Resuelve este problema de integración para poder continuar con la interpolación."
        else:
            titulo_texto = "🚨 EMERGENCIA - FALLASTE EN DESACTIVACIÓN"
            instruccion_texto = "Has fallado en desactivar la bomba. Resuelve este problema de integración para poder continuar con la desactivación."
        tk.Label(header_frame,
                text=titulo_texto,
                font=('Arial', 20, 'bold'),
                fg=self.colors['accent_red'],
                bg="#0f1f0f").pack(pady=15)
        tk.Label(header_frame,
                text=instruccion_texto,
                font=('Arial', 14),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(pady=5)
        # Información de estado
        estado_frame = tk.Frame(header_frame, bg="#0f1f0f")
        estado_frame.pack(pady=10)
        tk.Label(estado_frame,
                text=f"Vidas restantes: {'❤️' * self.vidas}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_red'],
                bg="#0f1f0f").pack(side='left', padx=20)
        tk.Label(estado_frame,
                text=f"Método de integración: {self.metodo_integracion_actual}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_yellow'],
                bg="#0f1f0f").pack(side='left', padx=20)
        # TEMPORIZADOR - Usar el tiempo restante actual
        self.lbl_tiempo = tk.Label(
            estado_frame,
            text="",
            font=("Arial", 12, "bold"),
            fg="yellow",
            bg="#0f1f0f"
        )
        self.lbl_tiempo.pack(side='left', padx=20)
        # Actualizar el label del tiempo inmediatamente
        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        self.lbl_tiempo.config(text=f"⏳ Tiempo: {minutos:02d}:{segundos:02d}")
        # Reiniciar temporizador con el tiempo actual
        self.iniciar_temporizador(header_frame)
        # Contenedor de dos columnas
        content_frame = tk.Frame(main_frame, bg="#0b2c0b")
        content_frame.pack(expand=True, fill='both', pady=20)
        # Columna izquierda - Problema
        left_frame = tk.Frame(content_frame, bg="#0b2c0b", width=320)
        left_frame.pack(side='left', fill='both',expand=True, padx=10)
        self.crear_panel_problema_integracion(left_frame)
        # Columna derecha - Entrada de respuesta
        right_frame = tk.Frame(content_frame, bg="#0f1f0f", relief='sunken', bd=2, width=300)
        right_frame.pack(side='left', fill='y',expand=False, padx=10, pady=10)
        self.crear_panel_respuesta_integracion(right_frame)
    def crear_panel_respuesta_integracion(self, parent):
        """Crea el panel para ingresar la respuesta de integración con scroll"""
        # Frame principal que contendrá el canvas y scrollbar
        main_container = tk.Frame(parent, bg="#0f1f0f")
        main_container.pack(expand=True, fill='both')
        # Crear canvas y scrollbar
        canvas = tk.Canvas(main_container, bg="#0f1f0f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(canvas, bg="#0f1f0f")
        # Configurar el scroll region cuando el frame se expanda
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        # Crear ventana en el canvas para el frame scrollable
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        # Configurar el canvas para usar el scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Ajustar el ancho del frame interno cuando cambie el tamaño del canvas
        def configurar_ancho_frame(event):
            canvas.itemconfig(1, width=event.width)  # 1 es el ID del window creado
        canvas.bind("<Configure>", configurar_ancho_frame)
        # ===== CONTENIDO DEL PANEL (dentro de scrollable_frame) =====
        tk.Label(scrollable_frame,
                text="INGRESA EL VALOR DE LA INTEGRAL",
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_yellow'],
                bg="#0f1f0f").pack(pady=20)
        # Instrucciones
        instrucciones_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        instrucciones_frame.pack(fill='x', padx=20, pady=10)
        instrucciones_text = f"Resuelve el problema usando el método de {self.metodo_integracion_actual}.\nIngresa el valor numérico resultante:"
        instrucciones_label = tk.Label(instrucciones_frame,
                                    text=instrucciones_text,
                                    font=('Arial', 12),
                                    fg=self.colors['text_gray'],
                                    bg="#0f1f0f",
                                    wraplength=300,
                                    justify='left')
        instrucciones_label.pack(anchor='w', pady=5)
        # Información sobre tolerancia
        tolerancia_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        tolerancia_frame.pack(fill='x', padx=20, pady=5)
        tolerancia_text = "💡 NOTA: Se acepta un margen de error del 2% + 0.01 unidades"
        tolerancia_label = tk.Label(tolerancia_frame,
                                text=tolerancia_text,
                                font=('Arial', 10, 'italic'),
                                fg=self.colors['accent_yellow'],
                                bg="#0f1f0f",
                                wraplength=350,
                                justify='left')
        tolerancia_label.pack(anchor='w', pady=5)
        # Entrada de respuesta
        entrada_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        entrada_frame.pack(fill='x', padx=20, pady=20)
        tk.Label(entrada_frame,
                text="Valor de la integral:",
                font=('Arial', 14),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(pady=10)
        self.entrada_integracion = tk.Entry(entrada_frame,
                                        font=('Arial', 14),
                                        width=20,
                                        justify='center',
                                        bg='white',
                                        fg='black')
        self.entrada_integracion.pack(fill='x', pady=10)
        self.entrada_integracion.focus()
        # Botones de acción
        botones_frame = tk.Frame(scrollable_frame, bg="#0f1f0f")
        botones_frame.pack(fill='x', padx=20, pady=20)
        btn_verificar = tk.Button(botones_frame,
                                text="✅ VERIFICAR INTEGRAL",
                                font=('Arial', 12, 'bold'),
                                fg='white',
                                bg=self.colors['accent_green'],
                                relief='raised',
                                bd=3,
                                command=self.verificar_integracion_emergencia)
        btn_verificar.pack(fill='x', pady=5)
        btn_ayuda = tk.Button(botones_frame,
                            text="📚 AYUDA DEL MÉTODO",
                            font=('Arial', 12, 'bold'),
                            fg='white',
                            bg=self.colors['accent_blue'],
                            relief='raised',
                            bd=3,
                            command=self.mostrar_ayuda_integracion)
        btn_ayuda.pack(fill='x', pady=5)
    def verificar_integracion_emergencia(self):
        """Verifica la respuesta del problema de integración en la interfaz completa"""
        if not hasattr(self, 'entrada_integracion'):
            messagebox.showerror("Error", "No se pudo encontrar el campo de entrada. Intenta nuevamente.")
            return
        entrada = self.entrada_integracion.get().strip()
        if not entrada:
            messagebox.showerror("Error", "Por favor ingresa un valor para la integral.")
            return
        try:
            respuesta_usuario = self.parsear_entrada(entrada)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Formato de respuesta inválido. Ingresa un número válido.")
            return
        # Tolerancia relativa + pequeña tolerancia absoluta
        tolerancia = abs(self.respuesta_integracion_correcta) * 0.02 + 0.01
        if abs(respuesta_usuario - self.respuesta_integracion_correcta) <= tolerancia:
            # Respuesta correcta - volver a la fase anterior EXACTA donde falló
            messagebox.showinfo(
                "¡Éxito!",
                f"✅ ¡Correcto! Has calculado el área correctamente.\n"
                f"Puedes continuar con el problema donde te equivocaste.\n"
                f"Vidas restantes: {self.vidas}"
            )
            # Volver a la fase anterior según la fase guardada
            if hasattr(self, 'fase_anterior'):
                if self.fase_anterior == "interpolacion":
                    # Volver a interpolación con el MISMO problema
                    self.fase_actual = "interpolacion"
                    self.crear_interfaz_interpolacion(regenerar_problema=False)
                elif self.fase_anterior == "desactivacion":
                    # Volver a desactivación con el MISMO problema (misma bomba)
                    self.fase_actual = "desactivacion"
                    # NO incrementamos problema_actual_desactivacion, para que vuelva al mismo
                    self.crear_interfaz_desactivacion()
            else:
                # Por defecto volver a interpolación
                self.fase_actual = "interpolacion"
                self.crear_interfaz_interpolacion(regenerar_problema=False)
        else:
            # Respuesta incorrecta - GAME OVER INMEDIATO (sin importar la fase)
            messagebox.showerror(
                "Error",
                f"❌ Incorrecto. La respuesta era: {self.respuesta_integracion_correcta:.6f}\n"
                f"Has fallado en calcular el área de la explosión.\n"
                f"💀 NIVEL PERDIDO"
            )
            # Mostrar interfaz de derrota inmediatamente
            self.mostrar_interfaz_derrota()
    def crear_panel_problema_integracion(self, parent):
        """Crea el panel que muestra el problema de integración"""
        problema_frame = tk.Frame(parent, bg="#0f1f0f", relief='raised', bd=3)
        problema_frame.pack(expand=True, fill='both', pady=10)
        # Título del problema
        tk.Label(problema_frame,
                text="PROBLEMA DE INTEGRACIÓN - CALCULA EL ÁREA",
                font=('Arial', 16, 'bold'),
                fg=self.colors['text_white'],
                bg="#0f1f0f").pack(pady=15)
        # Descripción del problema
        descripcion_frame = tk.Frame(problema_frame, bg="#0f1f0f")
        descripcion_frame.pack(expand=True, fill='both', padx=20, pady=10)
        problema_text = tk.Text(descripcion_frame,
                            font=('Arial', 12),
                            fg=self.colors['text_white'],
                            bg="#0f1f0f",
                            wrap='word',
                            width=60,
                            height=15)
        problema_text.pack(expand=True, fill='both')
        problema_text.insert('1.0', f"Resuelve la siguiente integral:\n\n{self.problema_integracion_actual}")
        problema_text.config(state='disabled')
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(descripcion_frame, orient='vertical', command=problema_text.yview)
        scrollbar.pack(side='right', fill='y')
        problema_text.config(yscrollcommand=scrollbar.set)
    def verificar_integracion(self, window=None):
            """Verifica la respuesta del problema de integración.
            Devuelve True si la penalización termina (respuesta correcta o nivel perdido),
            y False si el usuario debe seguir intentando en la misma ventana.
            """
            # Verificar que el campo de entrada existe
            if not hasattr(self, 'entrada_integracion'):
                messagebox.showerror("Error", "No se pudo encontrar el campo de entrada. Intenta nuevamente.")
                return False
            entrada = self.entrada_integracion.get().strip()
            if not entrada:
                messagebox.showerror("Error", "Por favor ingresa un valor para la integral.")
                return False
            try:
                # Usamos el mismo parser que en el resto del juego
                respuesta_usuario = self.parsear_entrada(entrada)
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Formato de respuesta inválido. Ingresa un número válido.")
                return False
            # Tolerancia relativa + pequeña tolerancia absoluta
            tolerancia = abs(self.respuesta_integracion_correcta) * 0.02 + 0.01
            if abs(respuesta_usuario - self.respuesta_integracion_correcta) <= tolerancia:
                # Respuesta correcta
                messagebox.showinfo(
                    "¡Éxito!",
                    f"✅ ¡Correcto! Has calculado el área correctamente.\n"
                    f"Has perdido una vida pero puedes continuar.\n"
                    f"Vidas restantes: {self.vidas}"
                )
                # Volver a la fase anterior según la fase actual
                if self.fase_actual == "interpolacion":
                    self.crear_interfaz_interpolacion()
                else:
                    self.crear_interfaz_desactivacion()
                # Cerrar ventana de penalización si existe
                if window is not None:
                    window.destroy()
                return True
            else:
                # Respuesta incorrecta - perder el nivel
                messagebox.showerror(
                    "Error",
                    f"❌ Incorrecto. La respuesta era: {self.respuesta_integracion_correcta:.6f}\n"
                    f"Has fallado en calcular el área de la explosión.\n"
                    f"💀 NIVEL PERDIDO"
                )
                # Reiniciar el juego
                self.reiniciar_juego()
                # Cerrar ventana de penalización si existe
                if window is not None:
                    window.destroy()
                return True
    def mostrar_ayuda_integracion(self):
            """Muestra ayuda sobre el método de integración actual"""
            ayuda_textos = {
                "Regla Trapezoidal": """
        REGLA TRAPEZOIDAL
        Fórmula:
        ∫f(x)dx ≈ (h/2) * [f(x₀) + 2f(x₁) + 2f(x₂) + ... + 2f(xₙ₋₁) + f(xₙ)]
        Donde:
        - h = (b - a)/n
        - n = número de subintervalos
        - x₀ = a, xₙ = b
        Características:
        - Aproxima el área bajo la curva con trapecios
        - Exacta para funciones lineales
        - Error proporcional a h²
        """,
                "Regla de 1/3 Simpson": """
        REGLA DE 1/3 DE SIMPSON
        Fórmula:
        ∫f(x)dx ≈ (h/3) * [f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + 4f(xₙ₋₁) + f(xₙ)]
        Donde:
        - h = (b - a)/n
        - n DEBE SER PAR
        - x₀ = a, xₙ = b
        Características:
        - Aproxima con parábolas
        - Exacta para polinomios de grado ≤ 3
        - Error proporcional a h⁴
        - Más precisa que trapezoidal
        """,
                "Regla de 3/8 Simpson": """
        REGLA DE 3/8 DE SIMPSON
        Fórmula:
        ∫f(x)dx ≈ (3h/8) * [f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + 3f(x₄) + ... + 3f(xₙ₋₁) + f(xₙ)]
        Donde:
        - h = (b - a)/n
        - n DEBE SER MÚLTIPLO DE 3
        - x₀ = a, xₙ = b
        Características:
        - Aproxima con polinomios cúbicos
        - Exacta para polinomios de grado ≤ 3
        - Error similar a 1/3 Simpson
        """,
                "Newton-Cotes Cerradas": """
        NEWTON-COTES CERRADAS
        Fórmula general:
        ∫f(x)dx ≈ α · (b - a) · Σ [cᵢ · f(xᵢ)]
        Características:
        - Usa puntos equiespaciados INCLUDYENDO extremos
        - Diferentes grados (n) disponibles
        - Coeficientes específicos para cada n
        - Incluye Trapezoidal (n=1) y Simpson (n=2,3)
        - Para n par, exacta para polinomios de grado n+1
        """,
                "Newton-Cotes Abiertas": """
        NEWTON-COTES ABIERTAS
        Fórmula general:
        ∫f(x)dx ≈ α · (b - a) · Σ [cᵢ · f(xᵢ)]
        Características:
        - Usa puntos equiespaciados EXCLUYENDO extremos
        - Diferentes grados (n) disponibles
        - Coeficientes específicos para cada n
        - Útil cuando los valores en extremos no están disponibles
        - Generalmente menos precisa que fórmulas cerradas
        """
            }
            ayuda = ayuda_textos.get(self.metodo_integracion_actual, "Información no disponible para este método.")
            # Agregar constantes específicas para Newton-Cotes
            if self.metodo_integracion_actual == "Newton-Cotes Cerradas":
                n_actual = None
                # Determinar n actual basado en el problema
                for n in self.constantes_newton_cotes_cerradas:
                    if f"n={n}" in self.problema_integracion_actual:
                        n_actual = n
                        break
                if n_actual:
                    const = self.constantes_newton_cotes_cerradas[n_actual]
                    ayuda += f"\n\nConstantes para n={n_actual}:\n"
                    ayuda += f"α = {const['alpha']}\n"
                    ayuda += f"Coeficientes: {const['coef']}"
            elif self.metodo_integracion_actual == "Newton-Cotes Abiertas":
                n_actual = None
                for n in self.constantes_newton_cotes_abiertas:
                    if f"n={n}" in self.problema_integracion_actual:
                        n_actual = n
                        break
                if n_actual:
                    const = self.constantes_newton_cotes_abiertas[n_actual]
                    ayuda += f"\n\nConstantes para n={n_actual}:\n"
                    ayuda += f"α = {const['alpha']}\n"
                    ayuda += f"Coeficientes: {const['coef']}"
            messagebox.showinfo(f"Ayuda - {self.metodo_integracion_actual}", ayuda) 

# ============= PANTALLA DE VICTORIA =============
class PantallaVictoria(tk.Frame):
    def __init__(self, master, callback_menu, callback_next, nivel_actual):
        super().__init__(master, bg="#0b1a0b")
        self.nivel_actual = nivel_actual
        
        # --- Configuración del Fondo ---
        try:
            self.bg_image = tk.PhotoImage(file="assets/fondo.png")
            bg_label = tk.Label(self, image=self.bg_image)
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Error cargando fondo:", e)
            self.configure(bg="#0a0f0a")
        
        container = tk.Frame(
            self,
            bg="#0b1a0b",
            width=950,
            height=650,
            highlightbackground="#00ff99",
            highlightthickness=6
        )
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(True)
        container.grid_propagate(True)

        # Título
        title_text = "✨🏆 ¡NIVEL SUPERADO! 🏆✨" if nivel_actual < 3 else "🎉🎓 ¡MISIÓN CUMPLIDA! 🎓🎉"
        title = tk.Label(
            container, 
            text=title_text,
            font=("Arial", 42, "bold"),
            fg="#00ff99",
            bg="#0b1a0b"
        )
        title.pack(pady=40)

        # Barra brillante
        glow = tk.Frame(container, bg="#00ff99", height=6)
        glow.pack(fill="x", padx=150, pady=10)

        # Mensaje
        msg_text = '''¡Has demostrado precisión y habilidad!
Continúa con la siguiente misión.''' if nivel_actual < 3 else '''¡Felicidades! Has completado todos los niveles.
Eres un experto en Métodos Numéricos.'''
        
        msg = tk.Label(
            container,
            text=msg_text,
            font=("Arial", 18, "italic"),
            fg="#c4ffd9",
            bg="#0b1a0b"
        )
        msg.pack(pady=20)

        # --- Botón Subir Archivo (Siempre visible al inicio) ---
        btn_upload = tk.Button(
            container,
            text="📄 Subir archivo de procedimientos",
            font=("Arial", 18, "bold"),
            bg="#1a3d6b", fg="white",
            activebackground="#335a9b",
            activeforeground="white",
            command=self.subir_archivo
        )  
        btn_upload.pack(pady=20, ipadx=20, ipady=10)

        # --- Botón Siguiente Nivel (Se guarda en self, NO se muestra aún) ---
        self.btn_next = tk.Button(
            container, text="➡ Siguiente Nivel",
            font=("Arial", 16, "bold"),
            bg="#004d26", fg="white",
            activebackground="#00994d",
            activeforeground="white",
            command=callback_next
        )

        # --- Botón Menú (Se guarda en self para manipularlo) ---
        self.btn_menu = tk.Button(
            container, text="🏠 Menú Principal",
            font=("Arial", 18, "bold"),
            bg="#1c1c3c", fg="white",
            activebackground="#32326b",
            activeforeground="white",
            command=callback_menu
        )

        # LÓGICA DE INICIO:
        # Si es Nivel 1 o 2: Mostramos el botón de Menú desde el principio.
        # Si es Nivel 3: NO mostramos el botón de Menú todavía (solo subir archivo).
        if self.nivel_actual < 3:
            self.btn_menu.pack(pady=10, ipadx=25, ipady=12)

        # Footer
        footer = tk.Label(
            container, 
            text="¡Excelente trabajo, soldado! 🚀",
            font=("Arial", 16, "italic"),
            fg="#9effc9",
            bg="#0b1a0b"
        )
        footer.pack(side="bottom", pady=30)

    def subir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona tu archivo de procedimientos",
            filetypes=[("Documento PDF", "*.pdf")]
        )
        if not ruta:
            return
        
        # Validar extensión
        if not ruta.lower().endswith(".pdf"):
            messagebox.showerror("Archivo inválido", "Debes seleccionar un archivo PDF.")
            return
        
        # Validar tamaño (2MB)
        try:
            size_kb = os.path.getsize(ruta) / (1024 * 1024) # en MB
            minimo_mb = 2.0
            
            if size_kb < minimo_mb:
                messagebox.showerror("Archivo insuficiente",
                                     f"El PDF debe pesar al menos {minimo_mb} MB.\n"
                                     f"El archivo actual pesa {size_kb:.2f} MB.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            return
        
        messagebox.showinfo("Archivo cargado", "Archivo válido. Procedimientos verificados.")
        
        # LÓGICA POST-SUBIDA:
        if self.nivel_actual < 3:
            # Niveles 1 y 2: Aparece el botón "Siguiente Nivel"
            self.btn_next.pack(pady=10, ipadx=25, ipady=12, before=self.btn_menu)
        else:
            # Nivel 3: Aparece el botón "Menú Principal" (que estaba oculto)
            self.btn_menu.pack(pady=20, ipadx=25, ipady=12)