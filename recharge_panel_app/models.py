from django.db import models
from recharge_panel_templates.config import Pool,operator_code_dict

# Create your models here.


class CreateUser(models.Model):
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    email_id = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    user_role = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    credit_assigned = models.FloatField()
    credit_used = models.FloatField()
    credit_available = models.FloatField()
    credit = models.FloatField()
    parent_id = models.IntegerField()

    # def __repr__(self):
    #     return self.user_name

    class Meta:
        db_table = 'user_master'

def get_data(query_param):
    instance = Pool()
    print instance
    cursor = instance.db
    if query_param['query'] == 'recharge_data':
        where_clause = ''
        final_data = []
        #cursor.execute("SET time zone 'Asia/Calcutta';")
        sql_query = "select mobile_number,request_id,circle,operator_code,date_time ::timestamp AT TIME ZONE 'Asia/Kolkata',recharge_status,remark,balance,amount from recharge_reports where 1=1 " ;
        if query_param.get("event_start_date",''):
            where_clause += " and date_time >='%s'"%query_param['event_start_date']
        if query_param.get("event_end_date",''):
            where_clause += " and date_time <='%s'"%query_param['event_end_date']
        if query_param.get("search",""):
            where_clause += " and (request_id ilike '%"+(query_param['search'])+"%' or cast(mobile_number as varchar) ilike '%"+(query_param['search'])+"%') "
        if query_param.get('user_role',0) and query_param.get('user_role',0) != 'admin':
            where_clause += " and user_id=%s"%int(query_param.get('user_id',0))
        if query_param.get('user_role',0) and query_param.get('user_role',0) == 'distributor':
            where_clause += " or parent_id=%s"%int(query_param.get('user_id',0))
        if query_param.get('user_role',0) and query_param.get('user_role',0) == 'admin' and query_param.get('selected_user_id',''):
            where_clause += " and user_id in (select id from user_master where id = %s or parent_id=%s)"%(int(query_param['selected_user_id']),int(query_param['selected_user_id']))
        final_clause = where_clause+" order by id desc limit %s offset %s"%(query_param['limit'],query_param['offset'])
        sql_query = sql_query+final_clause
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
        where_clause = 'select count(*),recharge_status from recharge_reports where recharge_status is not null'
        if query_param.get('user_role',0) and query_param.get('user_role',0) != 'admin':
            where_clause += " and user_id=%s"%int(query_param.get('user_id',0))
        cursor.execute("%s group by recharge_status;"%where_clause)
        result = cursor.fetchall()
        total_success = 0
        total_count = 0
        total_balance = 0
        print query_param.get('user_id',0)
        for values in result:
            print values
            if values[1] == 'SUCCESS':
                total_success += values[0]
            total_count += values[0]
        cursor.execute("select credit_assigned,credit_available from user_master where id = %s"%int(query_param.get('user_id',0)))
        for iterate_values in cursor.fetchall():
            total_credit = iterate_values[0]
            total_balance = iterate_values[1]
        return {"total_count":total_count,"total_success":total_success,"total_balance":total_balance,"total_credit":total_credit}

def verify_user(**kwargs):
    instance = Pool()
    cursor = instance.db
    cursor.execute("select user_role,credit_used,credit_available,id,parent_id from user_master where active=True and user_name='%s' and password = '%s'"%(kwargs['username'],kwargs['password']))
    result = cursor.fetchall()
    for values in result:
        print values
        return {"is_verified":1,"role":values[0],"credit_used":values[1],"credit_available":values[2],"user_id":values[3],'parent_id':values[4]}
    return  {"is_verified":0,"role":'guest'}

def get_user_credits(user_id):
    instance = Pool()
    cursor = instance.db
    cursor.execute("select credit_used,credit_available from user_master where active=True and id=%s"%(user_id))
    result = cursor.fetchall()
    for values in result:
        print values
        return {"credit_used":values[0],"credit_available":values[1]}
    return {"credit_used":0,"credit_available":0}

def check_user_exists(query_param):
    instance = Pool()
    cursor = instance.db
    cursor.execute("select id from user_master where user_name = '%s' ;"%query_param['user_name'])
    result = cursor.fetchall()
    for values in result:
        return {"is_exists":1}
    return {"is_exists":0}



def get_list_of_user(query_param):
    try:
        instance = Pool()
        cursor = instance.db
        cursor.execute("select id,user_name from user_master where user_role in ('admin','distributor') order by id asc; ")
        result = cursor.fetchall()
        user_list = []
        for values in result:
            user_list.append({str(values[0]):str(values[1])})
        return user_list
    except Exception as exc:
        print "XXXXXXXXXXXXXXXXXXX%s"%exc.message
    return []

def get_user_name(query_param):

    try:
        print(query_param)
        instance = Pool()
        cursor = instance.db
        print(cursor)
        cursor.execute("select user_name from user_master where id=%s"%int(query_param['parent_id']))
        result = cursor.fetchall()
        for values in result:
            return {"user_name":values[0]}
    except Exception as exc:
        print "XXXXXXXXXXXXXXXXXXX%s"%exc.message
    return {}
