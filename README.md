
# clashboard_postgresql

A [Plot.ly Dash](https://dash.plot.ly/) dashboard  to explore [ClinicalTrails.gov](https://clinicaltrials.gov/) data 
stored in a PostgreSQL database hosted by 
[Clinical Traials Transformation Initiative](https://aact.ctti-clinicaltrials.org/).


## Launch on AWS

* Create an t2.medium EC2 instance based on Ubuntu 18
* `sudo apt-get update`
* `sudo apt-get install -y python3-pip`
* clone this repo
* `sudo pip3 install -r requirements.txt`
* Create a file `.env` with the following:

  ```
  hostname=aact-db.ctti-clinicaltrials.org
  port=5432
  database=aact
  username=your_username
  password=your_password

  ```
* sudo gunicorn app:app.server

