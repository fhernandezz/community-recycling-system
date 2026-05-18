# community-recycling-system
Proyecto #1 Desarrollo de Software III Universidad de Costa Rica - Tema: Sistema de reciclaje comunitario MVC | Python

Sistema de Gestión de Reciclaje Comunitario

Descripción del Proyecto
El Sistema de Gestión de Reciclaje Comunitario es una aplicación de escritorio desarrollada en Python diseñada para centralizar, organizar y registrar las actividades de reciclaje dentro de una comunidad. El sistema facilita la administración de recicladores, puntos de recolección y registros de entregas, transformando datos cotidianos en información de valor para medir el impacto ambiental y optimizar la toma de decisiones.

Este proyecto fue desarrollado para el curso Desarrollo de Software III de la Universidad de Costa Rica, con el objetivo de aplicar patrones de diseño y principios de arquitectura de software utilizados en entornos profesionales reales.


Problema que Resuelve
En la mayoría de las comunidades, el reciclaje se gestiona de forma aislada y empírica. La falta de una plataforma centralizada impide registrar con precisión:
* Identidad: Quiénes participan activamente en el reciclaje.
* Trazabilidad: Qué materiales se entregan y en qué cantidades (peso).
* Logística: Cuáles puntos de recolección reciben mayor flujo.

Sin estos datos, es imposible medir el impacto real de las iniciativas ecológicas o generar estadísticas confiables. Este sistema resuelve dicha problemática digitalizando el proceso completo, centralizando la información y automatizando la generación de reportes métricos.


Tecnologías Utilizadas
Para garantizar un desarrollo modular y sin dependencias externas complejas, el sistema se construyó utilizando:
* Lenguaje: Python
* Interfaz Gráfica (GUI): Tkinter
* Persistencia de Datos: JSON
* Control de Versiones: Git y GitHub
* Arquitectura: Patrón por capas (MVC + Services/Repositories)

Módulos del Sistema

### 1. Gestión de Recicladores (Recycler)
Encargado del control de los usuarios del sistema. Permite:
* Registrar y dar de alta a nuevos recicladores con validación de datos duplicados.
* Consultar perfiles mediante identificadores únicos (ID) o filtrarlos por distrito.
* Administrar el estado del reciclador (Activo/Inactivo).

### 2. Gestión de Puntos de Recolección (CollectionPoint)
Optimiza el control de los centros de acopio. Permite:
* Registrar nuevos puntos de reciclaje y definir específicamente qué materiales aceptan.
* Monitorear la disponibilidad y calcular dinámicamente el porcentaje de ocupación de cada punto.
* Modificar el estado operativo del centro (Activo/Inactivo).

### 3. Gestión de Registros de Reciclaje (RecyclingRecord)
El núcleo operativo del sistema. Se encarga de:
* Registrar cada entrega asociando directamente al reciclador con el punto de recolección.
* Validar en tiempo real si el material entregado es permitido en dicho punto.
* Actualizar automáticamente la carga del centro de acopio y alimentar el historial general.

### 4. Reportes y Estadísticas
Transforma los datos almacenados en información visual y analítica mediante:
* Top de recicladores más activos.
* Estado de ocupación actual de los puntos de recolección.
* Historial de transacciones y estadísticas detalladas por tipo de material.

5. Seguridad y Autenticación (Login)
Incluye un módulo de inicio de sesión que restringe el acceso global a la aplicación, garantizando que solo los usuarios autorizados puedan interactuar con los módulos y modificar la información.

Arquitectura del Sistema

El proyecto implementa una arquitectura por capas basada en el patrón MVC, garantizando una separación clara de responsabilidades:

  View ──> Controller ──> Service ──> Repository ──> Model ──> Archivo JSON

Estructura del Código (src/):
src/
└── ucr/ac/cr/
    ├── models/          # Representación pura de los datos (Recycler, CollectionPoint, Record).
    ├── repositories/    # Persistencia y acceso directo a archivos JSON (BaseRepository, etc.).
    ├── services/        # Lógica de negocio, cálculos, validaciones y reportes.
    ├── controllers/     # Intermediarios entre la interfaz gráfica y la lógica de negocio.
    ├── views/           # Interfaz gráfica modular construida en Tkinter.
    ├── data/            # Archivos de almacenamiento (.json).
    └── main.py          # Punto de entrada de la aplicación e inyección de dependencias.


Para asegurar un código limpio, mantenible y escalable, se aplicaron rigurosamente los principios SOLID:

* SRP (Single Responsibility): Cada clase hace una sola cosa. Por ejemplo, Recycler solo modela datos, RecyclerService procesa las reglas de negocio y RecyclerView renderiza la pantalla.
* OCP (Open/Closed): El diseño de BaseRepository permite extender el sistema con nuevos tipos de repositorios sin necesidad de modificar el código base existente.
* LSP (Liskov Substitution): Cualquier repositorio concreto puede sustituir a la abstracción base sin alterar el comportamiento esperado del sistema.
* ISP (Interface Segregation): Los servicios exponen de forma limpia y exclusiva los métodos estrictamente necesarios para sus respectivos controladores.
* DIP (Dependency Inversion): El acoplamiento entre clases se reduce al mínimo mediante la inyección de dependencias centralizada en el archivo main.py.


Se seleccionaron las estructuras nativas de Python de acuerdo con las necesidades de rendimiento de cada operación:
List: Ideales para el almacenamiento secuencial de las entidades y listas de materiales.
Dictionary: Utilizados para la serialización/deserialización de archivos JSON y como acumuladores eficientes en el módulo de reportes.
Tuple: Empleadas para el manejo de resultados intermedios inmutables, por ejemplo: (nombre, total_kg).
Set: Utilizados para validar de forma eficiente (tiempo constante O(1)) si un material pertenece al conjunto permitido: {'plástico', 'vidrio', 'papel', 'metal'}.


Persistencia de Datos
El sistema implementa persistencia en archivos planos a través de archivos JSON independientes (recyclers.json, collection_points.json, records.json). Los datos se cargan automáticamente en memoria al iniciar la aplicación y se sincronizan tras cada operación de escritura.


1. Clonar el repositorio:
   git clone https://github.com/fhernandezz/community-recycling-system.git

2. Abrir el proyecto: Importar la carpeta raíz en su IDE preferido (PyCharm, VS Code, etc.).

3. Ejecutar la aplicación: Navegar hasta el directorio fuente y arrancar el script principal:
   cd src/ucr/ac/cr/
   python main.py

 Integrantes
* Fabricio Hernández López
* Brayan
* Valentina Badilla Morera


Más allá del cumplimiento de los requisitos funcionales, este proyecto ha sido diseñado poniendo especial énfasis en las buenas prácticas de ingeniería de software, logrando una estructura organizada, modular, testeable y fácilmente escalable ante futuras necesidades comunitarias.

