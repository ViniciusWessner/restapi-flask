from application import create_app
import os

if os.getenv('FLASK_ENV') == 'development':
    app = create_app('config.DevConfig')
if os.getenv('FLASK_ENV') == 'production':
    app = create_app('config.ProdConfig')
if os.getenv('FLASK_ENV') == 'mock':
    app = create_app('config.MockConfig')
else:
    print("Nenhuma variavel de ambiente setada")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
