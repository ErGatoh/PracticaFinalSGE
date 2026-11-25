# Entrega de Jorge Fernández - Sprint 0, paquete D

Grupo 3: Ventas y facturación.

## Archivos

- `../docs/openapi.yaml`: contrato OpenAPI completo, versión de diseño 0.1.0.
- `../docs/revision-contrato.md`: decisiones propuestas, correspondencia UML, integraciones y pendientes de validación conjunta.
- `../docs/validar_openapi.py`: validación reproducible de la especificación y los ejemplos.

## Cobertura del paquete D

| Tarea | Resultado |
|---|---|
| Definir peticiones de Ventas | Operaciones de pedidos, transiciones, facturas, cobros, anulación, CSV y estadísticas. |
| Definir datos y respuestas | Esquemas de entrada y salida, parámetros, restricciones y ejemplos. |
| Definir errores | Error común con timestamp, status, error, message y path; respuestas 400/404/409/503 según la operación. |
| Preparar consumo por CRM | Consultas I6 de pedidos y facturas por clienteId, con salida en array. |
| Preparar consumo por RRHH | Consulta mensual I9 con total facturado por comercialId. |
| Preparar consumo por portal | Formato común de KPIs y series. |
| Contrastar diseño | Contrastado con el dominio y los estados de referencia del PDF. Pendiente revisión de los UML reales de los compañeros. |
| Revisar con otros grupos | Preparados los puntos a acordar; todavía no se han recibido sus contratos ni confirmaciones. |

## Cómo explicar mi parte

Verificación técnica realizada: OpenAPI 3.0.3 válido, 14 rutas, 17 operaciones y 50 comprobaciones de ejemplos JSON correctas. Se valida la estructura, las referencias y los ejemplos, sin ejecutar un backend. El script permite repetir esa comprobación al modificar el contrato.

El contrato define cómo se podrá utilizar nuestro módulo antes de programarlo. Para cada operación establece la URL, el método HTTP, los datos enviados, la respuesta y los posibles errores. Las entradas de pedido solo admiten referencias, cantidades y descuentos: el backend obtiene los precios e impuestos desde Inventario y calcula los totales para evitar que el cliente los manipule.

CRM podrá consultar pedidos y facturas por cliente. RRHH consultará lo facturado por comercial en un mes y aplicará su comisión. El portal recibirá los indicadores con el mismo formato que los demás módulos. Todas estas consultas devuelven datos propios de Ventas.

Se utiliza 400 para entradas inválidas, 404 para referencias inexistentes, 409 para reglas de negocio y 503 si un proveedor no responde. Servir un pedido no consiste solo en cambiar el estado: requiere registrar salidas de Inventario. El problema de los fallos parciales está identificado para resolverlo con ese grupo.

La parte documental local está preparada. El cierre completo requiere recibir los UML, revisarlos entre todos, ratificar las decisiones propuestas y publicar el contrato en el repositorio común antes de H1.
