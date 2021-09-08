from flask import Flask, render_template, request
import numpy as np
import myFunction
import json
import datetime as time

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/info', methods=['GET'])
def getStation():
    # 역 이름, 호선 이름 get
    station = request.args.get('name');
    line = request.args.get('line');

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
    train_data_set.set_staion(station)
    train_data_set.load_station_data()#호선 정보 넣기기
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
    print(station)
    print(line)

    data_all = {
        'extensionsCrowd': Extensions_train_data["Crowd"],
        'externalCrowd': External_train_data["Crowd"],
        'upCrowd': Upward_train_data["Crowd"],
        'downCrowd': Downward_train_data["Crowd"],
        'extensionsWait': Extensions_train_data["Wait_time"],
        'externalWait': External_train_data["Wait_time"],
        'upWait': Upward_train_data["Wait_time"],
        'downWait': Downward_train_data["Wait_time"],
        'extensionsDest': Extensions_train_data["Destination"],
        'externalDest': External_train_data["Destination"],
        'upDest': Upward_train_data["Destination"],
        'downDest': Downward_train_data["Destination"],
        'nowtime': time_now
    }
    data_all = json.dumps(data_all, cls=NumpyEncoder)

    #print(type(Upward_train_data["Wait_time"]))

    return data_all

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/search')
def searchStation():
    return render_template("search-station.html")

@app.route('/header')
def getHeader():
    return render_template("header.html")

if __name__ == '__main__':
    app.run(debug=True)
