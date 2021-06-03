from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app.models.users_model import UsersModel
from http import HTTPStatus

authentication = Blueprint("authentication",  __name__)

@authentication.route("/register", methods=["POST"])
def register():
    session = current_app.db.session
    body = request.get_json()

    name = body.get("name")
    email = body.get("email")
    password = body.get("password")

    new_user = UsersModel(name=name, email=email)
    new_user.password = password

    session.add(new_user)
    session.commit()

    access_token = create_access_token(identity=new_user.user_id, expires_delta=timedelta(days=7))
    refresh_token = create_access_token(identity=new_user.user_id, fresh=True, expires_delta=timedelta(days=14))

    return {
        "name": new_user.name,
        "email": new_user.email,
        "access_token": access_token,
        "refresh_token": refresh_token
    }, HTTPStatus.CREATED

@authentication.route("/login", methods=["POST"])
def login():
    body = request.get_json()

    email = body.get("email")
    password = body.get("password")

    verify_user: UsersModel = UsersModel.query.filter_by(email=email).first()

    if not verify_user or not verify_user.check_password(password):
        return {"messagem": "User not found"}, HTTPStatus.NOT_FOUND
    
    access_token = create_access_token(identity=verify_user.user_id, expires_delta=timedelta(days=7))
    refresh_token = create_access_token(identity=verify_user.user_id, fresh=True, expires_delta=timedelta(days=14))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }, HTTPStatus.OK


@authentication.route("/refresh", methods=["GET"])
@jwt_required(fresh=True)
def refresh():
    user_id = get_jwt_identity()
    
    access_token = create_refresh_token(identity=user_id, expires_delta=timedelta(days=7))

    return {
        "access_token": access_token
    }, HTTPStatus.OK

@authentication.route("/data/user/<int:user_id>", methods=["GET"])
def data_user(user_id):
    verify_user: UsersModel = UsersModel.query.filter_by(user_id=user_id).first()

    if not verify_user:
        return {"messagem": "User not found"}, HTTPStatus.NOT_FOUND
    
    return {
        "name": verify_user.name,
        "email": verify_user.email
    }, HTTPStatus.OK