import json
import datetime
import logging
import requests

meteo_url = 'https://www.prevision-meteo.ch/services/json/'


def handler(event, context):
    data = json.loads(event['body'])
    if 'ville' not in data:
        logging.error('No meteo')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Ville non transmise'})}
    if not data['ville']:
        logging.error('No data in ville - text was empty {}'.format(data))
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Ville non transmise'})}

    reponse = requests.get(meteo_url + data['ville'])

    retour = {
        'output': 'Tu habites à {ville}'.format(ville=data['ville']),
        'meteo_rand': json.dumps(reponse),
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}
