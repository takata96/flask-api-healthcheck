from lib2to3.pgen2 import token
from lib2to3.pgen2.token import SLASH

from importlib_metadata import version
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_mysqldb import MySQL
from flask_redis import FlaskRedis
import redis, boto3, os
import pymsteams

app = Flask(__name__)
redis_client = FlaskRedis(app)
mysql = MySQL(app)

app.config['MYSQL_USER'] =  os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_IP')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
MS_TEAMS_WH = os.getenv('MS_TOKEN')



#app.config['MYSQL_USER'] =  'leonardo'
#app.config['MYSQL_PASSWORD'] = '123'
#app.config['MYSQL_HOST'] = '192.168.100.19'
#app.config['MYSQL_DB'] = 'desafio'


@app.route("/api")
def args():

    nome = request.args['nome']
    sobrenome = request.args['sobrenome']
    team = request.args['team']

    return jsonify(nome, sobrenome, team)

def versionAPI():
    ver = 'API: 1.0'
    return (ver)

def status():
    access = 'Status 200'
    return (access)

def noSQL():
    r = redis.Redis(host='192.168.100.36', port=6379, db=0)
    c = r.ping()

    try:
        if c == True:
            return ("Conectado noSQL")
    except:
        return ('Erro noSQL!')

def mSQL():
    cur = mysql.connection.cursor()
    try:
        cur.execute('''SELECT * FROM exemplo''')
        return ('Conectado mySQL')
    except:
        return ('Erro mySQL')

def awsSQS():
    try:
        conn = boto3.client(
               'sqs',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=('us-east-1')
                )
        queueUrl = conn.get_queue_url(QueueName='takata')
        queuemetadata = queueUrl['ResponseMetadata']
        queuestatuscode = queuemetadata['HTTPStatusCode']
        queueStatus = 'Fila: {}'.format(queuestatuscode)
        return('Fila: OK')
    except:
        return('Fila: Erro')

@app.route('/healthcheck')
def healthcheck():
    
    call = {
        'api': versionAPI(),
        'retorno': status()
        # nsql = noSQL()
        # sql = mSQL()
        # sqs = awsSQS()
    }
    

    myTeamsMessage = pymsteams.connectorcard(MS_TEAMS_WH)
    #myTeamsMessage.text(call)
    myTeamsMessage.text("API - OK")
    myTeamsMessage.send()
    
    return (call)


if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT',5000))
    app.debug = True
    app.run(host=host, port=port)
