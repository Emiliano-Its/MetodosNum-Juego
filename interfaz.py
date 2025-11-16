import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import random
import math
from metodos import MetodosCalculo

class MathDefuserGame:
    def __init__(self, root):
        self.root = root
        self.root.title("💣 MATH DEFUSER - INTERPOLACIÓN DE BOMBAS")
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
            "Bisección",
            "Falsa Posición",
            "Punto Fijo",
            "Newton-Raphson",
            "Secante"
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
        
        self.crear_interfaz_interpolacion()
    
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
        self.metodo_actual = random.choice(self.metodos_interpolacion)
        
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
        inicio = random.randint(x_min, x_max - (num_puntos - 1) * paso)
        
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
        
        # Generar 2-3 bombas objetivo en diferentes posiciones (siempre enteras)
        num_objetivos = random.randint(2, 3)
        
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

    def crear_interfaz_interpolacion(self):
        """Crea la interfaz para la fase de interpolación"""
        self.limpiar_interfaz()
        self.fase_actual = "interpolacion"
        
        # Generar nuevo problema
        self.generar_problema_aleatorio()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['dark_bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Header informativo
        header_frame = tk.Frame(main_frame, bg=self.colors['medium_bg'], relief='raised', bd=2)
        header_frame.pack(fill='x', pady=10)
        
        tk.Label(header_frame, 
                text=f"💣 NIVEL {self.nivel_actual} - INTERPOLACIÓN DE BOMBAS",
                font=('Arial', 20, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['medium_bg']).pack(pady=15)
        
        # Información del método
        metodo_frame = tk.Frame(header_frame, bg=self.colors['medium_bg'])
        metodo_frame.pack(pady=10)
        
        tk.Label(metodo_frame,
                text="MÉTODO ASIGNADO:",
                font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['medium_bg']).pack(side='left', padx=10)
        
        tk.Label(metodo_frame,
                text=self.metodo_actual,
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_green'],
                bg=self.colors['medium_bg']).pack(side='left', padx=10)
        
        # Información adicional sobre el tipo de puntos
        info_puntos_frame = tk.Frame(header_frame, bg=self.colors['medium_bg'])
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
                bg=self.colors['medium_bg']).pack()
        
        # Información de estado
        estado_frame = tk.Frame(header_frame, bg=self.colors['medium_bg'])
        estado_frame.pack(pady=10)
        
        tk.Label(estado_frame,
                text=f"VIDAS: {'❤️' * self.vidas}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_red'],
                bg=self.colors['medium_bg']).pack(side='left', padx=20)
        
        tk.Label(estado_frame,
                text=f"PUNTOS: {self.puntos}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['medium_bg']).pack(side='left', padx=20)
        
        tk.Label(estado_frame,
                text=f"BOMBAS A ENCONTRAR: {len(self.x_objetivo)}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_blue'],
                bg=self.colors['medium_bg']).pack(side='left', padx=20)
        
        # Contenedor de dos columnas
        content_frame = tk.Frame(main_frame, bg=self.colors['dark_bg'])
        content_frame.pack(expand=True, fill='both', pady=20)
        
        # Columna izquierda - Campo de batalla
        left_frame = tk.Frame(content_frame, bg=self.colors['dark_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        self.crear_campo_batalla(left_frame)
        
        # Columna derecha - Panel de control
        right_frame = tk.Frame(content_frame, bg=self.colors['medium_bg'], relief='sunken', bd=2)
        right_frame.pack(side='right', fill='both', padx=10, pady=10)
        
        self.crear_panel_control(right_frame)
    
    def crear_campo_batalla(self, parent):
        """Crea la visualización del campo de batalla"""
        campo_frame = tk.Frame(parent, bg=self.colors['light_bg'], relief='raised', bd=3)
        campo_frame.pack(expand=True, fill='both', pady=10)
        
        # Título del campo
        tk.Label(campo_frame,
                text="CAMPO DE BATALLA - DISTRIBUCIÓN DE BOMBAS",
                font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['light_bg']).pack(pady=10)
        
        # Canvas para dibujar el campo
        self.canvas = tk.Canvas(campo_frame, 
                               bg='#2c3e50',
                               highlightthickness=0)
        self.canvas.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Actualizar el canvas después de que se haya renderizado
        self.root.after(100, self.dibujar_campo_batalla)
    
    def dibujar_campo_batalla(self):
        """Dibuja las bombas en el campo de batalla"""
        self.canvas.delete("all")
        
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()
        
        if ancho <= 1 or alto <= 1:
            self.root.after(100, self.dibujar_campo_batalla)
            return
        
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
        
        # Asegurar que el rango no sea cero
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
                                  fill='#34495e', width=1, dash=(2, 4))
            self.canvas.create_text(x_pixel, alto - 30, text=f"{x}m", 
                                  fill=self.colors['text_gray'], font=('Arial', 10))
        
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
                                      fill=self.colors['accent_yellow'], width=2)
            
            # Coordenadas
            self.canvas.create_text(x_pixel, y_pixel-30, 
                                  text=f"({x}, {y:.1f})", 
                                  fill=self.colors['text_white'], font=('Arial', 8, 'bold'))
        
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
        """Crea el panel de control para ingresar respuestas"""
        # Crear un frame con scrollbar
        container = tk.Frame(parent, bg=self.colors['medium_bg'])
        container.pack(fill='both', expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(container, bg=self.colors['medium_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['medium_bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido del panel
        tk.Label(scrollable_frame,
                text="PANEL DE INTERPOLACIÓN",
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['medium_bg']).pack(pady=20)
        
        # Información de bombas explotadas
        info_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        info_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(info_frame,
                text="BOMBAS EXPLOTADAS (Puntos conocidos):",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['medium_bg']).pack(anchor='w')
        
        puntos_text = "\n".join([f"• ({x}, {y:.4f})" for x, y in sorted(self.puntos_detonados)])
        puntos_label = tk.Label(info_frame,
                               text=puntos_text,
                               font=('Arial', 10),
                               fg=self.colors['text_gray'],
                               bg=self.colors['medium_bg'],
                               justify='left')
        puntos_label.pack(anchor='w', pady=5)
        
        # Información de bombas a encontrar
        objetivo_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        objetivo_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(objetivo_frame,
                text="BOMBAS A ENCONTRAR (Coordenadas X):",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['medium_bg']).pack(anchor='w')
        
        objetivo_text = ", ".join([f"X = {x}" for x in self.x_objetivo])
        objetivo_label = tk.Label(objetivo_frame,
                                 text=objetivo_text,
                                 font=('Arial', 12, 'bold'),
                                 fg=self.colors['accent_blue'],
                                 bg=self.colors['medium_bg'])
        objetivo_label.pack(anchor='w', pady=5)
        
        # Instrucciones
        instrucciones_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        instrucciones_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(instrucciones_frame,
                text="INSTRUCCIONES:",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['medium_bg']).pack(anchor='w')
        
        instrucciones_text = f"Usa el método {self.metodo_actual} para calcular las coordenadas Y de las bombas en las posiciones X dadas."
        instrucciones_label = tk.Label(instrucciones_frame,
                                      text=instrucciones_text,
                                      font=('Arial', 10),
                                      fg=self.colors['text_gray'],
                                      bg=self.colors['medium_bg'],
                                      wraplength=350,
                                      justify='left')
        instrucciones_label.pack(anchor='w', pady=5)
        
        # Información sobre tolerancia
        tolerancia_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        tolerancia_frame.pack(fill='x', padx=20, pady=5)
        
        tolerancia_text = "💡 NOTA: Se acepta un margen de error del 0.5% + 0.01 unidades para cálculos manuales"
        tolerancia_label = tk.Label(tolerancia_frame,
                                   text=tolerancia_text,
                                   font=('Arial', 9, 'italic'),
                                   fg=self.colors['accent_yellow'],
                                   bg=self.colors['medium_bg'],
                                   wraplength=350,
                                   justify='left')
        tolerancia_label.pack(anchor='w', pady=5)
        
        # Entradas para las bombas objetivo
        entradas_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
        entradas_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(entradas_frame,
                text="INGRESA LAS COORDENADAS Y CALCULADAS:",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['medium_bg']).pack(anchor='w', pady=10)
        
        self.entradas = {}
        
        for x in self.x_objetivo:
            entrada_frame = tk.Frame(entradas_frame, bg=self.colors['medium_bg'])
            entrada_frame.pack(fill='x', pady=5)
            
            tk.Label(entrada_frame,
                    text=f"Para X = {x} | Y =",
                    font=('Arial', 10),
                    fg=self.colors['text_white'],
                    bg=self.colors['medium_bg']).pack(side='left')
            
            entry = tk.Entry(entrada_frame,
                           font=('Arial', 10),
                           width=15,
                           justify='center')
            entry.pack(side='left', padx=5)
            self.entradas[x] = entry
        
        # Botones de acción
        botones_frame = tk.Frame(scrollable_frame, bg=self.colors['medium_bg'])
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
        
        tk.Button(botones_frame,
                 text="🔄 NUEVO PROBLEMA",
                 font=('Arial', 12, 'bold'),
                 fg='white',
                 bg=self.colors['accent_yellow'],
                 relief='raised',
                 bd=3,
                 command=self.crear_interfaz_interpolacion).pack(fill='x', pady=5)
    
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
        """Verifica las respuestas del usuario con tolerancia adaptativa"""
        correctas = 0
        total = len(self.x_objetivo)
        
        resultados = []
        
        for x in self.x_objetivo:
            entrada = self.entradas[x].get().strip()
            y_correcta = self.respuestas_correctas[x]
            
            # Calcular tolerancia adaptativa basada en la magnitud del valor
            if y_correcta == 0:
                tolerancia = 0.01
            else:
                # Tolerancia relativa: 0.5% del valor + tolerancia base
                tolerancia = abs(y_correcta) * 0.005 + 0.01
            
            try:
                # Permitir diferentes formatos de entrada
                y_usuario = self.parsear_entrada(entrada)
                
                # Verificar si la respuesta es correcta dentro de la tolerancia
                if abs(y_usuario - y_correcta) <= tolerancia:
                    correctas += 1
                    resultados.append((x, y_correcta, y_usuario, True, tolerancia))
                else:
                    resultados.append((x, y_correcta, y_usuario, False, tolerancia))
                    
            except (ValueError, TypeError):
                # Entrada inválida
                resultados.append((x, y_correcta, "ENTRADA INVÁLIDA", False, tolerancia))
        
        # Mostrar resultados
        self.mostrar_resultados(resultados, correctas, total)
    
    def mostrar_resultados(self, resultados, correctas, total):
        """Muestra los resultados de la verificación con información de tolerancia"""
        # Crear ventana de resultados
        resultados_window = tk.Toplevel(self.root)
        resultados_window.title("RESULTADOS DE INTERPOLACIÓN")
        resultados_window.geometry("600x500")
        resultados_window.configure(bg=self.colors['dark_bg'])
        resultados_window.transient(self.root)
        resultados_window.grab_set()
        
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
        encabezados = ["X", "Y Correcta", "Y Ingresada", "Tolerancia", "Resultado"]
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
            
            # Y Correcta
            tk.Label(tabla_frame,
                    text=f"{y_correcta:.4f}",
                    font=('Arial', 9),
                    fg=self.colors['text_white'],
                    bg=self.colors['medium_bg']).grid(row=i, column=1, padx=5, pady=2)
            
            # Y Ingresada
            color_ingresado = self.colors['accent_green'] if correcto else self.colors['accent_red']
            texto_ingresado = str(y_usuario) if isinstance(y_usuario, (int, float)) else y_usuario
            tk.Label(tabla_frame,
                    text=texto_ingresado,
                    font=('Arial', 9),
                    fg=color_ingresado,
                    bg=self.colors['medium_bg']).grid(row=i, column=2, padx=5, pady=2)
            
            # Tolerancia usada
            tk.Label(tabla_frame,
                    text=f"±{tolerancia:.4f}",
                    font=('Arial', 8),
                    fg=self.colors['text_gray'],
                    bg=self.colors['medium_bg']).grid(row=i, column=3, padx=5, pady=2)
            
            # Resultado
            resultado_texto = "✅ CORRECTO" if correcto else "❌ INCORRECTO"
            color_resultado = self.colors['accent_green'] if correcto else self.colors['accent_red']
            tk.Label(tabla_frame,
                    text=resultado_texto,
                    font=('Arial', 9, 'bold'),
                    fg=color_resultado,
                    bg=self.colors['medium_bg']).grid(row=i, column=4, padx=5, pady=2)
        
        # Configurar grid weights
        for i in range(5):
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
            # Mostrar problema de integración en lugar de reiniciar directamente
            tk.Button(botones_frame,
                     text="🧮 RESOLVER PROBLEMA DE INTEGRACIÓN",
                     font=('Arial', 12, 'bold'),
                     fg='white',
                     bg=self.colors['accent_blue'],
                     command=lambda: [resultados_window.destroy(), self.mostrar_problema_integracion_emergencia()]).pack(fill='x', pady=5)
        else:
            tk.Button(botones_frame,
                     text="💀 GAME OVER - REINICIAR",
                     font=('Arial', 12, 'bold'),
                     fg='white',
                     bg=self.colors['accent_red'],
                     command=lambda: [resultados_window.destroy(), self.reiniciar_juego()]).pack(fill='x', pady=5)
    
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
        metodos_disponibles = self.metodos_desactivacion.copy()
        random.shuffle(metodos_disponibles)
        
        # Si hay más bombas que métodos, repetimos algunos métodos
        while len(metodos_disponibles) < num_bombas:
            metodos_disponibles.extend(self.metodos_desactivacion)
        
        for i in range(num_bombas):
            metodo = metodos_disponibles[i]
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
        """Crea la interfaz para la fase de desactivación"""
        self.limpiar_interfaz()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['dark_bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Header informativo
        header_frame = tk.Frame(main_frame, bg=self.colors['medium_bg'], relief='raised', bd=2)
        header_frame.pack(fill='x', pady=10)
        
        tk.Label(header_frame, 
                text=f"💣 NIVEL {self.nivel_actual} - DESACTIVACIÓN DE BOMBAS ({self.problema_actual_desactivacion + 1}/{len(self.problemas_desactivacion)})",
                font=('Arial', 20, 'bold'),
                fg=self.colors['accent_red'],
                bg=self.colors['medium_bg']).pack(pady=15)
        
        # Información del método
        metodo_frame = tk.Frame(header_frame, bg=self.colors['medium_bg'])
        metodo_frame.pack(pady=10)
        
        tk.Label(metodo_frame,
                text="MÉTODO DE DESACTIVACIÓN:",
                font=('Arial', 14, 'bold'),
                fg=self.colors['text_white'],
                bg=self.colors['medium_bg']).pack(side='left', padx=10)
        
        metodo_actual = self.metodos_desactivacion_asignados[self.problema_actual_desactivacion]
        tk.Label(metodo_frame,
                text=metodo_actual,
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_green'],
                bg=self.colors['medium_bg']).pack(side='left', padx=10)
        
        # Información de estado
        estado_frame = tk.Frame(header_frame, bg=self.colors['medium_bg'])
        estado_frame.pack(pady=10)
        
        tk.Label(estado_frame,
                text=f"VIDAS: {'❤️' * self.vidas}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_red'],
                bg=self.colors['medium_bg']).pack(side='left', padx=20)
        
        tk.Label(estado_frame,
                text=f"PUNTOS: {self.puntos}",
                font=('Arial', 12, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['medium_bg']).pack(side='left', padx=20)
        
        # Contenedor de dos columnas
        content_frame = tk.Frame(main_frame, bg=self.colors['dark_bg'])
        content_frame.pack(expand=True, fill='both', pady=20)
        
        # Columna izquierda - Problema
        left_frame = tk.Frame(content_frame, bg=self.colors['dark_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        self.crear_panel_problema(left_frame)
        
        # Columna derecha - Entrada de respuesta
        right_frame = tk.Frame(content_frame, bg=self.colors['medium_bg'], relief='sunken', bd=2)
        right_frame.pack(side='right', fill='both', padx=10, pady=10)
        
        self.crear_panel_respuesta(right_frame)
    
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
        """Crea el panel para ingresar la respuesta"""
        respuesta_frame = tk.Frame(parent, bg=self.colors['medium_bg'])
        respuesta_frame.pack(expand=True, fill='both')
        
        tk.Label(respuesta_frame,
                text="INGRESA TU RESPUESTA",
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['medium_bg']).pack(pady=20)
        
        # Instrucciones
        instrucciones_frame = tk.Frame(respuesta_frame, bg=self.colors['medium_bg'])
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
        entrada_frame = tk.Frame(respuesta_frame, bg=self.colors['medium_bg'])
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
        botones_frame = tk.Frame(respuesta_frame, bg=self.colors['medium_bg'])
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
    
    def verificar_desactivacion(self):
        """Verifica la respuesta de desactivación con soporte para múltiples raíces válidas"""
        respuesta_correcta = self.respuestas_desactivacion[self.problema_actual_desactivacion]
        
        try:
            if isinstance(respuesta_correcta, tuple):
                # Para sistemas de ecuaciones 3x3, leemos tres entradas
                valores = []
                for entry in self.entradas_desactivacion:
                    valor = entry.get().strip()
                    if valor == '':
                        raise ValueError("Falta un valor")
                    valores.append(self.parsear_entrada(valor))
                
                correcto = True
                for i, (usuario, correcta) in enumerate(zip(valores, respuesta_correcta)):
                    tolerancia = abs(correcta) * 0.01 + 0.01
                    if abs(usuario - correcta) > tolerancia:
                        correcto = False
                        break
            
            elif isinstance(respuesta_correcta, list):
                # Para ecuaciones no lineales con múltiples raíces válidas
                entrada = self.entrada_desactivacion.get().strip()
                if entrada == '':
                    raise ValueError("La entrada está vacía")
                    
                respuesta_usuario = self.parsear_entrada(entrada)
                correcto = False
                
                # Verificar contra todas las raíces válidas
                for raiz in respuesta_correcta:
                    tolerancia = abs(raiz) * 0.01 + 0.01
                    if abs(respuesta_usuario - raiz) <= tolerancia:
                        correcto = True
                        break
            
            else:
                # Para problemas de una sola respuesta
                entrada = self.entrada_desactivacion.get().strip()
                if entrada == '':
                    raise ValueError("La entrada está vacía")
                    
                respuesta_usuario = self.parsear_entrada(entrada)
                tolerancia = abs(respuesta_correcta) * 0.01 + 0.01
                correcto = abs(respuesta_usuario - respuesta_correcta) <= tolerancia
            
            if correcto:
                self.mostrar_resultado_desactivacion(True)
            else:
                self.vidas -= 1
                if self.vidas > 0:
                    # Mostrar problema de integración en lugar de resultado directo
                    self.mostrar_problema_integracion_emergencia()
                else:
                    self.mostrar_resultado_desactivacion(False)
                
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Formato de respuesta inválido: {str(e)}")
    
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
"""
        }
        
        ayuda = ayuda_textos.get(metodo_actual, "Información no disponible para este método.")
        messagebox.showinfo(f"Ayuda - {metodo_actual}", ayuda)
    
    def siguiente_nivel(self):
        """Avanza al siguiente nivel"""
        self.nivel_actual += 1
        self.crear_interfaz_interpolacion()
    
    def reiniciar_juego(self):
        """Reinicia el juego"""
        self.nivel_actual = 1
        self.vidas = 3
        self.puntos = 0
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
        """Limpia toda la interfaz"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # NUEVAS FUNCIONES PARA INTEGRACIÓN

    def mostrar_problema_integracion_emergencia(self):
        """Muestra un problema de integración como última oportunidad para evitar perder el nivel"""
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
        """Crea la interfaz para el problema de integración de emergencia"""
        self.limpiar_interfaz()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['dark_bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Header de emergencia
        header_frame = tk.Frame(main_frame, bg=self.colors['accent_red'], relief='raised', bd=3)
        header_frame.pack(fill='x', pady=10)
        
        tk.Label(header_frame, 
                text="🚨 EMERGENCIA - CALCULA EL ÁREA DE LA EXPLOSIÓN",
                font=('Arial', 20, 'bold'),
                fg='white',
                bg=self.colors['accent_red']).pack(pady=15)
        
        tk.Label(header_frame,
                text="¡Has fallado! Resuelve este problema de integración para evitar perder el nivel.",
                font=('Arial', 14),
                fg='white',
                bg=self.colors['accent_red']).pack(pady=10)
        
        # Información del método
        metodo_frame = tk.Frame(header_frame, bg=self.colors['accent_red'])
        metodo_frame.pack(pady=10)
        
        tk.Label(metodo_frame,
                text="MÉTODO DE INTEGRACIÓN:",
                font=('Arial', 14, 'bold'),
                fg='white',
                bg=self.colors['accent_red']).pack(side='left', padx=10)
        
        tk.Label(metodo_frame,
                text=self.metodo_integracion_actual,
                font=('Arial', 16, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['accent_red']).pack(side='left', padx=10)
        
        # Información de estado
        estado_frame = tk.Frame(header_frame, bg=self.colors['accent_red'])
        estado_frame.pack(pady=10)
        
        tk.Label(estado_frame,
                text=f"VIDAS RESTANTES: {'❤️' * self.vidas}",
                font=('Arial', 12, 'bold'),
                fg='white',
                bg=self.colors['accent_red']).pack(side='left', padx=20)
        
        # Contenedor de contenido
        content_frame = tk.Frame(main_frame, bg=self.colors['dark_bg'])
        content_frame.pack(expand=True, fill='both', pady=20)
        
        # Panel del problema
        problema_frame = tk.Frame(content_frame, bg=self.colors['light_bg'], relief='raised', bd=3)
        problema_frame.pack(expand=True, fill='both', pady=10)
        
        tk.Label(problema_frame,
                text="PROBLEMA DE INTEGRACIÓN",
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
                               width=80,
                               height=12)
        problema_text.pack(expand=True, fill='both')
        
        problema_text.insert('1.0', self.problema_integracion_actual)
        problema_text.config(state='disabled')
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(descripcion_frame, orient='vertical', command=problema_text.yview)
        scrollbar.pack(side='right', fill='y')
        problema_text.config(yscrollcommand=scrollbar.set)
        
        # Panel de respuesta - CORREGIDO CON BOTÓN VISIBLE
        respuesta_frame = tk.Frame(content_frame, bg=self.colors['medium_bg'], relief='sunken', bd=2)
        respuesta_frame.pack(fill='x', pady=10)
        
        tk.Label(respuesta_frame,
                text="INGRESA TU RESPUESTA:",
                font=('Arial', 14, 'bold'),
                fg=self.colors['accent_yellow'],
                bg=self.colors['medium_bg']).pack(pady=10)
        
        # Frame simple para la entrada
        entrada_frame = tk.Frame(respuesta_frame, bg=self.colors['medium_bg'])
        entrada_frame.pack(pady=10)
        
        tk.Label(entrada_frame,
                text="Valor de la integral:",
                font=('Arial', 12),
                fg=self.colors['text_white'],
                bg=self.colors['medium_bg']).pack(side='left', padx=5)
        
        # CREAR EL CAMPO DE ENTRADA DE MANERA DIRECTA
        self.entrada_integracion = tk.Entry(entrada_frame,
                                          font=('Arial', 14),
                                          width=20,
                                          justify='center',
                                          bg='white',
                                          fg='black')
        self.entrada_integracion.pack(side='left', padx=5)
        self.entrada_integracion.focus()
        
        # Botones en un frame simple - CORREGIDO PARA QUE SE VEAN LOS BOTONES
        botones_frame = tk.Frame(respuesta_frame, bg=self.colors['medium_bg'])
        botones_frame.pack(pady=10)
        
        # Botón VERIFICAR INTEGRAL - AHORA DEBERÍA SER VISIBLE
        btn_verificar = tk.Button(botones_frame,
                 text="✅ VERIFICAR INTEGRAL",
                 font=('Arial', 12, 'bold'),
                 fg='white',
                 bg=self.colors['accent_green'],
                 relief='raised',
                 bd=3,
                 command=self.verificar_integracion)
        btn_verificar.pack(side='left', padx=10, pady=5)
        
        # Botón AYUDA
        btn_ayuda = tk.Button(botones_frame,
                 text="📚 AYUDA DEL MÉTODO",
                 font=('Arial', 12, 'bold'),
                 fg='white',
                 bg=self.colors['accent_blue'],
                 relief='raised',
                 bd=3,
                 command=self.mostrar_ayuda_integracion)
        btn_ayuda.pack(side='left', padx=10, pady=5)

    def verificar_integracion(self):
        """Verifica la respuesta del problema de integración"""
        # Verificar que el campo de entrada existe
        if not hasattr(self, 'entrada_integracion'):
            messagebox.showerror("Error", "No se pudo encontrar el campo de entrada. Intenta nuevamente.")
            return
            
        entrada = self.entrada_integracion.get().strip()
        
        if not entrada:
            messagebox.showerror("Error", "Por favor ingresa un valor para la integral.")
            return
        
        try:
            respuesta_usuario = self.parsear_entrada(entrada)
            tolerancia = abs(self.respuesta_integracion_correcta) * 0.02 + 0.01
            
            if abs(respuesta_usuario - self.respuesta_integracion_correcta) <= tolerancia:
                # Respuesta correcta - solo pierde una vida y continúa
                messagebox.showinfo("¡Éxito!", 
                                  f"✅ ¡Correcto! Has calculado el área correctamente.\n"
                                  f"Has perdido una vida pero puedes continuar.\n"
                                  f"Vidas restantes: {self.vidas}")
                
                # Volver a la fase anterior
                if self.fase_actual == "interpolacion":
                    self.crear_interfaz_interpolacion()
                else:
                    self.crear_interfaz_desactivacion()
            else:
                # Respuesta incorrecta - perder el nivel
                messagebox.showerror("Error", 
                                   f"❌ Incorrecto. La respuesta era: {self.respuesta_integracion_correcta:.6f}\n"
                                   f"Has fallado en calcular el área de la explosión.\n"
                                   f"💀 NIVEL PERDIDO")
                self.reiniciar_juego()
                
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Formato de respuesta inválido. Ingresa un número válido.")

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