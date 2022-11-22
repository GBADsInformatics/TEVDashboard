
# GBADS Total Economic Value Dashboard

This dashboard was created ontop of the [GBADS Dashboard Template](https://github.com/GBADsInformatics/Dashboard_Template) by [@Amardeep](https://github.com/amardeep-1) and [@Nitin](https://github.com/Nitin501)

## Running in Docker
1. `docker run -d -p 80:8051 gbadsinformatics/tev-dash` \
  This exposes the dashboard on port `80` of your machine, you can change this number to any port you desire. \
  Do not change `8051` in the port argument.

## Installation
1. `git clone https://github.com/GBADsInformatics/TEV_Dashboard`
2. `cd dash`
3. `pip3 install -r requirements.txt`

## Running the App
1. `cd dash`
2. `python3 wsgi.py`
  
## Authors
- [@WilliamFitzjohn](https://github.com/WilliamFitzjohn)
- [@MatthewSzurkowski](https://github.com/MatthewSzurkowski)
