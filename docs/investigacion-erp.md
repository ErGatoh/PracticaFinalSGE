# Investigación de ERP - Sprint 0

Autor: Manuel. Grupo 3, paquete A. Fecha: 27/11/2026.

Estado: investigación completa para revisión. La prueba de Odoo está a medias: faltan el pago, la entrega parcial y la factura rectificativa.

## Objetivo

Antes de diseñar nuestro módulo hemos estudiado cómo gestionan las ventas tres ERP muy usados: **Odoo**, **SAP S/4HANA** y **Microsoft Dynamics 365 Business Central**. Nos fijamos en una sola cosa: el camino que recorre una venta desde que se crea el pedido hasta que se cobra. Al final sacamos ideas concretas para nuestro diseño.

## El camino común de una venta

Los tres ERP siguen los mismos cinco pasos, aunque los llamen de forma distinta:

1. **Presupuesto**: se ofrece un precio al cliente. Todavía no es una venta.
2. **Pedido**: el cliente acepta y el presupuesto se convierte en pedido.
3. **Entrega**: se sirve la mercancía y se descuenta del almacén.
4. **Factura**: se emite el documento de cobro.
5. **Cobro**: el cliente paga y la venta queda cerrada.

Dicho de forma sencilla: el pedido es la «promesa», la entrega es «cumplir la promesa», y la factura y el cobro son «pasar cuentas».

## Odoo

**Qué es:** un ERP de código abierto formado por aplicaciones que se instalan por separado (Ventas, Inventario, Facturación, CRM…). Versión actual: Odoo 19.

**Cómo gestiona las ventas:**

- Se crea un **presupuesto**. Al confirmarlo pasa a ser un **pedido de venta**.
- Al confirmar el pedido aparecen botones que llevan a la **entrega** (en Inventario) y a la **factura** (en Facturación).
- Se puede facturar por lo **pedido** o por lo **entregado** (política de facturación).
- Un pedido confirmado se puede **bloquear** para que nadie lo modifique.
- Por defecto cada paso (confirmar, entregar, facturar y registrar el pago) se hace a mano. Hay módulos extra para automatizarlo.

**Licencia:** tiene dos ediciones. *Community* es gratuita y de código abierto (LGPL v3). *Enterprise* se paga por usuario y mes: unos 25 € por usuario y mes en el plan Standard, con pago anual.

## SAP S/4HANA

**Qué es:** el ERP de SAP pensado para empresas grandes. Su parte de ventas se llama *Sales* (antes SD, *Sales and Distribution*).

**Cómo gestiona las ventas:** sigue un proceso llamado **Order to Cash** (del pedido al cobro).

- **Pedido de venta** → **documento de entrega** → **documento de facturación** → **cobro**.
- Cada documento **copia los datos del anterior**. La entrega copia productos y cantidades del pedido, y la factura copia del pedido y de la entrega.
- La factura puede hacerse **a partir del pedido o a partir de la entrega**. Lo decide la **configuración**: cada categoría de posición tiene un campo de «relevancia para facturación». En la posición estándar (TAN) se factura a partir de la entrega.
- La factura genera los apuntes de contabilidad **automáticamente**.
- Tiene paneles para ver los pedidos bloqueados, pendientes de entregar o pendientes de facturar.

**Licencia:** de pago, con un precio que se negocia con SAP o con un partner. No hay una tarifa pública sencilla.

## Microsoft Dynamics 365 Business Central

**Qué es:** el ERP de Microsoft para pequeñas y medianas empresas. Funciona en la nube y está integrado con Office y Teams.

**Cómo gestiona las ventas:**

- Puede empezar con una **oferta**, que se convierte en **pedido**.
- Al **registrar** el pedido se crean el **envío** y la **factura**, a la vez o por separado.
- Permite **envíos y facturas parciales**. En cada línea se indica cuánto se envía y cuánto se factura.
- Cuando el pedido está enviado y facturado del todo, **desaparece de la lista** de pedidos abiertos.
- Una factura **ya pagada no se borra**. Se corrige con un **abono** (factura rectificativa) o con una devolución.

**Licencia:** de pago por usuario y mes. El plan Essentials cuesta unos 80 $ y el Premium unos 110 $, con pago anual.

## Comparación

| | Odoo | SAP S/4HANA | Business Central |
|---|---|---|---|
| Pensado para | Pymes y empresas medianas | Grandes empresas | Pymes |
| Pasos de la venta | Presupuesto → pedido → entrega → factura → pago | Pedido → entrega → factura → cobro | Oferta → pedido → envío + factura → cobro |
| Entregas parciales | Sí | Sí | Sí |
| Cuándo se factura | Por lo pedido o por lo entregado (según el producto) | A partir del pedido o de la entrega (según la configuración) | Al registrar el pedido |
| Corregir una factura | Factura rectificativa (nota de crédito) | Documento de abono | Abono |
| Código abierto | Sí (Community) | No | No |
| Coste | Gratis o por usuario | Alto, con presupuesto | Por usuario |
| Dificultad para aprender | Baja | Alta | Media |

## Ventajas y desventajas

### Odoo

- **Ventajas:** gratis en la versión Community y fácil de probar con Docker. Es muy modular: instalas solo lo que necesitas.
- **Desventajas:** algunas funciones avanzadas solo están en la versión de pago. Por defecto muchos pasos son manuales.

### SAP S/4HANA

- **Ventajas:** muy completo y configurable: cada empresa decide si factura por pedido o por entrega. Todo queda conectado con contabilidad automáticamente.
- **Desventajas:** caro y complejo, hacen falta consultores para implantarlo. Demasiado grande para una empresa pequeña.

### Business Central

- **Ventajas:** integrado con Office, Teams y Power BI. Los envíos y las facturas parciales son muy sencillos.
- **Desventajas:** de pago por usuario y sin código abierto. Depende del ecosistema de Microsoft.

## Contraste con el contrato de la API (paquete D)

El contrato 0.1.0 (`docs/openapi.yaml`) coincide con los tres ERP en lo básico. En tres puntos la investigación aporta argumentos para las decisiones pendientes de `docs/revision-contrato.md`.

| Idea de los ERP | Qué hace el contrato 0.1.0 | Valoración |
|---|---|---|
| Estados claros del pedido | BORRADOR → CONFIRMADO → SERVIDO → FACTURADO; CANCELADO solo desde BORRADOR o CONFIRMADO | Coincide. El cobro se sigue en la factura (EMITIDA, COBRADA, VENCIDA, ANULADA) y no en el pedido, igual que en SAP y Business Central. |
| Copiar datos del documento anterior | La línea copia descripción, precio e IVA al crearse y no cambia si Inventario modifica el precio | Coincide con SAP. |
| Bloquear el pedido confirmado | Solo se puede modificar (PUT) en BORRADOR | Coincide con Odoo. |
| Consultar otros módulos | Cliente en CRM (I1), producto y stock en Inventario (I2), comercial en RRHH (I3) | Coincide. |
| Servir y facturar por partes | No: el pedido se sirve de una vez y hay una factura por pedido | Diferencia aceptable porque simplifica el módulo. Se puede dejar como mejora futura. |
| Corregir una factura | Solo se anula si no tiene cobros; la rectificación está sin definir | Pendiente. Los tres ERP corrigen con un abono o factura rectificativa. |
| Fallo a mitad de servir | Riesgo señalado; falta acordarlo con Inventario | Una sola base de datos no lo evita por sí misma: solo hay «todo o nada» si el programa agrupa los cambios en una transacción (en MySQL, por defecto, cada sentencia se confirma por separado). En microservicios cada servicio tiene su base de datos y no hay transacción común, así que hay que pactar con Inventario un lote o unas operaciones de compensación. |

Propuestas para la reunión del grupo:

1. **Factura rectificativa** para corregir facturas que ya tienen cobros, como hacen Odoo, SAP y Business Central.
2. **Entregas y facturas parciales fuera de H1**, anotadas como mejora para un sprint posterior.
3. **Salida por lote en Inventario**: pedir que registre todas las líneas del pedido o ninguna.

## Prueba de Odoo con Docker

### Cómo arrancarlo

El archivo está en [`docs/docker-compose.yml`](docker-compose.yml) (Odoo 19 y PostgreSQL 16). Desde la raíz del repositorio:

```powershell
docker compose -f docs/docker-compose.yml up -d
```

Después hay que abrir `http://localhost:8069`, crear una base de datos con **Demo Data** marcado e instalar las apps **Ventas** e **Inventario** (Facturación se instala con Ventas). Para apagarlo: `docker compose -f docs/docker-compose.yml down`.

Si se ejecuta `docker compose up -d` en una carpeta sin el archivo, Docker responde `no configuration file provided: not found`. Nos pasó en el primer intento.

### Resultados reales (27/11/2026, PC de Manuel con Windows)

Solo se anota lo que se ve en las capturas guardadas en [`docs/capturas/`](capturas/).

| Prueba | Resultado observado |
|---|---|
| Arranque | Odoo abrió en `localhost:8069` el formulario para crear la base de datos. |
| Venta 1 · S00001 → INV/2026/00001 | Cliente de ejemplo *Decor Addict* (Canadá), 2 × *Large Desk* a 0,00 € con impuesto «0% EX B». La factura quedó **Registrado** y marcada **PAGADO** sola, porque el total era 0 €. No apareció botón de pago. |
| Venta 2 · S00002 → INV/2026/00002 | Cliente nuevo *cliente salamanca*, 2 × *Large Desk* a 150,00 € con IVA 21 %. Base 300,00 €, IVA 63,00 €, total **363,00 €**. Estado **Registrado** y botón **Pagar** disponible. |
| Estados de la factura | Barra de estado **Borrador → Registrado**. El pago se muestra aparte (banda *PAGADO*). |
| Botones de una factura registrada | Enviar, Imprimir, Pagar (solo si queda importe), Vista previa, **Factura rectificativa** y Restablecer a borrador. |
| Fechas | En las dos facturas, fecha de factura, de vencimiento y de entrega: 27 nov. |

Qué nos dice para nuestro módulo:

- El cobro va aparte del estado de la factura, como en el contrato (EMITIDA / COBRADA).
- Odoo ofrece el botón **Factura rectificativa** en una factura registrada: apoya la propuesta 1 del apartado «Contraste con el contrato de la API» (falta probar qué genera).
- Odoo calculó base, IVA y total a partir de precio, cantidad e impuesto, como propone el contrato.

### Pendiente de comprobar

- Pulsar **Pagar** en INV/2026/00002 y anotar el estado final de la factura.
- Hacer captura del pedido confirmado y de la entrega validada (no hay capturas de esos pasos).
- **Entrega parcial**: pedir 2 unidades, entregar 1 y anotar qué hace Odoo.
- **Factura rectificativa**: crearla sobre una factura y anotar el resultado.
- Anotar los campos de un pedido y de una línea de pedido.
- Apagar con `docker compose down` y comprobar que los datos siguen al volver a arrancar.

## Fuentes

- [Odoo — Crear presupuestos](https://www.odoo.com/documentation/18.0/applications/sales/sales/sales_quotations/create_quotations.html)
- [Odoo — Licencias de Community y Enterprise](https://www.odoo.com/documentation/master/legal/licenses.html)
- [Odoo — Políticas de facturación (lo pedido o lo entregado)](https://www.odoo.com/documentation/17.0/applications/sales/sales/invoicing/invoicing_policy.html)
- [SAP Help — Billing Relevance (relevancia para facturación)](https://help.sap.com/erp2005_ehp_07/helpdata/en/3e/71b6535fe6b74ce10000000a174cb4/content.htm)
- [SAP Knowledge Base 3513573 — Facturación relacionada con pedido o con entrega](https://userapps.support.sap.com/sap/support/knowledge/en/3513573)
- [SAP Learning — Describing the Order-to-Cash Process](https://learning.sap.com/courses/exploring-sap-s-4hana-sales-essentials/describing-the-order-to-cash-process_e4256fc4-3382-4545-a18e-465b69737b5f)
- [Microsoft Learn — Vender productos con un pedido de venta (Business Central)](https://learn.microsoft.com/en-gb/dynamics365/business-central/sales-how-sell-products)
- [Microsoft Learn — Registrar ventas (Business Central)](https://learn.microsoft.com/en-us/dynamics365/business-central/ui-post-sales)
- [Microsoft — Precios de Dynamics 365 Business Central](https://www.microsoft.com/dynamics-365/products/business-central/pricing)
- [Docker Hub — Imagen oficial de Odoo](https://hub.docker.com/_/odoo)
- [MySQL — autocommit, Commit y Rollback](https://dev.mysql.com/doc/refman/26.10/en/innodb-autocommit-commit-rollback.html)
- [Microsoft Learn — Patrón Saga para transacciones distribuidas](https://learn.microsoft.com/azure/architecture/patterns/saga)

Los precios son las tarifas públicas consultadas en noviembre de 2026 y pueden cambiar.

## Ayuda de IA

Se ha utilizado Claude (Anthropic) para buscar información, redactar la comparación y contrastarla con el contrato OpenAPI. Manuel ha revisado el contenido y debe comprenderlo antes de entregarlo y defenderlo.
