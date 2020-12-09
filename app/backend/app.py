from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_cors import CORS
import json
from os import environ
from dotenv import load_dotenv
import random
import os
import base64
import boto3

load_dotenv()

import jwt
from datetime import datetime
import time
import dateutil.parser

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ["DB_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CORS(app)

# S3 Configuration
AWS_S3_CLIENT = boto3.client("s3")
AWS_S3_RESOURCE = boto3.resource("s3")
BUCKET_NAME = "vueducation"
# ==================
class Account(db.Model):

    account_id = db.Column(
        db.Integer(), primary_key=True, nullable=False, autoincrement=True
    )
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            "account_id": self.account_id,
            "username": self.username,
            "password": self.password,
        }


class User(db.Model):

    user_id = db.Column(
        db.Integer(), primary_key=True, nullable=False, autoincrement=True
    )
    username = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    about_me = db.Column(db.String(256))
    occupation = db.Column(db.String(128))
    image = db.Column(db.String(128))
    points = db.Column(db.Float())

    def __init__(
        self,
        username,
        first_name,
        last_name,
        email,
        about_me,
        occupation,
        image,
        points,
    ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.about_me = about_me
        self.occupation = occupation
        self.image = image
        self.points = points

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "about_me": self.about_me,
            "occupation": self.occupation,
            "image": self.image,
            "points": self.points,
        }


class Message(db.Model):

    message_id = db.Column(
        db.Integer(), primary_key=True, nullable=False, autoincrement=True
    )
    message = db.Column(db.String(256))
    sender = db.Column(db.String(128))
    receiver = db.Column(db.String(128))
    message_datetime = db.Column(db.String(128))

    def __init__(self, message, sender, receiver, message_datetime):
        self.message = message
        self.sender = sender
        self.receiver = receiver
        self.message_datetime = message_datetime

    def json(self):
        return {
            "message_id": self.message_id,
            "message": self.message,
            "sender": self.sender,
            "receiver": self.receiver,
            "message_datetime": self.message_datetime,
        }


class Promo(db.Model):

    voucher = db.Column(db.String(128), primary_key=True)
    code = db.Column(db.String(128))

    def json(self):
        return {"code": self.code}


accounts = {"kelvinngsl": "password", "officialtzuyu": "password"}

infos = {
    "kelvinngsl": {
        "username": "kelvinngsl",
        "first_name": "kelvin",
        "last_name": "ng",
        "email": "kelvinngsl@gmail.com",
        "about_me": "I'm extremely passionate in solving problem by leveraging my technical skill",
        "occupation": "student",
        "image": "kelvin.jpg",
        "points": 15999,
    },
    "officialtzuyu": {
        "username": "officialtzuyu",
        "first_name": "tzuyu",
        "last_name": "chou",
        "email": "officialtzuyu@gmail.com",
        "about_me": "I'm a kpop idol. Taiwanese Pride",
        "occupation": "kpop idol",
        "image": "tzuyu.jpg",
        "points": 17000,
    },
}

users = [
    {"id": 1, "username": "kelvinngsl", "image": "kelvin.jpg"},
    {"id": 2, "username": "franscorfiyanto", "image": "frans.jpg"},
    {"id": 3, "username": "officialtzuyu", "image": "tzuyu.jpg"},
    {"id": 4, "username": "tohjiamin", "image": "jiamin.jpg"},
]

messages = [
    {
        "id": 1,
        "message": "annyeong haseyo!!!! orimasdiasdnin??? from kelvin to ty",
        "message_datetime": "11:01 | 27/10/2020",
        "from": "kelvinngsl",
        "to": "officialtzuyu",
    },
    {
        "id": 2,
        "message": "annyeong haseyo!!!! orimasdiasdnin??? from kelvin to frans",
        "message_datetime": "11:01 AM    |    Today",
        "from": "kelvinngsl",
        "to": "franscorfiyanto",
    },
    {
        "id": 3,
        "message": "annyeong haseyo!!!! orimasdiasdnin??? from kel to jm",
        "message_datetime": "11:01 AM    |    Today",
        "from": "kelvinngsl",
        "to": "tohjiamin",
    },
    {
        "id": 4,
        "message": "annyeong haseyo!!!! orimasdiasdnin??? from ty to kel",
        "message_datetime": "11:01 AM    |    Today",
        "from": "officialtzuyu",
        "to": "kelvinngsl",
    },
]


@app.route("/accounts")
def get_accounts():
    accounts = Account.query.all()
    return jsonify([account.json() for account in accounts]), 200


@app.route("/messages")
def get_messages():
    messages = Message.query.all()
    return jsonify([message.json() for message in messages]), 200


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.json() for user in users]), 200


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    user = User.query.filter_by(username=username).first()

    return jsonify(user.json()), 200


@app.route("/users/<username>", methods=["PUT"])
def update_user(username):
    data = request.get_json()
    user = User.query.filter_by(username=username).first()

    user.username = data["username"]
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.email = data["email"]
    user.about_me = data["about_me"]
    user.occupation = data["occupation"]
    user.image = data["image"]
    user.points = data["points"]

    db.session.commit()

    return jsonify(user.json()), 200


@app.route("/users/<username>/points/add/<int:points>", methods=["PUT"])
def add_points(username, points):
    user = User.query.filter_by(username=username).first()
    user.points += points
    db.session.commit()

    return jsonify(user.json()), 201


@app.route("/users/<username>/points/deduct/<int:points>", methods=["PUT"])
def deduct_points(username, points):
    user = User.query.filter_by(username=username).first()
    user.points -= points
    db.session.commit()

    return jsonify(user.json()), 201


@app.route("/chat/users/<username>", methods=["GET"])
def get_chat_users2(username):
    users = []
    user_set = set()

    # Get Message related to this username
    messages = Message.query.filter(
        (Message.sender == username) | (Message.receiver == username)
    ).all()

    # Get all the unique user now
    for message in messages:
        if message.sender == username:
            user_set.add(message.receiver)

        if message.receiver == username:
            user_set.add(message.sender)

    for user in user_set:
        user_object = User.query.filter_by(username=user).first()
        users.append(user_object)

    return jsonify([user.json() for user in users]), 200


@app.route("/conversation/<username1>/<username2>", methods=["GET"])
def get_conversation(username1, username2):

    # Get Message related to this username
    # select * from messages where (username1 = sender and username2 = receiver) = receiver or (username2 = sender and username1 = receiver)
    messages = (
        Message.query.filter(
            or_(
                (Message.sender == username1) & (Message.receiver == username2),
                (Message.sender == username2) & (Message.receiver == username1),
            )
        )
        .order_by(Message.message_id)
        .all()
    )

    return jsonify([message.json() for message in messages]), 200


@app.route("/chat/send_message", methods=["POST"])
def send_message():
    data = request.get_json()

    print("received message", data["message"])
    print("received sender", data["sender"])
    print("received receiver", data["receiver"])

    now_datetime = datetime.datetime.now()
    message_datetime = now_datetime.strftime("%H:%M:%S | %d/%m/%Y")

    message = Message(
        data["message"], data["sender"], data["receiver"], message_datetime
    )

    db.session.add(message)
    db.session.commit()

    return jsonify(message.json()), 201


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    account = Account.query.filter_by(username=username).first()

    if account:
        if account.password == password:
            encoded_jwt = jwt.encode(
                {"username": username}, "12345", algorithm="HS256"
            ).decode("utf-8")
            return (
                jsonify(
                    {"status": True, "token": str(encoded_jwt), "username": username}
                ),
                200,
            )
    return jsonify({"status": False}), 400


@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    account = Account(username, password)
    user = User(username, "", "", "", "", "", "default.jpg", 0)

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "about_me": self.about_me,
            "occupation": self.occupation,
            "image": self.image,
            "points": self.points,
        }

    db.session.add(account)
    db.session.add(user)
    db.session.commit()

    encoded_jwt = jwt.encode({"username": username}, "12345", algorithm="HS256").decode(
        "utf-8"
    )

    return (
        jsonify({"status": True, "token": str(encoded_jwt), "username": username}),
        201,
    )


@app.route("/auth/me", methods=["GET"])
def me():
    token = request.headers.get("Authorization")

    if token == None or token == "":
        return jsonify({"status": False, "message": "Empty token"}), 401

    try:
        user = jwt.decode(token, "12345", algorithms="HS256")
        username = user["username"]
        print("decoded username", username)
    except:
        return jsonify({"status": False, "message": "Invalid token"}), 401

    user = User.query.filter_by(username=username).first()

    return jsonify({"status": True, "user": user.json()}), 200


# ! QUESTIONS
# ===================================================================================================
@app.route("/getQuestions")
def get_questions():
    with open("./backend/data/question.json") as fp:
        loaded_data = json.load(fp)
        loaded_data.reverse()
    return json.dumps(loaded_data)


@app.route("/getQuestionById/<questionId>")
def get_question_by_id(questionId):
    with open("./backend/data/question.json") as fp:
        loaded_data = json.load(fp)
        data = []
        for elem in loaded_data:
            if elem["questionId"] == int(questionId):
                data.append(elem)
    return json.dumps(data)


@app.route("/getAnswerByQuestionId/<questionId>")
def get_answer_by_question_id(questionId):
    with open("./backend/data/answer.json") as fp:
        loaded_data = json.load(fp)
        data = []
        for elem in loaded_data:
            if elem["questionId"] == int(questionId):
                data.append(elem)
    return json.dumps(data)


@app.route("/getCommentByQuestionId/<questionId>")
def get_comment_by_question_id(questionId):
    with open("./backend/data/comment.json") as fp:
        loaded_data = json.load(fp)
        data = []
        for elem in loaded_data:
            if elem["questionId"] == int(questionId):
                data.append(elem)
    return json.dumps(data)


@app.route("/getCommentByAnswerId/<answerId>")
def get_comment_by_answer_id(answerId):
    with open("./backend/data/comment.json") as fp:
        loaded_data = json.load(fp)
        data = []
        for elem in loaded_data:
            if elem["answerId"] == int(answerId):
                data.append(elem)
    return json.dumps(data)


@app.route("/addQuestion", methods=["POST"])
def add_question():
    questionTag = request.form.get("questionTag", False)
    questionTitle = request.form.get("questionTitle", False)
    questioner = request.form.get("questioner", False)
    filename = request.form.get("filename", False)
    image = request.form.get("image", False)

    s3_image_url = upload_to_s3(image, filename)
    image = s3_image_url

    with open("./backend/data/question.json") as fp:
        loaded_data = json.load(fp)

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    loaded_data.append(
        {
            "questionId": len(loaded_data) + 1,
            "questionTag": questionTag.split(","),
            "questionTitle": questionTitle,
            "timeAsked": timestamp,
            "questioner": questioner,
            "initial": questioner[0].upper(),
            "image": image,
            "filename": filename,
            "bestAnswerId": None,
        }
    )

    with open("./backend/data/question.json", "w+") as fp:
        json.dump(loaded_data, fp, indent=4)

    return jsonify("success")


@app.route("/postAnswer", methods=["POST"])
def post_answer():
    answeredBy = request.form.get("answeredBy", False)
    description = request.form.get("description", False)
    questionId = request.form.get("questionId", False)
    filename = request.form.get("filename", False)
    image = request.form.get("image", False)
    filename = request.form.get("filename", False)

    if description == "null":
        description = None
    if image == "null":
        image = None
    else:
        # image is not null, upload to s3
        s3_image_url = upload_to_s3(image, filename)
        image = s3_image_url

    with open("./backend/data/answer.json") as fp:
        loaded_data = json.load(fp)

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    loaded_data.append(
        {
            "answerId": len(loaded_data) + 1,
            "questionId": int(questionId),
            "answeredBy": answeredBy,
            "initial": answeredBy[0].upper(),
            "timeAnswered": timestamp,
            "upvote": 0,
            "downvote": 0,
            "image": image,
            "filename": filename,
            "description": description,
            "bestAnswer": False,
        }
    )

    with open("./backend/data/answer.json", "w+") as fp:
        json.dump(loaded_data, fp, indent=4)

    return jsonify("success")


def upload_to_s3(image, filename):
    # image is base64 now
    image_data = base64.b64decode(image)
    with open("./" + filename, "wb") as f:
        f.write(image_data)

    with open("./" + filename, "rb") as readfile:
        upload_path = filename
        AWS_S3_CLIENT.upload_fileobj(readfile, BUCKET_NAME, upload_path)

    os.remove("./" + filename)
    return "https://vueducation.s3-ap-southeast-1.amazonaws.com/{}".format(upload_path)


@app.route("/getVoteByAnswerId/<answerId>")
def get_vote_by_answer_id(answerId):
    with open("./backend/data/vote.json") as fp:
        loaded_data = json.load(fp)
        vote = 0
        for elem in loaded_data:
            if int(elem["answerId"]) == int(answerId):
                vote += int(elem["vote"])

    return json.dumps({"vote": vote})


@app.route("/getVoteByAnswerIdUser/<answerId>/<user>")
def get_vote_by_answer_id_user(answerId, user):
    with open("./backend/data/vote.json") as fp:
        loaded_data = json.load(fp)
        vote = 0
        for elem in loaded_data:
            if int(elem["answerId"]) == int(answerId) and elem["username"] == user:
                vote += int(elem["vote"])

    return json.dumps({"vote": int(vote)})


@app.route("/postVote/<answerId>/<username>/<vote>")
def post_vote(answerId, username, vote):
    with open("./backend/data/vote.json") as fp:
        loaded_data = json.load(fp)

    found = False
    to_be_deleted = None
    totalVote = 0

    for elem in loaded_data:
        if int(elem["answerId"]) == int(answerId) and elem["username"] == username:
            # elem['vote'] = vote
            to_be_deleted = elem
            found = True
        elif int(elem["answerId"]) == int(answerId):
            totalVote += int(elem["vote"])

    if found == True:
        loaded_data.remove(to_be_deleted)

    if found == False:
        loaded_data.append({"answerId": answerId, "vote": vote, "username": username})
        totalVote += 1

    with open("./backend/data/vote.json", "w+") as fp:
        json.dump(loaded_data, fp, indent=4)

    return json.dumps({"vote": totalVote})


@app.route("/markBestAnswer/<questionId>/<answerId>")
def mark_best_answer(questionId, answerId):
    with open("./backend/data/question.json") as fp:
        loaded_data = json.load(fp)

    for elem in loaded_data:
        if int(elem["questionId"]) == int(questionId):
            elem["bestAnswerId"] = answerId

    with open("./backend/data/question.json", "w+") as fp:
        json.dump(loaded_data, fp, indent=4)

    with open("./backend/data/answer.json") as fp:
        loaded_answer = json.load(fp)

    for elem in loaded_answer:
        if int(elem["answerId"]) == int(answerId):
            elem["bestAnswer"] = True

    with open("./backend/data/answer.json", "w+") as fp:
        json.dump(loaded_answer, fp, indent=4)

    return jsonify("success")


@app.route("/numberOfBestAnswer/<username>")
def num_of_best_answer(username):
    with open("./backend/data/answer.json") as fp:
        loaded_data = json.load(fp)

    total = 0
    for elem in loaded_data:
        if elem["answeredBy"] == username and elem["bestAnswer"]:
            total += 1

    return json.dumps({"total": total})


#############
# WORKSHOPS #
#############


@app.route("/getWorkshops")
def getWorkshops():
    with open("./backend/data/workshops.json") as fp:
        data = json.load(fp)
    return json.dumps(data)


@app.route("/getRecommended")
def getRecommended():
    data = json.load(open("./backend/data/workshops.json"))
    result = []
    for _ in range(4):
        try:
            result.append(data.pop(random.randrange(len(data))))
        except:
            continue
    return jsonify(result)


@app.route("/addWorkshop", methods=["GET", "POST"])
def addWorkshop():
    name = request.form.get("name", False)
    org = request.form.get("institution", False)
    descr = request.form.get("description", False)
    link = request.form.get("link", "")
    location = request.form.get("location", "")
    category = request.form.get("category", False)
    mode = request.form.get("mode", False)
    img = request.files.get("image", False)
    startDate = request.form.get("startDate", False)
    startTime = request.form.get("startTime", False)
    endDate = request.form.get("endDate", False)
    endTime = request.form.get("endTime", False)
    localeEnd = request.form.get("localeEnd", False)
    localeStart = request.form.get("localeStart", False)

    def convertTime(time):
        hours = time.split(":")[0]
        minutes = time.split(":")[1]
        if len(minutes) < 2:
            minutes = "0" + minutes
        timeEnd = "AM"
        if int(hours) > 12:
            timeEnd = "PM"
            hours = int(hours) - 12
        timeString = f"{hours}:{minutes}{timeEnd}"
        return timeString

    def convertDate(date):
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        dateString = f"{date.split('-')[2]} {months[int(date.split('-')[1]) - 1]} {date.split('-')[0]}"
        return dateString

    if (
        name
        and org
        and descr
        # and (link != "" or location != "")
        and category
        and img
        and mode
        and startDate
        and startTime
        and endDate
        and endTime
        and localeEnd
        and localeStart
    ):
        with open("./backend/data/workshops.json") as fp:
            data = json.load(fp)

        now = datetime.now()
        dt_string = now.strftime("%d%m%YT%H%M%S%f_") + img.filename
        filepath = os.path.join("./static/workshop", dt_string)
        img.save(filepath)

        try:
            index = data[-1]["index"] + 1
        except:
            index = 0
            
        data.append(
            {
                "index": index,
                "title": name,
                "institution": org,
                "description": descr,
                "img": f"/workshop/{dt_string}",
                "category": category,
                "link": link,
                "location": location,
                "mode": mode,
                "startDate": convertDate(startDate),
                "startTime": convertTime(startTime),
                "endDate": convertDate(endDate),
                "endTime": convertTime(endTime),
                "icalStart": f'{startDate.replace("-", "")}T{startTime.replace(":", "")}Z',
                "icalEnd": f'{endDate.replace("-", "")}T{endTime.replace(":", "")}Z',
                "localeStart": localeStart,
                "localeEnd": localeEnd,
            }
        )
        with open("./backend/data/workshops.json", "w+") as fp:
            json.dump(data, fp, indent=2)

        return jsonify("success")

    else:
        return jsonify("missing variables")


@app.route("/markcalendar", methods=["GET", "POST"])
def markCalendar():
    user = request.form.get("user", False)
    name = request.form.get("name", False)
    start = request.form.get("start", False)
    end = request.form.get("end", False)

    if user and name and start and end:
        with open("backend/data/workshop_database.json") as fp:
            json_data = json.load(fp)

        if json_data.get(user, False) == False:
            json_data[user] = []

        start = start.replace(",", "")
        end = end.replace(",", "")

        # startArr = start.split(" ")[:6]
        # tempYear = startArr.pop(3)
        # startArr.append(tempYear)
        # start = " ".join(startArr)

        # endArr = end.split(" ")[:6]
        # tempYear = endArr.pop(3)
        # endArr.append(tempYear)
        # end = " ".join(endArr)

        allDay = False

        if {
            "name": name,
            "start": start,
            "end": end,
            "allDay": allDay,
        } not in json_data[user]:
            json_data[user].append(
                {"name": name, "start": start, "end": end, "allDay": allDay}
            )

        with open("./backend/data/workshop_database.json", "w+") as fp:
            json.dump(json_data, fp, indent=2)

        return jsonify("success")

    else:
        return jsonify("missing variables")


@app.route("/getcalendar", methods=["GET", "POST"])
def getCalendar():
    user = request.form.get("user", False)

    with open("backend/data/workshop_database.json") as fp:
        json_data = json.load(fp)

    return jsonify(json_data.get(user, []))


# ! Promo
# ===================================================================================================
@app.route("/promo/<voucher>")
def get_promo(voucher):
    promo = Promo.query.filter_by(voucher=voucher).first()

    return jsonify(promo.json()), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

