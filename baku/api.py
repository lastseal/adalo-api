# -*- coding: utf-8 -*

import requests
import logging
import json
import jwt
import os

BASE_URL = os.getenv("BASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

TOKEN = jwt.encode({
    "scopes": [{"pattern": f".*/api/.*"}], 
    "userkey": "0"
}, SECRET_KEY, algorithm="HS256")

##
#

class Document:

    def __init__(self, data, session):
        for key in data:
            self.__dict__[key] = data[key]
        self.session = session

    @property
    def id(self):
        return self.__dict__['id']
    
    @property
    def created_at(self):
        return self.__dict__['created_at']
    
    @property
    def updated_at(self):
        return self.__dict__['updated_at']

    def save(self):
        return self.session.save(self.id, self.data)
    
    def remove(self):
        return self.session.remove(self.id)

##
#

class Session(requests.Session):
   
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.headers.update({"Authorization": f"Bearer {TOKEN}"})

    def count(self, criteria=None, order=None, created_at_min=None, created_at_max=None):

        params = {}

        if criteria is not None:
            params['criteria'] = json.dumps(criteria)

        if created_at_min is not None:
            params['created_at_min'] = created_at_min

        if created_at_max is not None:
            params['created_at_max'] = created_at_max

        logging.debug("counting in %s with %s", self.url, params)
       
        res = self.get(f"{self.url}/count", params=params)

        if res.status_code >= 400:
            raise Exception(f"{res.status_code}: {res.text}")
        
        logging.debug("res: %s", res.json())

        return res.json()["count"]
        
    def findAll(self, criteria=None, order=None, created_at_min=None, created_at_max=None):

        params = {}

        if criteria is not None:
            params['criteria'] = json.dumps(criteria)

        if created_at_min is not None:
            params['created_at_min'] = created_at_min

        if created_at_max is not None:
            params['created_at_max'] = created_at_max

        logging.debug("finding in %s with %s", self.url, params)
       
        res = self.get(self.url, params=params)

        if res.status_code >= 400:
            raise Exception(f"{res.status_code}: {res.text}")
        
        logging.debug("res: %s", res.json())

        return [Document(x, self) for x in res.json()]
    
    def findOne(self, criteria=None):

        data = self.findAll(criteria)

        if not data:
            raise Exception(f"Not data for {criteria} in ")
        
        return data[0]
    
    def create(self, data):

        logging.debug("creating in %s with %s", self.url, data)
       
        res = self.post(self.url, json=data)

        if res.status_code >= 400:
            raise Exception(f"{res.status_code}: {res.text}")

        return res.json()
    
    def save(self, id, data):

        logging.debug("updating in %s/%s with %s", self.url, id, data)
       
        res = self.put(f"{self.url}/{id}", json=data)

        if res.status_code >= 400:
            raise Exception(f"{res.status_code}: {res.text}")

        return res.json()
    
    def remove(self, id):

        logging.debug("removing in %s/%s", self.url, id)
       
        res = self.delete(f"{self.url}/{id}")

        if res.status_code >= 400:
            raise Exception(f"{res.status_code}: {res.text}")

        return res.text

##
#

class Collection(Session):
   
    def __init__(self, name):
        super().__init__(f"{BASE_URL}/api/collections/{name}")

##
#

class Request(Session):
   
    def __init__(self, uri):
        super().__init__(f"{BASE_URL}/{uri}")
