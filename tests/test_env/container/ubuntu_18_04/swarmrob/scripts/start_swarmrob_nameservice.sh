#!/bin/bash

/usr/local/bin/pyro4-ns -x --host=$($1 -I | cut -d' ' -f1) --port=9090
