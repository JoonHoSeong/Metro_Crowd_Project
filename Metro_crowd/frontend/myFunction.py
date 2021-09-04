import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Person_count



def time_to_str(second):
    second = int(second)
    if second >= 60 :
        minute = int(second / 60)
        second = int(second%60)
        time = str(minute) + ":" + str(second)
    else :
        time = "00:" + str(second)
    return time

class train_data:
    def __init__(self):
        self.train_id = [] #열차 ID
        self.train_updnLine = [] # 상하행선
        self.train_time = [] #도착예정시간
        self.train_line = [] #지하철 호선
        self.train_destination = [] # 종착지
        self.staion_name = '사당'

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
            self.train_destination.append(train_dataset.iloc[row]['bstatnNm'])  # 종착지하철역ID


    def Extensions_train_data(self):
        index = self.train_updnLine.index('내선')
        return [self.train_line[index], self.train_updnLine[index], time_to_str(self.train_time[index]),\
               self.train_destination[index], self.train_id[index]]

    def External_train_data(self):
        if '외선' in self.train_updnLine:
            index = self.train_updnLine.index('외선')
            return [self.train_line[index], self.train_updnLine[index], time_to_str(self.train_time[index]),\
                   self.train_destination[index], self.train_id[index]]
        else :
            return [None, None,None,None,None]


    def Upward_train_data(self):
        if '상행' in self.train_updnLine:
            index = self.train_updnLine.index('상행')
            return [self.train_line[index], self.train_updnLine[index], time_to_str(self.train_time[index]),\
                   self.train_destination[index], self.train_id[index]]
        else :
            return [None, None,None,None,None]


    def Downward_train_data(self):
        if '하행' in self.train_updnLine:
            index = self.train_updnLine.index('하행')
            return [self.train_line[index], self.train_updnLine[index], time_to_str(self.train_time[index]),\
                   self.train_destination[index], self.train_id[index]]
        else :
            return [None, None,None,None,None]
class crowded_detect:#혼잡도 리스트 반환
    def __init__(self):
        self.crowd_list = []

    def load_image(self): #using_random_image
        self.crowd_list = Person_count.run()

    def crowd(self):
        self.load_image()
        return self.crowd_list
