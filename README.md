# Last.fm Last Played Song API

## How it works

Send a request to the API URL, which is https://lastfm-last-played.powerpcfan.xyz/YOUR-LASTFM-USERNAME (replace YOUR-LASTFM-USERNAME with the last.fm username of the user you want to get the last played song for)

> [!TIP]
> If you are having issues with my domain since some ISPs block it due to it being registered recently, try this instead: https://corsproxy.io/?url=http://lastfm-last-played.powerpcfan.xyz/YOUR-LASTFM-USERNAME

Possible errors:
- INTERNAL_ERROR (500)
- TIMEOUT (504)
- USER_LIKELY_DOES_NOT_EXIST (404)
- NO_TRACKS_FOUND (200)
