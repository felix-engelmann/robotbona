from django.urls import path

app_name = 'common'

from .views import getToken
#from .app_views import initSoft, checkVersion, login, userInfo, robotList, getRecord, upload, defaultRobot

urlpatterns = [
    # url(r'^', include('django.contrib.auth.urls')),
    path('common/getToken.do', getToken, name="getToken"),
    #path('common/initSoft.do', initSoft, name="initSoft"),
    #path('common/uploadLog.do', upload, name="logging"),
    #path('common/checkNewVersion.do', checkVersion, name="checkVersion"),
    #path('common/login.do', login, name="login"),
    #path('personal/getUserInfo.do', userInfo, name="userInfo"),
    #path('index/getMyDefaultRobotInfo.do', defaultRobot, name="defaultRobot"),
    #path('robot/getMyRobotList.do', robotList, name="robotList"),
    #path('robot/getRobotClearRecordInfo.do', getRecord, name="getRecord"),
]
