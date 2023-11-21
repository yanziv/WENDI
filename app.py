from flask import (
    Flask,
    render_template,
    make_response,
    url_for,
    request,
    redirect,
    flash,
    session,
    send_from_directory,
    jsonify,
)
from werkzeug.utils import secure_filename

app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi

# import cs304dbi_sqlite3 as dbi

import random
import queries as queries

app.secret_key = "your secret here"
# replace that with a random key
app.secret_key = "".join(
    [
        random.choice(
            ("ABCDEFGHIJKLMNOPQRSTUVXYZ" + "abcdefghijklmnopqrstuvxyz" + "0123456789")
        )
        for i in range(20)
    ]
)

# This gets us better error messages for certain common request errors
app.config["TRAP_BAD_REQUEST_ERRORS"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("login.html", title="Main Page")



@app.route('/browse_all/', methods=["GET", "POST"])
def landing():
    if request.method == 'GET':
        return render_template('landing.html')


@app.route('/review/', methods=["GET", "POST"])
def review():
    if request.method == 'GET':
        return render_template('review.html')
 


@app.route("/dorm/<hid>")
def dorm(hid):
    conn = dbi.connect()
    roomsList = queries.show_rooms(conn, hid)
    print("hid: " + str(hid))
    print("roomList: " + str(roomsList))
    return render_template("dorm.html", dorm=roomsList, dormname=hid)


@app.route("/dorm/<hid>/room/<number>")
def room(hid, number):
    conn = dbi.connect()
    reviewList = queries.show_reviews(conn, number)
    print("reviewList: " + str(reviewList))
    return render_template("room.html", reviews=reviewList, dormname=hid, number=number)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", title="Login Page")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if queries.authenticate_user(username, password):
            return redirect(url_for("landing"))
        else:
            return redirect(url_for("index"))


@app.route("/formecho/", methods=["GET", "POST"])
def formecho():
    if request.method == "GET":
        return render_template(
            "form_data.html", method=request.method, form_data=request.args
        )
    elif request.method == "POST":
        return render_template(
            "form_data.html", method=request.method, form_data=request.form
        )
    else:
        # maybe PUT?
        return render_template("form_data.html", method=request.method, form_data={})


@app.route("/testform/")
def testform():
    # these forms go to the formecho route
    return render_template("testform.html")


if __name__ == "__main__":
    import sys, os

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert port > 1024
    else:
        port = os.getuid()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = "wendi_db"
    print("will connect to {}".format(db_to_use))
    dbi.conf(db_to_use)
    app.debug = True
    app.run("0.0.0.0", port)
