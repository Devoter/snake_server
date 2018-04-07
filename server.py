import bottle.ext.sqlite
import bottle
import json
import re
import settings

from datetime import datetime
from hashlib import sha256
from bottle import request, response

app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(dbfile=settings.DATABASE)
app.install(plugin)


def set_headers():
    response.set_header('Content-Type', 'application/json')
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
    response.set_header('Access-Control-Allow-Headers', 'Origin, Content-Type, X-Auth-Token')


def get_score(db):
    score = []
    for row in db.execute('SELECT score, name FROM scores ORDER BY score DESC, created ASC'):
        score.append({'score': row[0], 'name': row[1]})

    return score


@app.route('/', method='GET')
def score_table(db):
    score = get_score(db)
    set_headers()
    return json.dumps(score)


@app.route('/', method='OPTIONS')
def options_query():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
    response.set_header('Access-Control-Allow-Credentials', False)
    response.set_header('Access-Control-Max-Age', '86400')
    response.set_header('Access-Control-Allow-Headers',
                        'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept, Authorization, Cache-Control')


@app.post('/')
def append_score(db):
    data = request.json
    set_headers()
    if ('name' not in data) or ('score' not in data) or ('hash' not in data) or (type(data['name']) is not str) or (
            type(data['score']) is not int) or (re.match(r'^[0-9a-zA-Z_\-. ]{1,20}$', data['name']) is None) or (
            data['score'] < 0):
        response.status = 400
        return

    name = data['name']
    score = data['score']
    sum = data['hash']

    checksum = sha256()
    checksum.update((name + str(score)).encode('utf-8'))
    for i in range(0, 1000):
        checksum.update(checksum.hexdigest().encode('utf-8'))

    if checksum.hexdigest() != sum:
        response.status = 400
        return

    timestamp = int(datetime.now().timestamp())
    db.execute('INSERT OR IGNORE INTO scores VALUES (?, ?, ?, ?)', (sum, name, score, timestamp))
    updated_score = get_score(db)
    response.status = 201
    return json.dumps(updated_score)


app.run(host=settings.HOST, port=settings.PORT)
