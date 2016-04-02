import urllib2
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

REQUESTS = ["https://www.linkedin.com/jobs/search?keywords=Data+Scientist\
&location=San+Francisco+Bay+Area&trk=jobs_jserp_search_button_execute&locationId=us%3A84"] + \
           ["https://www.linkedin.com/jobs/search?keywords=Data+Scientist\
&locationId=us:84&start=325&count=25&trk=jobs_jserp_pagination_%s" % i for i in range(280)]

client = requests.Session()

HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
USERNAME = "XXX"
PASSWORD = "XXX"

html = client.get(HOMEPAGE_URL).content
soup = BeautifulSoup(html, "html.parser")
csrf = soup.find(id="loginCsrfParam-login")['value']

login_information = {
    'session_key': USERNAME,
    'session_password': PASSWORD,
    'loginCsrfParam': csrf,
}

print "... LOGGING IN ..."
client.post(LOGIN_URL, data=login_information)
print "... LOGGED IN ..."


def get_page(request):
    try:
        page = urllib2.urlopen(request)
        return page
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'Failed to reach url'
            print 'Reason: ', e.reason
            pass
        elif hasattr(e, 'code'):
            if e.code == 404:  # page not found
                print 'Error: ', e.code
                pass


if __name__ == "__main__":
    i = 1
    for url in REQUESTS:
        page = get_page(url)
        job_urls = parse_url_page(page)
        write_to_file(job_urls, "linkedin_data_scientist.txt")
        print i
        i += 1
