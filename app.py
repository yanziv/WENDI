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

from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit


# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi

# import cs304dbi_sqlite3 as dbi

import bcrypt
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


@app.route("/browse-all/", methods=["GET", "POST"])
def landing():
    conn = dbi.connect()
    
    if request.method == "GET":
        halls = queries.get_hall_names_given_complex(conn,'All Halls')
        return render_template("landing.html", halls=halls, browse='All Halls')

    else:
        hall_type = request.form["hall-type"]
        halls = queries.get_hall_names_given_complex(conn, hall_type)

        if hall_type == "All Halls":
            return redirect(url_for('landing'))
        
        else: # specific complex halls
            return render_template("landing.html", halls=halls, browse=hall_type)
        
        # elif hall_type == "Tower Complex":
        #     return render_template("landing.html", halls=halls, browse=hall_type)
        
        # elif hall_type == "East Side Complex":
        #     return render_template("landing.html", halls=halls, browse=hall_type)
        
        # elif hall_type == "West Side Complex":
        #     return render_template("landing.html", halls=halls, browse=hall_type)
        
        # elif hall_type == "The Quint":
        #     return render_template("landing.html", halls=halls, browse=hall_type)
        
        # elif hall_type == "Stone-Davis and Small Halls":
        #     return render_template("landing.html", halls=halls, browse=hall_type)


@app.route("/login/", methods=["POST"])
def login():
    username = request.form.get("username")
    passwd = request.form.get("password")
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("SELECT uid,hashed FROM userpass WHERE username = %s", [username])
    row = curs.fetchone()
    if row is None:
        # Same response as wrong password,
        # so no information about what went wrong
        flash("login incorrect. Try again or join")
        return redirect(url_for("index"))
    stored = row["hashed"]
    print("database has stored: {} {}".format(stored, type(stored)))
    print("form supplied passwd: {} {}".format(passwd, type(passwd)))
    hashed2 = bcrypt.hashpw(passwd.encode("utf-8"), stored.encode("utf-8"))
    hashed2_str = hashed2.decode("utf-8")
    print("rehash is: {} {}".format(hashed2_str, type(hashed2_str)))
    if hashed2_str == stored:
        session["username"] = username
        session["uid"] = row["uid"]
        session["logged_in"] = True
        session["visits"] = 1
        return redirect(url_for("landing"))
    else:
        flash("login incorrect. Try again or join")
        return redirect(url_for("index"))


@app.route("/review/", methods=["GET", "POST"])
def review():
    conn = dbi.connect()
    all_dorms = queries.get_all_dorms(conn)
    if request.method == "GET":
        return render_template("form.html", dorms=all_dorms)

    else:  # POST
        # 1: retrieve user input and insert review into the review table in wendi_db
        userID = session.get("uid")
        dorm = request.form.get("res-hall") # dorm is the 3-letter dorm encoding
        room_number = request.form.get("room-num")
        rid = queries.get_rid_given_hall_and_number(conn, dorm, room_number)
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
        hasMedia = "0"  # set hasMedia to False
        submission_time = datetime.now()

        # insert review into wendi_db and get review_id
        review_id = queries.insert_review(
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

        # check uploaded files
        # try:
        #     # session_id = int(session['id'])
        #     files = request.files.getlist('roomMedia')
            
        #     for file in files:
        #         if file and allowed_file(file.filename): # check if extension is allowed
        #             # hasMedia = True  # Set hasMedia to True as a valid file is found
        #             filename = secure_filename(file.filename)
        #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #             # Insert each file's information into the media table
        #             media_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #             queries.insert_media(conn, media_url, userID, review_id, cid=None)  # Assuming review_id is available

        # except Exception as err:
        #     flash('Upload failed {why}'.format(why=err))s
        #     return render_template('form.html')

        flash("Thank you for submitting a review!")
        return redirect(url_for("room", hid=dorm, number=room_number))


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


@app.route("/dorm/<hid>", methods=["GET", "POST"])
def dorm(hid):
    conn = dbi.connect()
    print("hid: " + str(hid))

    filterContent = queries.get_room_types(
        conn, hid
    )  # dropdown menu's values for all the room types
    print("filterContent ==== " + str(filterContent))
    if request.method == "POST":
        print("request.method ===== POST")

        roomsList = queries.show_rooms(conn, hid)
        return render_template(
            "dorm.html", dorm=roomsList, dormname=hid, filterContent=filterContent
        )
    else:
        print("request.method ===== GET")

        answer = request.args.get("room-type")
        print("room-type: " + str(answer))

        if answer == "All" or answer == None:
            filteredRooms = queries.show_rooms(conn, hid)
            answer = "All"
        else:
            filteredRooms = queries.sort_rooms_by(conn, hid, answer)
        # print(filteredRooms)

        # print("roomList: " + str(roomsList))
        return render_template(
            "dorm.html",
            dorm=filteredRooms,
            dormname=hid,
            filterContent=filterContent,
            filterType=answer,
        )


@app.route("/dorm/<hid>/room/<number>", methods=["GET", "POST"])
def room(hid, number):
    conn = dbi.connect()
    reviewList = queries.show_reviews(conn, number)
    print("reviewList: " + str(reviewList))

    uid = queries.get_username(conn,session.get('uid'))

    print("SESSION UID========" + str(session.get("uid")))
    print("USERNAME======"+str(uid))

    rid = queries.get_roomid(conn,hid,number)['id']

    if request.method == "GET":
        allComments = queries.get_comments(conn, rid)
        
        if uid == reviewList[0]['uid']:
            commenterType = "Reviewer"
        else:
            commenterType = "Commenter"

        return render_template(
            "room.html",
            reviews=reviewList,
            dormname=hid,
            number=number,
            allComments=allComments,
            usertype=commenterType
        )
    elif request.method == "POST":
        comment = request.form.get("comments")
        uid = uid['username']
        queries.insert_comment(conn, uid, rid, comment)

        return redirect(url_for("room", hid=hid, number=number))


# @app.route("/login/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username")
#         passwd = request.form.get("password")
#         conn = dbi.connect()
#         curs = dbi.dict_cursor(conn)
#         curs.execute("SELECT uid, hashed FROM userpass WHERE username = %s", [username])
#         row = curs.fetchone()
#         if row is None:
#             flash("Login incorrect. Try again or join.")
#             return redirect(url_for("index"))
#         stored = row["hashed"]
#         hashed2 = bcrypt.hashpw(passwd.encode("utf-8"), stored.encode("utf-8"))
#         hashed2_str = hashed2.decode("utf-8")
#         if hashed2_str == stored:
#             session["username"] = username
#             session["uid"] = row["uid"]
#             session["logged_in"] = True
#             session["visits"] = 1
#             return redirect(url_for("landing", username=username))
#         else:
#             flash("Login incorrect. Try again or join.")
#             return redirect(url_for("index"))
#     else:
#         # Handle the GET request
#         return render_template("login.html")


@app.route("/join/", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        username = request.form.get("usernamejoin")
        email = request.form.get("email")
        classYear = request.form.get("classYear")
        passwd1 = request.form.get("password1")
        passwd2 = request.form.get("password2")

        if passwd1 != passwd2:
            flash("Passwords do not match")
            return redirect(url_for("join"))

        hashed = bcrypt.hashpw(passwd1.encode("utf-8"), bcrypt.gensalt())
        hashed_password_str = hashed.decode("utf-8")

        conn = dbi.connect()
        curs = dbi.cursor(conn)

        try:
            curs.execute(
                """INSERT INTO userpass(username, email, classYear, hashed)
                            VALUES(%s, %s, %s, %s)""",
                [username, email, classYear, hashed_password_str],
            )
            conn.commit()
        except Exception as err:
            flash("That username is taken: {}".format(repr(err)))
            return redirect(url_for("join"))

        curs.execute("SELECT last_insert_id()")
        row = curs.fetchone()
        uid = row[0]

        flash("Account created successfully! Please log in with your account.")
        return redirect(url_for("index"))
    else:
        return render_template("join.html")


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    if "username" in session:
        session.pop("username")
        session.pop("uid")
        session.pop("logged_in")
        flash("You are logged out")
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


# @app.route("/addcomment/", methods=["POST"])
# def addcomment():

#     return redirect(url_for('room'), hid=)

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
