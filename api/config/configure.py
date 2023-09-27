import logging
from pydantic import BaseModel, EmailStr, conint, conlist, Json, constr, HttpUrl, FilePath, ValidationError
from os import environ, path
import yaml
from pprint import pprint
import sys



class database_schema(BaseModel):
    DB: constr(min_length=8,max_length=64) = "blogindex"
    DB_HOST: str = "db"
    DB_USER: constr(min_length=8,max_length=64) = "blogindex"
    DB_PASS: constr(min_length=8,max_length=64) = "In5ecuRe-P@5S"

class blogindex_schema(BaseModel):
    YAML: str = ""
    DEVEL: bool = False
    LOG_LEVEL: constr(pattern="NOTSET|DEBUG|INFO|WARN|ERROR|CRITICAL") = "INFO"
    LOG_FILE: str = "./logs/blogindex.log"
    
class auth0_schema(BaseModel):
    YAML: str = ""
    DOMAIN: str = "your.domain.com"
    API_AUDIENCE: str = "your.audience.com"
    ISSUER: str = "https://your.domain.com"
    ALGORITHMS: str = "RS256"

config = {
    "DATABASE":{
        "YAML": "",
        "DB": "blogindex",
        "DB_HOST": "db",
        "DB_USER": "blogindex",
        "DB_PASS": "In5ecuRe-Pa5S",
        "schema": "database"
    },
    "BLOGINDEX": {
        "YAML": "",
        "DEVEL": False,
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "blogindex.log",
        "schema": "blogindex"
    },
    "AUTH0": {
        "YAML": "",
        "DOMAIN": "your.domain.com",
        "API_AUDIENCE": "your.audience.com",
        "ISSUER": "https://your.domain.com",
        "ALGORITHMS": "RS256",
        "schema": "auth0"
    }
}



class Configure():
    def __init__(
            self,prefixes:list=[
                "BLOGINDEX",
                "AUTH0",
                "DATABASE"
            ],
            config:dict=config
        ):
        self.prefixes = prefixes
        self.config = config

    def from_yaml(self,prefix):
        """ Retrieves config from yaml file
        Args:
            filename (str): /path/to/config.yaml
            config (dict): configuration dictionary
        Returns:
            dict: configuration dictionary
        """
        # Get config yaml file and place it in a dict
        yaml_env = f"{prefix}_YAML"
        yaml_file = environ[yaml_env] if yaml_env in environ else config[prefix]["YAML"]
        if path.isfile(self.config[prefix]["YAML"]):
            with open(self.config[prefix]["YAML"]) as config_file:
                config_yaml = yaml.safe_load(config_file)
            # Only grab the keys defined in self.config
            for key in config:
                if key in config_yaml:
                    self.config[prefix][key] = config_yaml[key]

    def from_env(self,prefix):
        """Retrieves config from environment variables, overriding config from yaml
        Args:
            prefix (str): Environment Variable Prefix
            config (dict): configuration dictionary
        Returns:
            dict: configuration dictionary
        """
        for key in self.config[prefix]:
                v = f"{prefix}_{key}"
                if v in environ:
                    log_entry = f"Env Var {v}: "
                    log_entry += "*********" if "PASS" in key else f"{environ[v]}"
                    logging.debug(log_entry)
                    self.config[prefix][key] = environ[v]

    def validate(self,prefix):
        schema = globals()[self.config[prefix]["schema"] + "_schema"]
        try:
            schema(**self.config[prefix])
        except ValidationError as exc:
            logging.debug(f" Validation Error: {exc}")
            raise

    def get(self):
        for prefix in self.prefixes:
            self.from_yaml(prefix)
            self.from_env(prefix)
            self.validate(prefix)
            #self.get_prefix(prefix)
        return self.config



if __name__ == "__main__":
    prefixes = ["BLOGINDEX","AUTH0"]
    blogindex = Configure(config,prefixes)
    #blogindex.get()
    pprint(blogindex.get())
