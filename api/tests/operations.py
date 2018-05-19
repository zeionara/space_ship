import unittest
import crud_test_neo4j as crud_test
from crud_test_neo4j import TestCrud

crud_test.SINGULAR = 'operation'
crud_test.PLURAL = 'operations'

crud_test.FIELDS_TO_SHOW = 'id,start,end,head(id)'
crud_test.CHECKING_PARAM = 'head'

crud_test.FIRST_VALUE = '000000000000000000000002'
crud_test.SECOND_VALUE = '000000000000000000000007'

crud_test.CREATE_PARAMS = {'name': "'Prometheus'", 'start': "'2012-12-12%2013:59:12'", 'end': "'2013-12-12%2013:59:12'",
	'executors': "'000000000000000000000001,000000000000000000000002,000000000000000000000003'", 'requirements':"'00000000000000000000000000000001'",
 	crud_test.CHECKING_PARAM: '\'' + crud_test.FIRST_VALUE + '\''}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: '\'' + crud_test.SECOND_VALUE + '\''}

if __name__ == '__main__':
    unittest.main()