from services.credentials import auth_token,user_id
from services.spotifyClient import SpotifyClient

def main():
    spotifyClient=SpotifyClient(auth_token=auth_token,userId=user_id)

    num_tracks_to_visualize=int(input("How many tracks would you like to visualize? "))
    last_played_tracks=spotifyClient.getLastPlayedTracks(num_tracks_to_visualize)

    print(f"Here are the last {num_tracks_to_visualize} tracks you've listened to-")
    for idx,track in enumerate(last_played_tracks):
        print(f"{idx+1}) {track}")

    indexes=input("Enter indexes of tracks you want to use for recommendation seperated by a space : ")
    indexes=indexes.split()
    seed_tracks=[last_played_tracks[int(index)-1] for index in indexes]

    recommended_tracks=spotifyClient.getTrackRecommendations(seed_tracks)
    print(f"Here are some recommended tracks which will be added to your playlist:")
    for index,track in enumerate(recommended_tracks):
        print(f"{index+1}) {track}")

    playlist_name=input("Enter a name for your playlist: ")
    playlist=spotifyClient.createPlaylist(playlist_name)
    print(f"Playlist {playlist_name} was created successfully")

    spotifyClient.populatePlaylist(playlist,recommended_tracks)
    print(f"Recommended tracks successfully added to playlist {playlist_name}")

if __name__=="__main__":
    main()