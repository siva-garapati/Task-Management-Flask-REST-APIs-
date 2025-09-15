from flask import Blueprint, request, jsonify
from .models import Users, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Home Page"

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data['username']
    email = data['email']
    password = data['password']

    user = Users.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "msg":"user already exists"
        })
    hashed_password = generate_password_hash(password)

    new_user = Users(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'msg':'registration success'
    })


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=user.email)
        return jsonify({
            'msg':'login success.',
            'token':token
        })
    return jsonify({
        'msg':'check useremail or password'
    })

@main.route("/dash", methods=["GET"])
@jwt_required()
def dashboard():
    email = get_jwt_identity()
    print(email)
    user = Users.query.filter_by(email=email).first()
    return jsonify({"msg": f"Welcome {user.email}"})