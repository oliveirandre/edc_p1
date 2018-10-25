from django.shortcuts import render
from lxml import etree as ET
from django.template.defaulttags import register

info = []
def ligas(request):
    nomes = dict()
    paises = dict()
    imagensliga = dict()
    imagenspaises = dict()
    res = None
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                <ligas> {
                    for $c in doc('Ligas')/ligas/liga
                    return
                      <liga>
                        <idliga>{$c/idliga/text()}</idliga>
                        <imagemliga>{$c/imagemliga/text()}</imagemliga>
                        <imagempais>{$c/imagempais/text()}</imagempais>
                        <pais>{$c/pais/text()}</pais>
                        <nomeliga>{$c/nomeliga/text()}</nomeliga>
                      </liga>
                    } </ligas>
                """
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    dres = xmltodict.parse(res)
    lres = dres['ligas']['liga']
    for l in lres:
        nomes[l['idliga']] = l['nomeliga']
        imagensliga[l['idliga']] = l['imagemliga']
        paises[l['idliga']] = l['pais']
        imagenspaises[l['idliga']] = l['imagempais']
        
    tparams = {
        'nomes': nomes,
        'paisn': paises,
        'pais': imagenspaises,
        'liga': imagensliga,
    }

    return render(request, 'index.html', tparams)
def tabelas(request):
    fn = "app/liga.xml"
    tree = ET.parse(fn)
    info = dict()
    info2 = dict()
    info3 = dict()
    info4 = dict()
    info5 = dict()
    info6= dict()
    info7 = dict()
    info8 = dict()
    info9 = dict()
    x=''
    y=''
    k=''

    print(request.GET['idliga'])
    if 'idliga' in request.GET:
        query = '//liga[@idliga='+request.GET['idliga']+ ']/clube'
        query2 = '//liga[@idliga='+request.GET['idliga']+ ']'
        print(query)
        print('deu')
    else:
        query = '//liga[@idliga=1]/clube'

    curs = tree.xpath(query)
    curs2 = tree.xpath(query2)

    for c in curs2:
        x = c.find('nomeliga').text
        y = c.find('imagemliga').text
        k=c.find('idliga').text

    for c in curs:
        info[c.find('idclube').text] = c.find('nomeclube').text
        info2[c.find('idclube').text] = c.find('vitorias').text
        info3[c.find('idclube').text] = c.find('empates').text
        info4[c.find('idclube').text] = c.find('derrotas').text
        info5[c.find('idclube').text] = int(c.find('posicaoclube').text)
        info6[c.find('idclube').text] = c.find('imagemclube').text
        info7[c.find('idclube').text] = c.find('pontos').text
        info8[c.find('idclube').text] = c.find('golosmarcados').text
        info9[c.find('idclube').text] = c.find('golossofridos').text

    tparams = {
        'nomeclube': info,
        'vitorias' : info2,
        'empates' : info3,
        'derrotas' : info4,
        'posicaoclube' : sorted(info5.items(), key=lambda x: x[1]),
        'imagem' : info6,
        'pontos' : info7,
        'golosmarcados' : info8,
        'golossofridos' : info9,
        'imagemliga' : y,
        'nomeliga' : x,
        'idliga' : k
    }


    return render(request, 'tabela.html', tparams)

def clube(request):
    fn = "app/liga.xml"
    tree = ET.parse(fn)

    if ('idliga' and 'idclube') in request.GET:
        query = '//liga[@idliga='+request.GET['idliga']+ ']/clube[@idclube=' +request.GET['idclube'] + ']/jogadores/jogador'
        query2 = '//liga[@idliga='+request.GET['idliga']+ ']/clube[@idclube=' +request.GET['idclube'] + ']'
        print(query)
        #print('deu')
    else:
        query = '//liga[@idliga=1]/clube[@clube=1]//jogadores'

    info1 = dict();
    x=''
    y=''
    pos=''
    gm=''
    gs=''
    pont=''
    vit = ''
    derr=''
    emp=''
    cidade=''
    fund=''
    pres = ''
    trei = ''
    esta=''
    idliga= request.GET['idliga']
    idclube = request.GET['idclube']

    curs = tree.xpath(query)
    curs2 = tree.xpath(query2)
    print(curs)


    for c in curs2:
        x = c.find('imagemclube').text
        y=c.find('nomecompleto').text
        pos = c.find('posicaoclube').text
        gm = c.find('golosmarcados').text
        gs = c.find('golossofridos').text
        pont = c.find('pontos').text
        vit = c.find('vitorias').text
        derr = c.find('derrotas').text
        emp = c.find('empates').text
        cidade = c.find('cidade').text
        fund = c.find('anofundacao').text
        pres = c.find('presidente').text
        trei = c.find('treinador').text
        esta = c.find('estadio').text

        print(x)

    for c in curs:
        info1[c.find('idjogador').text] = c.find('nomejogador').text

    tparams = {
        'jogadores' : info1,
        'clube' : x,
        'nomecompleto' : y,
        'pontos' : pont,
        'gm' : gm,
        'gs' : gs,
        'pos' : pos,
        'vit' : vit,
        'derr' : derr,
        'emp' : emp,
        'cidade':cidade,
        'fundacao' : fund,
        'presidente': pres,
        'treinador': trei,
        'estadio' : esta,
        'idliga' : idliga,
        'idclube' : idclube
    }
    return render(request, 'clube.html', tparams)


def jogador(request):
    fn = "app/liga.xml"
    tree = ET.parse(fn)

    if ('idliga' and 'idclube' and 'idjogador') in request.GET:
        query = '//liga[@idliga=' + request.GET['idliga'] + ']/clube[@idclube=' + request.GET[
            'idclube'] + ']/jogadores/jogador[@idjogador=' + request.GET['idjogador'] + ']'
    else:
        query = '//liga[@idliga=1]/clube[@clube=1]//jogadores'

    curs = tree.xpath(query)
    a=''
    b=''
    c=''
    d=''
    e=''
    f=''
    g=''
    for c in curs:
        print(c.find('idade').text)
        d = c.find('idade').text
        g = c.find('clubesanteriores').text
        e = c.find('nacionalidade').text
        f = c.find('posicaojogador').text
        a = c.find('nomejogador').text
        b = c.find('numerojogador').text
        c = c.find('nacionalidade').text

    tparams = {
        'nome' : a,
        'numero' : b,
        'nacional' : c,
        'posicao' : f,
        'nacionalidade': e,
        'idade' : d,
        'anteriores' : g

    }


    return render(request, 'jogador.html', tparams)
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
