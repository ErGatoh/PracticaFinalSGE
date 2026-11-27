# Sprint 0 · API de Ventas

**Manuel · Grupo 3 · Paquete A**

He estudiado cómo gestionan las ventas tres ERP conocidos para tomar ideas antes de diseñar nuestro módulo: qué pasos sigue un pedido, cómo se factura y cómo se corrigen los errores. Es la parte de investigación del informe de análisis; el diseño y la implementación se apoyan en ella.

## Qué incluye

- ERP estudiados: Odoo, SAP S/4HANA y Microsoft Dynamics 365 Business Central.
- Comparación: proceso de venta, entregas parciales, facturación, corrección de facturas, licencia y dificultad.
- Contraste con el contrato de la API: qué coincide y tres propuestas para las decisiones pendientes.
- Prueba de Odoo con Docker: pasos y qué observar para compararlo con nuestro módulo.

## Dónde está cada cosa

- [Entrega_Manuel_A.md](Sprint0/Entrega_Manuel_A.md): investigación completa, comparación, ventajas y desventajas, y fuentes.

## Estado

**Investigación terminada para revisión:** 3 ERP comparados y contrastados con el contrato 0.1.0. Falta incorporarla al informe analisis.pdf y comentar con el equipo las propuestas sobre factura rectificativa, entregas parciales y salida por lote en Inventario.

Para repetir la prueba de Odoo, guarda el `docker-compose.yml` de la entrega en una carpeta vacía y ejecuta:

```powershell
docker compose up -d
# Abrir http://localhost:8069 y crear una base de datos con datos de demostración
docker compose down
```

Los precios citados son tarifas públicas de noviembre de 2026 y pueden cambiar.
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







**Adrián · Grupo 3 · Paquete B**

He dibujado cómo será el módulo de Ventas por dentro: qué datos guarda (pedidos, líneas, facturas y cobros) y qué puede hacer cada persona o módulo con él. Son los diagramas de clases y de casos de uso; sirven de base para el contrato de la API y para programar las entidades en el Sprint 1.

## Qué incluye

- Diagrama de clases: PedidoVenta, LineaPedidoVenta, Factura, Cobro, sus estados y las referencias a CRM, Inventario y RRHH.
- Diagrama de casos de uso: Comercial, Administración y Dirección, más los módulos que nos consultan (CRM, RRHH y portal).
- Contraste con el contrato de la API: correspondencia clase a clase y puntos para la reunión.

## Dónde está cada cosa

- [clases.puml](docs/uml/clases.puml) y [clases.png](docs/uml/clases.png): diagrama de clases.
- [casos-uso.puml](docs/uml/casos-uso.puml) y [casos-uso.png](docs/uml/casos-uso.png): diagrama de casos de uso.
- [Entrega_Adrian_B.md](Sprint0/Entrega_Adrian_B.md): explicación de los diagramas y contraste con el contrato.

## Estado

**Diagramas terminados para revisión:** alineados con el contrato 0.1.0. Falta contrastarlos con los diagramas de secuencia y estados de Marian y decidir en grupo los puntos abiertos (numeración, actor que sirve y factura, factura rectificativa).

Para volver a generar las imágenes desde la raíz, con Java y `plantuml.jar` en `tmp/`:

```powershell
java -jar tmp/plantuml.jar -charset UTF-8 -tpng docs/uml
```
