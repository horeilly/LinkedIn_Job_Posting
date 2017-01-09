import urllib2
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

# REQUESTS = ["https://www.linkedin.com/jobs/search?keywords=Data+Scientist\
# &location=San+Francisco+Bay+Area&trk=jobs_jserp_search_button_execute&locationId=us%3A84"] + \
# ["https://www.linkedin.com/jobs/search?keywords=Data+Scientist\
# # &locationId=us:84&start=325&count=25&trk=jobs_jserp_pagination_%s" % i for i in range(280)]

# REQUESTS = ["https://www.linkedin.com/vsearch/j?orig=JSHP&keywords=Biostatistician\&distance=50&locationType=I"
#             "&countryCode=us&postalCode=94118&trk=two_box_geo_fill"] + \
#     ["https://www.linkedin.com/vsearch/j?orig=JSHP&keywords=Biostatistician\&distance=50&locationType=I&countryCode"
#      "=us&postalCode=94118&trk=two_box_geo_fill&rsid=3703460571459628966248&openFacets=L,C&page_num=%s" % i for i in
#      range(8)]

client = requests.Session()

HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'

html = client.get(HOMEPAGE_URL).content
soup = BeautifulSoup(html, "html.parser")
csrf = soup.find(id="loginCsrfParam-login")['value']

login_information = {
    'session_key': '',
    'session_password': '',
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


def parse_url_page(page):
    soup = BeautifulSoup(page, "html.parser")
    jobs = soup.findAll("li", {"class": "job-listing"})
    return [job.a["href"] for job in jobs]


def parse_job_page(page, client):
    page = client.get(page).content
    soup = BeautifulSoup(page, "html.parser")
    results = soup.find_all("code", {"id": "decoratedJobPostingModule"})[0].string
    return json.loads(results)


def write_to_file(ls, filename):
    with open(filename, "a") as f:
        for entry in ls:
            f.write(entry + "\n")
    return None


if __name__ == "__main__":
    i = 1
    for url in REQUESTS:
        page = get_page(url)
        job_urls = parse_url_page(page)
        write_to_file(job_urls, "linkedin_data_scientist.txt")
        print i
        i += 1

    soup = get_page(REQUEST)
    print parse_job_page(soup)

    with open("Linked_In.txt", "rb") as f:
    	X = f.read().splitlines()
    X = X[6382:]

    test = parse_job_page2(X[0], client)

    print test

    with open("test_li.txt", "wb") as f:
    	json.dump(test, f)

    with open("Linked_In_Jobs.txt", "a") as f:
    	for url in X:
    		try:
    		    json.dump(parse_job_page(url, client), f)
    		except IndexError as e:
    			print e
    			pass
    		print i
    		i += 1
