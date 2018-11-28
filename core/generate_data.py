import time
import datetime
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from achlib.config import file_config
from achlib.util import logger

config = file_config()
log = logger.getLogger(__name__)

# Fetch the service account key JSON file contents

cred = credentials.Certificate(os.environ.get('PYTHONPATH')+'/core/key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cmpe295-achilis.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('users')
users_ref = ref.child('2134225533')

def simulate_player(cur_day):
    i = 0
    log.info("running simulator...")
    while True:
        if cur_day != str(datetime.datetime.now().day):
            cur_day, i = str(datetime.datetime.now().day), 0
        hr = (i%70) + 85
        users_ref.set({
            'heart_rate': hr,
            'no_of_steps': i,
            'distance_covered': float(i*0.762)
        })
        i += 1
        time.sleep(1)


if __name__ == "__main__":
    simulate_player(str(datetime.datetime.now().day))