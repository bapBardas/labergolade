from stravalib.client import Client
from stravalib.model import Activity
from collections import deque
import SheetRW as dbaccess
import time
from BergoladeConfig import *
# Print nicely
import pprint

client = Client()
# authorize_url = client.authorization_url(client_id=41559, redirect_uri='http://localhost/authorized')
# Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
# .....
pp = pprint.PrettyPrinter()

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
    print("For {firstname} {lastname}, I now have an access token {token}".format(firstname=athlete.firstname,lastname=athlete.lastname, token=client.access_token))


def get_initial_token():
    print('=====> No token before, this is the first one (ever)')
    # Extract the code from your webapp response
    token_response = client.exchange_code_for_token(client_id=strava_client_id, client_secret=strava_client_secret, code=strava_user_code)
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
    last_token_data=dbaccess.retrieve_last_token()
    # ... for the first time ...
    if last_token_data['access_token']:
        # ... time passes ...
        if time.time() > float(last_token_data["token_expires_at"]):
            print('=====> Token has expired, let\'s get a new one')
            refresh_response = client.refresh_access_token(strava_client_id, strava_client_secret, last_token_data['refresh_token'])
            access_token = refresh_response['access_token']
            refresh_token = refresh_response['refresh_token']
            expires_at = refresh_response['expires_at']
            dbaccess.store_access_token(access_token,expires_at,refresh_token)
        else:
            print('=====> Previous token was still valid')
            client.access_token=last_token_data['access_token']
            client.token_expires_at=last_token_data['token_expires_at']
            client.refresh_token=last_token_data['refresh_token']

    else:
        get_initial_token()

def transform_activity(activity):
    result = deque()
    dict_originalActivity = activity.to_dict()
    for key in dict_originalActivity:
        if key == 'athlete':
            'toto'#do nothing
        elif key == 'map':
            'toto'#do nothing
        else:
            result.append((key,dict_originalActivity[key]))

    result.appendleft(('id',activity.id))
    print(result)
    return result


def retrieve_and_store_activities():
    print('=====> retrieve last 10 activities')
    activities=client.get_activities(None, None, 10)
    for activity in activities:
        dbaccess.append_an_activity(transform_activity(activity))

        #
        # del current_activity['athlete']
        # del current_activity['map']

say_hello()
check_token()
retrieve_and_store_activities()