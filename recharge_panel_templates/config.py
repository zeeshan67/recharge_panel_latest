__author__ = 'verna'
import psycopg2

post_url = "http://localhost:8003/api/user_recharge"
operator_code_dict = {
                      "airtel_postpaid": 35,
                      "aircel_postpaid": 94,
                      "bsnl_postpaid": 36,
                      "vodafone_postpaid": 33,
                      "reliance_gsm_postpaid": 34,
                      "reliance_cdma_postpaid": 26,
                      "idea_postpaid": 42,
                      "tata_docomo_postpaid": 49,
                      "mts_postpaid": 38,
                      "loop_postpaid": 48,
                      "airtel_prepaid": 1,
                      "aircel_prepaid": 11,
                      "uninor_prepaid": 12,
                      "uninor_special_prepaid": 46,
                      "mts_prepaid": 16,
                      "vodafone_prepaid": 5,
                      "reliance_gsm_prepaid": 3,
                      "bsnl_prepaid": 2,
                      "reliance_cdma_prepaid": 29,
                      "tata_docomo_prepaid": 13,
                      "idea_prepaid": 4,
                      "loop_prepaid": 7,
                      "videocon_prepaid": 14,
                      "videocon_special_prepaid": 30,
                      "virgin_cdma_prepaid": 28,
                      "virgin_gsm_prepaid": 27,
                      "virgin_gsm__special_prepaid": 95,
                      "mtnl_prepaid": 8,
                      "mtnl_dl_special_prepaid": 55,
                      "mtnl_dl_topup_prepaid": 54,
                      "mtnl_mumbai_special_prepaid": 57,
                      "mtnl_mumbai_topup_prepaid": 56
                      }

class SingletonPool(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonPool, cls).__call__(*args, **kwargs)
            return cls.__instance

class Pool():
    __metaclass__ = SingletonPool
    cursor = None

    @property
    def db(self):
        if not self.cursor:
            try:
                conn=psycopg2.connect("host='localhost' dbname='recharge_db' user='postgres' password='root'")
                self.cursor = conn.cursor()
            except Exception as exc:
                print "I am unable to connect to the database. %s"%exc.message
        return self.cursor
