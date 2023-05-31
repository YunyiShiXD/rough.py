# coding=gbk
"""
    ��ָ����Ʒ��ע���豸��������
        client_ak_Info(access_key_id, access_key_secret)
        query_list_Info(IotInstanceId, ProductKey, DeviceName, Nickname)
        register_device()
"""

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_tea_util.client import Client as UtilClient

# �û�AK��Ϣ��ȫ�ֱ��������δ洢AccessKey ID & AccessKey Secret��Ϣ
user_ak_info_list = []

# ��ѯ������������δ洢IotInstanceId��ProductKey��DeviceName��Nickname
query_list = []


# �����û���AK��Ϣ
def client_ak_Info(access_key_id, access_key_secret):
    ak_info = str(access_key_id) + "," + str(access_key_secret)
    global user_ak_info_list    # ȫ�ֱ���
    user_ak_info_list = ak_info.split(",")


def query_list_Info(IotInstanceId, ProductKey, DeviceName, Nickname):
    query_info = str(IotInstanceId)  + "," + str(ProductKey) + "," + str(DeviceName) + "," + str(Nickname)
    global query_list    # ȫ�ֱ���
    query_list = query_info.split(",")
    print(query_list)


# ���ݴ�����Ϣ������AK�û�
def create_client(
    access_key_id: str,
    access_key_secret: str,
) -> OpenApiClient:
    """
            ʹ��AK&SK��ʼ���˺�Client
            @param access_key_id:
            @param access_key_secret:
            @return: Client
            @throws Exception
            """
    config = open_api_models.Config(
        # ������� AccessKey ID,
        access_key_id=access_key_id,
        # ������� AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # ���ʵ�����
    config.endpoint = f'iot.cn-shanghai.aliyuncs.com'
    return OpenApiClient(config)


# ����ָ����Ʒ��ע���豸����API�ӿ���Ϣ
def create_api_info() -> open_api_models.Params:
    """
    API ���
    @param path: params
    @return: OpenApi.Params
    """
    params = open_api_models.Params(
        # �ӿ�����,
        action='RegisterDevice',
        # �ӿڰ汾,
        version='2018-01-20',
        # �ӿ�Э��,
        protocol='HTTPS',
        # �ӿ� HTTP ����,
        method='POST',
        auth_type='AK',
        style='RPC',
        # �ӿ� PATH,
        pathname=f'/',
        # �ӿ����������ݸ�ʽ,
        req_body_type='formData',
        # �ӿ���Ӧ�����ݸ�ʽ,
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
    # �ɶ��û�������ʾ
    if "The device already exists." in outlog:
        return -1
    elif "The specified product does not exist." in outlog:
        return -2
    elif "The deviceName format is incorrect." in outlog:
        print("�豸���Ƴ���Ϊ4~32���ַ������԰���Ӣ����ĸ�����ֺ������ַ����̻��ߣ�-�����»��ߣ�_����at��@������Ǿ�ţ�.�������ð�ţ�:����")
    elif '"Success": true' in outlog:
        # ��outlog���ҳ� DeviceSecret
        start = outlog.find('"DeviceSecret": ') + len('"DeviceSecret": ')
        end = outlog.find(',', start)
        device_secret = outlog[start:end]
        # ����Ʒ & �豸��Ϣ����txt�ļ��б��棬�����ʽ�� ��Ʒ��:"DeviceName"+"DeviceSecret"
        with open('../__ali__device_and_node_infoTXT/device_info.txt', 'a+') as f:
            f.write(str(query_list[1]) + ':"' + str(query_list[2]) + '",' + device_secret + '\n')
        return 0
