#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFSTEST.PY

Created on Wed Jun 15 07:49:39 2022

@author: hudsonnash

OBJECTIVE: Test Cloudflare DDOS circumvention method.
"""

import cfscrape
import sys

scraper = cfscrape.create_scraper() # returns a requests.Session object
fd = open("cookie.txt", "w")
c = cfscrape.get_cookie_string("https://www.coa.gov.ph/reports/annual-audit-reports/aar-local-government-units/")
fd.write(str(c))
fd.close()  
print(c)

'''
Solution: Handle the JS puzzle in JavaScript. Max Gerhardt uses .NET with C# to work with Cloudflare's DDOS puzzle: https://stackoverflow.com/questions/32425973/how-can-i-get-html-from-page-with-cloudflare-ddos-portection
'''