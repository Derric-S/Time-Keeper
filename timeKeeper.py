
from __future__ import print_function
import httplib2
import os
import argparse
import time

from datetime import datetime
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Time Keeper'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

class stopwatch():
    startTime = None
    stopTime = None
    timeElapsed = None
    gameName = None

    def start(self):
        self.startTime = datetime.now()
        self.gameName = input("What game are you playing? ")

    def stop(self):
        self.stopTime = datetime.now()
        self.timeElapsed = self.stopTime - self.startTime

    def saveInfo(self):
        # Credentials and URL's
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        # Parsing data and entering into spreadsheet

        self.startTime = self.startTime.strftime("%-I:%M %p")
        currentTime = datetime.now().strftime("%-I:%M %p")
        currentDate = datetime.now().strftime("%m/%d/%y")

        data = [self.gameName, currentDate, self.startTime, currentTime, str(self.timeElapsed)[:-7]] # Format = Game, MM/DD/YYYY, HH:MM AM, HH:MM:SS

        body = {
        "majorDimension": "ROWS",
        "values": [data]
        }

        spreadsheetId = "1D2bZioQTjCvhG-jJc31ab3SWSxb82h9z0SWNryxdN-s"
        rangeName = "A2"
        valueInput = "USER_ENTERED"

        service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=valueInput, body=body).execute()

def main():
    timer = stopwatch()
    timer.start()
    print("\nPress ^C to stop the timer\n")
    t = 0
    while True:
        try:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t += 1
        except KeyboardInterrupt:
            break
    timer.stop()
    timer.saveInfo()

# Run the program

main()
