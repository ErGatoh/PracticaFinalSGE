"""Valida estructura OpenAPI 3.0.3, referencias y ejemplos JSON.

Instalación en un entorno Python propio:
    python -m pip install openapi-spec-validator
Ejecución desde cualquier carpeta:
    python docs/validar_openapi.py
"""

from pathlib import Path

import yaml
from openapi_spec_validator import validate
from openapi_schema_validator import OAS30Validator
from jsonschema import RefResolver


def main():
    path = Path(__file__).with_name("openapi.yaml")
    contract = yaml.safe_load(path.read_text(encoding="utf-8"))
    validate(contract)
    resolver = RefResolver.from_schema(contract)
    operations = 0
    examples = 0
    ids = set()
    for route, item in contract["paths"].items():
        for method, operation in item.items():
            if method not in {"get", "post", "put", "patch", "delete", "head", "options"}:
                continue
            operations += 1
            assert operation["operationId"] not in ids, "operationId repetido"
            ids.add(operation["operationId"])
            bodies = [operation.get("requestBody", {})]
            bodies.extend(operation["responses"].values())
            for body in bodies:
                if "$ref" in body:
                    body = resolver.resolve(body["$ref"])[1]
                for media, content in body.get("content", {}).items():
                    if media == "application/json" and "example" in content:
                        OAS30Validator(content["schema"], resolver=resolver).validate(content["example"])
                        examples += 1
    # También se revisan los ejemplos comunes de error aunque ningún path los usara.
    for response in contract["components"]["responses"].values():
        content = response["content"]["application/json"]
        OAS30Validator(content["schema"], resolver=resolver).validate(content["example"])
        examples += 1
    print(f"OK: OpenAPI {contract['openapi']}; {len(contract['paths'])} rutas; "
          f"{operations} operaciones; {examples} ejemplos JSON válidos.")
    print("Validación estática: no acredita aprobación del equipo ni funcionamiento de un backend.")


if __name__ == "__main__":
    main()
