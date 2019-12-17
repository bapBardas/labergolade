import pygsheets
import pprint
from BergoladeConfig import *

gc = pygsheets.authorize(service_file='/Users/bap/Documents/workspace/labergolade/stravapp-sa.json')
pp = pprint.PrettyPrinter()

# Open spreadsheet
sheet = gc.open('stravapp')

def append_an_activity(activity):
    print('=====> Appending an activity')
    activitiessheet = sheet.worksheet('title', 'activities')
    next_row = next_available_row(activitiessheet.title)
    if next_row == 1:
        initiate_headers()
        next_row = 2
    print('=====> writing activity')
    valeurs = []
    for (key, value) in activity:
        valeurs.append(value)

    activitiessheet.update_row(next_row, valeurs)


def activity_already_exists(id):
    first_column = sheet.worksheet('title', 'activities').get_col(1)
    if str(id) in first_column:
        return True
    else:
        return False


def initiate_headers():
    activities_sheet = sheet.worksheet('title', 'activities')
    activities_sheet.update_row(1, sheet_headers)


def next_available_row(worksheet):
    first_column = sheet.worksheet('title', worksheet).get_col(1)
    for idx, value in enumerate(first_column):
        if value == '':
            print('next available row  is : ', idx + 1)
            return (idx + 1)


def store_access_token(token, token_expires_at, refresh_token):
    tokensheet = sheet.worksheet('title', 'token')
    tokensheet.update_value('A2', token)
    tokensheet.update_value('B2', token_expires_at)
    tokensheet.update_value('C2', refresh_token)


def retrieve_last_token():
    wks = sheet.worksheet('title', 'token')
    token_data = {
        "access_token": wks.cell('A2').value,
        "token_expires_at": wks.cell('B2').value,
        "refresh_token": wks.cell('C2').value
    }
    return token_data


def get_last_token():
    return sheet.worksheet('title', 'token').cell('A2').value


def set_nb_columns(sheetName, size):
    wks = sheet.worksheet('title', sheetName)
    wks.cols = size
