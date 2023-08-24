# -*- coding: utf-8 -*

from datetime import datetime

import requests
import logging
import json
import time
import os

API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

##
#

class Record:

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

    # def save(self):
    #     return self.session.save(self.id, self.data)
    
    # def remove(self):
    #     return self.session.remove(self.id)

    def to_dict(self):
        return self.__dict__

##
#

class Session(requests.Session):
   
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.headers.update({"Authorization": f"Bearer {API_KEY}"})
        
    def findAll(self, params={}):

        logging.debug("finding in %s with %s", self.url, params)

        offset = 0
        limit = 100
        records = []

        while True:

            try:

                logging.debug("get records offset %d limit %d", offset, limit)

                res = self.get(self.url, params={"offset": offset, "limit": limit})

                if res.status_code >= 400:
                    logging.error(res.text)
                    return

                tmp = res.json()['records']

                if not tmp:
                    break

                records += tmp

                logging.debug("records found: %d", len(records))
                logging.debug("X-Ratelimit-Limit: %s", res.headers['X-Ratelimit-Limit'])
                logging.debug("X-Ratelimit-Remaining:  %s", res.headers['X-Ratelimit-Remaining'])
                logging.debug("X-Ratelimit-Reset: %s", res.headers['X-Ratelimit-Reset'])

                offset += limit

            except Exception as ex:
                logging.warning(ex)
                raise ex
       
            time.sleep(0.01)

        if "created_at_min" in params:
            dt = datetime.fromisoformat(params['created_at_min'])
            records = [x for x in records if datetime.fromisoformat(x['created_at'][:-1]) > dt ]

        return [Record(x, self) for x in records]
    
    def findOne(self, criteria=None):

        data = self.findAll(criteria)

        if not data:
            raise Exception(f"Not data for {criteria} in ")
        
        return data[0]
    
    # def create(self, data):

    #     logging.debug("creating in %s with %s", self.url, data)
       
    #     res = self.post(self.url, json=data)

    #     if res.status_code >= 400:
    #         raise Exception(f"{res.status_code}: {res.text}")

    #     return res.json()
    
    # def save(self, id, data):

    #     logging.debug("updating in %s/%s with %s", self.url, id, data)
       
    #     res = self.put(f"{self.url}/{id}", json=data)

    #     if res.status_code >= 400:
    #         raise Exception(f"{res.status_code}: {res.text}")

    #     return res.json()
    
    # def remove(self, id):

    #     logging.debug("removing in %s/%s", self.url, id)
       
    #     res = self.delete(f"{self.url}/{id}")

    #     if res.status_code >= 400:
    #         raise Exception(f"{res.status_code}: {res.text}")

    #     return res.text

##
#

class Collection(Session):
   
    def __init__(self, name):
        super().__init__(f"https://api.adalo.com/v0/apps/{APP_ID}/collections/{name}")
