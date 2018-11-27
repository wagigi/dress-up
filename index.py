import json
import datetime

who = "world"

def handler(event, context):
    data = {
        'output': f'Hello {who}',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
