# Power Hour

## Generate power hours from YouTube playlists

### Get started
To run, first ensure that you have [Docker and Docker Compose installed](https://docs.docker.com/compose/install/) on your machine.
From there, you will need
- A publicly viewable YouTube playlist link
- Optional - A YouTube API key with permissions for the YouTube Data API V3. This is necessary if you want to customize video editing using the "notes" section of playlist entries.
##### 1. Modify powerhour.env with your inputs
```
PLAYLIST_URL=https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID
YOUTUBE_API_KEY=YOUR_API_KEY
```
##### 2. Run the program using docker-compose
```
docker-compose run powerhour
```
##### 3. Open the output file from the `video_downloads` directory
```
# On OSX
open -a "Google Chrome" video_downloads/power_hour.mp4
```
