from flask import Blueprint, request, current_app
from app.models.casos_model import Casos
from app.models.users_model import UsersModel
from flask_jwt_extended import jwt_required
from http import HTTPStatus

casos = Blueprint("casos", __name__, url_prefix="/casos")

@casos.route("/create/<int:user_id>", methods=["POST"])
@jwt_required()
def create_casos(user_id):
    body = request.get_json()
    session = current_app.db.session

    verify_user: UsersModel = UsersModel.query.get(user_id)

    if not verify_user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    title = body.get("title")
    decription = body.get("decription")
    value = body.get("value")

    new_caso: Casos = Casos(title=title, decription=decription, value=value)
    verify_user.user_caso.append(new_caso)

    session.add(new_caso)
    session.commit()

    return {
        "caso": {
            "title": new_caso.title,
            "description": new_caso.decription,
            "value": new_caso.value
        }
    }, HTTPStatus.OK

@casos.route("/list_casos", methods=["GET"])
def list_casos():

    list_casos_db = Casos.query.all()

    return {
        "Casos": [{
            "title": element_caso.title,
            "description": element_caso.decription,
            "value": element_caso.value
            } for element_caso in list_casos_db]
    }, HTTPStatus.OK

@casos.route("/list_casos/user/<int:user_id>", methods=["GET"])
@jwt_required()
def list_casos_users(user_id):
    session = current_app.db.session

    verify_casos_user = session.query(UsersModel, Casos).join(Casos).filter(UsersModel.user_id == user_id).all()

    if not verify_casos_user:
        return {"messagem": "Esse usuário não existe ou não tem casos cadastrado"}, HTTPStatus.OK

    return {
        "Casos": [{
            "title": element_caso.title,
            "description": element_caso.decription,
            "value": element_caso.value
            } for data_user, element_caso in verify_casos_user]
    }, HTTPStatus.OK
    