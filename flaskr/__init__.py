import os

from flask import Flask

def create_app(test_config=None):
	# Crea y configura la aplicación
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
	)

	if test_config is None:
		# Cargamos la instancia config, si existe, entonces no testeamos
		app.config.from_pyfile('config.py', silent=True)
	else:
		# Cargamos la configuración de prueba si se pasa
		app.config.from_mapping(test_config)

	# Nos aseguramos de que existe la carpeta de la instancia
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Una página simple que dice Hola Mundo
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	return app	
