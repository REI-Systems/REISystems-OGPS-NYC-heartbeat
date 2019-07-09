# REISystems-OGPS-NYC-heartbeat

## Setup

Define 
 * `SLACK_API_TOKEN`
 * `SLACK_CHANNEL`
 * `SOLR_ENDPOINTS`
 * `SKIP_OK_MESSAGES`
 * `SLACK_OK_CHANNEL`
 
 Then
 * `pip install -r requirements.txt`
 * `python3 slacsolr_cloud_health_testk_test.py`

## Jenkins centOS job


```
#!/bin/bash

export TERM=xterm;

# set variable
VENV="${WORKSPACE}"/.venv

# delete folder and content if exists
if [ -d "$VENV" ]; then
	rm -fr "$VENV"
fi

#scl enable rh-python35 bash
source /opt/rh/rh-python35/enable

# create new virtualenv
virtualenv --no-site-packages "$VENV"

# activate virtualenv
source "$VENV"/bin/activate

pip install -r requirements.txt
python solr_cloud_health_test.py
```