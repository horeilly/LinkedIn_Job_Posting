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


def parse_job_page(page, client):
    page = client.get(page).content
    soup = BeautifulSoup(page, "html.parser")
    results = soup.find_all("code", {"id": "decoratedJobPostingModule"})[0].string
    return json.loads(results)


if __name__ == "__main__":
    with open("linkedin_data_scientist.txt", "rb") as f:
        job_urls = f.read().splitlines()

    with open("linkedin_data_scientist_job_data.json", "a") as f:
        for i in range(len(job_urls)):
            try:
                json.dump(parse_job_page(job_urls[i], client), f)
                f.write("\n")
            except IndexError as e:
                print e
                pass
            print i + 1
            i += 1
