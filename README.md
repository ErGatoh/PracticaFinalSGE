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

Basado en el enunciado de la práctica. Se ha utilizado **Codex (OpenAI)** como apoyo para redactar y validar el contrato y su documentación.
