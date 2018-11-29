import json
import datetime

who = "gagi"


def handler(event, context):
    data = {
        'output': f'Tu es un {who}',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}