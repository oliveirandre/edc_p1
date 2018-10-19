from django.shortcuts import render
from lxml import etree as ET

info = []
def ligas(request):
    fm = "app/liga.xml"
    tree = ET.parse(fm)
    info = dict()
    info2 = dict()
    info3 = dict()
    info4 = dict()
    query = '//liga'

    print("ola")
    curs = tree.xpath(query)
    for c in curs:
        info4[c.find('idliga').text] = c.find('pais').text
        info[c.find('idliga').text] = c.find('nomeliga').text
        print(c.find('nomeliga').text)
        info2[c.find('idliga').text] = c.find('imagemliga').text
        print(c.find('imagemliga').text)
        info3[c.find('idliga').text] = c.find('imagempais').text
        print(c.find('imagempais').text)



    tparams = {
        'nomes': info,
        'liga' : info2,
        'pais' : info3,
        'paisn' :info4,
    }
    return render(request, 'index.html', tparams)