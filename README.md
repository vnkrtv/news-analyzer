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

## Adding new sources  

To add a new data source, you must add its config it TEXT_SOURCES_CONFIG in news_analyzer.text_sources_config.py file and implement necessary modules.  
Below is an example of configuring a source for regularly receiving news from the "Medusa" RSS channel:

```python
TEXT_SOURCES_CONFIG = {
    "meduza": {
        "source_loader": WebLoader,
        "source_parser": text_sources.meduza.MeduzaRSSParser,
        "text_loader": WebLoader,
        "text_parser": text_sources.meduza.MeduzaArticleParser,
        "ner_extractor": NatashaNerExtractor,
        "tonality_determinant": DostoevskyTonalityDeterminant,
        "info": {"src_type": TextSourceType.rss, "src": "https://meduza.io/rss2/all"},
    }
}
```
### source_loader

Get content with links to data which should be loaded. Must implement BaseLoader (news_analyzer.modules.loaders.base_loader.py) interface:

```python
class BaseLoader(ABC):
    @abstractmethod
    async def load(self, src: str) -> str:
        raise NotImplementedError
```
For example:
- Get XML with last news from RSS channel (make HTTP request - that is what WebLoader does)
- Get JSON with latest posts from VK group by API request  
- Get JSON with latest posts on Twitter for several tags by API request

### source_parser 

Get list od links to data from content, which returns source_loader module. Must implement BaseSourceParser (news_analyzer.modules.parsers.base_source_parser.py) interface:

```python
class BaseSourceParser(ABC):
    @abstractmethod
    async def parse(self, src_text: str) -> List[str]:
        raise NotImplementedError
``` 

For example:
- Get list of latest news URLs from RSS channel XML (that is what MeduzaRSSParser does)
- Get list of posts ids from JSON with latest posts from VK group  

### text_loader  

Get data by link (list of links we got from source_parser module). Must implement BaseLoader interface (same as source_loader module).  

For example:
- Get HTML page content by news URL (that is what WebLoader does)
- Get JSON with post comments by API request (list of post id we got from source_parser module)  

### text_parser  
Return ArticleInfo schema by data got by text_loader module. Must implement BaseArticleParser (news_analyzer.modules.parsers.base_articles_parser.py) interface:
```python
class ArticleInfo(BaseSchema):
    text: str
    title: str
    date: datetime
...
class BaseArticleParser(ABC):
    @abstractmethod
    async def parse(self, text: str) -> ArticleInfo:
        raise NotImplementedError
```  
For example:
- Extract title, text and publication date from HTML page content (that is what MeduzaArticleParser does)
- Get same fields from JSON with post comments  

### ner_extractor  
Extract named entities from text. Default implementation - NatashaNerExtractor - could be left.   
Custom implementation must implement BaseNerExtractor interface:
```python
class BaseNerExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> List[NamedEntity]:
        raise NotImplementedError
```

### tonality_determinant  
Determines the tone of the text. Default implementation - DostoevskyTonalityDeterminant - could be left.   
Custom implementation must implement BaseTonalityDeterminant interface:
```python
class SentimentType(str, Enum):
    NEUTRAL: str = "neutral"
    NEGATIVE: str = "negative"
    POSITIVE: str = "positive"
    SKIP: str = "skip"
    SPEECH: str = "speech"
...
class BaseTonalityDeterminant(ABC):
    @abstractmethod
    def get_tonality(self, text: str) -> Dict[SentimentType, float]:
        raise NotImplementedError
```