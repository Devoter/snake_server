import bottle.ext.sqlite
import bottle
import json
import re
import settings

from datetime import datetime
from bottle import request, response
from encrypt import encrypt

app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(dbfile=settings.DATABASE)
app.install(plugin)


def set_headers():
    response.set_header('Content-Type', 'application/json')
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
    response.set_header('Access-Control-Allow-Headers', 'Origin, Content-Type, X-Auth-Token')


def get_score(db, new_id=''):
    score = []
    for row in db.execute('SELECT id, score, name FROM scores ORDER BY score DESC, created ASC'):
        score.append({'score': row[1], 'name': row[2], 'you': row[0] == new_id})

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
            type(data['score']) is not int) or (re.match(r'^[0-9A-Z_\-.\'"]{1,10}$', data['name']) is None) or (
            data['score'] < 0):
        response.status = 400
        return

    name = data['name']
    score = data['score']
    sum = data['hash']
    checksum = encrypt(name, score)

    if checksum.hexdigest() != sum:
        response.status = 400
        return

    timestamp = int(datetime.now().timestamp())
    ignore = False
    count = db.execute('SELECT COUNT(*) as cnt FROM scores ORDER BY score DESC, created ASC').fetchone()[0]

    if count >= 50:
        less = db.execute('SELECT COUNT(*) as cnt FROM scores WHERE score < ?', (score,)).fetchone()[0]
        if less > 0:
            db.execute(
                'DELETE FROM scores WHERE rowid = (SELECT rowid FROM scores ORDER BY score ASC, created DESC LIMIT 1)')
        else:
            ignore = True

    if ignore is False:
        db.execute('INSERT OR IGNORE INTO scores VALUES (?, ?, ?, ?)', (sum, name, score, timestamp))

    updated_score = get_score(db, sum)
    response.status = 201
    return json.dumps(updated_score)


app.run(host=settings.HOST, port=settings.PORT)
