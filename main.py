import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import random
import math

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
        
        # Estado del juego
        self.nivel_actual = 1
        self.vidas = 3
        self.puntos = 0
        self.metodo_actual = None
        self.fase_actual = "interpolacion"
        
        # Datos del problema actual
        self.puntos_detonados = []
        self.bombas_ocultas = []  # Lista de tuplas (x, y_real)
        self.x_objetivo = []      # Valores X que el usuario debe encontrar
        self.funcion_real = None
        self.respuestas_correctas = {}
        
        # Datos para la fase de desactivación
        self.problemas_desactivacion = []  # Lista de problemas a resolver
        self.respuestas_desactivacion = [] # Lista de respuestas correctas
        self.metodos_desactivacion_asignados = []  # Métodos asignados para cada problema
        self.problema_actual_desactivacion = 0     # Índice del problema actual
        
        self.crear_interfaz_interpolacion()
    
    def generar_problema_aleatorio(self):
        """Genera un nuevo problema de interpolación con puntos bien distribuidos"""
        # Determinar complejidad según nivel
        if self.nivel_actual <= 2:
            grado = random.randint(2, 3)
            num_puntos = grado + 2  # Un punto extra para asegurar buena interpolación
        else:
            grado = random.randint(3, 4)
            num_puntos = grado + 3  # Más puntos para mayor precisión
        
        # Generar función polinómica realista
        if grado == 2:
            # ax² + bx + c
            coef = [random.uniform(-2, 2), random.uniform(-5, 5), random.uniform(-10, 10)]
        elif grado == 3:
            # ax³ + bx² + cx + d
            coef = [random.uniform(-1, 1), random.uniform(-3, 3), random.uniform(-5, 5), random.uniform(-10, 10)]
        else:  # grado 4
            # ax⁴ + bx³ + cx² + dx + e
            coef = [random.uniform(-0.5, 0.5), random.uniform(-2, 2), random.uniform(-3, 3), 
                    random.uniform(-5, 5), random.uniform(-10, 10)]
        
        self.funcion_real = np.poly1d(coef)
        
        # Generar rango de X bien distribuido
        x_min = 0
        x_max = num_puntos + 3
        
        # Crear conjunto de X bien distribuidas (mezcla pares e impares)
        todas_x = list(range(x_min, x_max + 1))
        
        # Seleccionar puntos de referencia (bombas explotadas) bien distribuidos
        # Asegurar que haya puntos a ambos lados de los objetivos
        self.puntos_detonados = []
        
        # Siempre incluir puntos en los extremos
        extremos = [x_min, x_max]
        for x in extremos:
            if x in todas_x:
                y = float(self.funcion_real(x))
                self.puntos_detonados.append((x, y))
                todas_x.remove(x)
        
        # Seleccionar puntos internos bien distribuidos
        puntos_necesarios = num_puntos - len(self.puntos_detonados)
        if puntos_necesarios > 0:
            # Preferir puntos que no estén muy juntos
            x_internos = []
            while len(x_internos) < puntos_necesarios and todas_x:
                x_candidato = random.choice(todas_x)
                # Verificar que no esté muy cerca de puntos ya seleccionados
                demasiado_cerca = any(abs(x_candidato - p[0]) < 2 for p in self.puntos_detonados)
                if not demasiado_cerca:
                    x_internos.append(x_candidato)
                    todas_x.remove(x_candidato)
                else:
                    # Si no hay más opciones, tomar cualquier punto
                    x_internos.append(todas_x.pop(0))
            
            for x in x_internos:
                y = float(self.funcion_real(x))
                self.puntos_detonados.append((x, y))
        
        # Ordenar puntos por X
        self.puntos_detonados.sort(key=lambda p: p[0])
        
        # Generar bombas objetivo (X a interpolar)
        # Seleccionar puntos dentro del rango cubierto pero no en los puntos conocidos
        x_min_detonado = min(p[0] for p in self.puntos_detonados)
        x_max_detonado = max(p[0] for p in self.puntos_detonados)
        
        posibles_objetivos = []
        for x in range(x_min_detonado + 1, x_max_detonado):
            if x not in [p[0] for p in self.puntos_detonados]:
                # Verificar que no esté demasiado cerca de puntos conocidos
                cercano = any(abs(x - p[0]) <= 1 for p in self.puntos_detonados)
                if not cercano:
                    posibles_objetivos.append(x)
        
        # Si no hay suficientes objetivos, relajar el criterio
        if len(posibles_objetivos) < 3:
            for x in range(x_min_detonado + 1, x_max_detonado):
                if x not in [p[0] for p in self.puntos_detonados] and x not in posibles_objetivos:
                    posibles_objetivos.append(x)
        
        # Seleccionar 2-3 objetivos
        num_objetivos = min(3, len(posibles_objetivos))
        self.x_objetivo = random.sample(posibles_objetivos, num_objetivos)
        self.x_objetivo.sort()
        
        # Calcular valores reales de las bombas objetivo
        self.bombas_ocultas = [(x, float(self.funcion_real(x))) for x in self.x_objetivo]
        
        # Seleccionar método de interpolación
        self.metodo_actual = random.choice(self.metodos_interpolacion)
        
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
    
    def calcular_respuestas_correctas(self):
        """Calcula las respuestas correctas usando el método de interpolación asignado"""
        self.respuestas_correctas = {}
        
        # Ordenar puntos por X para los métodos que lo requieren
        puntos_ordenados = sorted(self.puntos_detonados, key=lambda p: p[0])
        
        for x_objetivo, y_real in self.bombas_ocultas:
            if self.metodo_actual == "Lagrange":
                y_calculado = self.interpolacion_lagrange(x_objetivo, puntos_ordenados)
            elif self.metodo_actual == "Newton hacia adelante":
                y_calculado = self.interpolacion_newton_adelante(x_objetivo, puntos_ordenados)
            elif self.metodo_actual == "Newton hacia atrás":
                y_calculado = self.interpolacion_newton_atras(x_objetivo, puntos_ordenados)
            else:  # Newton con diferencias divididas
                y_calculado = self.interpolacion_diferencias_divididas(x_objetivo, puntos_ordenados)
            
            self.respuestas_correctas[x_objetivo] = y_calculado
    
    def interpolacion_lagrange(self, x, puntos):
        """Interpolación de Lagrange"""
        resultado = 0.0
        n = len(puntos)
        
        for i in range(n):
            xi, yi = puntos[i]
            termino = yi
            
            for j in range(n):
                if i != j:
                    xj, yj = puntos[j]
                    termino *= (x - xj) / (xi - xj)
            
            resultado += termino
        
        return resultado
    
    def interpolacion_newton_adelante(self, x, puntos):
        """Interpolación de Newton hacia adelante"""
        puntos_ordenados = sorted(puntos, key=lambda p: p[0])
        n = len(puntos_ordenados)
        
        # Calcular diferencias divididas
        dif_div = self.calcular_diferencias_divididas(puntos_ordenados)
        
        # Aplicar fórmula de Newton hacia adelante
        resultado = puntos_ordenados[0][1]  # f(x0)
        producto = 1
        
        for i in range(1, n):
            producto *= (x - puntos_ordenados[i-1][0])
            resultado += dif_div[0][i] * producto
        
        return resultado
    
    def interpolacion_newton_atras(self, x, puntos):
        """Interpolación de Newton hacia atrás"""
        puntos_ordenados = sorted(puntos, key=lambda p: p[0])
        n = len(puntos_ordenados)
        
        # Calcular diferencias divididas
        dif_div = self.calcular_diferencias_divididas(puntos_ordenados)
        
        # Aplicar fórmula de Newton hacia atrás
        resultado = puntos_ordenados[-1][1]  # f(xn)
        producto = 1
        
        for i in range(1, n):
            producto *= (x - puntos_ordenados[n-i][0])
            resultado += dif_div[n-i-1][i] * producto
        
        return resultado
    
    def interpolacion_diferencias_divididas(self, x, puntos):
        """Interpolación con diferencias divididas (similar a Newton)"""
        # Para este juego, usaremos la misma implementación que Newton hacia adelante
        return self.interpolacion_newton_adelante(x, puntos)
    
    def calcular_diferencias_divididas(self, puntos):
        """Calcula la tabla de diferencias divididas"""
        n = len(puntos)
        x = [p[0] for p in puntos]
        y = [p[1] for p in puntos]
        
        # Inicializar tabla
        tabla = [[0] * n for _ in range(n)]
        
        # Primera columna son los valores de y
        for i in range(n):
            tabla[i][0] = y[i]
        
        # Calcular diferencias divididas
        for j in range(1, n):
            for i in range(n - j):
                tabla[i][j] = (tabla[i+1][j-1] - tabla[i][j-1]) / (x[i+j] - x[i])
        
        return tabla
    
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
                                  text=f"({x}, {y:.2f})", 
                                  fill=self.colors['text_white'], font=('Arial', 10, 'bold'))
        
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
                    y = self.interpolacion_lagrange(x, puntos_ordenados)
                else:
                    y = self.interpolacion_newton_adelante(x, puntos_ordenados)
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
            tk.Button(botones_frame,
                     text="🔄 REINTENTAR",
                     font=('Arial', 12, 'bold'),
                     fg='white',
                     bg=self.colors['accent_yellow'],
                     command=resultados_window.destroy).pack(fill='x', pady=5)
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
            problema, respuesta = self.generar_problema_por_metodo(metodo)
            
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
    
    def generar_problema_por_metodo(self, metodo):
        """Genera un problema específico para el método dado"""
        if metodo == "Interpolación lineal":
            return self.generar_problema_interpolacion_lineal()
        elif metodo in ["Montante", "Gauss-Jordan", "Eliminación Gaussiana"]:
            return self.generar_problema_sistema_ecuaciones(metodo)
        elif metodo in ["Gauss-Seidel", "Jacobi"]:
            return self.generar_problema_sistema_diagonal_dominante(metodo)
        else:  # Métodos para ecuaciones no lineales
            return self.generar_problema_ecuacion_no_lineal(metodo)
    
    def generar_problema_interpolacion_lineal(self):
        """Genera un problema de interpolación lineal con contexto específico"""
        # Diferentes tipos de problemas de interpolación lineal
        tipos_problemas = [
            {
                "nombre": "Logaritmo natural",
                "puntos": [(2, math.log(2)), (4, math.log(4))],
                "objetivo": 3,
                "texto": "ln(3)",
                "func": math.log
            },
            {
                "nombre": "Seno",
                "puntos": [(0, math.sin(0)), (math.pi/2, math.sin(math.pi/2))],
                "objetivo": math.pi/4,
                "texto": "sin(π/4)",
                "func": math.sin
            },
            {
                "nombre": "Coseno", 
                "puntos": [(0, math.cos(0)), (math.pi/2, math.cos(math.pi/2))],
                "objetivo": math.pi/3,
                "texto": "cos(π/3)",
                "func": math.cos
            },
            {
                "nombre": "Exponencial",
                "puntos": [(0, math.exp(0)), (2, math.exp(2))],
                "objetivo": 1,
                "texto": "e¹",
                "func": math.exp
            },
            {
                "nombre": "Raíz cuadrada",
                "puntos": [(1, math.sqrt(1)), (4, math.sqrt(4))],
                "objetivo": 2,
                "texto": "√2",
                "func": math.sqrt
            },
            {
                "nombre": "Logaritmo base 10",
                "puntos": [(1, math.log10(1)), (10, math.log10(10))],
                "objetivo": 5,
                "texto": "log₁₀(5)",
                "func": math.log10
            }
        ]
        
        tipo = random.choice(tipos_problemas)
        x1, y1 = tipo["puntos"][0]
        x2, y2 = tipo["puntos"][1]
        x_objetivo = tipo["objetivo"]
        texto_objetivo = tipo["texto"]
        
        # Calcular respuesta usando interpolación lineal
        respuesta = y1 + (y2 - y1) * (x_objetivo - x1) / (x2 - x1)
        
        problema = f"""
PROBLEMA DE INTERPOLACIÓN LINEAL:

Estima el valor de {texto_objetivo} usando interpolación lineal con los puntos conocidos:
- En x = {x1}, y = {y1:.4f}
- En x = {x2}, y = {y2:.4f}

¿Cuál es el valor estimado para x = {x_objetivo}?
"""
        return problema, respuesta
    
    def generar_problema_sistema_ecuaciones(self, metodo):
        """Genera un sistema de ecuaciones lineales 3x3 con coeficientes más variados"""
        # Generar solución aleatoria con más variedad
        x = random.randint(-8, 8)
        y = random.randint(-8, 8)
        z = random.randint(-8, 8)

        # Generar coeficientes más variados con negativos
        a11 = random.randint(-5, 5)
        a12 = random.randint(-5, 5)
        a13 = random.randint(-5, 5)
        a21 = random.randint(-5, 5)
        a22 = random.randint(-5, 5)
        a23 = random.randint(-5, 5)
        a31 = random.randint(-5, 5)
        a32 = random.randint(-5, 5)
        a33 = random.randint(-5, 5)

        # Asegurar que el sistema tenga solución única
        det = a11*(a22*a33 - a23*a32) - a12*(a21*a33 - a23*a31) + a13*(a21*a32 - a22*a31)
        if det == 0:
            # Usar coeficientes por defecto que tengan solución única
            a11, a12, a13 = 2, -3, 1
            a21, a22, a23 = -1, 2, 4
            a31, a32, a33 = 3, 1, -2

        # Calcular los términos independientes
        b1 = a11*x + a12*y + a13*z
        b2 = a21*x + a22*y + a23*z
        b3 = a31*x + a32*y + a33*z

        # Formatear los coeficientes para mostrar signos correctos
        def formato_coef(coef, variable):
            if coef == 0:
                return ""
            elif coef == 1:
                return f"+ {variable}" 
            elif coef == -1:
                return f"- {variable}"
            elif coef > 0:
                return f"+ {coef}{variable}"
            else:
                return f"- {abs(coef)}{variable}"

        # Construir las ecuaciones
        eq1 = f"{a11 if a11 != 1 else ''}{'x' if a11 != 0 else ''} {formato_coef(a12, 'y')} {formato_coef(a13, 'z')} = {b1}".strip()
        eq2 = f"{a21 if a21 != 1 else ''}{'x' if a21 != 0 else ''} {formato_coef(a22, 'y')} {formato_coef(a23, 'z')} = {b2}".strip()
        eq3 = f"{a31 if a31 != 1 else ''}{'x' if a31 != 0 else ''} {formato_coef(a32, 'y')} {formato_coef(a33, 'z')} = {b3}".strip()

        # Limpiar las ecuaciones (quitar espacios extra y posibles signos + al inicio)
        import re
        eq1 = re.sub(r'^\s*\+\s*', '', eq1)
        eq2 = re.sub(r'^\s*\+\s*', '', eq2)
        eq3 = re.sub(r'^\s*\+\s*', '', eq3)

        problema = f"""
PROBLEMA DE SISTEMA DE ECUACIONES (Método: {metodo}):

Resuelve el siguiente sistema 3x3 usando el método de {metodo}:

{eq1}
{eq2}
{eq3}

Ingresa los valores de x, y, z.
"""
        return problema, (x, y, z)
    
    def generar_problema_sistema_diagonal_dominante(self, metodo):
        """Genera un sistema 3x3 diagonalmente dominante para métodos iterativos"""
        # Generar solución
        x = random.uniform(-5, 5)
        y = random.uniform(-5, 5)
        z = random.uniform(-5, 5)

        # Generar coeficientes para una matriz diagonalmente dominante
        # Para cada fila, el valor absoluto del elemento diagonal es mayor que la suma de los valores absolutos de los otros elementos
        a11 = random.randint(8, 12)
        a12 = random.randint(-2, 2)
        a13 = random.randint(-2, 2)
        a21 = random.randint(-2, 2)
        a22 = random.randint(8, 12)
        a23 = random.randint(-2, 2)
        a31 = random.randint(-2, 2)
        a32 = random.randint(-2, 2)
        a33 = random.randint(8, 12)

        # Asegurar diagonal dominante
        if abs(a11) < abs(a12) + abs(a13):
            a11 = abs(a12) + abs(a13) + random.randint(1, 3)
        if abs(a22) < abs(a21) + abs(a23):
            a22 = abs(a21) + abs(a23) + random.randint(1, 3)
        if abs(a33) < abs(a31) + abs(a32):
            a33 = abs(a31) + abs(a32) + random.randint(1, 3)

        # Calcular términos independientes
        b1 = a11*x + a12*y + a13*z
        b2 = a21*x + a22*y + a23*z
        b3 = a31*x + a32*y + a33*z

        # Formatear
        def formato_coef(coef, variable):
            if coef == 0:
                return ""
            elif coef == 1:
                return f"+ {variable}" 
            elif coef == -1:
                return f"- {variable}"
            elif coef > 0:
                return f"+ {coef}{variable}"
            else:
                return f"- {abs(coef)}{variable}"

        eq1 = f"{a11 if a11 != 1 else ''}{'x' if a11 != 0 else ''} {formato_coef(a12, 'y')} {formato_coef(a13, 'z')} = {b1:.2f}".strip()
        eq2 = f"{a21 if a21 != 1 else ''}{'x' if a21 != 0 else ''} {formato_coef(a22, 'y')} {formato_coef(a23, 'z')} = {b2:.2f}".strip()
        eq3 = f"{a31 if a31 != 1 else ''}{'x' if a31 != 0 else ''} {formato_coef(a32, 'y')} {formato_coef(a33, 'z')} = {b3:.2f}".strip()

        # Limpiar
        import re
        eq1 = re.sub(r'^\s*\+\s*', '', eq1)
        eq2 = re.sub(r'^\s*\+\s*', '', eq2)
        eq3 = re.sub(r'^\s*\+\s*', '', eq3)

        problema = f"""
PROBLEMA DE SISTEMA DE ECUACIONES (Método: {metodo}):

Resuelve el siguiente sistema 3x3 usando el método de {metodo}:

{eq1}
{eq2}
{eq3}

Ingresa los valores de x, y, z.
"""
        return problema, (x, y, z)
    
    def generar_problema_ecuacion_no_lineal(self, metodo):
        """Genera un problema de ecuación no lineal más realista"""
        if metodo == "Bisección":
            # Generar ecuación cuadrática con raíces reales
            a = random.randint(1, 3)
            b = random.randint(-8, 8)
            c = random.randint(-10, 10)
            
            # Calcular raíces
            discriminante = b**2 - 4*a*c
            if discriminante >= 0:
                raiz1 = (-b + math.sqrt(discriminante)) / (2*a)
                raiz2 = (-b - math.sqrt(discriminante)) / (2*a)
                raices = [raiz1, raiz2]
                # Seleccionar una raíz que esté en un rango razonable
                raiz = random.choice([r for r in raices if -10 <= r <= 10])
            else:
                # Si no hay raíces reales, generar una nueva ecuación
                return self.generar_problema_ecuacion_no_lineal(metodo)
            
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de {metodo}:
{a}x² + {b}x + {c} = 0

La raíz debe encontrarse en un intervalo donde la función cambie de signo.
"""
            return problema, raiz
            
        elif metodo == "Newton-Raphson":
            # Ecuación trascendental realista
            tipo = random.choice(["exponencial", "trigonometrica"])
            
            if tipo == "exponencial":
                # f(x) = e^(-x) - x
                # Raíz: x ≈ 0.567143
                respuesta = 0.5671432904097838
                problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de {metodo}:
e^(-x) - x = 0

Usa el método de Newton-Raphson con un valor inicial apropiado.
"""
            else:  # trigonometrica
                # f(x) = x·cos(x) - ln(x)
                # Raíz alrededor de 1.2-1.3
                respuesta = 1.2926957193733982
                problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de {metodo}:
x·cos(x) - ln(x) = 0

Usa el método de Newton-Raphson con un valor inicial apropiado.
"""
            return problema, respuesta
        
        elif metodo == "Secante":
            # Ecuación mixta
            a = random.randint(1, 3)
            b = random.randint(1, 3)
            c = random.randint(-5, 5)
            
            # f(x) = a·sin(x) + b·cos(x) - c
            # Encontrar una raíz aproximada
            respuesta = random.uniform(0.5, 3)
            
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de {metodo}:
{a}·sin(x) + {b}·cos(x) - {c} = 0

Usa el método de la secante con dos puntos iniciales.
"""
            return problema, respuesta
        
        elif metodo == "Punto Fijo":
            # Generar una ecuación adecuada para Punto Fijo
            tipo = random.choice(["exponencial", "cubica", "trigonometrica"])
            if tipo == "exponencial":
                # Ecuación: e^(-x) - x = 0  -> x = e^(-x)
                # La raíz está alrededor de 0.567
                respuesta = 0.5671432904097838
                problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de Punto Fijo:
e^(-x) - x = 0

Transforma la ecuación a la forma x = e^(-x) y aplica el método.
"""
            elif tipo == "cubica":
                # Ecuación: x³ - x - 1 = 0 -> x = (x + 1)^(1/3)
                # Raíz real: aproximadamente 1.3247
                respuesta = 1.324717957244746
                problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de Punto Fijo:
x³ - x - 1 = 0

Transforma la ecuación a una forma adecuada x = g(x) y aplica el método.
"""
            else: # trigonometrica
                # Ecuación: sin(x) - x/2 = 0 -> x = 2*sin(x)
                # Raíz alrededor de 1.895
                respuesta = 1.8954942670339809
                problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de Punto Fijo:
sin(x) - x/2 = 0

Transforma la ecuación a la forma x = 2*sin(x) y aplica el método.
"""
            return problema, respuesta
        
        else:  # Falsa Posición
            # Ecuación polinomial o racional
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            c = random.randint(-8, 8)
            
            # Encontrar raíces de ecuación cuadrática
            discriminante = b**2 - 4*a*c
            if discriminante >= 0:
                raiz1 = (-b + math.sqrt(discriminante)) / (2*a)
                raiz2 = (-b - math.sqrt(discriminante)) / (2*a)
                raices = [raiz1, raiz2]
                # Seleccionar una raíz que esté en un rango razonable
                respuesta = random.choice([r for r in raices if -10 <= r <= 10])
            else:
                respuesta = random.uniform(-5, 5)
            
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra una raíz de la ecuación usando el método de {metodo}:
{a}x² + {b}x + {c} = 0

La raíz debe encontrarse en un intervalo donde la función cambie de signo.
"""
            return problema, respuesta
    
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
        
        instrucciones_text = f"Resuelve el problema usando el método de {metodo_actual}."
        if isinstance(respuesta_actual, tuple):
            instrucciones_text += "\nIngresa los valores de x, y, z en los campos correspondientes:"
        else:
            instrucciones_text += "\nIngresa el valor numérico resultante:"

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
        """Verifica la respuesta de desactivación"""
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

Garantiza convergencia pero es lento.
""",
            "Falsa Posición": """
MÉTODO DE LA FALSA POSICIÓN (Regula Falsi)

Similar a bisección pero usa interpolación lineal:

c = (a*f(b) - b*f(a)) / (f(b) - f(a))

Generalmente converge más rápido que bisección.
""",
            "Punto Fijo": """
MÉTODO DEL PUNTO FIJO

Transforma f(x)=0 en x = g(x)
Iteración: x_{n+1} = g(x_n)

Converge si |g'(x)| < 1 en la región de interés.
""",
            "Newton-Raphson": """
MÉTODO DE NEWTON-RAPHSON

Iteración: x_{n+1} = x_n - f(x_n)/f'(x_n)

Características:
- Convergencia cuadrática (muy rápida)
- Requiere cálculo de derivada
- Puede divergir si el valor inicial es malo
""",
            "Secante": """
MÉTODO DE LA SECANTE

Similar a Newton-Raphson pero usa aproximación de la derivada:

x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))

No requiere cálculo de derivada, convergencia superlineal.
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
donde L_i(x) = Π (x - x_j) / (x_i - x_j) para j ≠ i

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

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MathDefuserGame(root)
    root.mainloop()