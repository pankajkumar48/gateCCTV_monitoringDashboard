from flask import Flask, request, Response, jsonify
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
import time
import datetime
import psycopg2

PATH_TO_TEST_IMAGES_DIR = './images'

 

app = Flask(__name__)



def sendEmail(args):
    with app.app_context():
        mail=Mail(app)
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = '********@gmail.com'
        app.config['MAIL_PASSWORD'] = '********'
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)
        msg = Message('Vehicle trespassing', sender = '********@gmail.com', recipients = ['**********@gmail.com'])
        msg.body = "This Vehicle is hanging around the campus for more than 4 hours"
        read_blob(vehicleNo)
        with app.open_resource("images/imageRead.jpeg") as fp:
            msg.attach("images/imageRead.jpeg", "image/jpeg", fp.read())
        mail.send(msg)
        print("Email sent")

# Blobs from http://www.postgresqltutorial.com/postgresql-python/blob/
@app.route('/insertRecord', methods=['POST'])
def write_blob():

    vehicleNo = request.form.get("vehicleNo")
    vehicleType = request.form.get("vehicleType")
    decision = request.form.get("decision")

    print("Insertion happening")
    res = "Starting insertion"
    """ insert a BLOB into a table """
    conn = None
    try:
        # read data from a picture
        drawing = open('images/imageIn.jpeg', 'rb').read()
        # Database credentials
        hostname = 'localhost'
        username = 'pankaj kumar'
        password = '**********'
        database = 'postgres'
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        # create a new cursor object
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("INSERT INTO vehicleRecords(vehicleType, vehicleNo, vehicleImage, decision) VALUES(%s,%s,%s,%s)",(vehicleType, vehicleNo, psycopg2.Binary(drawing), decision))
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgresQL database
        cur.close()
        res = "Successfully Inserted"
    except (Exception, psycopg2.DatabaseError) as error:
        print("hi")
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return res


def read_blob(vehicleNo):
    """ read BLOB data from a table """
    conn = None
    # Database credentials
    hostname = 'localhost'
    username = 'pankaj kumar'
    password = '*********'
    database = 'postgres'
    try:
        # read database configuration
        #params = config()
        # connect to the PostgresQL database
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        # create a new cursor object
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(""" SELECT vehicleImage
                        FROM vehicleRecords
                        WHERE vehicleNo = %s """,
                    (vehicleNo,))
 
        blob = cur.fetchone()
        open("images/imageRead.jpeg", 'wb').write(blob[0])
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# https://stackoverflow.com/questions/46860816/how-do-i-take-picture-from-client-sidehtml-and-save-it-to-server-sidepython

@app.route('/')
def index():
    return Response(open('./static/index.html').read(), mimetype="text/html")

@app.route('/gates')
def gates():
    return Response(open('./static/getImage.html').read(), mimetype="text/html")

@app.route('/dashboard')
def dashboard():
    return Response(open('./static/dashboard.html').read(), mimetype="text/html")

# save the image as a picture
@app.route('/image', methods=['POST'])
def image():

    i = request.files['image']  # get the image
    #f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    f = 'imageIn.jpeg'
    i.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))

    return Response("%s saved" % f)



# Check whether vehicle is blacklisted
@app.route('/checkList', methods=['POST'])
def checkList():
    # Database credentials
    hostname = 'localhost'
    username = 'pankaj kumar'
    password = '**********'
    database = 'postgres'
    vehicleNo = request.form.get("vehicleNo")
    vehicleType = request.form.get("vehicleType")
    print(f"{vehicleType}, {vehicleNo}")
    conn = None
    res = "Whitelisted"
    try:
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        cur = conn.cursor()
        cur.execute(""" SELECT vehicleNo
                        FROM listedVehicles
                        WHERE vehicleNo = %s """,
                    (vehicleNo,))
 
        blob = cur.fetchone()
        if blob[0] is not None:
            res = "Blacklisted"
        cur.close()
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return res



if __name__ == '__main__':
    
    #Cron Job type Scheduler from https://stackoverflow.com/questions/55427781/is-there-a-way-to-run-python-flask-function-every-specific-interval-of-time-and
    # This scheduler will send email every 30 minutes
    scheduler = APScheduler()
    scheduler.add_job(func=sendEmail, args=['job run'], trigger='interval', id='job', seconds=1800)
    scheduler.start()


    app.run(debug=True, host='0.0.0.0')