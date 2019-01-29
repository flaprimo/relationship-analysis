# Relationship analysis
<a href='https://travis-ci.org/flaprimo/relationship-analysis'><img src='https://secure.travis-ci.org/flaprimo/relationship-analysis.png?branch=master'></a>

Pipeline to analyze aggregated conversations between 2 individuals over multiple chat/call services.

Supported services:
* Telegram (chat export)
* Whatsapp (chat export)
* Calls history

## Steps
Analysis is performed in several sequential pipelines, which produce intermediate results in the output.

## Installation
1. Intall required linux packages: `sudo apt install python3 python3-dev python3-venv`
2. Create a virtual environment: `python3 -m venv venv`
3. Enter in the virtual environment: `. venv/bin/activate`
4. Install python required modules `pip install requirements.txt`