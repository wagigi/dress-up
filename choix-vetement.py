import json
import datetime
import postgresql.driver
import requests
import logging

meteo_url = 'https://www.prevision-meteo.ch/services/json/'

db = postgresql.driver.connect(
    user='dress_up_user',
    password='azerty123',
    host='dress-up-d.cx6dq3mfz1fd.eu-west-1.rds.amazonaws.com',
    database='dress_up',
    port=5432
)


def handler(event, context):
    data = json.loads(event['body'])

    if 'id_user' not in data:
        logging.error('No id_user sent')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'id_user non transmis'})}
    else:
        id_user = data["id_user"]

    if 'ville' not in data:
        logging.error('No meteo')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Ville non transmise'})}
    if not data['ville']:
        logging.error(f'No data in ville - text was empty {json.dumps(data)}')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Ville non transmise'})}

    vetements = db.prepare(f"""
    select v.id_vetement, v.nom_vetement, c.couleur, v.note_chaleur, e.endroit, v.jourx_max_port, v.avantage 
    FROM vetement as v, couleur as c, endroit_corps as e
    WHERE proprietaire = {id_user} and c.id_couleur = v.couleur and e.id = v.endroit_du_corps
    """)

    user = db.prepare(f"""
    select nom, prenom FROM "user"
    WHERE id_user = {id_user}
    """)

    reponse = requests.get(meteo_url + data['ville'])

    meteo = json.loads(reponse.content.decode('utf-8'))

    if "errors" in meteo:
        logging.error("Error with meteo API {errors}".format(errors=json.dumps(meteo)))
        return {'statusCode': 418,
                'body': json.dumps(meteo),
                'headers': {'Content-Type': 'application/json'}}

    temp_day_min = meteo["fcst_day_0"]["tmin"]
    temp_day_max = meteo["fcst_day_0"]["tmax"]
    condition = meteo["fcst_day_0"]["condition_key"]

    propri = user()

    if not propri:
        retour = {
            'output': 'ko, user not found',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return {'statusCode': 400,
                'body': json.dumps(retour),
                'headers': {'Content-Type': 'application/json'}}

    les_vetements = vetements()

    garde_robe = {}

    for vetement in les_vetements:
        garde_robe[vetement[1]] = {"id": vetement[0],
                                   "couleur": vetement[2],
                                   "note chaleur": vetement[3],
                                   "endroit": vetement[4],
                                   "jours_max_port": vetement[5],
                                   "avantage": vetement[6]
                                   }

    retour = {"Nom": propri[0][0].capitalize(),
              "Prenom": propri[0][1].capitalize(),
              "garde_robe": garde_robe}

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}
