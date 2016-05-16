
import urllib

import maxminddb
import GeoIP
import re
import os

import io
import gzip

__author__ = 'brizzbane'


def iplookup(ip_address):
    asn = gi.org_by_addr(ip_address)
    geo = reader.get(ip_address)

    lookup = {'city': None, 'postal': None, 'region': None, 'region_code': None, 'latitude': None,
              'longitude': None, 'time_zone': None, 'country': None, 'country_code': None, 'continent': None,
              'continent_code': None, 'asn': None, 'isp': None}

    try:
        lookup['asn'], isp = re.search('^(AS[0-9]+) (.+)', asn).groups()
        lookup['isp'] = isp.decode('utf-8', 'ignore')
    except (TypeError, AttributeError):
        pass

    if geo:
        if 'continent' in geo:
            lookup['continent'] = geo['continent']['names']['en']
            lookup['continent_code'] = geo['continent']['code']

        if 'country' in geo:
            lookup['country'] = geo['country']['names']['en']
            lookup['country_code'] = geo['country']['iso_code']

        if 'subdivisions' in geo:
            if 'iso_code' in geo['subdivisions'][0]:
                lookup['region'] = geo['subdivisions'][0]['names']['en']
                lookup['region_code'] = geo['subdivisions'][0]['iso_code']

        if 'city' in geo:
            lookup['city'] = geo['city']['names']['en']

        if 'postal' in geo:
            lookup['postal'] = geo['postal']['code']

        if 'location' in geo:
            if 'latitude' in geo['location']:
                lookup['latitude'] = geo['location']['latitude']
                lookup['longitude'] = geo['location']['longitude']

            if 'time_zone' in geo['location']:
                lookup['time_zone'] = geo['location']['time_zone']

        return lookup

def update():
    ipdb_urls = [('http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz', 'GeoIPASNum.dat'),
                 ('http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz', 'GeoLite2-City.mmdb')]

    for url, outfilename in ipdb_urls:
        response = urllib.urlopen(url)
        compressedfile = io.BytesIO(response.read())
        decompressedfile = gzip.GzipFile(fileobj=compressedfile, mode='rb')
        with open('%s/%s' % (os.path.dirname(__file__), outfilename), 'w') as outfile:
            outfile.write(decompressedfile.read())

try:
    reader = maxminddb.open_database('%s/GeoLite2-City.mmdb' % os.path.dirname(__file__))
    gi = GeoIP.open('%s/GeoIPASNum.dat' % os.path.dirname(__file__), GeoIP.GEOIP_STANDARD)
except IOError:
    update()



