from collections import namedtuple
from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def custom_sql_get_dict(sql_cmd):
    with connection.cursor() as cursor:
        cursor.execute(sql_cmd)
        #cursor.fetchall()
        #print(cursor.fetchall())
        querydict = dictfetchall(cursor)

    return querydict


def custom_sql_get_tuple(sql_cmd):
    with connection.cursor() as cursor:
        cursor.execute(sql_cmd)
        cursor.fetchall()
        querytuple = namedtuplefetchall(cursor)

    return querytuple
# >>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2")
# >>> cursor.fetchall()
# ((54360982, None), (54360880, None))
#
# >>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2")
# >>> dictfetchall(cursor)
# [{'parent_id': None, 'id': 54360982}, {'parent_id': None, 'id': 54360880}]
#
# >>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2")
# >>> results = namedtuplefetchall(cursor)
# >>> results
# [Result(id=54360982, parent_id=None), Result(id=54360880, parent_id=None)]
# >>> results[0].id
# 54360982
# >>> results[0][0]
# 54360982