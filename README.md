Introduction
------------
aws lambda code for import aws elb logs to elasticsearch

Version
-------
- OS: Amazon linux
- Python: 2.7.6

Installation
------------
- install virtualenv
```
sudo pip install virtualenv
```
- create virtualenv
```
virtualenv --no-site-packages venv
or
./make_virtualenv.sh
```
- attach
```
source venv/bin/activate
```
- install python package
```
pip install -r requirements.txt
```

Set Config
-------------------------
Modify configuration for set elasticsearch information
- file name: lambda_function.py
- configs
```
ES_HOST: elasticsearch host
ES_PORT: elasticsearch port (default 80) 
ES_BULK_CHUNK_SIZE: bulk upload chuk size (default 1000)
```

Make lambda package
-------------------
run make_lambda_pkg.sh<br />
Must run script on Amazon linux.<br />
If you run script on ubuntu, package(zip file) is not understood in lambda.<br />
```
./make_lambda_pkg.sh
```
