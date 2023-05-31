"""
    TPC��ʽ����MQTT���ӣ�����豸�ڰ����Ƶ� ���ߣ�
       mqtt_connect_TCP((product_key, device_name, device_secret)
"""
from linkkit import linkkit
import time
import logging
import deviceLogInfo.deviceLogInfo as logInfo

# config log
__log_format = '%(asctime)s-%(process)d-%(thread)d - %(name)s:%(module)s:%(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(format=__log_format)


def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)


def UserID_get(user):
    global UserID
    UserID = user


def mqtt_connect_TCP(product_key, device_name, device_secret):
    lk = linkkit.LinkKit(
        host_name="cn-shanghai",
        product_key=product_key,
        device_name=device_name,
        device_secret=device_secret)
    lk.enable_logger(logging.DEBUG)
    lk.on_disconnect = on_disconnect
    lk.config_mqtt(secure="")
    lk.connect_async()
    linkkitstate = lk.check_state()
    while linkkitstate == lk.LinkKitState.CONNECTING:
        # �豸�ƶ����ߺ󣬼����ڱ����ռ���
        # �˴���Ҫ���ǰ���û�ID��Ϣ
        logInfo.node_log_Saved(UserID, )
        time.sleep(5)
        while linkkitstate != lk.LinkKitState.CONNECTING:
            mqtt_connect_TCP(product_key, device_name, device_secret)
            break
