# URL Shortener

## Description
Generates short URLs, redirects to the original URL and counts visitors for each url. 

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
```


## Usage

### Run Server
```bash
gunicorn url_shortener.wsgi
```
### Create Short URL
#### Request
```bash
curl -X POST "http://127.0.0.1:8000/shortener/" -H "accept: application/json" -H "Content-Type: application/json" -H "X-CSRFToken: YOUR-CSRF-TOKEN" -d "{ \"url\": \"https://example.com\"}"
```
#### Response
```json
{
    "url": "https://example.com",
    "slug": "BXaL",
    "visitor_count": "2020-01-01T00:00:00Z"
}
```
201 Created
### List Short URLs
#### Request
```bash
curl -X GET "http://127.0.0.1:8000/shortener/" -H "accept: application/json" -H "X-CSRFToken: YOUR-CSRF-TOKEN"
```
#### Response
```json
[
  {
    "url": "https://example.com",
    "slug": "0GrR",
    "visitor_count": 1
  }
]
```
200 OK


### Redirect to Original URL
#### Request
```bash
curl -X GET "http://127.0.0.1:8000/r/0GrR/" -H "accept: application/json" -H "X-CSRFToken: YOUR-CSRF-TOKEN"
```
#### Response
302 Found