#get the names of each sheet...

url = "https://www.sec.gov/cgi-bin/viewer?action=view&cik=51143&accession_number=0001047469-15-001106"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page,"lxml")

for i in soup.find_all(class_='xbrlviewer'):
        print i.text,i.attrs['href']


#Then maybe connect to sec.gov or FTP
page2 = urllib2.urlopen("https://www.sec.gov/Archives/edgar/data/51143/000104746915001106/R2.htm")
soup2 = BeautifulSoup(page2,"lxml")


import re
for f in soup2.find_all(class_="pl"):
    print { f.text : re.search("defref\_((us-gaap|ibm)\_[a-zA-Z]+)",f.a['onclick']).group(1).split("_") }

#Now we have what XBRL tag actually means...
