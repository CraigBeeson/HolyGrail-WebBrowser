import flask
import sqlite3

app = flask.Flask(__name__)
app.use_reloader = False;

def FlaskApp():
	app.run()
	
@app.route("/documents")
@app.route("/documents/<plugin>")
def home(plugin=0):
	DBCon = sqlite3.connect("DocsFiles/Docs.db")
	cursor = DBCon.cursor()
	cursor.execute("SELECT * FROM Plugins")
	plugins = cursor.fetchall()
	cursor.execute("SELECT * FROM Plugin_Desc WHERE plugin_num = " + str(plugin))
	desc = cursor.fetchall()
	return flask.render_template("DocsHtml.html", plugins = plugins, desc = desc[0][1])