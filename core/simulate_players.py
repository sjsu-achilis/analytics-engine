import time
import datetime
import os
import math
import random

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
userids = ['2134225533','1342252213','1673662323','9978656676','1414252511']

def simulate_player(cur_day):
    log.info("running simulator...")
    # set users
    for user in userids:
        users_ref = ref.child(user)
        users_ref.set({
            'heart_rate': 0,
            'no_of_steps': 0,
            'distance_covered':0
        })
    # start simulation
    while True:
        # set no of steps to 0 when day changes
        if cur_day != str(datetime.datetime.now().day):
            cur_day = str(datetime.datetime.now().day)
            for user in userids:
                users_ref = ref.child(user)
                users_ref.update({
                    'no_of_steps': 0
                })
        
        for user in userids:
            users_ref = ref.child(user)
            hr = math.ceil(100.0 * random.uniform(0.75,1.25))
            do_steps = bool(random.randint(1,101) % 2)
            if do_steps:
                steps = int(users_ref.get()['no_of_steps']) + 1
                users_ref.update({
                    'heart_rate': hr,
                    'no_of_steps': steps,
                    'distance_covered': math.ceil(float(steps*0.762))
                })
            else:
                users_ref.update({
                    'heart_rate': hr
                })

        time.sleep(0.5)


if __name__ == "__main__":
    simulate_player(str(datetime.datetime.now().day))