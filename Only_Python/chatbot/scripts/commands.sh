#!/usr/bin/env bash

python -m unittest

coverage run --source=bot, handlers, settings -m unittest
coverage report -m

psql -c 'create database chat_bot'

psql -d chat_bot