import psycopg2
from contextlib import closing
import datetime

class model():  # (DB,DB_USER,DB_HOST,DB_PW):
    def __init__(self, DB, DB_USER, DB_HOST, DB_PW):
        self.DB = DB
        self.DB_USER = DB_USER
        self.DB_HOST = DB_HOST
        self.DB_PW = DB_PW


    def curator_request(self, mag_number):
        with closing(psycopg2.connect(dbname=self.DB, user=self.DB_USER,
                                      password=self.DB_PW,
                                      host=self.DB_HOST)) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT mag_name, curator_name, grade, mail, phone FROM public.all_crs WHERE mag_number = %(mag_number)s',{'mag_number': mag_number})
                if cursor != 0:
                    for row in cursor:
                        a = row
                        b = '{0}{1}{2}{3}{4}{5}{6}{7}'.format('Магазин: ', a[0], '\nКуратор: ', a[1], '\nПочта:   ', a[3], '\nТелефон: ', a[4])
                        return b
        del conn

    def reg_curator_request(self, region):
        with closing(psycopg2.connect(dbname=self.DB, user=self.DB_USER,
                                      password=self.DB_PW,
                                      host=self.DB_HOST)) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT mag_name, curator_name, grade, mail, phone FROM public.reg_crs WHERE region = %(region)s', {'region': region})
                if cursor != 0:
                    for row in cursor:
                        a = row
                        b = '{0}{1}{2}{3}{4}{5}{6}{7}'.format('Магазин: ', a[0] ,'\nКуратор: ' , a[1] , '\nПочта:   ' , a[3] , '\nТелефон: ' , a[4])
                        return b
        del conn


    def get_curator(self, mag_number):
        if self.curator_request(mag_number):
            return self.curator_request(mag_number)
        else:
            b = ('Куратор не найден:(\nПожалуйста, проверь корректность отправленного номера магазина.')
            return b

    def get_reg_curator(self, mag_number):
        if self.curator_request(mag_number):
            return self.curator_request(mag_number)
        else:
            b = ('Куратор не найден:(\nПожалуйста, проверь корректность отправленного номера магазина.')
            return b

    def event(self, recepient_id, event, eventparam = 'NULL'):
        with closing(psycopg2.connect(dbname=self.DB, user=self.DB_USER,
                                      password=self.DB_PW,
                                      host=self.DB_HOST)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO public.botstatistic(recepient_id, event, eventparam, datetime) VALUES (%s, %s, %s, %s);',
                    (recepient_id, event, eventparam, datetime.date.today()))
                conn.commit()
        del conn
        return 'success'