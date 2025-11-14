# DataShop Data Pipeline

Elaborado por Juan Sebastián Fajardo Acevedo
## Descripción General del Proyecto

Este proyecto implementa un pipeline automatizado para el procesamiento y aseguramiento de calidad sobre datos de ventas de una tienda ficticia llamada DataShop.
El objetivo principal es aplicar conceptos de DataOps, como estos:

- Flujo ETL estructurado

- Validación de calidad de datos

- Pruebas unitarias

- Versionamiento del pipeline

- Reproducibilidad

- Generación automática de reportes

El sistema toma datos crudos, los transforma, verifica su integridad y genera un reporte JSON diario que sea validado.

## Estructura del Proyecto

La estructura general del proyecto es la siguiente:

<img width="301" height="375" alt="image" src="https://github.com/user-attachments/assets/0f15fd05-8a63-4c26-b393-2c93c8b10628" />


- data/input/ : contiene los datos crudos que se procesan.

- data/output/ : almacena los reportes generados.

- scripts/ : contiene los módulos del pipeline de transformación y calidad.

- tests/ : incluye las pruebas unitarias.

- requirements.txt : dependencias del proyecto.

## 2. Configuración del Entorno

Para ejecutar el proyecto localmente, primero se deben instalar las dependencias.

**2.1 Crear el entorno**

conda create -n datashop python=3.10

conda activate datashop

**2.2 Instalar dependencias**
pip install -r requirements.txt

## 3. Ejecución del Pipeline

El pipeline está compuesto por estos dos procesos:

- Validación de calidad de datos

- Transformación y generación de reporte

Los dos scripts toca ejecutarlos desde la raíz del proyecto.

**3.1 Validación de Calidad**

Este script asegura que los datos cumplan reglas básicas:

Que no existan campos obligatorios vacíos, los valores numéricos sean positivos, las fechas tengan formato correcto, y la estructura del JSON sea válida

comando: python scripts/data_quality_check.py

<img width="1319" height="122" alt="image" src="https://github.com/user-attachments/assets/0d379bba-3fe1-493f-9d7b-0659e4ea8ef6" />

**3.2 Transformación de Datos**

Este script procesa los datos validados y genera un reporte con los estos campos:

- total_sales (ventas totales)

- total_items (cantidad total de ítems)

- unique_products (productos únicos vendidos)

- daily_summary (resumen estructurado)

Comando: python scripts/transform.py
<img width="1318" height="124" alt="image" src="https://github.com/user-attachments/assets/f55aec6a-29b9-4127-a4df-efcb5770170f" />

## 4. Pruebas Unitarias (Pytest)

El proyecto tiene pruebas unitarias enfocadas en validación de estructura, los tipos de datos, las reglas de negocio, y la transformación correcta

Comando: pytest

<img width="1333" height="560" alt="image" src="https://github.com/user-attachments/assets/18ec9e28-6d2b-442e-9c98-830e338b96e8" />

## 5. Datos de Entrada

El archivo principal de entrada es: data/input/data.json  y este archivo contiene una lista de ventas.
<img width="480" height="173" alt="image" src="https://github.com/user-attachments/assets/0aaec6b9-8ea6-4c0d-a4e5-34f168af9c39" />
<img width="606" height="168" alt="image" src="https://github.com/user-attachments/assets/5d8583dd-8570-42cc-8c57-357fe435bc2a" />

## 6. Datos de Salida, que es el Reporte

El reporte JSON generado es así:

<img width="475" height="464" alt="image" src="https://github.com/user-attachments/assets/209ef069-16a1-430d-9a36-a7cc0406ba4a" />

## 7. Lógica Interna del Pipeline
**7.1 Módulo de Calidad (data_quality_check.py)**

Este módulo se encarga de revisar que los datos de entrada cumplan con todas las condiciones mínimas necesarias antes de ser procesados, tambien verifica que existan los campos que son obligatorios, confirma que los valores tengan el tipo de dato correcto como enteros, flotantes o cadenas de texto y también asegura que no haya cantidades negativas. Además, revisa que las fechas tengan el formato estándar YYYY-MM-DD. Si alguna de estas revisiones falla, el script vota el error correspondiente y detiene la ejecución del pipeline para que nop haya resultados incorrectos.

**7.2 Módulo de Transformación (transform.py)**

Este módulo realiza la parte central del procesamiento, entonces a partir de los datos validados, calcula el total de ventas multiplicando la cantidad vendida por el precio de cada producto, cuenta cuántos productos distintos hay y genera estadísticas globales del conjunto de datos; luego, organiza toda esta información en un reporte final y lo guarda como un archivo JSON utilizando la fecha del sistema para identificarlo.

 ## 8. Consideraciones y Buenas Prácticas

Este proyecto fue diseñado para que pueda ejecutarse de manera reproducible en cualquier máquina, manteniendo rutas relativas que evitan errores por diferencias de entornos. El uso de pruebas unitarias con Pytest garantiza que los datos se estén procesando correctamente y que los resultados sean confiables.El pipeline está estructurado para que la validación ocurra siempre antes de cualquier transformación, evitando que errores en los datos se propaguen a las etapas finales.

##  9. Conclusión

El pipeline ofrece un flujo de trabajo completo basado en prácticas fundamentales de DataOps. Permite que verifiquemos los datos crudos antes de procesarlos, detectar errores oportunamente y producir resultados consistentes y confiables. Como tiene una estructura modular es más fácil de mantener, escalar y adaptar a nuevos requerimientos, proporcionando una base sólida para procesos de análisis de datos automatizados.
