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

    ville = db.prepare(f"""
    select ville FROM "user"
    WHERE id_user = {id_user}
    """)

    la_ville = ville()
    if not la_ville:
        retour = {
            'output': 'ko, ville not found',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return {'statusCode': 400,
                'body': json.dumps(retour),
                'headers': {'Content-Type': 'application/json'}}

    reponse = requests.get(meteo_url + la_ville[0][0])

    meteo = json.loads(reponse.content.decode('utf-8'))

    if "errors" in meteo:
        logging.error("Error with meteo API {errors}".format(errors=json.dumps(meteo)))
        return {'statusCode': 418,
                'body': json.dumps(meteo),
                'headers': {'Content-Type': 'application/json'}}

    temp_day_min = meteo["fcst_day_0"]["tmin"]
    temp_day_max = meteo["fcst_day_0"]["tmax"]

    indice = decide_indice_chaleur_requis(temp_day_min, temp_day_max)

    vetements = db.prepare(f"""
            select v.id_vetement, v.nom_vetement, c.couleur, v.note_chaleur, e.endroit, v.jourx_max_port, v.avantage
            FROM vetement as v, couleur as c, endroit_corps as e
            WHERE proprietaire = {id_user} and c.id_couleur = v.couleur and e.id = v.endroit_du_corps
            """)

    les_vetements = vetements()

    if indice == 20:
        chaleur_rech = 5
    elif indice == 15:
        chaleur_rech = 4
    elif indice == 12:
        chaleur_rech = 3
    elif indice == 10:
        chaleur_rech = 2
    elif indice == 5:
        chaleur_rech = 1
    else:
        chaleur_rech = 3

    tenue = []
    habits_choisi = []
    for vetement in les_vetements:
        if vetement[4] not in habits_choisi:
            if vetement[3] == chaleur_rech or vetement[3] == chaleur_rech - 1:
                tenue.append(vetement)
                habits_choisi.append(vetement[4])

    while 'jambes' not in habits_choisi:
        indice_revu = 2
        for vetement in les_vetements:
            if vetement[4] not in habits_choisi:
                if vetement[3] == chaleur_rech - indice_revu:
                    tenue.append(vetement)
                    habits_choisi.append(vetement[4])
        indice_revu += 1

    while 'torse' not in habits_choisi:
        indice_revu = 2
        for vetement in les_vetements:
            if vetement[4] not in habits_choisi:
                if vetement[3] == chaleur_rech - indice_revu:
                    tenue.append(vetement)
                    habits_choisi.append(vetement[4])
        indice_revu += 1

    retour = {"Tenue_du_jour": tenue}

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}


def decide_indice_chaleur_requis(temp_min, temp_max):
    if temp_max - temp_min < 5:
        # use temp max only
        if temp_max < 0:
            return 20
        elif temp_max < 10:
            return 15
        elif temp_max < 15:
            return 12
        elif temp_max < 20:
            return 10
        elif temp_max < 30:
            return 5
    else:
        # use les deux temps
        # TODO: Améliorer la décision ~
        if temp_max < 0:
            return 20
        elif temp_max < 10:
            return 15
        elif temp_max < 15:
            return 12
        elif temp_max < 20:
            return 10
        elif temp_max < 30:
            return 5
