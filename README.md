# Adalo Api
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Instalación

```bash
pip install git+https://github.com/lastseal/adalo-api
```

## Tutorial

### Paso 1: Configurar Variables de Ambiente

En un archivo ```.env``` agregar el id de la aplicación en Adalo y el Api Key de acceso.

```txt
APP_ID=c3d3ad91-c569-47b7-bbab-a40823e02f6a
API_KEY=82goso92zcemcn1ecw8lyzvie
```

### Paso 2: Importar Módulo

En tu código importar el módulo y configurar la colección con la que se va a trabajar.

```python
from adalo import api

multimedia = api.Collection("t_bfmoi0f5mg6a1qj8crygzfami")
```

### Paso 3: Leer Datos de la Colección

Se buscan los datos de la colección de Adalo desde una fecha en adelante.

```python
multimedia = api.Collection("t_bfmoi0f5mg6a1qj8crygzfami")

items = multimedia.findAll({"created_at_min": "2023-07-26T00:00:00"})
print(items)
```

Para buscar todos los registros de la colección no se le pasa ningún parámetro.

```python
multimedia = api.Collection("t_bfmoi0f5mg6a1qj8crygzfami")

items = multimedia.findAll()
print(items)
```

### Paso 4: Relacionar Colecciones

```python
companies = api.Collection("t_8ckhaq1iyfze15oc17pd9bde3").findAll(fields=["id", "Nombre"])

multimedia = api.Collection("t_bfmoi0f5mg6a1qj8crygzfami", {
    "Cia_receptora": [x.to_dict() for x in companies]
})

items = multimedia.findAll()

for item in items:
    print(item.to_dict())
