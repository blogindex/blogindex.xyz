"""
api/helpers/configuration.py
------------------------
- blogindex.config set with sane default values
- default values overriden with values from
  1. config.yml
  2. environment variables.

  config.yml will always override defaults
  environment vars will override everything

Usage:
------------------------
# Import
from .helpers.configuration import config_schema, blogindex

# Setup Class
blogindex = blogindex()
# Run Init <-- This can be done any time you want to reload the configuration on the fly
blogindex.get(config_schema)

# Access config
LOG_LEVEL = blogindex.config['LOG_LEVEL']
"""
import logging
from pydantic import BaseModel, EmailStr, conint, conlist, Json, constr, HttpUrl, FilePath
from os import environ, path
import yaml
from pprint import pprint
import sys

class config_schema(BaseModel):
    CONFIG_FILE: str = "/blogindex.xyz/config.yml"
    API_KEY_ADMIN: constr(min_length=14,max_length=39) = "aaaa-bbbb-cccc"
    API_KEY_HASH: constr(min_length=12,max_length=64) = "In5ecuRe-h@sH"
    DEVEL: bool = False
    LOG_LEVEL: constr(pattern="NOTSET|DEBUG|INFO|WARN|ERROR|CRITICAL")
    LOG_FILE: FilePath = "/blogindex.xyz/logs/blogindex.dev"
    DB: constr(min_length=8,max_length=64) = "blogindex"
    DB_USER: constr(min_length=8,max_length=64) = "blogindex"
    DB_PASS: constr(min_length=12,max_length=64) = "In5ecuRe-P@5S"
    DB_URL: str

class blogindex():
    def __init__(self):
        self.config_environ = {}
        self.config_yaml = {}
        self.config = {
            "CONFIG_FILE": "/blogindex.xyz/config.yml",
            "API_KEY_ADMIN": "aaaa-bbbb-cccc",
            "API_KEY_HASH":  "In5ecuRe-h@sH",
            "DEVEL": False,
            "LOG_LEVEL": "INFO",
            "LOG_FILE": "/blogindex.xyz/logs/blogindex.dev",
            "DB": "blogindex",
            "DB_USER": "blogindex",
            "DB_PASS": "In5ecuRe-P@5S",
            "DB_URL_TEMPLATE": "postgresql+psycopg2://<<DB_USER>>:<<DB_PASS>>@db/<<DB>>"
        }
        
    def get(self,schema):
        # Check if CONFIG_FILE is defined in environment variables
        if 'BLOGINDEX_CONFIG_FILE' in environ:
            self.config['CONFIG_FILE'] = environ['BLOGINDEX_CONFIG_FILE']
        else:
            self.config['CONFIG_FILE'] = "/blogindex.xyz/config.yml"

        # Get config yaml file and place it in a dict
        if path.isfile(self.config['CONFIG_FILE']):
            with open(self.config['CONFIG_FILE']) as config_file:
                self.config_yaml = yaml.safe_load(config_file)
            # Only grab the keys defined in self.config
            for key in self.config:
                if key in self.config_yaml:
                    self.config[key] = self.config_yaml[key]
        
        # Check for environment variables contained in self.config
        for key in self.config:
            if "BLOGINDEX_"+key in environ:
                self.config[key] = environ["BLOGINDEX_"+key]
        
        # Set DB_URL
        if not 'DB_URL' in self.config:
            self.config["DB_URL"] = self.config["DB_URL_TEMPLATE"]
        self.config["DB_URL"] = self.config["DB_URL"].replace("<<DB_USER>>",self.config["DB_USER"])
        self.config["DB_URL"] = self.config["DB_URL"].replace("<<DB_PASS>>",self.config["DB_PASS"])
        self.config["DB_URL"] = self.config["DB_URL"].replace("<<DB>>",self.config["DB"])
        logging.debug(f"DB_URL = {self.config['DB_URL']}")
        print(f"\n\
            ####################\n\
            DB_URL = {self.config['DB_URL']}")


        # Validate self.config
        config_model = config_schema(**self.config)
        try:
            # Attempt to 
            logging.debug(pprint(config_model))
            print(pprint(config_model))
        except ValidationError as exc:
            raise
        return self.config

if __name__ == "__main__":
    blogindex = blogindex_config()
    pprint(blogindex.get(config_schema))
