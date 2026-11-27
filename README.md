# Sprint 0 · Investigación de ERP

**Manuel · Grupo 3 · Paquete A**

He estudiado cómo gestionan las ventas tres ERP conocidos para tomar ideas antes de diseñar nuestro módulo: qué pasos sigue un pedido, cómo se factura y cómo se corrigen los errores. Es la parte de investigación del informe de análisis; el diseño y la implementación se apoyan en ella.

## Qué incluye

- ERP estudiados: Odoo, SAP S/4HANA y Microsoft Dynamics 365 Business Central.
- Comparación: proceso de venta, entregas parciales, facturación, corrección de facturas, licencia y dificultad.
- Relación con el contrato de la API: qué coincide y tres propuestas para las decisiones pendientes.
- Prueba de Odoo con Docker: resultados reales y lo que falta por comprobar.

## Dónde está cada cosa

- [Entrega_Manuel_A.md](Sprint0/Entrega_Manuel_A.md): investigación completa, comparación, ventajas y desventajas, y fuentes.
- [analisis.pdf](docs/analisis.pdf): informe de análisis; por ahora incluye la investigación y faltan los diagramas UML.
- [docker-compose.yml](docs/docker-compose.yml): Odoo 19 y PostgreSQL 16 para la prueba.
- [capturas/](docs/capturas/): capturas reales de la prueba de Odoo.

## Estado

**Investigación terminada para revisión:** 3 ERP comparados y contrastados con el contrato 0.1.0. Falta comentar con el equipo las propuestas sobre factura rectificativa, entregas parciales y salida por lote en Inventario, y terminar la prueba de Odoo (pago, entrega parcial y factura rectificativa).

Para repetir la prueba de Odoo desde la raíz:

```powershell
docker compose -f docs/docker-compose.yml up -d
# Abrir http://localhost:8069 y crear una base de datos con datos de demostración
docker compose -f docs/docker-compose.yml down
```

Los precios citados son tarifas públicas de noviembre de 2026 y pueden cambiar.

---

# Sprint 0 · API de Ventas

**Jorge Fernández · Grupo 3 · Paquete D**

He diseñado cómo se comunicará el módulo de Ventas con la web y el resto del ERP: qué se puede solicitar, qué datos hay que enviar y qué respuestas o errores se recibirán. Es el contrato de la API; su implementación llegará después.

## Qué incluye

- Pedidos: crear, consultar, modificar, confirmar, servir y cancelar.
- Facturas: emitir, consultar, registrar cobros, anular y exportar CSV.
- Integraciones: consultas de CRM, facturación por comercial para RRHH e indicadores para el portal.

## Dónde está cada cosa

- [openapi.yaml](docs/openapi.yaml): contrato con operaciones, datos y ejemplos.
- [revision-contrato.md](docs/revision-contrato.md): decisiones propuestas, relación con UML y acuerdos pendientes.
- [Entrega_Jorge_D.md](Sprint0/Entrega_Jorge_D.md): resumen de mi entrega.
- [validar_openapi.py](docs/validar_openapi.py): comprueba la estructura y los ejemplos del contrato.

## Estado

**Propuesta 0.1.0 validada técnicamente:** 14 rutas y 17 operaciones. Falta contrastarla con los UML del equipo y acordarla con los grupos implicados antes de congelarla en H1. Las decisiones pendientes están identificadas en el documento de revisión.

Para repetir la validación desde la raíz, con Python 3 en Windows:

```powershell
python -m venv tmp/openapi-venv
./tmp/openapi-venv/Scripts/python.exe -m pip install openapi-spec-validator==0.9.0
./tmp/openapi-venv/Scripts/python.exe docs/validar_openapi.py
```

La validación comprueba el documento; no demuestra que el futuro backend funcione.
