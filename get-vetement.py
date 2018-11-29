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

    id_user = data["id_user"]

    vetements = db.prepare(f"""
    select v.id_vetement, v.nom_vetement, c.couleur, v.note_chaleur, e.endroit, v.jourx_max_port FROM vetement as v, 
    couleur as c, endroit_corps as e
    WHERE proprietaire = {id_user} and c.id_couleur = v.couleur and e.id = v.endroit_du_corps
    """)

    user = db.prepare(f"""
    select nom, prenom FROM "user"
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

    les_vetements = vetements()

    garde_robe = {}

    for vetement in les_vetements:
        print(vetement)
        garde_robe[vetement[1]] = {"id": vetement[0],
                                   "couleur": vetement[2],
                                   "note chaleur": vetement[3],
                                   "endroit": vetement[4],
                                   "jours_max_port": vetement[5]
                                   }

    retour = {"Nom": propri[0][0],
              "Prenom": propri[0][1],
              "garde_robe": garde_robe}

    return {'statusCode': 200,
            'body': json.dumps(retour),
            'headers': {'Content-Type': 'application/json'}}
