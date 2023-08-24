# -*- coding: utf-8 -*

from micro import config
from adalo import api

companies = api.Collection("t_8ckhaq1iyfze15oc17pd9bde3").findAll(fields=["id", "Nombre"])
print("companies:", len(companies))

multimedia = api.Collection("t_bfmoi0f5mg6a1qj8crygzfami", {
    "Cia_receptora": [x.to_dict() for x in companies]
})

items = multimedia.findAll({"created_at_min": "2023-08-03T18:52:21"})

for item in items:
    print(item.to_dict())