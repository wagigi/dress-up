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

    id_user = data["id_user"]

    user = db.prepare(f"""
    select * FROM "user"
    WHERE id_user = {id_user}
    """)

    propri = user()

    if not propri:
        retour = {
            'output': 'ko, user not found',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return {'statusCode': 400,
                'body': json.dumps(retour),
                'headers': {'Content-Type': 'application/json'}}

    retour = {"Nom": propri[0][1].capitalize(),
              "Prenom": propri[0][2].capitalize(),
              "sexe": propri[0][3],
              "frillosite": propri[0][4],
              "ville": propri[0][5].capitalize()}

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}
