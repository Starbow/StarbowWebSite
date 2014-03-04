import json


def dictfetchall(cursor):
    """ Returns all rows from a cursor as a dict """
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class DatatableQuery(object):
    """
    Requires additional post args:
        dimensions are used for GROUP BY
        observations are used for selecting columns

    Must implement:
      * `COLUMN_LOOKUP`
      * `def tables(self, params)`

    You may optionally implement:
      * `def where(self, params)`
    """
    @property
    def COLUMN_LOOKUP(self):
        raise NotImplementedError()

    def tables(self, params):
        raise NotImplementedError()

    def where(self, params):
        return "1=1"

    def __init__(self, args):
        self.args = args
        self.dimensions = []
        self.observations = []
        if self.args.get('dimensions', False):
            self.dimensions = self.args['dimensions'].split(',')
        if self.args.get('observations', False):
            self.observations = self.args['observations'].split(',')
        self.columns = self.dimensions + self.observations

    def execute(self, cursor):
        # Construct the standard query parts based on the requested dimensions/observations
        groupby, countColumn, countby = "", "*", ""
        if self.dimensions:
            groupby = 'GROUP BY ' + ', '.join(self.dimensions)
            countColumn = 'distinct '+self.dimensions[-1]
            if self.dimensions[:-1]:
                countby = 'GROUP BY ' + ', '.join(self.dimensions[:-1])

        # Assemble the basic seach terms and params
        basicParams = list()
        select = ', '.join(self.COLUMN_LOOKUP[column] for column in self.columns)
        tables = self.tables(basicParams)
        where = self.where(basicParams)

        # Assemble the terms and params required for filtering
        filterParams = list(basicParams)
        orderby = self.orderby(filterParams)
        limitby = self.limitby(filterParams)
        filterby = self.filterby(filterParams)

        # Get the filtered results
        filtered_query_template = "SELECT SQL_CALC_FOUND_ROWS {} FROM {} WHERE {} AND {} {} {} {}"
        filtered_query = filtered_query_template.format(select, tables, where, filterby, groupby, orderby, limitby)
        cursor.execute(filtered_query, filterParams)
        data = [[row[c] for c in self.columns] for row in dictfetchall(cursor)]

        # Get the total number of filtered rows
        cursor.execute("SELECT FOUND_ROWS()")
        filtered_total = cursor.fetchone()[0]

        # Get the total number of possible results
        counting_query_template = "SELECT count({}) FROM {} WHERE {} {}"
        counting_query = counting_query_template.format(countColumn, tables, where, countby)
        cursor.execute(counting_query, basicParams)
        counting_total = cursor.fetchone()[0]

        # Format the results for datatable's consumptions
        return json.dumps(dict(
            sEcho=int(self.args['sEcho']),
            iTotalRecords=counting_total,
            iTotalDisplayRecords=filtered_total,
            aaData=data
        ))

    def filterby(self, params):
        filterRules = list()

        # Create terms for global search parameters
        searchString = self.args.get('sSearch', "")
        if searchString != "":
            for i, columnName in enumerate(self.columns):
                if self.args.get('bSearchable_{}'.format(i), False) == 'true':
                    filterRules.append("{} LIKE %s".format(columnName))
                    params.append('%{}%'.format(searchString))
            if filterRules:
                filterRules = ['({})'.format(' OR '.join(filterRules))]

        # Create terms for column specific paramters
        for i, columnName in enumerate(self.columns):
            searchable = self.args.get('bSearchable_'.format(i), False) == 'true'
            searchString = self.args.get('sSearch_{}'.format(i), "")
            if searchable and searchString != "":
                filterRules.append("{} LIKE %s".format(columnName))
                params.append('%{}%'.format(searchString))

        # return 1=1 by default so that where AND filterby is valid no matter what
        return " AND ".join(filterRules) if filterRules else "1=1"

    def orderby(self, params):
        orderRules = list()
        if 'iSortingCols' in self.args:
            for i in range(int(self.args['iSortingCols'])):
                sortColumn = int(self.args['iSortCol_{}'.format(i)])
                if self.args.get('bSortable_{}'.format(sortColumn), False) == 'true':
                    # Don't trust the user input on the sort direction here.
                    sortDir = self.args.get('sSortDir_{}'.format(i), False)
                    sortDir = ("ASC" if sortDir == 'asc' else "DESC")
                    rule = "{} {}".format(self.columns[sortColumn], sortDir)
                    orderRules.append(rule)

        return " ORDER BY "+", ".join(orderRules) if orderRules else ""

    def limitby(self, params):
        limitby = ""
        if 'iDisplayStart' in self.args and self.args['iDisplayLength'] != "-1":
            # Casting to an int makes these args safe for query construction
            offset = int(self.args['iDisplayStart'])
            length = int(self.args['iDisplayLength'])
            limitby = " LIMIT {}, {}".format(offset, length)
        return limitby
