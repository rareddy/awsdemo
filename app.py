__author__ = 'spousty'

import psycopg2
from bottle import route, run, get, static_file, DEBUG
import os,json



@route('/')
def index():
    return static_file("index.html", root='./')

@get('/ws/animals')
def getzips():
    results = []
    try:
        conn = psycopg2.connect(database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
                                host=os.environ.get('DB_HOST'), password=os.environ.get('DB_PASSWORD'))
    except:
        print("couldn't make connection" + os.environ.get('DB_HOST'))

    cur = conn.cursor()
    cur.execute("""select id, name, type from animal""")
    rows = cur.fetchall()

    for row in rows:
        result = {}
        result = {'id': row[0], 'name': row[1], 'type': row[2]}
        results.append(result)

    return json.dumps({'results': list(results)})


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
