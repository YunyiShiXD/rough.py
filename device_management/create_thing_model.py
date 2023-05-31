"""
    “为指定产品的物模型增加功能” 调用流程：
        client_ak_Info(access_key_id, access_key_secret)
        query_list_Info(IotInstanceId, ResourceGroupId, ProductKey)
        create_thing_model(flag): flag=1 温度  =2 湿度  =3 光照
"""

from alibabacloud_iot20180120.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_tea_util.client import Client as UtilClient
import os

# 用户AK信息的全局变量：依次存储AccessKey ID & AccessKey Secret信息
user_ak_info_list = []

# 查询命令参数：依次存储IotInstanceId、ResourceGroupId、ProductKey
query_list = []


# 传入用户的AK信息
def client_ak_Info(access_key_id, access_key_secret):
    ak_info = str(access_key_id) + "," + str(access_key_secret)
    global user_ak_info_list  # 全局变量
    user_ak_info_list = ak_info.split(",")


def query_list_Info(IotInstanceId, ResourceGroupId, ProductKey):
    query_info = str(IotInstanceId) + "," + ResourceGroupId + "," + str(ProductKey)
    global query_list  # 全局变量
    query_list = query_info.split(",")


# 根据传入信息，创建AK用户
def create_client(
        access_key_id: str,
        access_key_secret: str,
) -> OpenApiClient:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @param region_id:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = f'iot.cn-shanghai.aliyuncs.com'
    return OpenApiClient(config)


def create_api_info() -> open_api_models.Params:
    """
    API 相关
    @param path: params
    @return: OpenApi.Params
    """
    params = open_api_models.Params(
        # 接口名称,
        action='CreateThingModel',
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


# 设置产品的物模型属性：1 增加温度属性； 2 增加湿度属性； 3 增加光照属性
def create_thing_model(flag):
    client = create_client(user_ak_info_list[0], user_ak_info_list[1])
    params = create_api_info()
    # query params
    queries = {}
    queries['IotInstanceId'] = query_list[0]
    queries['ProductKey'] = query_list[2]

    # 导入产品物模型的JSON文件
    """
            1、 判断设置的物模型属性，对”模块ID和名称“进行命名
            2、 用txt文件分别存储已添加的设备次序，以便命名操作
                  注：txt文件用a+模式，即追加模式
    """
    # 新增温度属性
    if flag == 1:
        # 温度属性 Name 由前端获取用户命名
        # 温度属性 Identifer 命名
        IdentifierFlag = 0
        file_path = os.path.join(os.path.dirname(__file__), '..', '__ali__device_and_node_infoTXT', 'Temp_node_Identifier.txt')
        with open(file_path, 'r') as file:
            data = file.read()
            while True:
                if str(IdentifierFlag) not in data:
                    with open(file_path, 'a+') as f:
                        f.write(str(IdentifierFlag) + ' ')
                        break
                else:
                    IdentifierFlag += 1
                    print(IdentifierFlag)
        queries['ThingModelJson'] = '''{
        "productKey": "%s",
        "properties": [
            {
                "custom": true,
                "identifier": "test_%s",
                "name": "tempNode_%s",
                "rwFlag": "READ_WRITE",
                "desc": "显示节点温度数据",
                "required": false,
                "productKey": "%s",
                "dataType": "FLOAT",
                "dataSpecs": {
                    "custom": true,
                    "dataType": "FLOAT",
                    "max": "50.00",
                    "min": "-20.00",
                    "step": "0.01",
                    "unit": "/°C",
                    "unitName": "摄氏度"
                }
            }
        ]
    }''' % (query_list[2], str(IdentifierFlag), str(IdentifierFlag), query_list[2])

    # 新增湿度属性
    if flag == 2:
        # 湿度属性 Name 由前端获取用户命名
        # 湿度属性 Identifer 命名
        IdentifierFlag = 0
        file_path = os.path.join(os.path.dirname(__file__), '..', '__ali__device_and_node_infoTXT', 'Humi_node_Identifier.txt')
        with open(file_path, 'r') as file:
            data = file.read()
            while True:
                if str(IdentifierFlag) not in data:
                    with open(file_path, 'a+') as f:
                        f.write(str(IdentifierFlag) + ' ')
                        break
                else:
                    IdentifierFlag += 1
                    print(IdentifierFlag)
        queries['ThingModelJson'] = '''{
                "productKey": "%s",
                "properties": [
                    {
                        "custom": true,
                        "identifier": "test_%s",
                        "name": "humiNode_%s",
                        "rwFlag": "READ_WRITE",
                        "desc": "显示节点湿度数据",
                        "required": false,
                        "productKey": "%s",
                        "dataType": "FLOAT",
                        "dataSpecs": {
                            "custom": true,
                            "dataType": "FLOAT",
                            "max": "100.00",
                            "min": "0.00",
                            "step": "0.01",
                            "unit": "%%RH",
                            "unitName": "相对湿度"
                        }
                    }
                ]
            }''' % (query_list[2], str(IdentifierFlag), str(IdentifierFlag), query_list[2])

    # 新增光照属性
    if flag == 3:
        # 光照属性 Name 由前端获取用户命名
        # 湿度属性 Identifer 命名
        IdentifierFlag = 0
        file_path = os.path.join(os.path.dirname(__file__), '..', '__ali__device_and_node_infoTXT', 'Light_node_Identifier.txt')
        with open(file_path, 'r') as file:
            data = file.read()
            while True:
                if str(IdentifierFlag) not in data:
                    with open(file_path, 'a+') as f:
                        f.write(str(IdentifierFlag) + ' ')
                        break
                else:
                    IdentifierFlag += 1
                    print(IdentifierFlag)
        queries['ThingModelJson'] = '''{
                "productKey": "%s",
                "properties": [
                    {
                        "custom": true,
                        "identifier": "test_%s",
                        "name": "lightNode_%s",
                        "rwFlag": "READ_WRITE",
                        "desc": "显示节点光照数据",
                        "required": false,
                        "productKey": "%s",
                        "dataType": "FLOAT",
                        "dataSpecs": {
                            "custom": true,
                            "dataType": "FLOAT",
                            "max": "50.00",
                            "min": "-20.00",
                            "step": "0.01",
                            "unit": "/°C",
                            "unitName": "摄氏度"
                        }
                    }
                ]
            }''' % (query_list[2], str(IdentifierFlag), str(IdentifierFlag), query_list[2])

    queries['FunctionBlockId'] = 'nodeDatums'
    queries['FunctionBlockName'] = '传感节点数据'
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

    # 如果产品已发布，则先取消发布
    if "An error occurred. The product has been published." in outlog:
        print("An error occurred")
        return None
