
def dictfetchall(cursor):
    """ Returns all rows from a cursor as a dict """
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
