import requests
from django.conf import settings



def send_single_sms(apikey,code,mobile):
    """
    发送单条短信-云片网
    :param apikey:
    :param mobile:
    :param code:
    :return:
    """
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    text = '【杜俊通】您的验证码是{}'.format(code)

    res = requests.post(url,data={
        'apikey':apikey,
        'mobile':mobile,
        'text':text
    })

    result = res.json()
    return result

if __name__ == '__main__':

    result = send_single_sms('de6b3f7745bfb241d943fcb9c13127b4','1234','13714160953')
    print(result)