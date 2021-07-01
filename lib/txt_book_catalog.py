import base64
import re

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

from lib.util import Utils
from lib import config


def extract_image(txt_path, image_path):
    """
    ocr 提取图片中的文字转换为bookmarks
    :param txt_path:
    :param image_path:
    :return:
    """
    try:
        secret_id = config.get('tencent.api.secretId')
        secret_key = config.get('tencent.api.secretKey')
        cred = credential.Credential(secret_id, secret_key)

        http_profile = HttpProfile()
        http_profile.endpoint = "ocr.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", client_profile)

        req = models.GeneralBasicOCRRequest()

        with open(image_path, "rb") as f:
            base64_data = base64.b64encode(f.read())

        req.ImageBase64 = str(base64_data, encoding="utf-8")
        resp = client.GeneralBasicOCR(req)

        for text in resp.TextDetections:

            if re.fullmatch('[.0-9]+', text.DetectedText):
                line = "@" + text.DetectedText.replace('.', '') + "\n"
            else:
                line = text.DetectedText
            Utils.write_file(txt_path, line, 'a+')
    except TencentCloudSDKException as err:
        print(err)


# if __name__ == '__main__':
#     list_files = Utils.list_files("../output/images", [".png"])
#
#     for file in list_files:
#         print(file)
#         extract_image('../output/软件产品架构师手记2.txt', file)
