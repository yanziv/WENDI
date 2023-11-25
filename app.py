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
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit

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


THE_QUINT = ["Beebe", "Cazenove", "Monger", "Pomeroy", "Shafer"]
TOWER_COMPLEX = ["Claflin", "Lake House", "Severance", "Tower Court"]
EAST_SIDE_COMPLEX = ["Bates", "Freeman", "McAfee"]
SD_AND_SMALL_HALLS = ["Casa Cervantes", "French House", "Stone-Davis"]
ALL_HALLS = THE_QUINT + TOWER_COMPLEX + EAST_SIDE_COMPLEX + SD_AND_SMALL_HALLS


@app.route("/browse_all/", methods=["GET", "POST"])
def landing():
    if request.method == "GET":
        flash("Not Yet Implemented for the Draft Version!")
        return render_template("landing.html")
    # else:
    # id is post id and then uid should be retrieved from cached username
    #     if request.form['submit'] == 'All Halls':
    #         return render_template('landing.html')
    #     elif request.form['submit'] == 'Tower Complex':
    #         return render_template('landing.html')
    #     elif request.form['submit'] == 'East Side Halls':
    #         return render_template('landing.html')
    #     elif request.form['submit'] == 'West Side Halls':
    #         return render_template('landing.html')
    #     elif request.form['submit'] == 'The Quint':
    #         return render_template('landing.html')
    #     elif request.form['submit'] == 'Stone-Davis and Small Halls':
    #         return render_template('landing.html')


@app.route("/review/", methods=["GET", "POST"])
def review():
    conn = dbi.connect()
    all_dorms = queries.get_all_dorms(conn)
    if request.method == "GET":
        return render_template("form.html", dorms=all_dorms)

    else:  # retrieve user input and insert review into wendi_db
        userID = session.get("user_login_id")
        dorm = request.form.get("res-hall")
        flash(dorm)
        hall_id = queries.get_hid_given_hall_name(conn, dorm)["id"]
        flash(hall_id)
        rid = request.form.get("rid")
        overallRating = request.form.get("overall")
        startDate = request.form.get("start-date")
        length = request.form.get("length-of-stay")
        size = request.form.get("size")
        storage = request.form.get("storage")
        ventilation = request.form.get("ventilation")
        cleanliness = request.form.get("cleanliness")
        bathroom = request.form.get("bathroom")
        accessibility = request.form.get("accessibility")
        sunlight = request.form.get("sunlight")
        bugs = request.form.get("bugs")
        window = request.form.get("window")
        noise = request.form.get("noise")
        comments = request.form.get("comments")
        hasMedia = "1"  # HARD-CODE THIS TO BE 1, REMEMBER TO FIX
        submission_time = datetime.now()

        # insert review into wendi_db
        queries.insert_review(
            conn,
            userID,
            rid,
            overallRating,
            startDate,
            length,
            size,
            storage,
            ventilation,
            cleanliness,
            bathroom,
            accessibility,
            sunlight,
            bugs,
            window,
            noise,
            comments,
            hasMedia,
            submission_time,
        )
        flash("Thank you for submitting a review!")
        # not sure if should use redirect here
        return redirect(url_for("room", hid=hall_id, number=rid))


def allowed_file(filename):
    """
    This is a helper function that checks whether the file the user uploads
    has the extensions we support. Returns a boolean value.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }


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
            # User authenticated successfully, store their username in the session
            session["user_login_id"] = username
            return redirect(url_for("landing"))
        else:
            return redirect(url_for("index"))


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search_term", "").lower()
    # Query wendi_db database to get matching results
    conn = dbi.connect()
    # Search by either hid or number
    results_individual = queries.search_by_hid_or_number(conn, search_term)
    # Search by both hid and number
    results_combined = queries.search_by_hid_and_number(conn, search_term)
    return jsonify({"individual": results_individual, "combined": results_combined})


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
