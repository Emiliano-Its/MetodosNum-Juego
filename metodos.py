import numpy as np
import random
import math

class MetodosCalculo:
    def __init__(self):
        pass
    
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
        """Interpolación de Newton hacia adelante (requiere puntos equiespaciados)"""
        puntos_ordenados = sorted(puntos, key=lambda p: p[0])
        n = len(puntos_ordenados)
        
        # Verificar que los puntos sean equiespaciados
        diferencias = [puntos_ordenados[i+1][0] - puntos_ordenados[i][0] for i in range(n-1)]
        if len(set(diferencias)) > 1:
            # Si no son equiespaciados, usar diferencias divididas como fallback
            return self.interpolacion_diferencias_divididas(x, puntos_ordenados)
        
        # Calcular diferencias finitas
        dif_finitas = self.calcular_diferencias_finitas(puntos_ordenados)
        
        # Aplicar fórmula de Newton hacia adelante
        h = diferencias[0]  # Paso (debe ser constante)
        x0 = puntos_ordenados[0][0]
        s = (x - x0) / h
        
        resultado = puntos_ordenados[0][1]  # f(x0)
        producto = 1
        
        for i in range(1, n):
            producto *= (s - (i - 1)) / i
            resultado += dif_finitas[0][i] * producto
        
        return resultado
    
    def interpolacion_newton_atras(self, x, puntos):
        """Interpolación de Newton hacia atrás (requiere puntos equiespaciados)"""
        puntos_ordenados = sorted(puntos, key=lambda p: p[0])
        n = len(puntos_ordenados)
        
        # Verificar que los puntos sean equiespaciados
        diferencias = [puntos_ordenados[i+1][0] - puntos_ordenados[i][0] for i in range(n-1)]
        if len(set(diferencias)) > 1:
            # Si no son equiespaciados, usar diferencias divididas como fallback
            return self.interpolacion_diferencias_divididas(x, puntos_ordenados)
        
        # Calcular diferencias finitas
        dif_finitas = self.calcular_diferencias_finitas(puntos_ordenados)
        
        # Aplicar fórmula de Newton hacia atrás
        h = diferencias[0]  # Paso (debe ser constante)
        xn = puntos_ordenados[-1][0]
        s = (x - xn) / h
        
        resultado = puntos_ordenados[-1][1]  # f(xn)
        producto = 1
        
        for i in range(1, n):
            producto *= (s + (i - 1)) / i
            resultado += dif_finitas[n-i-1][i] * producto
        
        return resultado
    
    def calcular_diferencias_finitas(self, puntos):
        """Calcula la tabla de diferencias finitas para puntos equiespaciados"""
        n = len(puntos)
        y = [p[1] for p in puntos]
        
        # Inicializar tabla
        tabla = [[0] * n for _ in range(n)]
        
        # Primera columna son los valores de y
        for i in range(n):
            tabla[i][0] = y[i]
        
        # Calcular diferencias finitas
        for j in range(1, n):
            for i in range(n - j):
                tabla[i][j] = tabla[i+1][j-1] - tabla[i][j-1]
        
        return tabla
    
    def interpolacion_diferencias_divididas(self, x, puntos):
        """Interpolación con diferencias divididas (funciona con puntos no equiespaciados)"""
        puntos_ordenados = sorted(puntos, key=lambda p: p[0])
        n = len(puntos_ordenados)
        
        # Calcular diferencias divididas
        dif_div = self.calcular_diferencias_divididas(puntos_ordenados)
        
        # Aplicar fórmula de Newton con diferencias divididas
        resultado = puntos_ordenados[0][1]  # f[x0]
        producto = 1
        
        for i in range(1, n):
            producto *= (x - puntos_ordenados[i-1][0])
            resultado += dif_div[0][i] * producto
        
        return resultado
    
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
        """Genera un sistema de ecuaciones lineales 3x3 con coeficientes no cero en todas las variables"""
        # Generar solución aleatoria
        x = random.randint(-8, 8)
        y = random.randint(-8, 8)
        z = random.randint(-8, 8)

        # MEJORA: Generar coeficientes no cero para todas las variables en todas las ecuaciones
        def coef_no_cero():
            return random.choice([i for i in range(-5, 6) if i != 0])
        
        # Generar coeficientes asegurando que ninguna variable tenga coeficiente cero
        a11, a12, a13 = coef_no_cero(), coef_no_cero(), coef_no_cero()
        a21, a22, a23 = coef_no_cero(), coef_no_cero(), coef_no_cero()
        a31, a32, a33 = coef_no_cero(), coef_no_cero(), coef_no_cero()

        # Asegurar que el sistema tenga solución única
        det = a11*(a22*a33 - a23*a32) - a12*(a21*a33 - a23*a31) + a13*(a21*a32 - a22*a31)
        if abs(det) < 0.1:  # Si el determinante es casi cero, usar coeficientes por defecto
            a11, a12, a13 = 2, -3, 1
            a21, a22, a23 = -1, 2, 4
            a31, a32, a33 = 3, 1, -2

        # Calcular los términos independientes
        b1 = a11*x + a12*y + a13*z
        b2 = a21*x + a22*y + a23*z
        b3 = a31*x + a32*y + a33*z

        # Formatear los coeficientes para mostrar signos correctos
        def formato_coef(coef, variable):
            if coef == 1:
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
        """Genera un sistema 3x3 diagonalmente dominante con coeficientes no cero"""
        # Generar solución
        x = random.uniform(-5, 5)
        y = random.uniform(-5, 5)
        z = random.uniform(-5, 5)

        # MEJORA: Generar coeficientes no cero para todas las variables
        def coef_no_cero():
            return random.choice([i for i in range(-5, 6) if i != 0])
        
        # Generar coeficientes iniciales
        a11, a12, a13 = coef_no_cero(), coef_no_cero(), coef_no_cero()
        a21, a22, a23 = coef_no_cero(), coef_no_cero(), coef_no_cero()
        a31, a32, a33 = coef_no_cero(), coef_no_cero(), coef_no_cero()

        # Asegurar diagonal dominante
        a11 = abs(a12) + abs(a13) + random.randint(1, 3)
        a22 = abs(a21) + abs(a23) + random.randint(1, 3)
        a33 = abs(a31) + abs(a32) + random.randint(1, 3)

        # Calcular términos independientes
        b1 = a11*x + a12*y + a13*z
        b2 = a21*x + a22*y + a23*z
        b3 = a31*x + a32*y + a33*z

        # Formatear
        def formato_coef(coef, variable):
            if coef == 1:
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
        """Genera un problema de ecuación no lineal con múltiples raíces válidas"""
        # Lista de funciones con sus raíces reales
        funciones = [
            {
                "func_str": "x³ - 6.5x + 2",
                "func": lambda x: x**3 - 6.5*x + 2,
                "raices": self.encontrar_raices_reales(lambda x: x**3 - 6.5*x + 2, -5, 5),
                "intervalo": [-3, 3]
            },
            {
                "func_str": "3x³ - 2x - 3", 
                "func": lambda x: 3*x**3 - 2*x - 3,
                "raices": self.encontrar_raices_reales(lambda x: 3*x**3 - 2*x - 3, -2, 2),
                "intervalo": [0, 2]
            },
            {
                "func_str": "x³ + 2x² + 10x - 20",
                "func": lambda x: x**3 + 2*x**2 + 10*x - 20,
                "raices": self.encontrar_raices_reales(lambda x: x**3 + 2*x**2 + 10*x - 20, 0, 3),
                "intervalo": [1, 2]
            },
            {
                "func_str": "e^(-x) - x",
                "func": lambda x: math.exp(-x) - x,
                "raices": self.encontrar_raices_reales(lambda x: math.exp(-x) - x, -1, 2),
                "intervalo": [0, 1]
            },
            {
                "func_str": "x³ - 2x² - 5x + 6",
                "func": lambda x: x**3 - 2*x**2 - 5*x + 6,
                "raices": self.encontrar_raices_reales(lambda x: x**3 - 2*x**2 - 5*x + 6, -3, 4),
                "intervalo": [-2, 3]
            },
            {
                "func_str": "x⁴ - 3x² + x - 1",
                "func": lambda x: x**4 - 3*x**2 + x - 1,
                "raices": self.encontrar_raices_reales(lambda x: x**4 - 3*x**2 + x - 1, -2, 2),
                "intervalo": [-2, 2]
            }
        ]
        
        funcion = random.choice(funciones)
        func_str = funcion["func_str"]
        raices = funcion["raices"]
        intervalo = funcion["intervalo"]
        
        if not raices:
            # Si no se encontraron raíces, usar una por defecto
            raices = [random.uniform(intervalo[0], intervalo[1])]
        
        if metodo == "Bisección":
            # Para bisección, especificar el intervalo
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra UNA raíz de la función en el intervalo [{intervalo[0]}, {intervalo[1]}] usando el método de bisección:
f(x) = {func_str}

La función tiene {len(raices)} raíz(es) real(es) en este intervalo.
Cualquiera de ellas es aceptable como respuesta.
"""
        elif metodo == "Falsa Posición":
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra UNA raíz de la función en el intervalo [{intervalo[0]}, {intervalo[1]}] usando el método de falsa posición:
f(x) = {func_str}

La función tiene {len(raices)} raíz(es) real(es) en este intervalo.
Cualquiera de ellas es aceptable como respuesta.
"""
        elif metodo == "Newton-Raphson":
            # Para Newton-Raphson, sugerir un valor inicial
            x0 = random.choice(raices) + random.uniform(-0.5, 0.5)
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra UNA raíz de la función usando el método de Newton-Raphson:
f(x) = {func_str}

Valor inicial sugerido: x₀ = {x0:.2f}

La función tiene {len(raices)} raíz(es) real(es).
Cualquiera de ellas es aceptable como respuesta.
"""
        elif metodo == "Secante":
            # Para secante, sugerir dos valores iniciales
            x0 = random.choice(raices) + random.uniform(-0.8, -0.2)
            x1 = random.choice(raices) + random.uniform(0.2, 0.8)
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra UNA raíz de la función usando el método de la secante:
f(x) = {func_str}

Valores iniciales sugeridos: x₀ = {x0:.2f}, x₁ = {x1:.2f}

La función tiene {len(raices)} raíz(es) real(es).
Cualquiera de ellas es aceptable como respuesta.
"""
        else:  # Punto Fijo
            # Para punto fijo, mostrar la ecuación transformada
            transformaciones = [
                f"x = ({func_str.replace('f(x) = ', '')} + x) / 2",
                f"x = -({func_str.replace('f(x) = ', '')}) + x",
                f"x = ({func_str.replace('f(x) = ', '')}) / 10 + x"
            ]
            transformacion = random.choice(transformaciones)
            x0 = random.choice(raices) + random.uniform(-0.3, 0.3)
            
            problema = f"""
PROBLEMA DE ECUACIÓN NO LINEAL (Método: {metodo}):

Encuentra UNA raíz de la función usando el método de punto fijo:
f(x) = {func_str}

Transformación sugerida: {transformacion}
Valor inicial sugerido: x₀ = {x0:.2f}

La función tiene {len(raices)} raíz(es) real(es).
Cualquiera de ellas es aceptable como respuesta.
"""
        
        # Devolver el problema y la lista de raíces válidas
        return problema, raices
    
    def encontrar_raices_reales(self, func, x_min, x_max, num_puntos=1000):
        """Encuentra raíces reales de una función en un intervalo dado"""
        raices = []
        x_vals = np.linspace(x_min, x_max, num_puntos)
        y_vals = [func(x) for x in x_vals]
        
        # Buscar cambios de signo
        for i in range(1, len(x_vals)):
            if y_vals[i-1] * y_vals[i] < 0:
                # Hay una raíz en este intervalo, refinar con bisección
                a, b = x_vals[i-1], x_vals[i]
                for _ in range(20):  # 20 iteraciones de bisección
                    c = (a + b) / 2
                    if func(a) * func(c) < 0:
                        b = c
                    else:
                        a = c
                raiz = (a + b) / 2
                # Verificar que no sea una raíz duplicada
                if not any(abs(raiz - r) < 0.001 for r in raices):
                    raices.append(raiz)
        
        # También buscar raíces donde la función cruza cero sin cambio de signo (puntos de tangencia)
        for i in range(1, len(x_vals)-1):
            if abs(y_vals[i]) < 0.01 and (y_vals[i-1] * y_vals[i+1] <= 0):
                raiz = x_vals[i]
                if not any(abs(raiz - r) < 0.001 for r in raices):
                    raices.append(raiz)
        
        return raices

    # MÉTODOS DE INTEGRACIÓN

    def generar_problema_trapezoidal(self, n):
        """Genera problema para regla trapezoidal"""
        # Seleccionar función y límites
        funciones = [
            {"func": lambda x: 1 - x**2, "a": 0, "b": 1, "desc": "1 - x²"},
            {"func": lambda x: x**3 + 2*x, "a": 0, "b": 2, "desc": "x³ + 2x"},
            {"func": lambda x: math.sin(x), "a": 0, "b": math.pi, "desc": "sin(x)"},
            {"func": lambda x: math.exp(x), "a": 0, "b": 1, "desc": "eˣ"},
            {"func": lambda x: 3*x**2 - 2*x + 1, "a": -1, "b": 1, "desc": "3x² - 2x + 1"},
            {"func": lambda x: math.cos(x), "a": 0, "b": math.pi/2, "desc": "cos(x)"}
        ]
        
        funcion_elegida = random.choice(funciones)
        f = funcion_elegida["func"]
        a = funcion_elegida["a"]
        b = funcion_elegida["b"]
        desc = funcion_elegida["desc"]
        
        # Calcular respuesta usando regla trapezoidal
        h = (b - a) / n
        resultado = (f(a) + f(b)) / 2
        for i in range(1, n):
            resultado += f(a + i * h)
        resultado *= h
        
        problema = f"""
PROBLEMA DE INTEGRACIÓN - REGLA TRAPEZOIDAL

Calcula la integral aproximada de la función:
f(x) = {desc}

Desde x = {a} hasta x = {b}
Usando la Regla Trapezoidal con n = {n} subintervalos.

La fórmula de la Regla Trapezoidal es:
∫f(x)dx ≈ (h/2) * [f(x₀) + 2f(x₁) + 2f(x₂) + ... + 2f(xₙ₋₁) + f(xₙ)]
donde h = (b - a)/n

¿Cuál es el valor aproximado de la integral?
"""
        return problema, resultado

    def generar_problema_simpson13(self, n):
        """Genera problema para regla de 1/3 de Simpson (n par)"""
        funciones = [
            {"func": lambda x: 1 - x**2, "a": 0, "b": 1, "desc": "1 - x²"},
            {"func": lambda x: x**4 - 2*x**2 + 1, "a": -1, "b": 1, "desc": "x⁴ - 2x² + 1"},
            {"func": lambda x: math.sin(x), "a": 0, "b": math.pi, "desc": "sin(x)"},
            {"func": lambda x: math.exp(-x**2), "a": 0, "b": 1, "desc": "e^(-x²)"},
            {"func": lambda x: 1/(1+x**2), "a": 0, "b": 1, "desc": "1/(1+x²)"}
        ]
        
        funcion_elegida = random.choice(funciones)
        f = funcion_elegida["func"]
        a = funcion_elegida["a"]
        b = funcion_elegida["b"]
        desc = funcion_elegida["desc"]
        
        # Calcular respuesta usando regla de 1/3 de Simpson
        h = (b - a) / n
        resultado = f(a) + f(b)
        
        for i in range(1, n):
            if i % 2 == 0:
                resultado += 2 * f(a + i * h)
            else:
                resultado += 4 * f(a + i * h)
        
        resultado *= h / 3
        
        problema = f"""
PROBLEMA DE INTEGRACIÓN - REGLA DE 1/3 DE SIMPSON

Calcula la integral aproximada de la función:
f(x) = {desc}

Desde x = {a} hasta x = {b}
Usando la Regla de 1/3 de Simpson con n = {n} subintervalos (n par).

La fórmula de la Regla de 1/3 de Simpson es:
∫f(x)dx ≈ (h/3) * [f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + 4f(xₙ₋₁) + f(xₙ)]
donde h = (b - a)/n

¿Cuál es el valor aproximado de la integral?
"""
        return problema, resultado

    def generar_problema_simpson38(self, n):
        """Genera problema para regla de 3/8 de Simpson (n múltiplo de 3)"""
        funciones = [
            {"func": lambda x: 1 - x**2, "a": 0, "b": 1, "desc": "1 - x²"},
            {"func": lambda x: x**3 + x, "a": 0, "b": 2, "desc": "x³ + x"},
            {"func": lambda x: math.cos(x), "a": 0, "b": math.pi/2, "desc": "cos(x)"},
            {"func": lambda x: math.log(1 + x), "a": 0, "b": 1, "desc": "ln(1+x)"},
            {"func": lambda x: math.sqrt(1 + x), "a": 0, "b": 1, "desc": "√(1+x)"}
        ]
        
        funcion_elegida = random.choice(funciones)
        f = funcion_elegida["func"]
        a = funcion_elegida["a"]
        b = funcion_elegida["b"]
        desc = funcion_elegida["desc"]
        
        # Calcular respuesta usando regla de 3/8 de Simpson
        h = (b - a) / n
        resultado = f(a) + f(b)
        
        for i in range(1, n):
            if i % 3 == 0:
                resultado += 2 * f(a + i * h)
            else:
                resultado += 3 * f(a + i * h)
        
        resultado *= 3 * h / 8
        
        problema = f"""
PROBLEMA DE INTEGRACIÓN - REGLA DE 3/8 DE SIMPSON

Calcula la integral aproximada de la función:
f(x) = {desc}

Desde x = {a} hasta x = {b}
Usando la Regla de 3/8 de Simpson con n = {n} subintervalos (n múltiplo de 3).

La fórmula de la Regla de 3/8 de Simpson es:
∫f(x)dx ≈ (3h/8) * [f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + 3f(x₄) + ... + 3f(xₙ₋₁) + f(xₙ)]
donde h = (b - a)/n

¿Cuál es el valor aproximado de la integral?
"""
        return problema, resultado

    def generar_problema_newton_cotes_cerradas(self, n, constantes_newton_cotes_cerradas):
        """Genera problema para Newton-Cotes Cerradas"""
        funciones = [
            {"func": lambda x: 1 - x**2, "a": 0, "b": 1, "desc": "1 - x²"},
            {"func": lambda x: x**4, "a": 0, "b": 1, "desc": "x⁴"},
            {"func": lambda x: math.sin(x), "a": 0, "b": math.pi, "desc": "sin(x)"},
            {"func": lambda x: math.exp(x), "a": 0, "b": 1, "desc": "eˣ"}
        ]
        
        funcion_elegida = random.choice(funciones)
        f = funcion_elegida["func"]
        a = funcion_elegida["a"]
        b = funcion_elegida["b"]
        desc = funcion_elegida["desc"]
        
        # Obtener constantes de la tabla
        constantes = constantes_newton_cotes_cerradas.get(n)
        if not constantes:
            n = 4  # Valor por defecto
            constantes = constantes_newton_cotes_cerradas[n]
        
        alpha = constantes["alpha"]
        coef = constantes["coef"]
        
        # Calcular respuesta usando Newton-Cotes Cerradas
        h = (b - a) / n
        resultado = 0
        for i in range(n + 1):
            resultado += coef[i] * f(a + i * h)
        resultado *= alpha * (b - a)
        
        # Formatear coeficientes para mostrar
        coef_str = " + ".join([f"{coef[i]}·f(x{i})" for i in range(len(coef))])
        
        problema = f"""
PROBLEMA DE INTEGRACIÓN - NEWTON-COTES CERRADAS (n={n})

Calcula la integral aproximada de la función:
f(x) = {desc}

Desde x = {a} hasta x = {b}
Usando la fórmula de Newton-Cotes Cerradas de grado {n}.

La fórmula es:
∫f(x)dx ≈ α · (b - a) · Σ [cᵢ · f(xᵢ)]
donde:
α = {alpha}
Coeficientes: {coef_str}
xᵢ son puntos equiespaciados desde {a} hasta {b}

¿Cuál es el valor aproximado de la integral?
"""
        return problema, resultado

    def generar_problema_newton_cotes_abiertas(self, n, constantes_newton_cotes_abiertas):
        """Genera problema para Newton-Cotes Abiertas"""
        funciones = [
            {"func": lambda x: 1 - x**2, "a": 0, "b": 1, "desc": "1 - x²"},
            {"func": lambda x: x**3, "a": 0, "b": 2, "desc": "x³"},
            {"func": lambda x: math.cos(x), "a": 0, "b": math.pi/2, "desc": "cos(x)"},
            {"func": lambda x: math.log(1 + x), "a": 0, "b": 1, "desc": "ln(1+x)"}
        ]
        
        funcion_elegida = random.choice(funciones)
        f = funcion_elegida["func"]
        a = funcion_elegida["a"]
        b = funcion_elegida["b"]
        desc = funcion_elegida["desc"]
        
        # Obtener constantes de la tabla
        constantes = constantes_newton_cotes_abiertas.get(n)
        if not constantes:
            n = 2  # Valor por defecto
            constantes = constantes_newton_cotes_abiertas[n]
        
        alpha = constantes["alpha"]
        coef = constantes["coef"]
        
        # Calcular respuesta usando Newton-Cotes Abiertas
        # Para fórmulas abiertas, los puntos no incluyen los extremos
        h = (b - a) / (n + 2)
        resultado = 0
        for i in range(1, n + 2):  # i desde 1 hasta n+1
            resultado += coef[i] * f(a + i * h)
        resultado *= alpha * (b - a)
        
        # Formatear coeficientes para mostrar
        coef_str = " + ".join([f"{coef[i]}·f(x{i})" for i in range(1, len(coef)-1)])
        
        problema = f"""
PROBLEMA DE INTEGRACIÓN - NEWTON-COTES ABIERTAS (n={n})

Calcula la integral aproximada de la función:
f(x) = {desc}

Desde x = {a} hasta x = {b}
Usando la fórmula de Newton-Cotes Abiertas de grado {n}.

La fórmula es:
∫f(x)dx ≈ α · (b - a) · Σ [cᵢ · f(xᵢ)]
donde:
α = {alpha}
Coeficientes: {coef_str}
xᵢ son puntos equiespaciados entre {a} y {b} (sin incluir extremos)

¿Cuál es el valor aproximado de la integral?
"""
        return problema, resultado