__author__ = 'verna'
import psycopg2

post_url = "http://localhost:8003/api/user_recharge"
operator_code_dict = {
                    "airtel_postpaid":35,
                    "aircel_postpaid":94,
                    "bsnl_postpaid":36,
                    "vodafone_postpaid":33,
                    "reliance_gsm_postpaid":34,
                    "reliance_cdma_postpaid":26,
                    "idea_postpaid":42,
                    "tata_docomo_postpaid":49,
                    "mts_postpaid":38,
                    "airtel_prepaid":1,
                    "aircel_prepaid":13,
                    "uninor_prepaid":12,
                    "mts_prepaid":16,
                    "vodafone_prepaid":14,
                    "reliance_gsm_prepaid":3,
                    "bsnl_prepaid":2,
                    "reliance_cdma_prepaid":29,
                    "tata_docomo_prepaid":13,
                    "idea_prepaid":4,
}


class Pool():
    _instance = None
    cursor = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Pool, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    @property
    def db(self):
        if not self.cursor:
            try:
                conn=psycopg2.connect("host='localhost' dbname='recharge_db' user='postgres' password='root'")
                self.cursor = conn.cursor()
            except Exception as exc:
                print "I am unable to connect to the database. %s"%exc.message
        return self.cursor
