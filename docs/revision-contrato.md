# Revisión del contrato de Ventas - Sprint 0

Autor: Jorge Fernández. Grupo 3, paquete D. Fecha: 24/11/2026.

Estado: contrato de diseño completo para revisión. No aprobado por los otros grupos ni congelado en H1. No hay backend implementado ni pruebas reales de comunicación entre servicios en este sprint.

## Fuentes y alcance

- Enunciado: `../Practica_SGE_ERP_Microservicios.pdf`, páginas 7-8 (integraciones), 10-16 (normas comunes), 22-24 (Ventas), 31 (estados), 34 (Sprint 0) y 37-39 (entregables y evaluación).
- Reparto interno: `../Sprint0/Reparto_Sprint_0_Ventas.txt`, persona D.
- Formato: OpenAPI 3.0.3, https://spec.openapis.org/oas/v3.0.3.
- Entregable: `openapi.yaml`, una única fuente del contrato. No se mantiene una segunda copia que pueda quedar desactualizada.

Se documentan todos los endpoints mínimos de Ventas, las estructuras de entrada y salida, los filtros, los errores comunes, I6, I9, el formato del portal y los endpoints técnicos. El diseño no requiere autenticación, conforme al enunciado.

## Decisiones que concreta esta propuesta

El PDF no define cada campo de los DTO ni todos los casos límite. Las siguientes decisiones están propuestas para que el equipo y los consumidores las revisen antes de H1:

| Tema | Decisión propuesta |
|---|---|
| Listados | Array directo, sin paginación ni envoltorio. Filtros combinados con AND; sin coincidencias devuelve `[]`. |
| Fechas | `desde` y `hasta` inclusivos. `desde > hasta` produce 400. Zona de negocio Europe/Madrid. |
| Líneas | Cantidad entera positiva; descuento explícito entre 0 y 100; IVA 4, 10 o 21. Un BORRADOR puede no tener líneas; no podrá confirmarse. |
| Importes | Base de línea redondeada HALF_UP, IVA calculado sobre esa base y redondeado HALF_UP; totales suman líneas ya redondeadas. |
| Edición | PUT reemplaza todas las líneas y obtiene precios actuales para esas líneas. Se conservan número, fecha e id. Nunca se actualizan pedidos automáticamente cuando Inventario cambia precios. |
| Estados repetidos | Repetir una transición devuelve 409; no duplica operaciones externas. |
| Factura | Una por pedido. Devuelve también las líneas y cobros para permitir ficha 360 e impresión sin añadir endpoints no exigidos. |
| Vencimiento | Fecha de emisión + 30 días naturales; VENCIDA si fecha actual es posterior y queda pendiente. Un cobro parcial no elimina el vencimiento. |
| Anulación | Solo sin cobros; no devuelve stock ni reutiliza número. Pedido permanece FACTURADO para evitar otra factura accidental. La refacturación/rectificación no está especificada y requiere acuerdo. |
| I9 | Array `{comercialId, totalFacturado}`. Suma total con IVA por fecha de emisión, excluyendo ANULADA. RRHH aplica después el 2 %. Debe ratificarse si se quiere usar base sin IVA. |
| KPIs | Facturado y ticket medio con IVA, excluyendo anuladas. Pendientes = BORRADOR + CONFIRMADO. Top 5 por unidades facturadas del mes. Empates por productoId ascendente. |
| CSV | UTF-8, `;`, punto decimal, dos decimales, fechas ISO. Sin resultados: cabecera. Excluye ANULADA; incluye estado para distinguir las demás. |
| Campos calculados | Nunca se aceptan estado, precio, IVA, totales, números ni ids locales dentro de las entradas. Los obtiene/calcula el servidor. |

Los identificadores fiscales y precios de los ejemplos son ilustrativos, no datos maestros oficiales. La representación JSON numérica puede mostrarse como `100` o `100.00`; no debe convertirse en texto para aparentar dos decimales. El cálculo monetario se hará con BigDecimal.

## Correspondencia con UML

| Concepto UML (figura 9) | DTO/contrato | Observaciones |
|---|---|---|
| PedidoVenta | `Pedido` / `PedidoEntrada` | id, número, fecha, clienteId, comercialId, estado, baseImponible, totalIva, total y observaciones. |
| LineaPedidoVenta | `LineaPedido` / `LineaEntrada` | Referencia productoId y copia descripción/precioUnitario/IVA. El UML llama `getImporte()` a un cálculo; la API expone baseImponible, cuotaIva y total. |
| Factura | `Factura` | pedidoId, serie, número, fechas, datos fiscales, estado, total. Añade líneas y resumen de cobros como proyección de lectura. |
| Cobro | `Cobro` / `CobroEntrada` | id, fecha, importe y método. |
| EstadoPedidoVenta | `EstadoPedido` | BORRADOR, CONFIRMADO, SERVIDO, FACTURADO, CANCELADO. |
| EstadoFactura | `EstadoFactura` | EMITIDA, COBRADA, VENCIDA, ANULADA. |
| MetodoPago | `metodo` | TRANSFERENCIA, TARJETA, EFECTIVO. |

Flujo de la figura 14: creación → BORRADOR; confirmar → CONFIRMADO; servir → SERVIDO; crear factura → FACTURADO. Cancelar solo desde BORRADOR o CONFIRMADO. FACTURADO y CANCELADO son finales.

El contrato coincide con los modelos de referencia del PDF. La revisión contra los diagramas reales de Adrián y Marian queda pendiente porque no están en esta carpeta. No se presupone que los hayan revisado o aprobado.

## Compatibilidad entre grupos

| Integración | Solicitud | Lo que debe acordarse y comprobarse |
|---|---|---|
| I1, Ventas → CRM | `GET /api/clientes/{id}` | id, estado, NIF y razón social; nombre exacto de propiedades del DTO de CRM. Solo ACTIVO puede confirmar. Cliente inexistente = 404, inactivo = 409. |
| I2, Ventas → Inventario | `GET /api/productos/{id}` | id, descripción/nombre, precio de venta, IVA y stock; acordar nombres y escala monetaria. |
| I2, Ventas → Inventario | `POST /api/movimientos` | Producto, cantidad, tipo SALIDA y referenciaExterna PV. Concretar el cuerpo usando su OpenAPI, no inventar que ya está acordado. |
| I3, Ventas → RRHH | `GET /api/empleados/{id}` | id, rol COMERCIAL y criterio de empleado activo; nombres exactos según su OpenAPI. |
| I6, CRM → Ventas | `GET /api/pedidos?clienteId=3` | Array de Pedido; conserva clienteId, comercialId, número, fecha, estado, líneas y total. |
| I6, CRM → Ventas | `GET /api/facturas?clienteId=3` | Array de Factura; incluye número, fechas, estado, datos fiscales, líneas, importes y cobros. |
| I9, RRHH → Ventas | `GET /api/estadisticas/ventas-por-comercial?mes=11&anio=2026` | Array por comercialId; absentemente facturado = 0; acordar total con/sin IVA y exclusión de anuladas. |
| Portal → Ventas | `GET /api/estadisticas` | modulo, generadoEn, kpis y series conforme al formato común del PDF. |

Las consultas de CRM, RRHH y portal se resuelven con datos locales: no necesitan acceder directamente a la BD de Ventas ni consultar servicios de terceros a través de Ventas.

### Riesgo que hay que resolver con Inventario

Una transacción MySQL local no puede deshacer movimientos ya aceptados por Inventario. Si un pedido tiene varias líneas y falla una SALIDA después de completar otra, no debe marcarse SERVIDO ni reenviarse todo el pedido sin control. Antes de implementar se debe acordar una estrategia con Inventario (operación de lote atómica o identificación idempotente por pedido/línea y recuperación/compensación documentada). El PDF solo prescribe movimientos individuales y referenciaExterna; no garantiza idempotencia ni atomicidad entre servicios. Este contrato señala el problema sin prometer una garantía que aún no existe.

## Revisión pendiente antes de congelar H1

- [ ] Manuel: contraste de alcance con la comparación ERP y requisitos del informe de análisis.
- [ ] Adrián: confirmar atributos, relaciones y casos de uso de sus diagramas con estos DTO y operaciones.
- [ ] Marian: contrastar secuencia, estados y llamadas I1/I2/I3 con sus diagramas.
- [ ] CRM: confirmar que las dos consultas I6 y los campos fiscales cubren su ficha 360.
- [ ] Inventario: confirmar campos de producto/movimiento y resolver fallos parciales al servir.
- [ ] RRHH: confirmar el cuerpo I9 y la base de cálculo de comisiones.
- [ ] Equipo: ratificar anulación, edición de líneas, CSV, KPIs y fechas.
- [ ] Comité: revisar y aprobar contrato en `erp-integracion/contratos/`; registrar H1.

## Entrega

1. Revisar `docs/openapi.yaml` en una herramienta compatible con OpenAPI 3.0.3.
2. Incorporar únicamente cambios acordados y volver a validar el contrato.
3. Subirlo al repositorio del módulo y, mediante el flujo de la clase, al repositorio común `erp-integracion/contratos/` usando el nombre de archivo que acuerde el comité.
4. Tras H1, proponer cualquier cambio mediante PR en `erp-integracion` y obtener aprobación de los grupos consumidores.

No se ha realizado ninguna publicación ni comunicación a los compañeros desde esta carpeta. No hay remoto Git configurado aquí: esta entrega local queda lista para incorporar al repositorio del grupo.

## Ayuda de IA

Se ha utilizado Codex (OpenAI) para analizar el enunciado, redactar el contrato, preparar ejemplos y comprobar su estructura. Jorge debe revisar y comprender el diseño antes de entregarlo y defenderlo. Esta declaración se incluirá también en el README oficial del módulo cuando exista.
