#!/bin/bash
source ~/manchetes_brasil/env/bin/activate
python3 main.py >> /var/log/manchetes_brasil/daily.log
