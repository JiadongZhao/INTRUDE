Python module dependencies: flask, datetime, flaskext.mysql, csv, os, platform, json, requests

RUN SITE: python backend_interface.py
    uses/calls interface.html and PRcommenter.py
    requires mysqlParams.txt in input file
    accesses a defined data folder (machine-specific), from which it pulls dupPR pair info (txt files)
    accesses fork database, duppr_pair table

PRcommenter.py
    called from within the site, by interface.py
    requires authParams.txt in input file

Files in input folder:
    mysqlParams.txt: Contains MySQL authentication info. Format (row order) below.
        MYSQL_USERNAME
        MYSQL_PASSWORD
        MYSQL_HOST
    authParams.txt: Contains GitHub authentication info. Format below.
        GH_USERNAME
        GH_TOKEN
        

How to execute:
    python backend_interface.py
    url: python backend_interface.py