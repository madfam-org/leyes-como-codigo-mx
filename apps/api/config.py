"""Centralized configuration for the API app."""

import os

from elasticsearch import Elasticsearch

ES_HOST = os.getenv("ES_HOST", "http://elasticsearch:9200")
INDEX_NAME = "articles"

# Singleton ES client for connection pooling across requests
es_client = Elasticsearch([ES_HOST])
