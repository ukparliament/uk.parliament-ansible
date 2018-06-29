#!/usr/bin/python3

import os
import argparse
#import daemon
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from apscheduler.schedulers.blocking import BlockingScheduler
import signal
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
# from pymongo import MongoClient
import urllib3
urllib3.disable_warnings()
import datetime
import json
import sched, time
#import daemon

working_directory = "/opt/google-analytics/"

def get_service(api_name, api_version, scope, key_file_location, service_account_email):

           credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scope)

           http = credentials.authorize(httplib2.Http())

           # Build the service object.
           service = build(api_name, api_version, http=http)

           return service




def get_results(service, profile_id):
               # Use the Analytics Service Object to query the Core Reporting API
               # for the number of sessions within the past seven days.
               return service.data().realtime().get(
                   #ids='ga:158434803',
                   #ids='ga:158454199',
                   ids='ga:' + profile_id,
                   dimensions='rt:trafficType',
                   metrics='rt:activeUsers').execute()






data = {}

def print_totals_for_all_results(results):
           totals = results.get('totalsForAllResults')
           for metric_name, metric_total in totals.items():
               print ('Metric Name  = %s' % metric_name)
               print ('Metric Total = %s' % metric_total)

           return metric_total;

def main():
         # Define the auth scopes to request.
         scope = ['https://www.googleapis.com/auth/analytics.readonly']
         # Use the developer console and replace the values with your
         # service account email and relative location of your key file.
         service_account_email = 'google-analytics@datadog-integration-208315.iam.gserviceaccount.com'
         key_file_location = "/opt/google-analytics/key.json"
         # Authenticate and construct service.
         service = get_service('analytics', 'v3', scope, key_file_location,
         service_account_email)
          # Insert rtUsers into mongo
#         mongoServer = 'localhost'
#         client = MongoClient(mongoServer, 27017)
#         db = client.parliament
#         collectionGABeta = db.gabeta
#         collectionGAWWW = db.gawww

         metric_total =int( print_totals_for_all_results(get_results(service, '158454199')))
         dataPoint = {}
         dataPoint['timestamp'] = datetime.datetime.utcnow()
         dataPoint['totalUsers'] = metric_total
         collectionGABeta.insert(dataPoint)
         data['rt'] = []
         data['rt'].append({
             'beta-active-users': metric_total
         })
         metric_total = int(print_totals_for_all_results(get_results(service, '159113584')))
         dataPoint = {}
         dataPoint['timestamp'] = datetime.datetime.utcnow()
         dataPoint['totalUsers'] = metric_total
         collectionGAWWW.insert(dataPoint)
         data['rt'].append({
             'www-active-users': metric_total
         })
         with open ('/opt/google-analytics/google-analytics.json', 'w') as outfile:
             json.dump(data, outfile)
if __name__ == '__main__':
#   main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', seconds=60)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
      scheduler.start()
    except (KeyboardInterrupt, SystemExit):
      pass
