HTTP Monitoring tool
====================

Install
-------

* Create virtual env (python 3.5.1)
* Install requirements
* Fill config
* Run `main.py`
* ???
* Profit

Config
------

* Simple json file `config.json`
* `interval` - seconds - how often requests are made
* `urls` array of object that contains information about HTTP endpoints to verify
 * `url` - required - simple url
 * `content` - optional - verifies if web page contains requested string