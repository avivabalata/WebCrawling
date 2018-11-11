from bs4 import BeautifulSoup

# import the library used to query a website
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

# specify the url
wiki = "https://en.wikipedia.org/wiki/Gal_Gadot"

# Query the website and return the html to the variable 'page'
page = urlopen(wiki)

# Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page, "lxml")

films_table = soup.find("table", class_="wikitable sortable")

##############################################################

# Generate lists
# Generate lists
moviesUrls = []
A = []
B = []
C = []
D = []
rowSpanYear = 0
rowSpanYearValue = ""
yearBoolean = 0
rowSpanRole = 0
rowSpanRoleValue = ""
roleBoolean = 0

for row in films_table.tbody.findAll("tr"):
    cells = row.findAll('td')
    if len(cells) == 5:

        ##############

        if cells[0].has_attr('rowspan'):
            rowSpanYear = int(cells[0].attrs['rowspan']) - 1
            rowSpanYearValue = cells[0].find(text=True)
            moviesUrls.append(cells[1].find('i').find('a').attrs['href'])
            A.append(cells[0].find(text=True))
            B.append(cells[1].find(text=True))
            C.append(cells[2].find(text=True))
            D.append(cells[3].find(text=True))
        else:
            if cells[2].has_attr('rowspan'):
                rowSpanRole = int(cells[2].attrs['rowspan']) - 1
                rowSpanRoleValue = cells[2].find(text=True)
                moviesUrls.append(cells[1].find('i').find('a').attrs['href'])
                A.append(cells[0].find(text=True))
                B.append(cells[1].find(text=True))
                C.append(cells[2].find(text=True))
                D.append(cells[3].find(text=True))
            else:
                moviesUrls.append(cells[1].find('i').find('a').attrs['href'])
                A.append(cells[0].find(text=True))
                B.append(cells[1].find(text=True))
                C.append(cells[2].find(text=True))
                D.append(cells[3].find(text=True))


                ########################################
    if len(cells) == 4:

        if rowSpanYear > 0:
            A.append(rowSpanYearValue)
            moviesUrls.append(cells[0].find('i').find('a').attrs['href'])
            B.append(cells[0].find(text=True))
            C.append(cells[1].find(text=True))
            D.append(cells[2].find(text=True))
            rowSpanYear = rowSpanYear - 1

        else:
            if rowSpanRole > 0:
                C.append(rowSpanRoleValue)
                moviesUrls.append(cells[1].find('i').find('a').attrs['href'])
                A.append(cells[0].find(text=True))
                B.append(cells[1].find(text=True))
                D.append(cells[2].find(text=True))
                rowSpanRole = rowSpanRole - 1
print(moviesUrls)

#########################################


import pandas as pd
df=pd.DataFrame()
df['Year']=A
df['Title']=B
df['Role']=C
df['Director']=D
df


######################################################

actors = []

for movie in moviesUrls:

    mo = urlopen('https://en.wikipedia.org' + movie)
    soup = BeautifulSoup(mo, "lxml")
    if soup.find(id="Cast"):
        castTitle = soup.find(id="Cast")
    if soup.find(id="Voice_cast"):
        castTitle = soup.find(id="Voice_cast")

    isMany = False
    if castTitle is not None:

        actorList = castTitle.findNext("ul")

        while len(actorList.findAll('li')) == 1 and actorList.findNext("ul"):
            isMany = True
            for actor in actorList.findAll('li'):
                if actor.find('a') is not None and actor.find('a').has_attr('href'):
                    url = actor.find('a').attrs['href']
                    if url not in actors:
                        if url.startswith('/wiki'):
                            actors.append(url)
            actorList = actorList.findNext("ul")
        if isMany == False:
            for actor in actorList.findAll('li'):
                if actor.find('a') is not None and actor.find('a').has_attr('href'):
                    url = actor.find('a').attrs['href']
                    if url not in actors:
                        if url.startswith('/wiki'):
                            actors.append(url)

actors.remove('/wiki/Gal_Gadot')
print(len(actors))

######################################################
name = []
years = []
country = []
awards = []

for actor in actors:
    actorPage = urlopen('https://en.wikipedia.org' + actor)
    soup = BeautifulSoup(actorPage, "lxml")
    actorName = soup.find("h1", id="firstHeading").find(text=True)
    name.append(actorName)

    if soup.find(class_="bday") is None:
        years.append('---')
    else:
        bday = soup.find(class_="bday")
        born = bday.findNext(text=True)
        year = born[:4]
        years.append(year)

    if soup.find(class_="birthplace") is None:
        country.append('---') # Todo : check if there is a year
    else:
        place = soup.find(class_="birthplace")
        born = place.findAll('a')
        if len(born) > 1:
            country.append(born[1].find(text=True))
        else:
            if len(born) > 0:
                if ',' in born[0].find(text=True):
                    country.append(born[0].find(text=True).split(",",1)[1])
                else:
                    country.append(born[0].find(text=True))


print(name)
print(years)


