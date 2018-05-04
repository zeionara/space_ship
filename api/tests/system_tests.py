import unittest
import crud_test_cassandra as crud_test
from crud_test_cassandra import TestCrud

crud_test.SINGULAR = 'systemTest'
crud_test.PLURAL = 'systemTests'

crud_test.FIELDS_TO_SHOW = 'date,time,result'
crud_test.CHECKING_PARAM = 'result'

crud_test.FIRST_VALUE = 13
crud_test.SECOND_VALUE = 17

crud_test.CREATE_PARAMS = {'timestamp': "'2112-12-11 12:12:12'", 'system': "'000000000000000000000003'", 
	crud_test.CHECKING_PARAM: crud_test.FIRST_VALUE}
crud_test.UPDATE_PARAMS = {crud_test.CHECKING_PARAM: crud_test.SECOND_VALUE}

#http://localhost:1881/api/create/position/fields=ok,position(x)&where=timestamp:'2017-02-18%2023:59:57',x:10.0,y:10.2,z:10.3,speed:10.4,attackangle:10.5,directionangle:10.6
#http://localhost:1881/api/create/position/fields=position(timestamp,x,y,z)&where=timestamp:'2111-11-11%2012:12:12',x:1.0,y:1.0,z:1.0,speed:1.0,attackangle:1.0,directionangle:1.0


if __name__ == '__main__':
    unittest.main()