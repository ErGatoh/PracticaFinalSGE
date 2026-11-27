# Sprint 0 · Persona B — Diagramas de clases y casos de uso

Autor: Adrián. Grupo 3, paquete B: Ventas y facturación. ERP «Meseta». Fecha: 27/11/2026.

## 1. Objetivo

Antes de programar hay que dejar claro **qué datos guarda el módulo** y **qué se podrá hacer con él**. Para eso he hecho dos diagramas UML:

- **Diagrama de clases**: qué datos tienen los pedidos, sus líneas, las facturas y los cobros, y cómo se relacionan.
- **Diagrama de casos de uso**: qué puede hacer cada persona desde la aplicación y qué piden los otros módulos.

Los dos están alineados con el contrato de la API de Jorge (`docs/openapi.yaml`, versión 0.1.0), para que diagramas y contrato describan lo mismo.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `docs/uml/clases.puml` | Código PlantUML del diagrama de clases. |
| `docs/uml/clases.png` | Imagen del diagrama de clases. |
| `docs/uml/casos-uso.puml` | Código PlantUML del diagrama de casos de uso. |
| `docs/uml/casos-uso.png` | Imagen del diagrama de casos de uso. |

El enunciado pide la fuente (PlantUML o similar) y la imagen, por eso se entregan las dos.

## 3. Diagrama de clases

### 3.1 Clases de nuestro módulo

| Clase | Para qué sirve | Datos clave |
|---|---|---|
| **PedidoVenta** | El pedido que hace un cliente. | número `PV-2026-0001`, fecha, cliente, comercial, estado y totales. |
| **LineaPedidoVenta** | Cada producto del pedido. | producto, cantidad, precio, descuento e IVA (4, 10 o 21). |
| **Factura** | El documento de cobro de un pedido servido. | número `F-2026-0001`, fechas de emisión y vencimiento (+30 días), NIF y razón social del cliente, estado y totales. |
| **Cobro** | Cada pago que hace el cliente de una factura. | fecha, importe y método de pago. |
| **ContadorNumeracion** | Lleva el último número usado por tipo (PV o F) y año. | tipo, año y último número. |

Y tres enumerados:

- **EstadoPedidoVenta**: BORRADOR, CONFIRMADO, SERVIDO, FACTURADO, CANCELADO.
- **EstadoFactura**: EMITIDA, COBRADA, VENCIDA, ANULADA.
- **MetodoPago**: TRANSFERENCIA, TARJETA, EFECTIVO.

### 3.2 Relaciones

- Un pedido **contiene** sus líneas (composición): si se borra el pedido, desaparecen sus líneas. Es `0..*` porque un BORRADOR puede no tener líneas todavía, aunque no se podrá confirmar sin al menos una.
- Un pedido **se factura en** como mucho una factura (`0..1`): hay una factura por pedido.
- Una factura **recibe** cero o más cobros (composición).

### 3.3 Datos que vienen de otros módulos

Cliente (CRM), Producto (Inventario) y Empleado (RRHH) aparecen en gris porque **no son nuestros**: no tenemos tablas para ellos. Solo guardamos su id (`clienteId`, `productoId`, `comercialId`) y los consultamos por la API (I1, I2 e I3). Así se cumple la regla 1 del enunciado: cada microservicio es dueño de sus datos.

Algunos datos se **copian** en el momento y ya no cambian:

- La línea copia descripción, precio e IVA del producto al crearse. Si Inventario cambia el precio después, el pedido no cambia.
- La factura copia el NIF y la razón social del cliente desde CRM.

### 3.4 Atributos calculados

Los atributos que empiezan por `/` son **derivados**: se calculan a partir de otros y no hace falta guardarlos.

- Línea: `/baseImponible` = cantidad × precio × (1 − descuento/100); `/cuotaIva` = base × IVA/100; `/total` = base + cuota. Redondeo HALF_UP a 2 decimales.
- Factura: `/totalCobrado` = suma de los cobros; `/pendiente` = total − totalCobrado.

## 4. Diagrama de casos de uso

### 4.1 Actores

| Actor | Tipo | Qué hace |
|---|---|---|
| **Comercial** | Persona | Crea, edita, confirma, cancela y consulta pedidos. |
| **Administración** | Persona | Sirve pedidos, factura, registra cobros, anula, imprime y exporta facturas. |
| **Dirección** | Persona | Consulta los indicadores (KPIs). |
| **crm-service** | Sistema | Consulta pedidos y facturas de un cliente para su ficha 360 (I6). |
| **rrhh-service** | Sistema | Consulta lo facturado por comercial para calcular comisiones (I9). |
| **erp-portal** | Sistema | Consulta los KPIs para el cuadro de mando de dirección. |
| **inventario-service** | Sistema | Le pedimos precio e IVA y le registramos las SALIDAS (I2). |

### 4.2 Relaciones «include» y «extend»

- **Crear pedido** incluye validar el cliente (I1), validar el comercial (I3) y obtener precio e IVA (I2).
- **Editar pedido** incluye obtener precio e IVA (I2), porque al editar se cargan los precios actuales de las líneas.
- **Confirmar pedido** incluye validar que el cliente sigue ACTIVO (I1).
- **Servir pedido** incluye registrar la SALIDA de stock en Inventario (I2).
- **Generar factura** incluye consultar el cliente en CRM (I1) para copiar NIF y razón social.
- **Imprimir factura** extiende a **Consultar facturas**: es algo opcional que se hace desde la consulta.

## 5. Contraste con el contrato de la API (paquete D)

Respondo al punto pendiente de `docs/revision-contrato.md`: «Adrián: confirmar atributos, relaciones y casos de uso de sus diagramas con estos DTO y operaciones».

| Diagrama | Contrato 0.1.0 | Valoración |
|---|---|---|
| PedidoVenta | `Pedido` / `PedidoEntrada` | Coincide campo a campo. |
| LineaPedidoVenta | `LineaPedido` / `LineaEntrada` | Coincide. Los derivados `/baseImponible`, `/cuotaIva` y `/total` son los mismos campos que expone la API. |
| Factura | `Factura` | Coincide. He añadido `comercialId`, que está en el contrato y hace falta para I9. `/totalCobrado` y `/pendiente` coinciden con la API. `pedidoId` sale de la relación con PedidoVenta. |
| Cobro | `Cobro` / `CobroEntrada` | Coincide. |
| Enumerados | `EstadoPedido`, `EstadoFactura`, `metodo` | Mismos valores. En Java se llama `EstadoPedidoVenta`, como en la figura 9; en la API, `EstadoPedido`. |
| Casos de uso | 17 operaciones | Las 14 operaciones de negocio están cubiertas («Consultar pedidos» agrupa listar y ver detalle). «Imprimir factura» no necesita operación propia: es del frontal y usa los datos de la factura. Las 3 técnicas (salud, Swagger y contrato) no son casos de uso. |
| ContadorNumeracion | No aparece | Correcto: es interno, no se expone en la API. |

Puntos para la reunión del grupo:

1. **ContadorNumeracion** es una propuesta mía para cumplir la numeración correlativa sin huecos. Se puede quitar si preferimos otra solución.
2. **Quién sirve y quién factura**: he puesto a Administración porque el enunciado dice que administración usará el PC, pero hay que confirmarlo.
3. **VENCIDA**: no hay un actor que la marque. La propuesta de Jorge es calcularla al consultar (fecha actual > vencimiento y queda pendiente), y por eso aparece el método `estaVencida()`.
4. **Factura rectificativa**: si el grupo acepta la propuesta de Manuel, habrá que añadirla a los dos diagramas.
5. Falta contrastarlo con los diagramas de secuencia y estados de Marian (paquete C).

## 6. Cómo generar las imágenes

Las imágenes se generan a partir de los `.puml`. Hay dos formas:

- **VS Code:** instalar la extensión *PlantUML* (jebbs), abrir el `.puml` y pulsar `Alt + D` para ver la vista previa. Para exportar: botón derecho → *Export Current Diagram*.
- **Línea de comandos:** con Java instalado, descargar `plantuml.jar` de https://plantuml.com/download en la carpeta `tmp/` (está en `.gitignore`) y ejecutar desde la raíz:

```powershell
java -jar tmp/plantuml.jar -charset UTF-8 -tpng docs/uml
```

Si se cambia un diagrama, hay que volver a generar el PNG para que la imagen y el código coincidan.

## Ayuda de IA

Se ha utilizado Claude (Anthropic) para preparar los diagramas en PlantUML, contrastarlos con el contrato OpenAPI y redactar esta entrega. Adrián ha revisado el contenido y debe comprenderlo antes de entregarlo y defenderlo.
