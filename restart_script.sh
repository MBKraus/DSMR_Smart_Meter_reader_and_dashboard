#!/bin/bash

logger 'restarting dashboard'
pkill python
cd <absolute path to app.py> && . <absolute path to env>/bin/activate && python app.py
