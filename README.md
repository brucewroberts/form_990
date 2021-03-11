# form_990
Form 990 Instrumentl Coding Challenge

# References

* [AWS IRS Form 990 Documentation](https://docs.opendata.aws/irs-990/readme.html)

# Results

* Store endpoint: http://0.0.0.0:5001/api/v1/store-form?form_id=201132069349300318 (did it this way instead of a separate script for initial simplicity)
* Recipients filtered by state: http://0.0.0.0:5001/api/v1/get-receivers?state=CA
* All filings with optional currency conversion: http://0.0.0.0:5001/api/v1/get-filings?currency=GBP

# Punchlist

## P1

* ~~Git repo~~
* ~~Review XML~~
* ~~XML parser~~
* ~~DB schema/script~~
* ~~Flask core setup~~
* ~~create_app() method~~
* ~~app/blueprint_main/routes.py~~
* ~~app/blueprint_api/routes.py~~
* ~~app/lib/db~~
* ~~instance/app.cnf~~
* ~~requirements.txt: mysql, defusedxml, others TDB~~
* ~~download 990 script~~
* ~~JSON endpoints~~
* ~~basic sanity check tests~~

## P2

* ~~docker container~~
* endpoint parameter validation: useargs added to requirements.txt
* logging
* PEP8 formatting

...
