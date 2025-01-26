from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
import re


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'mongodb',
    'port': 27017,
    'username': 'admin',
    'password': 'admin',
}

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('cpf', type=str, required=True, help="O campo CPF não pode ser vazio")
_user_parser.add_argument('first_name', type=str, required=True, help="O campo firstName não pode ser vazio")
_user_parser.add_argument('last_name', type=str, required=True, help="O campo lastName não pode ser vazio")
_user_parser.add_argument('email', type=str, required=True, help="O campo email não pode ser vazio")
_user_parser.add_argument('birth_Date', type=str, required=True, help="O campo birthDate não pode ser vazio")


api = Api(app)
db = MongoEngine(app)


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    email = db.EmailField(required=True)
    birth_Date = db.DateTimeField(required=True)


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects.all())


class User(Resource):
    
    def validate_cpf(self, cpf):
        # Verifica se o CPF tem a máscara correta
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', cpf):
            return False

        # Pega somente os dígitos numéricos
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se tem 11 dígitos e se não são todos iguais
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Valida o primeiro dígito verificador
        sum_of_products = sum(a * b for a, b in zip(numbers[:9], range(10, 1, -1)))
        first_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != first_digit:
            return False

        # Valida o segundo dígito verificador
        sum_of_products = sum(a * b for a, b in zip(numbers[:10], range(11, 1, -1)))
        second_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != second_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()

        if not self.validate_cpf(data['cpf']):
            return {"message": "CPF inválido"}, 400
        
        try:
            response = UserModel(**data).save()
            return {"message": "Usuario cadastrado com sucesso"}, 200
        except NotUniqueError:
            return {"message": "Usuário ja existe"}, 400

    def get(self, cpf):
        response = UserModel.objects(cpf=cpf)
        
        if response:
            return jsonify(response)
        else:
            return {"message": "Usuário não encontrado"}, 404


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
