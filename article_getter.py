import urllib2
import csv
import os
import simplejson
import time

APIKEY = "1b4cac59cb03d2d3d8b0dbce3937236e:6:59424119"
SECTIONS = ["Business", "Obituaries", "Arts", "Sports", "World"]
BASEURL = "http://api.nytimes.com/svc/search/v1/article?query=nytd_section_facet:["
FIELDS = "]&fields=url,title,body&offset="
END = "&rank=newest&api-key="


def build_url(section, offset):
    return BASEURL + section + FIELDS + str(offset) + END + APIKEY


def geturls():
    num_of_articles = 2000
    for section in SECTIONS:
        print section
        offset = 0
        while offset < num_of_articles:
            print offset
            url = build_url(section, offset)
            json = simplejson.load(urllib2.urlopen(url))
            num_of_articles = add_to_file(json, section, num_of_articles)
            offset += 10
            time.sleep(1)


def add_to_file(json, section, num):
    if os.path.exists(section + '.tsv'):
        writer = csv.writer(open(section + '.tsv', 'ab'), delimiter="	")
    else:
        writer = csv.writer(open(section + '.tsv', 'wb'), delimiter="	")
    for article in json['results']:
        if 'body' in article:
            body = article['body'].encode("utf8")
            if 'title' in article:
                title = article['body'].encode("utf8")
                if 'url' in article:
                    url = article['url'].encode("utf8")
                    writer.writerow([url, title, body])
        else:
            num += 10
    return num


if __name__ == "__main__":
    geturls()
    print "Done"
