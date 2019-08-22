[![Codacy Badge](https://api.codacy.com/project/badge/Grade/530da9ba675f4785b6ca1f37f012fbe9)](https://www.codacy.com/app/izolot/edge-parser?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=izolot/edge-parser&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/izolot/edge-parser.svg?branch=master)](https://travis-ci.org/izolot/edge-parser)

## Instalation:
```bash
 git clone https://github.com/izolot/edge-parser.git
 cd edge-parser
 python3 -m venv env
 source env/bin/activate
 pip3 install -r requirements.txt
 export PYTHONPATH=$PYTHONPATH:$PWD/edge-parser/
```
## Settings:
``` bash
 nano config.py
 ```
 ``` python
 class Config(object):
    DEBUG = False
    TESTING = False
    ARCHIVE_PATH = "full path to archive"
 ```
 cameras.config -  file for parser, it is include path to different cameras in one big archive. Those paths needs for quick search.    
 
## TODO TASKS
- [ ] api for add camera(camera.config)
- [ ] show structure dirs
- [ ] remove temp files
