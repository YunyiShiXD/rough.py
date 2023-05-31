#coding=gbk
"""
    “为指定产品的物模型删去指定功能” 调用流程：
        client_ak_Info(access_key_id, access_key_secret)
        query_list_Info(IotInstanceId, ResourceGroupId, ProductKey)
        delete_thing_model(flag): flag=1 温度  =2 湿度  =3 光照
"""

from alibabacloud_iot20180120.client import Client as Iot20180120Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_iot20180120 import models as iot_20180120_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class DeleteThingModel:
    def __init__(self):
        pass

    @staticmethod
    # 删除物模型
    # 根据传入信息，创建AK用户
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Iot20180120Client:
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
        return Iot20180120Client(config)

    @staticmethod
    def delete_thing_model(access_key_id, access_key_secret, iot_instance_id,
                           resource_group_id, product_key, node_identifier):
        client = DeleteThingModel.create_client(access_key_id, access_key_secret)
        delete_thing_model_request = iot_20180120_models.DeleteThingModelRequest(
            iot_instance_id=iot_instance_id,
            resource_group_id=resource_group_id,
            product_key=product_key,
            function_block_id='test_module',
            # Array, 可选, 需要删除的属性标识符列表。最多传入10个属性标识符。
            property_identifier=[
                node_identifier
                # 'RunningState'  属性的标识符
            ]
        )
        runtime = util_models.RuntimeOptions()
        resp = client.delete_thing_model_with_options(delete_thing_model_request, runtime)
        print(UtilClient.to_jsonstring(resp))
