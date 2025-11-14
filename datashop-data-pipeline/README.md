# DataShop Data Pipeline

Proyecto de ejemplo para DataOps (DataShop) — pipeline que genera un informe diario con:
- Ventas totales del día anterior
- Top 5 productos más vendidos
- Cliente con la compra más grande del día

## Estructura
- scripts/: transform.py y data_quality_check.py
- tests/: pruebas unitarias con pytest
- dags/: DAG de Airflow
- data/input: archivos CSV de entrada (se simulan localmente)
- data/output: reportes generados
- .github/workflows: CI con GitHub Actions

## Cómo usar
1. Crear virtualenv e instalar dependencias: `pip install -r requirements.txt`
2. Colocar `data/input/orders_{yesterday}.csv` y `data/input/customers.csv`
3. Ejecutar controles de calidad: `python scripts/data_quality_check.py`
4. Generar reporte: `python scripts/transform.py`

## Nota
Se incluye un archivo de ejemplo de órdenes (fecha ayer) dentro de `data/input/`.
