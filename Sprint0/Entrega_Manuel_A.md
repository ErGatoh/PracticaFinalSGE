# Entrega de Manuel - Sprint 0, paquete A

Grupo 3: Ventas y facturación.

## Archivos

- `../docs/investigacion-erp.md`: investigación completa de Odoo, SAP S/4HANA y Business Central, comparación, relación con el contrato y fuentes.
- `../docs/analisis.pdf`: informe de análisis con la investigación; pendiente de añadir los diagramas UML.
- `../docs/docker-compose.yml`: Odoo 19 y PostgreSQL 16 para probar Odoo en local.
- `../docs/capturas/`: capturas reales de la prueba de Odoo.

## Cobertura del paquete A

| Tarea | Resultado |
|---|---|
| Estudiar 3 ERP conocidos | Odoo, SAP S/4HANA y Microsoft Dynamics 365 Business Central, con fuentes oficiales. |
| Ver cómo gestionan pedidos y ventas | Proceso de presupuesto, pedido, entrega, factura y cobro en cada uno. |
| Comparación sencilla | Tabla con proceso, entregas parciales, facturación, corrección de facturas, licencia, coste y dificultad. Ventajas y desventajas de cada uno. |
| Parte de investigación del informe | Incluida en `analisis.pdf`. Faltan los diagramas de los paquetes B y C. |
| Prueba de Odoo con Docker | Odoo arrancado y dos facturas creadas, una de 0 € y otra de 363 €. Pendiente: pago, entrega parcial y factura rectificativa. |
| Contrastar con el contrato | Contrastado con `openapi.yaml` 0.1.0. Tres propuestas para las decisiones pendientes. |

## Cómo explicar mi parte

Los tres ERP siguen el mismo camino: presupuesto, pedido, entrega, factura y cobro. Cambia cuándo se factura: Odoo lo decide por producto (lo pedido o lo entregado), SAP por configuración (a partir del pedido o de la entrega) y Business Central al registrar el pedido. Los tres corrigen una factura emitida con un abono o factura rectificativa, sin borrarla.

El contrato de Jorge coincide con los ERP en lo básico: estados claros del pedido, el cobro seguido en la factura, la línea que copia precio e IVA, el pedido que solo se modifica en BORRADOR y las consultas a CRM, Inventario y RRHH.

De la comparación salen tres propuestas para el equipo: usar factura rectificativa para corregir facturas con cobros, dejar las entregas y facturas parciales para después de H1 y acordar con Inventario una salida por lote o unas compensaciones. Una sola base de datos no evita por sí misma que un proceso quede a medias: hace falta agrupar los cambios en una transacción. En microservicios no hay transacción común, así que hay que pactarlo con Inventario.

La prueba de Odoo se hizo en local con Docker. Odoo calculó base, IVA y total a partir de precio, cantidad e impuesto, y mostró la factura como Borrador → Registrado, con el pago aparte. El cierre requiere terminar la prueba, comentar las propuestas con el equipo y añadir los UML al informe.
