from django.shortcuts import render
from lxml import etree as ET
from django.template.defaulttags import register
from BaseXClient import BaseXClient
import xmltodict

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
    nomeclube = dict()
    vitorias = dict()
    empates = dict()
    derrotas = dict()
    posicaoclube = dict()
    imagemclube = dict()
    pontos = dict()
    golosmarcados = dict()
    golossofridos = dict()
    nomeliga = ''
    idliga = ''
    imagemliga = ''

    fn = "app/liga.xml"
    tree = ET.parse(fn)
    if 'idliga' in request.GET:
        query = '//liga[@idliga=' + request.GET['idliga'] + ']'
    liga = tree.xpath(query)
    for c in liga:
        nomeliga = c.find('nomeliga').text
        imagemliga = c.find('imagemliga').text
        idliga = c.find('idliga').text

    res = None
    if request.GET['idliga'] == "1":
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        try:
            input = """
                    <liga> {
                      let $idliga := "1"
                      for $c in doc('Ligas')/ligas/liga
                      where $c/idliga/text() = $idliga
                      return
                      for $a in $c//clube
                        return
                        <clube>
                          <idclube>{$a/idclube/text()}</idclube>
                          <nomeclube>{$a/nomeclube/text()}</nomeclube>
                          <vitorias>{$a/vitorias/text()}</vitorias>
                          <empates>{$a/empates/text()}</empates>
                          <derrotas>{$a/derrotas/text()}</derrotas>
                          <posicaoclube>{$a/posicaoclube/text()}</posicaoclube>
                          <imagemclube>{$a/imagemclube/text()}</imagemclube>
                          <pontos>{$a/pontos/text()}</pontos>
                          <golosmarcados>{$a/golosmarcados/text()}</golosmarcados>
                          <golossofridos>{$a/golossofridos/text()}</golossofridos>
                        </clube>
                    } </liga>
                    """
            query = session.query(input)
            res = query.execute()
            query.close()
        finally:
            if session:
                session.close()
        dres = xmltodict.parse(res)
        lres = dres['liga']['clube']

    else:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        try:
            input = """
                    <liga> {
                      let $idliga := "2"
                      for $c in doc('Ligas')/ligas/liga
                      where $c/idliga/text() = $idliga
                      return
                      for $a in $c//clube
                        return
                        <clube>
                          <idclube>{$a/idclube/text()}</idclube>
                          <nomeclube>{$a/nomeclube/text()}</nomeclube>
                          <vitorias>{$a/vitorias/text()}</vitorias>
                          <empates>{$a/empates/text()}</empates>
                          <derrotas>{$a/derrotas/text()}</derrotas>
                          <posicaoclube>{$a/posicaoclube/text()}</posicaoclube>
                          <imagemclube>{$a/imagemclube/text()}</imagemclube>
                          <pontos>{$a/pontos/text()}</pontos>
                          <golosmarcados>{$a/golosmarcados/text()}</golosmarcados>
                          <golossofridos>{$a/golossofridos/text()}</golossofridos>
                        </clube>
                    } </liga>
                    """
            query = session.query(input)
            res = query.execute()
            query.close()
        finally:
            if session:
                session.close()
        dres = xmltodict.parse(res)
        lres = dres['liga']['clube']

    for l in lres:
        nomeclube[l['idclube']] = l['nomeclube']
        vitorias[l['idclube']] = l['vitorias']
        empates[l['idclube']] = l['empates']
        derrotas[l['idclube']] = l['derrotas']
        golosmarcados[l['idclube']] = l['golosmarcados']
        golossofridos[l['idclube']] = l['golossofridos']
        posicaoclube[l['idclube']] = l['posicaoclube']
        imagemclube[l['idclube']] = l['imagemclube']
        pontos[l['idclube']] = l['pontos']

    tparams = {
        'nomeclube': nomeclube,
        'vitorias': vitorias,
        'empates': empates,
        'derrotas': derrotas,
        'posicaoclube': sorted(posicaoclube.items(), key=lambda x: x[1]),
        'imagem': imagemclube,
        'pontos': pontos,
        'golosmarcados': golosmarcados,
        'golossofridos': golossofridos,
        'imagemliga': imagemliga,
        'nomeliga': nomeliga,
        'idliga': idliga
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
