from flask import Flask, request, render_template
from flaskext.mysql import MySQL
import myFunction



app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

app.config['MYSQL_DATABASE_HOST'] = 'test.cy2mahvlzze7.ap-northeast-2.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'j6332335'
app.config['MYSQL_DATABASE_DB'] = 'team_project'
mysql = MySQL()
mysql.init_app(app)



'''
#person_count 실행
@app.route("/count", methods=["GET"])
def get_stInfo():

#지하철 역명 얻어오기


@app.route("/count", methods=["Post"])
def send_info():

#지하철 도착예정정보, 혼잡도 반환
'''

@app.route("/")
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
