# This is the test file to testing the library

from avant_link import AvantLink
from pprint import pprint

if __name__ == '__main__':
    avant_link = AvantLink(affiliate_id = '<YOUR-AFFILIATE-ID>', 
	    auth_key = '<YOUR-AUTH-KEY>')
    from datetime import datetime
    start_date = datetime.strptime('2013-02-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime('2013-03-25 23:59:59', '%Y-%m-%d %H:%M:%S')
    print 'start_date: %s' %(start_date.strftime('%Y-%m-%d %H:%M:%S'))
    print 'end_date: %s' %(end_date.strftime('%Y-%m-%d %H:%M:%S'))
    pprint(avant_link.get(start_date = start_date, end_date = end_date))
