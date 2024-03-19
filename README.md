# Invoice Manager

Web API built with DRF for handling invoice and invoice detail requests

## Setup

Cloning and setting up enviornment (python 3.10 or above required)
```shell
git clone https://github.com/divyjx/InvoiceManager.git .
python -m venv myenv
source myenv/bin/activate
pip install - requirements.txt
```

Starting server
```shell
cd InvoiceManager
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```



## Tests
For checking functioning of api endpoints
```shell
./manager.py test
```

## Requests
Allowed method and urls. Here pk denotes integer primary key.

|methods | urls|use|json template|
|--------|-----|--------|:-|
| GET |      /invoices     | list all | None
| POST |     /invoices     | create | inovoice
| GET |      /invoices/pk| retrieve | None
| PUT |      /invoices/pk|  update | invoice or invoice + detail
| PATCH |    /invoices/pk| partial update | invoice or details or invoice + details
| DELETE |   /invoices/pk| delete | None

Example
```
>>> curl -X GET http://127.0.0.1:8010/invoices/2
{"invoice":{"id":2,"date":"2024-03-19T08:44:54.350161Z","customer_name":"Nwww changes"},"details":{"id":2,"description":"Product description patched","quantity":null,"unit_price":null,"price":90.0,"invoice":2}}
```

## JSON templates 

* invoice
```
{
    "customer_name":"XYZ"
}
```
* details
```
{
    "details":{
        "description":"ABC",
        "price":null,
        "unit_price":90,
        "qunatity":100
    }
}
```

* invoice + details
```
{
    "customer_name":"XYZ",
    "details":{
        "description":"ABC",
        "price":null,
        "unit_price":90,
        "qunatity":100
    }
}
```

