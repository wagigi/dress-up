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

    meteo = json.loads(reponse.content.decode('utf-8'))

    if meteo["errors"]:
        return {'statusCode': 418,
                'body': json.dumps(meteo),
                'headers': {'Content-Type': 'application/json'}}

    temp_day_min = meteo["fcst_day_0"]["tmin"]
    temp_day_max = meteo["fcst_day_0"]["tmax"]
    condition = meteo["fcst_day_0"]["condition_key"]

    retour = {
        'output': 'Tu habites à {ville}'.format(ville=data['ville']),
        'temp_min': temp_day_min,
        'temp_max': temp_day_max,
        'meteo': condition,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}
