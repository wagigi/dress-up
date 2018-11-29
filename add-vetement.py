import json
import datetime
import logging
import postgresql
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

    if 'nom' not in data:
        logging.error('No nom in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Nom non transmise'})}
    else:
        nom = data["nom"]

    if 'note_chaleur' not in data:
        logging.error('No note_chaleur in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'note_chaleur non transmise'})}
    else:
        note_chaleur = data["note_chaleur"]

    if 'jour_max' not in data:
        logging.error('No jour_max in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'jour_max non transmise'})}
    else:
        jour_max = data["jour_max"]

    if 'couleur' not in data:
        logging.error('No couleur in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'couleur non transmise'})}
    else:
        couleur = data["couleur"]

    if 'endroit' not in data:
        logging.error('No endroit in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'endroit non transmise'})}
    else:
        endroit = data["endroit"]

    if 'proprietaire' not in data:
        logging.error('No proprietaire in body')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'proprietaire non transmise'})}
    else:
        proprio = data["proprietaire"]

    requete = db.prepare(f"""
    INSERT INTO vetement (nom_vetement, note_chaleur, jourx_max_port, endroit_du_corps, couleur, proprietaire)
    VALUES ('{nom}',
            {note_chaleur},
            {jour_max},
            {endroit},
            {couleur},
            {proprio}
    )
    RETURNING id_vetement;
    """)

    retour = {
        'id_vetement': requete()[0][0],
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}
