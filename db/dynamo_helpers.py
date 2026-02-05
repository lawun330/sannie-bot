'''
This script is for reading and writing scraped data to DynamoDB.
It is used by api.py when the AWS environment variables and table names are set; otherwise no-op.
The tables are:
- sannie-pages (pk topic_url)
- sannie-contents (pk page_url)
- sannie-articles (pk content_url)
The data is stored as a JSON string in the attribute "data".
'''

# import libraries
import os
import json

# optional DynamoDB: only init if all required env vars are set
def _dynamo_available():
    '''Return True if all required environment variables are set, False otherwise.'''
    return all([
        os.getenv('AWS_ACCESS_KEY'),
        os.getenv('AWS_SECRET_ACCESS_KEY'),
        os.getenv('AWS_REGION'),
        os.getenv('DYNAMODB_TABLE_PAGES'),
        os.getenv('DYNAMODB_TABLE_CONTENTS'),
        os.getenv('DYNAMODB_TABLE_ARTICLES'),
    ])

_dynamodb = None
_tables = {}


def _get_client():
    '''Return DynamoDB client if all required environment variables are set, False otherwise.'''
    global _dynamodb, _tables
    if not _dynamo_available():
        return False
    if _dynamodb is None:
        import boto3
        _dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        )
        _tables = {
            'pages': _dynamodb.Table(os.getenv('DYNAMODB_TABLE_PAGES')),
            'contents': _dynamodb.Table(os.getenv('DYNAMODB_TABLE_CONTENTS')),
            'articles': _dynamodb.Table(os.getenv('DYNAMODB_TABLE_ARTICLES')),
        }
    return True


def get_pages(topic_url):
    '''Return list of page URLs for topic_url, or None if not found.'''
    if not _get_client():
        return None
    try:
        r = _tables['pages'].get_item(Key={'topic_url': topic_url})
        item = r.get('Item')
        if not item or 'data' not in item:
            return None
        return json.loads(item['data'])
    except Exception as e:
        print("DynamoDB get_pages error:", e)
        return None


def put_pages(topic_url, data):
    '''Store pages data (list) for topic_url.'''
    if not _get_client():
        return
    try:
        _tables['pages'].put_item(Item={
            'topic_url': topic_url,
            'data': json.dumps(data, ensure_ascii=False),
        })
    except Exception as e:
        print("DynamoDB put_pages error:", e)


def get_contents(page_url):
    '''Return list of content items for page_url, or None if not found.'''
    if not _get_client():
        return None
    try:
        r = _tables['contents'].get_item(Key={'page_url': page_url})
        item = r.get('Item')
        if not item or 'data' not in item:
            return None
        return json.loads(item['data'])
    except Exception as e:
        print("DynamoDB get_contents error:", e)
        return None


def put_contents(page_url, data):
    '''Store contents data (list) for page_url.'''
    if not _get_client():
        return
    try:
        _tables['contents'].put_item(Item={
            'page_url': page_url,
            'data': json.dumps(data, ensure_ascii=False),
        })
    except Exception as e:
        print("DynamoDB put_contents error:", e)


def get_article(content_url):
    '''Return article data for content_url, or None if not found.'''
    if not _get_client():
        return None
    try:
        r = _tables['articles'].get_item(Key={'content_url': content_url})
        item = r.get('Item')
        if not item or 'data' not in item:
            return None
        return json.loads(item['data'])
    except Exception as e:
        print("DynamoDB get_article error:", e)
        return None


def put_article(content_url, data):
    '''Store article data for content_url.'''
    if not _get_client():
        return
    try:
        _tables['articles'].put_item(Item={
            'content_url': content_url,
            'data': json.dumps(data, ensure_ascii=False),
        })
    except Exception as e:
        print("DynamoDB put_article error:", e)
