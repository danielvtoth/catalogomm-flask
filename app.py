from flask import Flask, render_template
import config
import controllers

app = Flask(__name__, template_folder='templates')
app.register_blueprint(controllers.main)

if __name__ == '__main__':
	app.run(host=config.env['host'], port=config.env['port'], debug=True)