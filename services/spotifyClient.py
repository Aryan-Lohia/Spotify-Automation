import json
import requests

from models.track import Track
from models.playlist import Playlist


class SpotifyClient:
    def __init__(self, auth_token, userId):
        self.auth_token = auth_token
        self.userId = userId

    def getLastPlayedTracks(self, limit=10):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        print(response.json())
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for track in
                  response_json["items"]]
        return tracks

    def getTrackRecommendations(self, seedtracks, limit=50):
        seed_tracks_url = ""
        for seed_track in seedtracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for track in response_json["tracks"]]
        return tracks

    def createPlaylist(self, name):
        data = json.dump({
            "name": name,
            "description": "Recommended Tracks",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self.userId}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populatePlaylist(self,playlist,tracks):
        track_uris=[track.createSpotifyUrl() for track in tracks]
        data=json.dumps(track_uris)
        url=f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response=self._place_post_api_request(url,data)
        response_json=response.json()
        return response_json

    def _place_get_api_request(self, url):
        response = requests.get(url, headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        })
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(url, data=data, headers={"content-type": "application/json",
                                                          "Authorization": f"Bearer {self.auth_token}"
                                                          })
        return response

