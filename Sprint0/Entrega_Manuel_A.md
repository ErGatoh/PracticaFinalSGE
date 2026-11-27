# Sprint 0 · Persona A — Investigación de ERP

Autor: Manuel. Grupo 3, paquete A: Ventas y facturación. ERP «Meseta». Fecha: 27/11/2026.

## 1. Objetivo

Antes de diseñar nuestro módulo hemos estudiado cómo gestionan las ventas tres ERP muy usados: **Odoo**, **SAP S/4HANA** y **Microsoft Dynamics 365 Business Central**. Nos fijamos en una sola cosa: el camino que recorre una venta desde que se crea el pedido hasta que se cobra. Al final sacamos ideas concretas para nuestro diseño.

## 2. El camino común de una venta

Los tres ERP siguen los mismos cinco pasos, aunque los llamen de forma distinta:

1. **Presupuesto**: se ofrece un precio al cliente. Todavía no es una venta.
2. **Pedido**: el cliente acepta y el presupuesto se convierte en pedido.
3. **Entrega**: se sirve la mercancía y se descuenta del almacén.
4. **Factura**: se emite el documento de cobro.
5. **Cobro**: el cliente paga y la venta queda cerrada.

Dicho de forma sencilla: el pedido es la «promesa», la entrega es «cumplir la promesa», y la factura y el cobro son «pasar cuentas».

## 3. Odoo

**Qué es:** un ERP de código abierto formado por aplicaciones que se instalan por separado (Ventas, Inventario, Facturación, CRM…). Versión actual: Odoo 19.

**Cómo gestiona las ventas:**

- Se crea un **presupuesto**. Al confirmarlo pasa a ser un **pedido de venta**.
- Al confirmar el pedido aparecen botones que llevan a la **entrega** (en Inventario) y a la **factura** (en Facturación).
- Se puede facturar por lo **pedido** o por lo **entregado** (política de facturación).
- Un pedido confirmado se puede **bloquear** para que nadie lo modifique.
- Por defecto cada paso (confirmar, entregar, facturar y registrar el pago) se hace a mano. Hay módulos extra para automatizarlo.

**Licencia:** tiene dos ediciones. *Community* es gratuita y de código abierto (LGPL v3). *Enterprise* se paga por usuario y mes: unos 25 € por usuario y mes en el plan Standard, con pago anual.

## 4. SAP S/4HANA

**Qué es:** el ERP de SAP pensado para empresas grandes. Su parte de ventas se llama *Sales* (antes SD, *Sales and Distribution*).

**Cómo gestiona las ventas:** sigue un proceso llamado **Order to Cash** (del pedido al cobro).

- **Pedido de venta** → **documento de entrega** → **documento de facturación** → **cobro**.
- Cada documento **copia los datos del anterior**. La entrega copia productos y cantidades del pedido, y la factura copia del pedido y de la entrega.
- El orden es **estricto**: no se puede facturar mercancía sin entregarla. Los servicios son la excepción y se facturan directamente desde el pedido.
- La factura genera los apuntes de contabilidad **automáticamente**.
- Tiene paneles para ver los pedidos bloqueados, pendientes de entregar o pendientes de facturar.

**Licencia:** de pago, con un precio que se negocia con SAP o con un partner. No hay una tarifa pública sencilla.

## 5. Microsoft Dynamics 365 Business Central

**Qué es:** el ERP de Microsoft para pequeñas y medianas empresas. Funciona en la nube y está integrado con Office y Teams.

**Cómo gestiona las ventas:**

- Puede empezar con una **oferta**, que se convierte en **pedido**.
- Al **registrar** el pedido se crean el **envío** y la **factura**, a la vez o por separado.
- Permite **envíos y facturas parciales**. En cada línea se indica cuánto se envía y cuánto se factura.
- Cuando el pedido está enviado y facturado del todo, **desaparece de la lista** de pedidos abiertos.
- Una factura **ya pagada no se borra**. Se corrige con un **abono** (factura rectificativa) o con una devolución.

**Licencia:** de pago por usuario y mes. El plan Essentials cuesta unos 80 $ y el Premium unos 110 $, con pago anual.

## 6. Comparación

| | Odoo | SAP S/4HANA | Business Central |
|---|---|---|---|
| Pensado para | Pymes y empresas medianas | Grandes empresas | Pymes |
| Pasos de la venta | Presupuesto → pedido → entrega → factura → pago | Pedido → entrega → factura → cobro | Oferta → pedido → envío + factura → cobro |
| Entregas parciales | Sí | Sí | Sí |
| Cuándo se factura | Por lo pedido o por lo entregado | Normalmente por lo entregado | Al registrar el pedido |
| Corregir una factura | Nota de crédito | Documento de abono | Abono |
| Código abierto | Sí (Community) | No | No |
| Coste | Gratis o por usuario | Alto, con presupuesto | Por usuario |
| Dificultad para aprender | Baja | Alta | Media |

## 7. Ventajas y desventajas

### Odoo

- **Ventajas:** gratis en la versión Community y fácil de probar con Docker. Es muy modular: instalas solo lo que necesitas.
- **Desventajas:** algunas funciones avanzadas solo están en la versión de pago. Por defecto muchos pasos son manuales.

### SAP S/4HANA

- **Ventajas:** muy completo y muy controlado, ningún paso se puede saltar. Todo queda conectado con contabilidad automáticamente.
- **Desventajas:** caro y complejo, hacen falta consultores para implantarlo. Demasiado grande para una empresa pequeña.

### Business Central

- **Ventajas:** integrado con Office, Teams y Power BI. Los envíos y las facturas parciales son muy sencillos.
- **Desventajas:** de pago por usuario y sin código abierto. Depende del ecosistema de Microsoft.

## 8. Contraste con el contrato de la API (paquete D)

El contrato 0.1.0 (`docs/openapi.yaml`) coincide con los tres ERP en lo básico. En tres puntos la investigación aporta argumentos para las decisiones pendientes de `docs/revision-contrato.md`.

| Idea de los ERP | Qué hace el contrato 0.1.0 | Valoración |
|---|---|---|
| Estados claros del pedido | BORRADOR → CONFIRMADO → SERVIDO → FACTURADO; CANCELADO solo desde BORRADOR o CONFIRMADO | Coincide. El cobro se sigue en la factura (EMITIDA, COBRADA, VENCIDA, ANULADA) y no en el pedido, igual que en SAP y Business Central. |
| Copiar datos del documento anterior | La línea copia descripción, precio e IVA al crearse y no cambia si Inventario modifica el precio | Coincide con SAP. |
| Bloquear el pedido confirmado | Solo se puede modificar (PUT) en BORRADOR | Coincide con Odoo. |
| Consultar otros módulos | Cliente en CRM (I1), producto y stock en Inventario (I2), comercial en RRHH (I3) | Coincide. |
| Servir y facturar por partes | No: el pedido se sirve de una vez y hay una factura por pedido | Diferencia aceptable porque simplifica el módulo. Se puede dejar como mejora futura. |
| Corregir una factura | Solo se anula si no tiene cobros; la rectificación está sin definir | Pendiente. Los tres ERP corrigen con un abono o factura rectificativa. |
| Fallo a mitad de servir | Riesgo señalado; falta acordarlo con Inventario | En un ERP de un solo sistema no pasa, porque entrega y stock están en la misma base de datos. En microservicios hay que pactarlo. |

Propuestas para la reunión del grupo:

1. **Factura rectificativa** para corregir facturas que ya tienen cobros, como hacen Odoo, SAP y Business Central.
2. **Entregas y facturas parciales fuera de H1**, anotadas como mejora para un sprint posterior.
3. **Salida por lote en Inventario**: pedir que registre todas las líneas del pedido o ninguna.

## 9. Prueba de Odoo con Docker

Guarda esto como `docker-compose.yml` en una carpeta vacía:

```yaml
services:
  web:
    image: odoo:19.0
    depends_on:
      - db
    ports:
      - "8069:8069"
  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
```

Pasos:

1. En esa carpeta ejecuta `docker compose up -d`.
2. Abre `http://localhost:8069` y crea una base de datos marcando **datos de demostración**.
3. Instala las apps **Ventas**, **Inventario** y **Facturación**.
4. Haz una venta completa: presupuesto → confirmar → validar entrega → crear factura → registrar pago.
5. Al terminar, apágalo con `docker compose down`.

Qué apuntar durante la prueba, para compararlo con nuestro módulo:

- Qué campos tienen un pedido y una línea de pedido.
- Por qué estados pasa el pedido y qué botones aparecen en cada uno.
- Qué pasa si solo se entrega una parte.
- Cómo se corrige una factura ya emitida.

## 10. Fuentes

- [Odoo — Crear presupuestos](https://www.odoo.com/documentation/18.0/applications/sales/sales/sales_quotations/create_quotations.html)
- [Odoo — Licencias de Community y Enterprise](https://www.odoo.com/documentation/master/legal/licenses.html)
- [SAP Learning — Describing the Order-to-Cash Process](https://learning.sap.com/courses/exploring-sap-s-4hana-sales-essentials/describing-the-order-to-cash-process_e4256fc4-3382-4545-a18e-465b69737b5f)
- [Microsoft Learn — Vender productos con un pedido de venta (Business Central)](https://learn.microsoft.com/en-gb/dynamics365/business-central/sales-how-sell-products)
- [Microsoft Learn — Registrar ventas (Business Central)](https://learn.microsoft.com/en-us/dynamics365/business-central/ui-post-sales)
- [Microsoft — Precios de Dynamics 365 Business Central](https://www.microsoft.com/dynamics-365/products/business-central/pricing)
- [Docker Hub — Imagen oficial de Odoo](https://hub.docker.com/_/odoo)

Los precios son las tarifas públicas consultadas en noviembre de 2026 y pueden cambiar.

## Ayuda de IA

Se ha utilizado Claude (Anthropic) para buscar información, redactar la comparación y contrastarla con el contrato OpenAPI. Manuel ha revisado el contenido y debe comprenderlo antes de entregarlo y defenderlo.
