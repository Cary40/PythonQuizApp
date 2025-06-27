import random

# === Preguntas que se realizaran en cuestionario de python ===
preguntas = [
    ("¿Cómo se clasifica el lenguaje Python?",
     ["Compilado", "Binario", "Interpretado"], 2),

    ("¿Quién fue el creador de Python?",
     ["Dennis Ritchie", "Guido van Rossum", "James Gosling"], 1),

    ("¿De dónde proviene el nombre 'Python'?",
     ["De un personaje mitológico", "De la serpiente pitón", "De un programa de humor"], 2),

    ("¿Qué función se usa para mostrar un texto por pantalla?",
     ["print()", "mostrar()", "imprimir()"], 0),

    ("¿Cuál es la extensión que deben tener los archivos de Python?",
     [".ps", ".python", ".py"], 2),

    ("¿A qué tipo de dato representa el valor True ?",
     ["float", "bool", "str"], 1),

    ("¿Qué hace la función type() en Python?",
     ["Declara una variable", "Muestra el tipo de dato de una variable", "Cambia el tipo de dato"], 1),

    ("¿Qué tipo de tipado tiene Python?",
     ["Fijo", "Dinámico", "Estático"], 1),

    ("¿Qué función permite ingresar datos por teclado?",
     ["insert()", "input()", "scan()"], 1),

    ("¿Qué tipo de dato devuelve por defecto la función input()?",
     ["bool", "int", "str"], 2),

    ("¿Qué palabra clave inicia un bucle condicional?",
     ["switch", "if", "while"], 2),

    ("¿Qué estructura permite repetir un bloque de código, un número específico de veces?",
     ["until", "for", "repeat"], 1),

    ("¿Qué palabra se usa para plantear una condición en Python?",
     ["if", "when", "cond"], 0),

    ("¿Cómo se asigna un valor a una variable en Python?",
     ["nombre_variable = valor", "int nombre_variable = valor", "var nombre_variable: valor"], 0),

    ("¿Qué operador se utiliza para comparar igualdad?",
     ["==", "=", ":="], 0),

    ("¿Cuál es el operador de asignación en Python?",
     ["==", "=", ":="], 1),

    ("¿Qué estructura permite evaluar varias condiciones seguidas?",
     ["if - else if - else", "if - elif - else", "switch - case"], 1),

    ("¿Qué tipo de dato puede almacenar varios elementos y además se puede modificar?",
     ["tuple", "list", "int"], 1),

    ("¿Qué tipo de dato NO permite modificaciones?",
     ["tuple", "dict", "list"], 0),

    ("¿Qué tipo de estructura almacena pares de clave y valor?",
     ["list", "dict", "set"], 1),

    ("¿Qué tipo de dato se usa para almacenar texto?",
     ["str", "int", "bool"], 0),

    ("¿Qué tipo de dato representa números decimales?",
     ["char", "int", "float"], 2),

    ("¿Qué valor retorna la expresión type(3.14)?",
     ["float", "int", "str"], 0),

    ("¿Qué valor retorna type(\"Hola\")?",
     ["bool", "char", "str"], 2),

    ("¿Cuál de los siguientes es un valor booleano?",
     ["\"False\"", "0", "False"], 2),

    ("¿Para qué sirve la guía PEP8 en Python?",
     ["Escribir código legible y coherente", "Acelerar la ejecución", "Crear gráficos automáticamente"], 0),

    ("¿Cuál de estas herramientas permite analizar si se cumple PEP8?",
     ["pyeditor", "flake8", "webstorm"], 1),

    ("¿Cuál de las siguientes opciones NO forma parte de PEP8?",
     ["Usar nombres en mayúscula para variables", "Nombrar variables descriptivamente", "Usar sangría consistente"], 0),

    ("¿Qué función convierte un string a entero?",
     ["int()", "str()", "bool()"], 0),

    ("¿Qué regla es válida al nombrar variables en Python?",
     ["No usar palabras clave", "Empezar con números", "Usar espacios"], 0),

    ("¿Qué característica tiene Python con respecto a la portabilidad?",
     ["Multiplataforma", "Monoplataforma", "Solo Windows"], 0),

    ("¿Qué tipo de estructura devuelve la función range()?",
     ["Un booleano", "Un string", "Una secuencia numérica"], 2),

    ("¿Cuál es una ventaja de los lenguajes interpretados como Python?",
     ["Necesitan compilarse antes", "Son menos portables", "Permiten desarrollo más rápido"], 2),

    ("¿Qué representa el valor None en Python?",
     ["Un booleano", "Un número", "Un valor nulo"], 2),

    ("¿Para qué sirve Tkinter en Python?",
     ["Crear interfaces gráficas", "Conectar a bases de datos", "Ejecutar código desde terminal"], 0),

    ("¿Qué módulo se importa para usar Tkinter?",
     ["import guiBuilder", "import interface", "import tkinter"], 2),

    ("¿Cuál es la instrucción correcta para crear una ventana principal en Tkinter?",
     ["root = tk.Tk()", "window = Tkinter.start()", "root = window.create()"], 0),

    ("¿Qué método inicia el bucle principal en una app de Tkinter?",
     ["window.start_loop()", "mainloop.run(root)", "root.mainloop()"], 2),

    ("¿Qué función cumple Label in Tkinter?",
     ["Mostrar texto o imágenes", "Solicitar ingreso de datos", "Crear bases de datos"], 0),

    ("¿Qué representa una clase en Programación Orientada a Objetos (POO)?",
     ["Un molde para crear objetos", "Una estructura para listas", "Una instrucción para importar módulos"], 0),

    ("¿Qué método se usa para construir un objeto en Python?",
     ["create_object()", "__init__", "start()"], 1),

    ("¿Qué pilar de la POO permite que métodos con el mismo nombre actúen distinto según la clase?",
     ["Encapsulamiento", "Polimorfismo", "Herencia inversa"], 1),

    ("¿Qué palabra clave se utiliza para definir una clase?",
     ["object", "class", "define"], 1),

    ("¿Para qué se usa el encapsulamiento en POO?",
     ["Copiar métodos entre clases", "Eliminar métodos no usados", "Proteger atributos internos"], 2),
]

def obtener_preguntas_aleatorias(preguntas, cantidad=10):
    """Selecciona al azar una 10 de preguntas del listado."""
    if cantidad > len(preguntas):
        raise ValueError("La cantidad de preguntas solicitadas excede el total disponible.")
    return random.sample(preguntas, cantidad)

preguntas_seleccionadas = obtener_preguntas_aleatorias(preguntas)