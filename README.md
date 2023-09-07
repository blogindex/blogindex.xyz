# blogindex.xyz
A Value 4 Value Blogging Community

## What is this repo?
This will be the base for blogindex.xyz.  All future sites will deploy from this repository.

## What's done?

### /api
- main.py
  - sets up FastAPI
- models.py
  - contains pydantic models defining the database
- schemas.py
  - contains pydantic schemas to verify data
- database.py
  - sets up database connections
- crud.py
  - Contains `c`reate, `r`ead, `u`pdate, and `d`elete functions.

- helpers
  - configuration.py
    - defines configuration of site with class `blogindex()`

