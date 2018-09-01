# raspberry-instants

## Installing

### Archlinux packages

- pulseaudio
- pulseaudio-alsa
- alsa-utils
- python (3.7)
- python-pip
- python-cairo
- python-gobject
- gst-plugins-base
- gst-plugins-good
- gst-plugins-bad

### Python packages

- firebase-admin
- google-cloud-firestore

## Running

Run `python main.py`


## Usage

- Digit a song code: `Song code: <Your code>`
- To exit: type `-` + Enter


## Firebase

This project uses Firebase Cloud Firestore and Storage services.

### Cloud Firestore collection format

```json
{
    "songs": [
        {
            "0" : "song_name.mp3"
        },
        {
            "1" : "other_song_name.ogg"
        },
        ,
        {
            "2" : "more_songs_name.aac"
        }
        // ...
    ]
}
```