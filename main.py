from stravalib.client import Client
from stravalib.model import Activity
from collections import deque
import SheetRW as dbaccess
import time
import weather
import datetime
from BergoladeConfig import *
# Print nicely
import pprint

client = Client()
# authorize_url = client.authorization_url(client_id=41559, redirect_uri='http://localhost/authorized')
# Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
# .....
pp = pprint.PrettyPrinter()
start_time = time.time()


def say_hello():
    print(""" ██╗      █████╗         ██████╗ ███████╗██████╗  ██████╗  ██████╗ ██╗      █████╗ ██████╗ ███████╗
 ██║     ██╔══██╗        ██╔══██╗██╔════╝██╔══██╗██╔════╝ ██╔═══██╗██║     ██╔══██╗██╔══██╗██╔════╝
 ██║     ███████║        ██████╔╝█████╗  ██████╔╝██║  ███╗██║   ██║██║     ███████║██║  ██║█████╗ 
 ██║     ██╔══██║        ██╔══██╗██╔══╝  ██╔══██╗██║   ██║██║   ██║██║     ██╔══██║██║  ██║██╔══╝  
 ███████╗██║  ██║        ██████╔╝███████╗██║  ██║╚██████╔╝╚██████╔╝███████╗██║  ██║██████╔╝███████╗
 ╚══════╝╚═╝  ╚═╝        ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝""")
    print("""                                          
                                                    .'  `.
                                                   /      \\
                     o                            /        |
                      8ooooooooo               __________  |
                        ``8'                  /.-------. \ |
                         |`                   ||      ` ` |<
                          `|___________________\\      |||| )
                          / _____________________\ ._._.'.'(
                         / |                     \\ ``--'
                        //|`                      \\
                       //  `|                      \\
                      //   |`                      .\\
         .d888888b.  //     `|                   .'.'\\  .d888888b.
      o8Y'   .    `Y//      |`                  / /   \\Y'    .  .`Y8o
    oY'   .  .   . //Y8o     `|               .'.'  dY'\\  .  .     .`Yo
   dY  .     .    //   Yb    |`              / /   dY.  \\    .    .  .Yb
  dY .  .  . .  .//   . Yb    `|           .'.'   dY   . \\ . . . .     Yb
 oY.   . .   .  //  .    Yb   |`          / /    oY .    .\\  .  . .   . Yo
o8    .   .  . // .    .  8b   `| =.=   .'.'    o8     .   \\ . .   .     8o
8Y  .    . . .//__________Y8___|`_____ / /      8P  .     . \\.. .     .  Y8
8............@/__ ........ 8   .'.  ..`.'       8............\@)...........8
8    .   . (`-.__`--.__   d8  /. . |..  \       8     .  .  . . . .     .  8
8b    .    .(@   `--.__`--.__|....  .... |      8b.    .   .  .  .   .    d8
Y8 .    . .  `-._      `--.__|..   @     |      Y8   .  . . . . . . .  .  8Y
 Yb   .  .   .  .`-._   dP   |.... |.    |       Yb.     .    .    .     dP
  Yb.   .  . . . .   `-dP     \  . |... /         Yb .  .  .  .  .  .  .dP
   Yo. .     .    .  .oP `--.__`.__|__.'           Yo. .      .      ..oP
    `8o.  .  .  .  .o8'            |                `8o.  .   .   . .o8'
      `Y88booood888P'             =.=                 `Y88boooood888P'
          \"\"\"\"\"\"                                          \"\"\"\"\"\"\" 
""")


def print_athlete():
    athlete = client.get_athlete()
    print("For {firstname} {lastname}, I now have an access token {token}".format(firstname=athlete.firstname,
                                                                                  lastname=athlete.lastname,
                                                                                  token=client.access_token))


def get_initial_token():
    print('=====> No token before, this is the first one (ever)')
    # Extract the code from your webapp response
    token_response = client.exchange_code_for_token(client_id=strava_client_id, client_secret=strava_client_secret,
                                                    code=strava_user_code)
    # Let's store that short-lived access token somewhere 
    client.access_token = token_response['access_token']
    # You must also store the refresh token to be used later on to obtain another valid access token 
    # in case the current is already expired
    client.refresh_token = token_response['refresh_token']
    # An access_token is only valid for 6 hours, store expires_at somewhere and
    # check it before making an API call.
    client.token_expires_at = token_response['expires_at']
    # And now we store all that precious in a database
    dbaccess.store_access_token(client.access_token, client.token_expires_at, client.refresh_token)


def check_token():
    last_token_data = dbaccess.retrieve_last_token()
    # ... for the first time ...
    if last_token_data['access_token']:
        # ... time passes ...
        if time.time() > float(last_token_data["token_expires_at"]):
            print('=====> Token has expired, let\'s get a new one')
            refresh_response = client.refresh_access_token(strava_client_id, strava_client_secret,
                                                           last_token_data['refresh_token'])
            access_token = refresh_response['access_token']
            refresh_token = refresh_response['refresh_token']
            expires_at = refresh_response['expires_at']
            dbaccess.store_access_token(access_token, expires_at, refresh_token)
        else:
            print('=====> Previous token was still valid')
            client.access_token = last_token_data['access_token']
            client.token_expires_at = last_token_data['token_expires_at']
            client.refresh_token = last_token_data['refresh_token']

    else:
        get_initial_token()


def transform_activity(activity):
    print('=====> Processing activity id: {0}, {1}seconds', activity.id, (time.time() - start_time))
    detailed_activity = client.get_activity(activity.id)
    result = deque()
    dict_originalActivity = activity.to_dict()

    for key in dict_originalActivity:
        if key in activity_keys_to_drop:
            'Just drop it'  # we do nothing with those
        elif key == 'map':
            result.append(('simple_map', activity.map.summary_polyline))
            result.append((key, detailed_activity.map.polyline))
        elif key == 'gear':
            if detailed_activity.gear and detailed_activity.gear.name:
                result.append(('gear_name', detailed_activity.gear.name))
            else:
                result.append(('gear_name', ''))
        elif key == 'photos':
            result.append(('photos_count', detailed_activity.photos.count))
            if detailed_activity.photos.count > 0:
                result.append(('photo_urls', detailed_activity.photos.primary.urls['600']))
            else:
                result.append(('photo_urls', ''))  # in order to keep a correct alignment in the table between column name and value
        else:
            result.append((key, dict_originalActivity[key]))

    # add some extra fields :
    result.appendleft(('id', activity.id))

    # Append weather information if activity is close to now:
    difference = datetime.datetime.now() - (activity.start_date_local + activity.elapsed_time)
    if (difference.total_seconds()) < 3600:
        print('=====> This is a recent activity, we retrieve the current weather report')
        activity_weather = weather.get_weather(str(activity.end_latlng[0]), str(activity.end_latlng[1]))
        for key in activity_weather:
            result.append((key, activity_weather[key]))

    print(result)
    return result


def retrieve_and_store_last_activities():
    print('=====> retrieve last activities if any new one: %s seconds ' % (time.time() - start_time))
    activities = client.get_activities(None, None, 5)
    raw_ids = dbaccess.retrieve_raw_ids()
    for activity in activities:
        if str(activity.id) not in raw_ids:
            dbaccess.append_raw_activity(transform_activity(activity))


def retrieve_and_store_archives():
    print('=====> retrieve 2000 last archives')
    activities = client.get_activities(None, None, 2000)
    raw_ids = dbaccess.retrieve_raw_ids()
    for activity in activities:
        if str(activity.id) not in raw_ids:
            dbaccess.append_raw_activity(transform_activity(activity))


def convert_activity_to_gold(raw_activity_id):
    raw_activity = dbaccess.retrieve_raw_activity_row(raw_activity_id)
    result = raw_activity.copy()

    # Convertion :
    result[3] = round(float(result[3])/1000, 2)   # convert Distance to km
    result[32] = round(float(result[32]) * 3.6, 2)  # convert average speed to km/h
    result[33] = round(float(result[33]) * 3.6, 2)  # convert max speed to km/h

    dbaccess.append_gold_activity(result)


def convert_raw_to_gold():
    print('=====> Converting raw to gold : %s seconds ' % (time.time() - start_time))
    activities_to_convert = dbaccess.activities_to_convert_ids()
    for activity_id in activities_to_convert:
        convert_activity_to_gold(activity_id)


def stravapp(request):
    # say_hello()   # disable that if in GCP
    check_token()
    retrieve_and_store_last_activities()
    convert_raw_to_gold()
    return 'Done'


stravapp('toto')