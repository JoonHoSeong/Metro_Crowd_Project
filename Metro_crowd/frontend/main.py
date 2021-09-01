from flask import Flask, request, render_template
from flaskext.mysql import MySQL
import myFunction



app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

app.config['MYSQL_DATABASE_HOST'] = ''
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''

mysql = MySQL()
mysql.init_app(app)




#person_count 실행
@app.route("/count", methods=["GET"])






@app.route("/")
def index():
    return render_template('index.html')





    


if __name__ == '__main__':
    app.run(debug=True)
