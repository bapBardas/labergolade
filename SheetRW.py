from typing import List, Any

import pygsheets
from pygsheets import Cell
import pprint
from BergoladeConfig import *
import time

gc = pygsheets.authorize(service_file='stravapp-sa.json')
pp = pprint.PrettyPrinter()
start_time = time.time()

# Open spreadsheet
sheet = gc.open('stravapp')


def append_raw_activity(activity):
    print('=====> Appending a raw activity: %s seconds ' % (time.time() - start_time))
    activitiessheet = sheet.worksheet('title', 'raw_activities')
    next_row = next_available_row('raw_activities')
    if next_row == 1:
        initiate_raw_headers()
        next_row = 2
    print('=====> writing activity: %s seconds ' % (time.time() - start_time))
    valeurs = []
    for (key, value) in activity:
        valeurs.append(value)

    activitiessheet.update_row(next_row, valeurs)


def append_gold_activity(activity):
    print('=====> Appending a gold activity: %s seconds ' % (time.time() - start_time))
    activitiessheet = sheet.worksheet('title', 'gold_activities')
    next_row = next_available_row('gold_activities')
    if next_row == 1:
        initiate_gold_headers()
        next_row = 2
    print('=====> writing activity: %s seconds ' % (time.time() - start_time))
    activitiessheet.update_row(next_row, activity)


def retrieve_raw_ids():
    return sheet.worksheet('title', 'raw_activities').get_col(1)


def initiate_raw_headers():
    activities_sheet = sheet.worksheet('title', 'raw_activities')
    activities_sheet.update_row(1, raw_headers)


def initiate_gold_headers():
    activities_sheet = sheet.worksheet('title', 'gold_activities')
    activities_sheet.update_row(1, gold_headers)

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


def activities_to_convert_ids():
    raw_wks = sheet.worksheet('title', 'raw_activities')
    gold_wks = sheet.worksheet('title', 'gold_activities')
    raw_activities_id = raw_wks.get_col(1)
    gold_activities_id = gold_wks.get_col(1)
    result = list(set(raw_activities_id) - set(gold_activities_id))
    return result


def retrieve_raw_activity_row(raw_id):
    raw_wks = sheet.worksheet('title', 'raw_activities')
    list_cell = raw_wks.find(raw_id, False, True, True, False, (1,1), None)
    if len(list_cell) != 1:
        print('ERROR when retrieving raw activity with id : ' + raw_id)
    else:
        cell: Cell = list_cell[0]
        return raw_wks.get_row(cell.row)
