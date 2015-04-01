#!/bin/bash
set -e
. bin/activate
if [ ! -f test.db ]; then
    python deploy_db.py
fi
su -c "python reconnect_myro.py"
python app.py
