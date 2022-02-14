# Articles analyzer  

Description coming soon...

## Installation 

Coming soon ...
`dostoevsky download fasttext-social-network-model`

## Run

`make run-prod`

## Usage

Run in 1 command:
`make run-prod`  

This command will launch with docekr compose following services:
- db - PostgreSQL for storing data  
- cache - Redis for caching data  
- api - container with web app, providing analysis requests  
- data-loader - container, providing loading data from sources, configured in news_analyzer/text_sources_config.py

## API  

Optional query params are marked with [brackets].

- `/api/v1/ping` - check that app is up
```
$ curl http://localhost:8080/api/v1/ping
"OK"
```
- `/api/v1/sources/?[type=<str>]` - get data sources
    - type - source type
```
$ curl "http://localhost:8080/api/v1/sources?type=rss" | jq
[
  {
    "name": "meduza",
    "src_type": "rss",
    "src": "https://meduza.io/rss2/all",
    "src_id": 1
  }
]
```
- `/api/v1/source/{src_id:<int>}/articles` - get articles loaded from source
```
$ curl http://localhost:8080/api/v1/source/1/articles | jq
[
  {
    "src_id": 1,
    "title": "Путин за один день провел переговоры с Байденом, Макроном и Лукашенко",
    "text": "Президент России Владимир Путин и президент США ...",
    "date": "2022-02-12T17:42:00",
    "neutral_sentiment": 0.6151,
    "negative_sentiment": 0.30737,
    "positive_sentiment": 0.05502,
    "skip_sentiment": 0.12593,
    "speech_sentiment": 0.01034,
    "article_id": 4
  },
  ...
]
```
- `/api/v1/analyze/entities?[src_id=<int>&name=<str>&start_date_ts=<int>&end_date_ts=<int>]` - get named entities with an average tonality score grouped by entities  
    - src_id - source id  
    - name - part of named entity name. With specified name parameter as "Владимир", both "Владимир Путин" and "Владимир Зеленский" entities data will be returned   
    - start_date_ts - start date timestamp. If set, only entities from news uploaded no earlier than start date will be taken into account in the calculations  
    - end_date_ts - end date timestamp. If set, only entities from news uploaded no older than end date will be taken into account in the calculations 
```
$ curl "http://localhost:8080/api/v1/analyze/entities?&name=Владимир&src_id=1&start_date_ts=1111313131" | jq
{
  "entities": [
    {
      "name": "Владимир Путин",
      "entity_type": "PER",
      "mean_neutral_sentiment": 0.6151,
      "mean_negative_sentiment": 0.30737,
      "mean_positive_sentiment": 0.05502,
      "mean_skip_sentiment": 0.12593,
      "mean_speech_sentiment": 0.01034,
      "count": 3
    }
  ],
  "start_date": "2005-03-20T13:05:31",
  "end_date": null
}
```
- `/api/v1/analyze/entities/group_by_sources?[src_id=<int>&name=<str>&start_date_ts=<int>&end_date_ts=<int>]` - get named entities with an average tonality score grouped by entities and sources    
    - src_id - source id  
    - name - part of named entity name. With specified name parameter as "Владимир", both "Владимир Путин" and "Владимир Зеленский" entities data will be returned   
    - start_date_ts - start date timestamp. If set, only entities from news uploaded no earlier than start date will be taken into account in the calculations  
    - end_date_ts - end date timestamp. If set, only entities from news uploaded no older than end date will be taken into account in the calculations 
```
$ curl "http://localhost:8080/api/v1/analyze/entities/group_by_sources?name=Владимир&src_id=1&start_date_ts=1111313131" | jq
{
  "entities": [
    {
      "name": "Владимир Путин",
      "entity_type": "PER",
      "mean_neutral_sentiment": 0.6151,
      "mean_negative_sentiment": 0.30737,
      "mean_positive_sentiment": 0.05502,
      "mean_skip_sentiment": 0.12593,
      "mean_speech_sentiment": 0.01034,
      "count": 3,
      "src_name": "meduza"
    }
  ],
  "start_date": "2005-03-20T13:05:31",
  "end_date": null
}
```