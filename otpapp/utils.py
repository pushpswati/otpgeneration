from django.conf import settings
from nextverpapp import  models
import random
import datetime,json
import requests
from django.utils import timezone
import http.client



def send_sms(mobile,msg):
    conn = http.client.HTTPConnection("api.msg91.com")
    msg="OTP is "+msg+" for www.synhealth.com login"
    #http://api.msg91.com/api/sendhttp.php?sender=MSGIND&route=4&mobiles=918553759008&authkey=207401AWsCJw5O5ac38535&country=91&message=Hello! This is a test message
    urlstr="/api/sendhttp.php?sender=SYNHLT&route=4&mobiles="+mobile+"&authkey=207401AWsCJw5O5ac38535&country=91&message="+msg
    conn.request("GET",urlstr )
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

class OTP(object):

    def __init__(self,customer):
        self.customer=customer

    def verify_otp(self,valid_otp):
        """
        :param customer:
        :return:
        """
        try:
            customer_otp=models.CustomerOtp.objects.get(customer=self.customer)
            created=customer_otp.created
            current_time=timezone.now()
            timedelta=(created-current_time).total_seconds()
            print("abs(timedelta/60)",abs(timedelta/60), customer_otp.is_verified)

            if abs(timedelta / 60) <= settings.OTP_EXPIRE_TIME and customer_otp.is_verified and customer_otp.otp==str(valid_otp):
                return "verified"

            if abs(timedelta/60)<=settings.OTP_EXPIRE_TIME and customer_otp.otp==str(valid_otp):

                customer_otp.is_verified=True
                customer_otp.save()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None


    def save_otp(self):
        """
        :param customer:
        :return:
        """
        otp="%0.4d" % random.randint(0,9999)
        try:
            customer_otp=models.CustomerOtp.objects.get(customer=self.customer)
            customer_otp.otp=otp
            customer_otp.is_verified=False
            customer_otp.created=datetime.datetime.now()
            customer_otp.save()
            mobile = str(self.customer.mobile)
            send_sms(mobile, str(otp))
            return otp
        except models.CustomerOtp.DoesNotExist as e:
            print(e)
        print("customer",self.customer)
        models.CustomerOtp.objects.create(customer=self.customer,otp=otp)
        mobile=str(self.customer.mobile)
        send_sms(mobile,str(otp))
        return otp




def payment_request(payload):
    headers = {"X-Api-Key": "4c0f35615931709e48258e266af5765f", "X-Auth-Token": "f4000559c5f32e0e6a954cb1196cfd26"}
    payload['purpose']='SynHealth'
    payload['redirect_url']='http://www.synhealth.com/payment/success'
    payload['send_email']=False
    payload['send_sms']=False
    payload['webhook']='http://35.197.74.144:8899/payment/webhook'
    payload['allow_repeated_payments']=False
    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
    #print(response.text)

    return json.loads(response.text)

