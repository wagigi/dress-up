import json
import datetime
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

    nom = data["nom"]
    note_chaleur = data["note_chaleur"]
    jour_max = data["jour_max"]
    couleur = data["couleur"]
    endroit = data["endroit"]

    requete = db.prepare(f"""
    INSERT INTO vetement (nom_vetement, note_chaleur, jourx_max_port, endroit_du_corps, couleur)
    VALUES ('{nom}',
            {note_chaleur},
            {jour_max},
            {endroit},
            {couleur}
    )
    RETURNING id_vetement;
    """)

    return {'statusCode': 200,
            'body': {"id_vetement": requete()[0][0]},
            'headers': {'Content-Type': 'application/json'}}
