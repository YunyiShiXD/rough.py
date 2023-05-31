# coding=gbk
"""
    在指定产品下注册设备调用流程
        client_ak_Info(access_key_id, access_key_secret)
        query_list_Info(IotInstanceId, ProductKey, DeviceName, Nickname)
        register_device()
"""

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_tea_util.client import Client as UtilClient

# 用户AK信息的全局变量：依次存储AccessKey ID & AccessKey Secret信息
user_ak_info_list = []

# 查询命令参数：依次存储IotInstanceId、ProductKey、DeviceName、Nickname
query_list = []


# 传入用户的AK信息
def client_ak_Info(access_key_id, access_key_secret):
    ak_info = str(access_key_id) + "," + str(access_key_secret)
    global user_ak_info_list    # 全局变量
    user_ak_info_list = ak_info.split(",")


def query_list_Info(IotInstanceId, ProductKey, DeviceName, Nickname):
    query_info = str(IotInstanceId)  + "," + str(ProductKey) + "," + str(DeviceName) + "," + str(Nickname)
    global query_list    # 全局变量
    query_list = query_info.split(",")
    print(query_list)


# 根据传入信息，创建AK用户
def create_client(
    access_key_id: str,
    access_key_secret: str,
) -> OpenApiClient:
    """
            使用AK&SK初始化账号Client
            @param access_key_id:
            @param access_key_secret:
            @return: Client
            @throws Exception
            """
    config = open_api_models.Config(
        # 必填，您的 AccessKey ID,
        access_key_id=access_key_id,
        # 必填，您的 AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = f'iot.cn-shanghai.aliyuncs.com'
    return OpenApiClient(config)


# “在指定产品下注册设备”的API接口信息
def create_api_info() -> open_api_models.Params:
    """
    API 相关
    @param path: params
    @return: OpenApi.Params
    """
    params = open_api_models.Params(
        # 接口名称,
        action='RegisterDevice',
        # 接口版本,
        version='2018-01-20',
        # 接口协议,
        protocol='HTTPS',
        # 接口 HTTP 方法,
        method='POST',
        auth_type='AK',
        style='RPC',
        # 接口 PATH,
        pathname=f'/',
        # 接口请求体内容格式,
        req_body_type='formData',
        # 接口响应体内容格式,
        body_type='json'
    )
    return params


def register_device():
    client = create_client(user_ak_info_list[0], user_ak_info_list[1])
    params = create_api_info()

    # query params
    queries = {}
    queries['IotInstanceId'] = query_list[0]
    queries['ProductKey'] = query_list[1]
    queries['DeviceName'] = query_list[2]
    queries['Nickname'] = query_list[3]

    # body params
    body = {}
    body['ApiProduct'] = None
    body['ApiRevision'] = None
    # runtime options
    runtime = util_models.RuntimeOptions()
    request = open_api_models.OpenApiRequest(
        query=OpenApiUtilClient.query(queries),
        body=body
    )
    resp = client.call_api(params, request, runtime)
    outlog = UtilClient.to_jsonstring(resp)
    print(outlog)
    # 可对用户进行提示
    if "The device already exists." in outlog:
        return -1
    elif "The specified product does not exist." in outlog:
        return -2
    elif "The deviceName format is incorrect." in outlog:
        print("设备名称长度为4~32个字符，可以包含英文字母、数字和特殊字符：短划线（-）、下划线（_）、at（@）、半角句号（.）、半角冒号（:）。")
    elif '"Success": true' in outlog:
        # 从outlog中找出 DeviceSecret
        start = outlog.find('"DeviceSecret": ') + len('"DeviceSecret": ')
        end = outlog.find(',', start)
        device_secret = outlog[start:end]
        # 将产品 & 设备信息存入txt文件中保存，输出格式： 产品名:"DeviceName"+"DeviceSecret"
        with open('../__ali__device_and_node_infoTXT/device_info.txt', 'a+') as f:
            f.write(str(query_list[1]) + ':"' + str(query_list[2]) + '",' + device_secret + '\n')
        return 0
