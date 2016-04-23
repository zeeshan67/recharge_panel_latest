from django.db import models

# Create your models here.


class CreateUser(models.Model):
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email_id = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)
    address = models.CharField(max_length=30)

    def __repr__(self):
        return self.name
from recharge_panel_templates.config import Pool,operator_code_dict



def get_data(query_param):
    instance = Pool()
    print instance
    cursor = instance.db
    if query_param['query'] == 'recharge_data':
        where_clause = ''
        final_data = []
        sql_query = "select mobile_number,request_id,circle,operator_code,date_time,recharge_status,remark,balance,amount from recharge_reports where 1=1 " ;
        if query_param.get("event_start_date",''):
            where_clause += " and date_time >='%s'"%query_param['event_start_date']
        if query_param.get("event_end_date",''):
            where_clause += " and date_time <='%s'"%query_param['event_end_date']
        if query_param.get("search",""):
            where_clause += " and (request_id ilike '%"+(query_param['search'])+"%' or cast(mobile_number as varchar) ilike '%"+(query_param['search'])+"%') "
        final_clause = where_clause+" order by id desc limit %s offset %s"%(query_param['limit'],query_param['offset'])
        sql_query = sql_query+final_clause
        print sql_query
        cursor.execute(sql_query)
        records = cursor.fetchall()
        for list_value in records:
            date_time = str(list_value[4]).split('.')[0]
            # print list_value[5],list_value[6]
            operator = 'NA'
            if list_value[3]:
                operator = operator_code_dict.keys()[operator_code_dict.values().index(list_value[3])]
            final_data.append({"mobile_number":list_value[0],"request_id":list_value[1],
                               "circle":list_value[2],"operator":operator,"date_time":date_time,
                               "recharge_status":list_value[5],"remark":list_value[6],
                               "balance":str(list_value[7]),"amount":list_value[8]
                               })

        cursor.execute("select count(*) from recharge_reports where 1=1 "+where_clause)
        result = cursor.fetchone()
        total_record = 0
        for values in result:
            print values
            total_record= values
        return {"total_count":total_record,"final_data":final_data}
        # print records
    if query_param['query'] == 'dashboard_data':
        cursor.execute("select count(*),recharge_status from recharge_reports where recharge_status is not null group by recharge_status;")
        result = cursor.fetchall()
        total_success = 0
        total_count = 0
        for values in result:
            print values
            if values[1] == 'SUCCESS':
                total_success += values[0]
            total_count += values[0]
        return {"total_count":total_count,"total_success":total_success}