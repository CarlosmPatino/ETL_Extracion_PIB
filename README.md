🌍 Pipeline ETL: Extracción del PIB Mundial desde la web

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) automatizado que extrae la lista de todos los países ordenados por su PIB (Producto Interno Bruto) en miles de millones de dólares, según los datos más recientes del Fondo Monetario Internacional (FMI).



🚀 Flujo del Pipeline

1️⃣ Extracción (Extract)

Se obtiene la información directamente desde la web utilizando web scraping con BeautifulSoup y requests.
2️⃣ Transformación (Transform)

Se limpian y estructuran los datos en un DataFrame de Pandas.

Se convierten los valores a miles de millones de dólares, redondeando a dos decimales.

Se ordenan los países según su PIB.

3️⃣ Carga (Load)

Se almacena la información en un archivo CSV 7 una base de datos para su posterior uso y análisis.

🛠 Tecnologías Utilizadas

Python 3.11.9

Pandas – Manipulación y transformación de datos.

BeautifulSoup & Requests – Web scraping.

NumPy – Operaciones numéricas.

SQLite - Almacenamiento en base de datos.
