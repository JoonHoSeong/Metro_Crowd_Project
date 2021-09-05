from flask import Flask, request, render_template, redirect, session
from flaskext.mysql import MySQL
import json
import myFunction
import datetime as time

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )


@app.route('/info/<string:station>', methods=['GET'])
def getStName(station):
    station = json.loads(station) #역명 불러오기

    # 현재시간 load
    load_time = time.datetime.now()
    hour = load_time.hour
    minute = load_time.minute
    second = load_time.second
    time_now = str(hour) + ':' + str(minute) + ":" + str(second)

    # 혼잡도 계산 API Load
    crowd_data = myFunction.crowded_detect()

    # 열차 도착 정보
    train_data_set = myFunction.train_data()
    train_data_set.set_staion(station['name'])
    train_data_set.load_station_data()
    Extensions_train_data = train_data_set.Extensions_train_data()  # 내선
    External_train_data = train_data_set.External_train_data()  # 외선
    Upward_train_data = train_data_set.Upward_train_data()  # 상행
    Downward_train_data = train_data_set.Downward_train_data()  # 하행

    # 내선(호선정보, 방향, 대기시간, 목적지, 열차고유번호, 현재시간, 혼잡도(0,1,2로 반환))
    if Extensions_train_data[0] == None:
        print("내선 열차 미존재")
        Extensions_train_data = {"Line": None,
                               "Direction": None,
                               "Wait_time": "00:00",
                               "Destination": None,
                               "ID": None,
                               "Now_time": time_now,
                               "Crowd": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    else:
        Extensions_train_data = {"Line": Extensions_train_data[0],
                                 "Direction": Extensions_train_data[1],
                                 "Wait_time": Extensions_train_data[2],
                                 "Destination": Extensions_train_data[3],
                                 "ID": Extensions_train_data[4],
                                 "Now_time": time_now,
                                 "Crowd": crowd_data.crowd()}

    # 외선(호선정보, 방향, 대기시간, 목적지, 열차고유번호, 현재시간, 혼잡도(0,1,2로 반환))
    if External_train_data[0] == None:
        print("외선 열차 미존재")
        External_train_data = {"Line": None,
                               "Direction": None,
                               "Wait_time": "00:00",
                               "Destination": None,
                               "ID": None,
                               "Now_time": time_now,
                               "Crowd": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    else:
        External_train_data = {"Line": External_train_data[0],
                               "Direction": External_train_data[1],
                               "Wait_time": External_train_data[2],
                               "Destination": External_train_data[3],
                               "ID": External_train_data[4],
                               "Now_time": time_now,
                               "Crowd": crowd_data.crowd()}

    # 상행(호선정보, 방향, 대기시간, 목적지, 열차고유번호, 현재시간, 혼잡도(0,1,2로 반환))
    if Upward_train_data[0] == None:
        print("상행 열차 미존재")
        Upward_train_data = {"Line": None,
                               "Direction": None,
                               "Wait_time": "00:00",
                               "Destination": None,
                               "ID": None,
                               "Now_time": time_now,
                               "Crowd": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    else:
        Upward_train_data = {"Line": Upward_train_data[0],
                             "Direction": Upward_train_data[1],
                             "Wait_time": Upward_train_data[2],
                             "Destination": Upward_train_data[3],
                             "ID": Upward_train_data[4],
                             "Now_time": time_now,
                             "Crowd": crowd_data.crowd()}

    # 하행(호선정보, 방향, 대기시간, 목적지, 열차고유번호, 현재시간, 혼잡도(0,1,2로 반환))
    if Downward_train_data[0] == None:
        print("하행 열차 미존재")
        Downward_train_data = {"Line": None,
                               "Direction": None,
                               "Wait_time": "00:00",
                               "Destination": None,
                               "ID": None,
                               "Now_time": time_now,
                               "Crowd": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    else:
        Downward_train_data = {"Line": Downward_train_data[0],
                                 "Direction": Downward_train_data[1],
                                 "Wait_time": Downward_train_data[2],
                                 "Destination": Downward_train_data[3],
                                 "ID": Downward_train_data[4],
                                 "Now_time": time_now,
                                 "Crowd": crowd_data.crowd()}


    print(Extensions_train_data)
    print(External_train_data)
    print(Upward_train_data)
    print(Downward_train_data)

    print(station['name'])
    return render_template('index.html')


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/search')
def searchStation():
    return render_template("search-station.html")


if __name__ == '__main__':
    app.run(debug=True)
