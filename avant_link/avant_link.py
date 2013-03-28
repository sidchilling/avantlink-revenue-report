'''avant_link: Python library to extract revenue data from AvantLink
'''

__version__ = '1.0'
__author__ = 'Siddharth Saha (sidchilling@gmail.com)'

import requests
import xml.etree.ElementTree as ET

class AvantLink(object):
    
    BASE_URL = 'https://www.avantlink.com/api.php'

    affiliate_id = ''
    auth_key = ''
    
    # Some private variables pre-set
    _module = 'AffiliateReport'
    _output = 'xml'
    _report_id = 1

    def __init__(self, affiliate_id, auth_key):
	assert affiliate_id and auth_key, 'missing args'
	self.affiliate_id = affiliate_id
	self.auth_key = auth_key
    
    def _make_params(self, start_date, end_date):
	# This method make the params dict to be sent with the request
	return {
		'date_begin' : start_date.strftime('%Y-%m-%d %H:%M:%S'),
		'date_end' : end_date.strftime('%Y-%m-%d %H:%M:%S'),
		'auth_key' : self.auth_key,
		'module' : self._module,
		'output' : self._output,
		'report_id' : self._report_id,
		'affiliate_id' : self.affiliate_id,
		'auth_key' : self.auth_key
	       }
    
    def _return_in_cents(self, amount):
	# This method returns an amount in the format $10.45 and returns in cents
	return int(float(amount[1:]) * 100)

    def _make_merchant_dict(self, merchant):
	# This makes the merchant dict for a merchant
	return {
		'ad-impressions' : int(merchant.find('Ad_Impressions').text),
		'click-throughs' : int(merchant.find('Click_Throughs').text),
		'sales' : self._return_in_cents(amount = merchant.find('Sales').text),
		'number-of-sales' : int(merchant.find('Number_of_Sales').text),
		'commissions' : self._return_in_cents(amount = \
			merchant.find('Commissions').text),
		'incentives' : self._return_in_cents(amount = \
			merchant.find('Incentives').text),
		'number-of-adjustments' : merchant.find('Number_of_Adjustments').text,
		'conversion-rate' : merchant.find('Conversion_Rate').text,
		'30-day-network-conversion-rate' : merchant.find('_30_day_Network_Conversion_Rate').text,
		'average-sale-amount' : self._return_in_cents(amount = \
			merchant.find('Average_Sale_Amount').text),
		'click-through-rate' : merchant.find('Click_Through_Rate').text,
		'cpc-earnings' : self._return_in_cents(amount = \
			merchant.find('CPC_Earnings').text),
		'ecpm' : self._return_in_cents(amount = merchant.find('eCPM').text),
		'epc' : self._return_in_cents(amount = merchant.find('EPC').text),
		'total-commissions-earnings' : self._return_in_cents(amount = \
			merchant.find('Total_Commissions_Earnings').text)
	       }

    def get(self, start_date, end_date):
	'''This method gets the data and returns a revenue report
	'''
	assert start_date and end_date, 'missing args'
	r = requests.get(url = self.BASE_URL, params = \
		self._make_params(start_date = start_date, end_date = end_date))
	if r.ok:
	    tree = ET.fromstring(r.content)
	    res = {} # This is the return dict
	    for merchant_table in tree.findall('Table1'):
		res[merchant_table.find('Merchant').text] = self._make_merchant_dict(merchant = \
			merchant_table)
	    return res
	else:
	    raise Exception('Cannot connect to AvantLink')


