import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from yolov5 import Person_count

class train_data:
    def __init__(self):
        self.train_id = []
        self.train_updnLine = []
        self.train_time = []
        self.train_line = []
        self. staion_name = '사당'

    def set_staion(self, station):
        self.station_name = station

    def load_station_data(self):
        get_metrodata = Person_count.load_metro_data()
        get_metrodata.set_station(station=self.station_name)
        get_metrodata.set_station_code()
        train_dataset = get_metrodata.load_API_data()
        train_dataset = train_dataset.sort_values(by='barvlDt' ,ascending=True) #도착 시간 오름차순 정령
        train_dataset = train_dataset.sort_values(by='updnLine', ascending=False) # 하행, 외선, 상행, 내선 순서

        for row in range(len(train_dataset), ):
            self.train_id.append(train_dataset.iloc[row]['btrainNo'])
            self.train_updnLine.append(train_dataset.iloc[row]['updnLine'])
            self.train_time.append(train_dataset.iloc[row]['barvlDt'])
            self.train_line.append(train_dataset.iloc[row]['subwayId'])


    def Extensions_train_data(self):
        index = self.train_updnLine.index('내선')
        return self.train_id[index], self.train_time[index], self.train_line[index]

    def External_train_data(self):
        index = self.train_updnLine.index('외선')
        return self.train_id[index], self.train_time[index], self.train_line[index]

    def Upward_train_data(self):
        index = self.train_updnLine.index('상행')
        return self.train_id[index], self.train_time[index], self.train_line[index]

    def Downward_train_data(self):
        index = self.train_updnLine.index('하행')
        return self.train_id[index], self.train_time[index], self.train_line[index]

class crowded_detect:#혼잡도 리스트 반환
    def __init__(self):
        self.crowd = []

    def using_random_image(self):
        self.crowd_list = Person_count.run()

    def crowd(self):
        return self.crowd_list
