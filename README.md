# SerenUp smart bracelet simulator

Simulate a SerenUp device that measures user's serendipity.

## Requirements
1. Set `AWS_KINESIS_STREAM_NAME` to match the stream you use for ingesting data into AWS Timestream DB
2. Copy `config.example.yml` and set users ids and their bracelets/devices

## Execute
1. Install dependencies
```sh
pipenv install
```
2. Run simulator
```sh
python main.py
```
