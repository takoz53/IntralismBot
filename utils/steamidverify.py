from steam import SteamID
import re
def getSteamURL(input):
    """ Checks whether inputted value is a proper Steam URL or not"""
    steamURL = re.search(r"^((?:https?:\/\/)?steamcommunity\.com\/(?:profiles|id)\/([a-zA-Z0-9]+)|([0-9]{17}))$", input)
    if steamURL:
        if steamURL.group(2):
            return dict({'is64': False, 'Value': steamURL.group(0)})
        if steamURL.group(3):
            return dict({'is64': True, 'Value': steamURL.group(3)})
    return None
        

def getSteam64(input):
    """ Function which converts and returns URL -> Steam64"""
    steamID = getSteamURL(input)
    if steamID is None:
        return None

    if steamID['is64']:
        return steamID
    if not steamID['is64']:
        newSteamID = SteamID.from_url(steamID.get('Value'), http_timeout=30)
        return newSteamID.as_64
    return None

