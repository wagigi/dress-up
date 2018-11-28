import json
import datetime
import logging

who = "gagi"


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

    retour = {
        'output': 'Tu habites à {ville}'.format(ville=data['ville']),
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}
