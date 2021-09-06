import os
import requests, json
import numpy as np
import pandas as pd
from argparse import Namespace
import mysql.connector
from PIL import Image
import io
import datetime as time
import random
import detect

class load_image:

    def __init__(self):
        self.host = 'test.cy2mahvlzze7.ap-northeast-2.rds.amazonaws.com'
        self.user = 'admin'
        self.pw = 'j6332335'
        self.db =  'team_project'

    def create_random_image_index(self, image_num=10):
        image_index_list = []
        for i in range(0,image_num,1):
            image_index_list = np.append(image_index_list, random.randrange(284))
        return image_index_list


    def readBLOB(self, image_id):
        #make predict_temp directory
        if not os.path.isdir('./predict_tmp'):
            os.mkdir('./predict_tmp')
        # print("Reading BLOB data from indoor_picture table")

        try:
            connection = mysql.connector.connect(host=self.host,
                                                 database=self.db,
                                                 user=self.user,
                                                 password=self.pw)

            cursor = connection.cursor()
            #load & save images
            for index, id_num in enumerate(image_id):
                sql_fetch_blob_query = """SELECT picture from indoor_picture where id = {} """.format(id_num)
                cursor.execute(sql_fetch_blob_query)
                record = cursor.fetchone()
                image = record[0]
                img = Image.open(io.BytesIO(image))
                img.save('./predict_tmp/'+str(index+100)+'.png', format='png')



        except mysql.connector.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed")


class person_determination:
    def __init__(self):
        self.peron_num=0
        self.first_param = 20
        self.second_param = 45

    def Determination(self, p_num):
        self.person_num = p_num
        if self.person_num <= self.first_param:
            return 0
        elif self.person_num <= self.second_param:
            return 1
        else :
            return 2
    #0:여유  1:보통  2:혼잡

    def person_congresion_list(self, p_num_list=[]):
        congresion_list = []
        tmp = p_num_list[1]
        for i in range(0,len(p_num_list),2):
            #if p_num_list[i] == p_num_list[i] or p_num_list[i] == tmp:
            #    p_num_list[i] = 0
            p_num = p_num_list[i] + p_num_list[i+1]
            #tmp = p_num_list[i + 1]
            congresion_list = np.append(congresion_list,self.Determination(p_num))
        return congresion_list

    def set_param(self,first = None, second = None):
        self.first_param = first
        self.second_param = second



def my_detect(img=None):
    opts = Namespace(weights=['yolov5s6.pt'],
                     source=img,  #사진 불러오는 방식에 따라 변경 필요함
                     imgsz=[720, 1280],
                     conf_thres=0.1,
                     iou_thres=0.45,
                     max_det=200,
                     device='',
                     view_img=False,
                     save_txt=False,
                     save_conf=False,
                     save_crop=False,
                     nosave=False,
                     classes=[0],
                     agnostic_nms=False,
                     augment=False,
                     visualize=False,
                     update=False,
                     project='runs/detect',
                     name='exp',
                     exist_ok=False,
                     line_thickness=1,
                     hide_labels=False,
                     hide_conf=False,
                     half=False,
                     tfl_int8=False)
    person_cnt_list = detect.main(opts)
    print('detect Done')
    return person_cnt_list
    '''
    weights='yolov5x6.pt',  # model.pt path(s)
    source='data/images',  # file/dir/URL/glob, 0 for webcam
    imgsz=640,  # inference size (pixels)
    conf_thres=0.008,  # confidence threshold
    iou_thres=0.45,  # NMS IOU threshold
    max_det=300,  # maximum detections per image
    device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    view_img=False,  # show results
    save_txt=False,  # save results to *.txt
    save_conf=False,  # save confidences in --save-txt labels
    save_crop=False,  # save cropped prediction boxes
    nosave=False,  # do not save images/videos
    classes= '0',  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=True,  # class-agnostic NMS
    augment=False,  # augmented inference
    visualize=False,  # visualize features
    update=False,  # update all models
    project='runs/detect',  # save results to project/name
    name='exp',  # save results to project/name
    exist_ok=False,  # existing project/name ok, do not increment
    line_thickness=1,  # bounding box thickness (pixels)
    hide_labels=False,  # hide labels
    hide_conf=False,  # hide confidences
    half=False,  # use FP16 half-precision inference
    tfl_int8=False,  # INT8 quantized TFLite model
    '''

# noinspection PyStatementEffect
class load_metro_data: # 실시간 지하철 도착정보
    def __init__(self):
        self.station = ''
        self.key = '61584e6867776e733933454a4b6761'
        self.station_code =''
        self.base_url = 'http://swopenapi.seoul.go.kr/api/subway/'+self.key+'/json/realtimeStationArrival/0/10/'
        self.url = ''


    def set_url(self):
        self.url = self.base_url + self.station

    def print_param(self):
        return print(self.station, self.station_code)

    def set_station(self, station=''):
        self.station = station
        self.set_station_code()
        self.set_url()

    def set_key(self, key):
        self.key = key

    def set_station_code(self):
        base_url = 'http://openapi.seoul.go.kr:8088/sample/json/SearchInfoBySubwayNameService/1/5/'
        url = base_url + self.station
        response = requests.get(url)
        data = json.loads(response.text)
        self.station_code = int(data['SearchInfoBySubwayNameService']['row'][0]['STATION_CD'])


    def load_API_data(self):
        #if self.check_train_is_avilable_time():
            #API 연결 상태 확인 및 load
        info = ['subwayId', 'updnLine', 'trainLineNm',
                  'subwayHeading','statnFid','statnTid',
                  'statnId','statnNm','ordkey',
                  'btrainSttus','barvlDt','btrainNo',
                  'bstatnId','recptnDt','arvlMsg2',
                  'arvlMsg3','arvlCd','subwayList',
                  'statnList','bstatnNm']
#        print("Person_count staion load_API_data: ", self.station)
#        print("Person_count staion load_API_data: ", self.station_code)
#        print("Person_count staion load_API_data: ", self.url)
        response_data = pd.DataFrame(columns= info, index=None)
        #print(self.url) #url확인
        response = requests.get(self.url)
        data = json.loads(response.text)
        try :
            if data['code'] == 'INFO-200':
                print("해당 역에대한 데이터가 존재하지 않습니다.(서울시 지하철 API 오류)")
                return response_data
        except:
            if data['errorMessage']['code'] == 'INFO-000': #정상작동
                print("Realtime API Connect Success")
                for num in range(0, len(data['realtimeArrivalList']), 1):
                    data_list = {"Index" : num
                    ,'subwayId' : data['realtimeArrivalList'][num]['subwayId'] #지하철 호선ID
                    ,'updnLine' : data['realtimeArrivalList'][num]['updnLine']#상하행선 구분(내선:0, 외선:1, 상행, 하행)
                    ,'trainLineNm'  : data['realtimeArrivalList'][num]['trainLineNm']#도착지방면 (성수행 - 구로디지털단지방면)
                    ,'subwayHeading' : data['realtimeArrivalList'][num]['subwayHeading']#내리는문방향(오른쪽,왼쪽)
                    ,'statnFid' : data['realtimeArrivalList'][num]['statnFid']#이전지하철역ID
                    ,'statnTid' : data['realtimeArrivalList'][num]['statnTid']#다음지하철역ID
                    ,'statnId' : data['realtimeArrivalList'][num]['statnId']#지하철역ID
                    ,'statnNm' : data['realtimeArrivalList'][num]['statnNm']#지하철역명
                    #data['realtimeArrivalList'][num]['tmsitCo']#환승노선수
                    ,'ordkey' : data['realtimeArrivalList'][num]['ordkey']#도착예정열차순번
                    ,'btrainSttus' : data['realtimeArrivalList'][num]['btrainSttus']#열차종류(급행,ITX)
                    ,'barvlDt' : data['realtimeArrivalList'][num]['barvlDt']#열차도착예정시간(단위:초)
                    ,'btrainNo' : data['realtimeArrivalList'][num]['btrainNo']#열차번호(현재운행하고 있는 호선별 열차번호)
                    ,'bstatnId': data['realtimeArrivalList'][num]['bstatnId']#종착지하철역ID
                    ,'recptnDt' : data['realtimeArrivalList'][num]['recptnDt']#열차도착정보를 생성한 시각
                    ,'arvlMsg2' : data['realtimeArrivalList'][num]['arvlMsg2']#첫번째도착메세지(전역 진입, 전역 도착 등)
                    ,'arvlMsg3' : data['realtimeArrivalList'][num]['arvlMsg3']#두번째도착메세지(종합운동장 도착, 12분 후 (광명사거리) 등)
                    ,'arvlCd' : data['realtimeArrivalList'][num]['arvlCd']#도착코드(0:진입, 1:도착, 2:출발, 3:전역출발, 4:전역진입, 5:전역도착, 99:운행중)
                    ,'subwayList' : data['realtimeArrivalList'][num]['subwayList']#연계호선ID(1002, 1007 등 연계대상 호상ID)
                    ,'statnList' : data['realtimeArrivalList'][num]['statnList']#연계지하철역ID(1002000233,1007000744)
                    ,'bstatnNm' : data['realtimeArrivalList'][num]['bstatnNm']} #종착지하철역명

                    response_data = response_data.append(data_list, ignore_index=True)
                return response_data

            elif data['errorMessage']['code'] == 'INFO-100': #인증키 오류
                print("Authentication key Error : INFO-100")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-500':  # 서버 오류
                print("Server key Error : INFO-500")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-200':  # 데이터 없음
                print("Data Error : INFO-200")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-301':  # request type error
                print("Request Type Error : INFO-301")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-310':  # Can't found Service error
                print("API can't found Service : INFO-310")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-331':  # start index error
                print("Start Index Error : INFO-331")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-332':  # End Index error
                print("End Index Error : INFO-332")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-333':  # request location type error (request location must be interger)
                print("Request location Type Error : INFO-333")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-334':  # start index > end index error
                print("Index Error : INFO-334")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-335':  # request sample data error (Max sample data num is 5)
                print("Request Sample Data Error : INFO-335")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-336':  # request data error (Can't call over 1000 request at once)
                print("Request Data Error : INFO-336")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-600':  # DB Connect error
                print("DB Connect Error : INFO-600")
                return response_data
            elif data['errorMessage']['code'] == 'INFO-601':  # SQL Sentence error
                print("SQL Sentence Error : INFO-601")
                return response_data
            else:
                print('Unexpected Error')
                return response_data
           # else :
           #     print("지하철 운영시간이 아닙니다.")
           #     return 0


    def check_train_is_avilable_time(self):
        #checktime
        load_time = time.datetime.now()
        hour = load_time.hour
        minute = load_time.minute
        second = load_time.second
        time_now = str(hour) + str(minute) + str(second)
        url = 'http://openapi.seoul.go.kr:8088/' + self.key + '/json/SearchFirstAndLastTrainbyLineServiceNew/1/5/02호선/1/1/ /' +self.station_code
        response = requests.get(url)
        data = json.loads(response.text)
        start_time = data['SearchFirstAndLastTrainbyLineServiceNew']['row'][0]['FIRST_TIME']
        end_time = data['SearchFirstAndLastTrainbyLineServiceNew']['row'][0]['LAST_TIME']
        if time_now <= end_time and time_now >= start_time:
            return True
        else:
            return False



def run() :
    image_data_set = load_image()
    determination = person_determination()

    #시연을 위한 random한 id(사진 인덱스)를 선택
    image_data_set.readBLOB(image_id = image_data_set.create_random_image_index(20))
    predict_image_path = './predict_tmp/'
    p_cnt_list = []
    p_cnt_list = np.append(p_cnt_list, my_detect(img = predict_image_path))

    #객차별 혼잡도 계산(2장씩 이용)
    congresion_list = determination.person_congresion_list(p_cnt_list)
    return congresion_list
