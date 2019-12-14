#import library
import gspread
#Service client credential from oauth2client
from oauth2client.service_account import ServiceAccountCredentials
# Print nicely
import pprint
import json
#Create scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#create some credential using that scope and content of startup_funding.json
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/bap/Documents/workspace/labergolade/stravapp-sa.json',scope)
#create gspread authorize using that credential
client = gspread.authorize(creds)

#client.create('stravapp').sheet1
#Now will can access our google sheets we call client.open on StartupName
sheet = client.open('stravapp')
pp = pprint.PrettyPrinter()

def append_an_activity(activity):
    print('=====> Appending an activity')
    activitiessheet = sheet.worksheet('activities')
    print('=====> activities)
    for i, (key, value) in enumerate(activity.items()):
        activitiessheet.update_cell(1,i+1,key)
        activitiessheet.update_cell(2,i+1,value)



def store_access_token(token, token_expires_at, refresh_token):
    tokensheet = sheet.worksheet('token')
    tokensheet.update_acell('A2',token)
    tokensheet.update_acell('B2',token_expires_at)
    tokensheet.update_acell('C2',refresh_token)

def retrieve_last_token():
    token_data = {
        "access_token": sheet.worksheet('token').acell('A2').value,
        "token_expires_at": sheet.worksheet('token').acell('B2').value,
        "refresh_token": sheet.worksheet('token').acell('C2').value
    } 
    return token_data

def get_last_token():
    return sheet.worksheet('token').acell('A2').value
