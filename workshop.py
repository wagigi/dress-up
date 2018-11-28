import json
import datetime


def handler(event, context):
    data = {
        'output': 'Allez vous faire enculer vous et votre sujet de merde',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
