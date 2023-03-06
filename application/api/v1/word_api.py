from application.api.v1 import api_bp
from flask import jsonify, request, current_app
from flask import jsonify
import re
import json
from application.api.v1.models import IzohliLugat
from elasticsearch import Elasticsearch
import requests

es = Elasticsearch(hosts=[f"http://{current_app.config['ELASTICSEARCH_DOMAIN']}"])

es_index_name="izohli_lugat"

# let's check if elasticsearch index exists. if not create it
resp=requests.get(f"http://{current_app.config['ELASTICSEARCH_DOMAIN']}/{es_index_name}")
if resp.status_code!=200:
    index_mapping={"mappings":{"properties":{"word":{"type":"text"}}}}
    es.indices.create(index=es_index_name, body=index_mapping)
    current_app.logger.info(f"created elasticsearch index {es_index_name}")


@api_bp.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

@api_bp.route("/word/elasticsearch/index")
def elastic_search_index():
    all_words=IzohliLugat.query.all()
    docs=[{"word":word.latin} for word in all_words]
    current_app.logger.info(f"will elasticsearch index {len(docs)} word docs")
    for i,doc in enumerate(docs):
        es.index(index=es_index_name,id=i,body=doc)
        current_app.logger.debug(f"finished indexing {doc}")
    return {"status":"indexing complete"}

@api_bp.route("/word/elasticsearch/<query>/<fuzziness>")
def elastic_search(query:str,fuzziness:str):
    try:
        fuzziness_int=int(fuzziness)
    except Exception as e:
        current_app.logger.info(e)
        fuzziness_int=2
    search_results = es.search(index=es_index_name, body={'query': {'match': {'word': {'query': query,'fuzziness':fuzziness_int}}}})
    search_records=[hit['_source'] for hit in search_results['hits']['hits']]
    return jsonify(search_records)

@api_bp.route("/word/<char_type>/<word>")
def get_word(char_type:str,word:str):    
    if char_type=='cyr':
        current_app.logger.debug(f"will get word {word} in latin")
        found_words=IzohliLugat.query.filter_by(cyr=word).all()
    else:
        current_app.logger.debug(f"will get word {word} in latin")
        found_words=IzohliLugat.query.filter_by(latin=word).all()
    current_app.logger.debug(f"found {len(found_words)} words")
    found_words=[record.as_dict() for record in found_words]
    return jsonify(found_words)

@api_bp.route("/word/<id>")
def get_word_by_id(id:int):
    found_word=IzohliLugat.query.get(id)
    current_app.logger.debug(f"word def is : {found_word.as_dict()}")
    return jsonify(found_word.as_dict())

@api_bp.route("/search/<char_type>/<search_key>")
def search(char_type:str,search_key:str):
    if char_type=='cyr':
        found_words=IzohliLugat.query.filter(IzohliLugat.cyr.like(f"{search_key}%")).all()
    elif char_type=='latin':
        found_words=IzohliLugat.query.filter(IzohliLugat.latin.like(f"{search_key}%")).all()    
    current_app.logger.debug(f"found {len(found_words)} words for search key {search_key}")
    found_words=[record.as_dict() for record in found_words]
    return jsonify(found_words)


def search_from_elasticsearch(query:str,fuzziness:str):
    try:
        fuzziness_int=int(fuzziness)
    except Exception as e:
        current_app.logger.info(e)
        fuzziness_int=2
    search_results = es.search(index=es_index_name, body={'query': {'match': {'word': {'query': query,'fuzziness':fuzziness_int}}}})
    search_records=[hit['_source'] for hit in search_results['hits']['hits']]
    return search_records


@api_bp.route("/elastic/search/<search_key>/<fuzziness>")
def search_words_with_elastic_search(search_key:str,fuzziness:str):    
    found_words_list=search_from_elasticsearch(search_key,fuzziness)
    current_app.logger.debug(f"found_words_list type : {type(found_words_list)}")
    found_words=[item["word"] for item in found_words_list]
    found_records=[]
    for found_word in found_words:
        records=IzohliLugat.query.filter(IzohliLugat.latin.like(found_word)).all()
        found_records.extend(records)
    found_dict_records=[record.as_dict() for record in found_records]
    return jsonify(found_dict_records)
