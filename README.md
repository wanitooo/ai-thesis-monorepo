## TODO:

- ~~Separate a single mix audio~~
- ~~Integrate this separation into an HTTP route~~
- ~~Create route for DPCL DPRNN separation~~
- For DPRNN and RNN
  - Create a route for WER score
  - Create a route for SI SNR score

## Notes:

- ~~You need to create a file field model that will convert a user uploaded audio file into an audio file path~~
- ~~https://joel-hanson.medium.com/drf-how-to-make-a-simple-file-upload-api-using-viewsets-1b1e65ed65ca~~
- ~~https://github.com/Joel-hanson/simple-file-upload~~
- ~~Feed mixed audio into pretrained model, return filepath to seperated audios~~

## Installation

Install the required dependencies first

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run django migrations

```
python manage.py makemigrations
python manage.py migrate
```

## Running the server

```
python manage.py runserver
```

## API DOC

## POST /upload-file

#### A file blob of the audio needs to be sent in the "file" field of the request (via FormData)

INPUT

```
{
"file": <Multipart form-data of file>,
}
```

OUTPUT:

```
{
    "file": "/media/mixed/somefile.wav",
    "uploaded_on": "2023-10-30T09:02:49.959560Z"
}
```

## POST /drnn-separate and /dprnn-separate:

#### NOTE: The file should have already been uploaded via /upload-file

INPUT

```
{
"file": "media/mixed/somefile.wav",
}
```

OUTPUT:

```
{
"message": "Succesfully separated audio",
"spk_1": "https://s3.endpoint.com/media/separated/drnn/spk1/somefile-separated.wav",
"spk_2": "https://s3.endpoint.com/media/separated/drnn/spk2/somefile-separated.wav",
}
```
