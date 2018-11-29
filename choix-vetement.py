import json
import datetime
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

    id_vetement = data["id_vetement"]

    requete = db.prepare(f"""
    DELETE FROM vetement
    WHERE id_vetement = {id_vetement}
    """)

    deletion = requete()[1]

    if deletion == 1:
        data = {
            'output': 'ok',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return {'statusCode': 200,
                'body': json.dumps(data),
                'headers': {'Content-Type': 'application/json'}}
    else:
        data = {
            'output': 'ko, vetement not found',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return {'statusCode': 400,
                'body': json.dumps(data),
                'headers': {'Content-Type': 'application/json'}}

