import json
import datetime
import logging
import postgresql.driver

db = postgresql.driver.connect(
    user='dress_up_user',
    password='azerty123',
    host='dress-up-d.cx6dq3mfz1fd.eu-west-1.rds.amazonaws.com',
    database='dress_up',
    port=5432
)


def handler(event, context):
    data = json.loads(event['body'])

    if 'ville' not in data:
        logging.error('No ville in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Ville non transmise'})}

    if 'id_user' not in data:
        logging.error('No id_user in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'id_user non transmis'})}

    update_ville = db.prepare(f"""
    UPDATE "user" SET ville = {data['ville']} where id_user = {data['id_user']};
    """)

    updation = update_ville()[1]

    if updation == 1:
        data = {
            'output': 'ok',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return {'statusCode': 200,
                'body': json.dumps(data),
                'headers': {'Content-Type': 'application/json'}}
    else:
        data = {
            'output': 'ko, ville not changed',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return {'statusCode': 400,
                'body': json.dumps(data),
                'headers': {'Content-Type': 'application/json'}}


