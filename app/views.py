from django.shortcuts import render
from lxml import etree as ET
from django.template.defaulttags import register
from BaseXClient import BaseXClient
import xmltodict
from django.shortcuts import redirect
import feedparser

def ligas(request):
    nomes = dict()
    paises = dict()
    imagensliga = dict()
    imagenspaises = dict()
    res = None
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:listLigas()
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
    feed = feedparser.parse('http://feeds.jn.pt/JN-Desporto')
    print(feed)
    tparams = {
        'nomes': nomes,
        'paisn': paises,
        'pais': imagenspaises,
        'liga': imagensliga,
        'feed' : feed
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
        query = '//liga[@idliga=' + str(request.GET['idliga']) + ']'
    liga = tree.xpath(query)
    for c in liga:
        nomeliga = c.find('nomeliga').text
        imagemliga = c.find('imagemliga').text
        idliga = c.find('idliga').text

    res = None
    if 'idliga' in request.GET:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        try:
            input = """
                    import module namespace funcs="com.funcs.my.index" at "index.xqm";
                    funcs:showLiga('{}')
                    """.format(request.GET['idliga'])
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
        'posicaoclube': sorted(posicaoclube.items(), key=lambda x: int(x[1])),
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
    info1 = dict();
    if ('idclube') in request.GET:
        id=str(request.GET['idclube'])
    else:
        id=1

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:showClube('{}')
                """.format(request.GET['idclube'])
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:showJogadores('{}')
                """.format(request.GET['idclube'])
        query = session.query(input)
        res2 = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    dres = xmltodict.parse(res)
    lres = dres['clube']['club']
    dres2 = xmltodict.parse(res2)
    lres2 = dres2['jogadores']['jogador']
    if lres2 != None:
        for c in lres2:
            if c != 'idjogador':
                info1[c['idjogador']] = c['nomejogador']
            else:
                break
        tparams = {
            'jogadores' : info1,
            'clube' : lres['imagemclube'],
            'nomecompleto' : lres['nomecompleto'],
            'pontos' : lres['pontos'],
            'gm' : lres['golosmarcados'],
            'gs' : lres['golossofridos'],
            'pos' : lres['posicaoclube'],
            'vit' : lres['vitorias'],
            'derr' : lres['derrotas'],
            'emp' : lres['empates'],
            'cidade':lres['cidade'],
            'fundacao' : lres['anofundacao'],
            'presidente': lres['presidente'],
            'treinador': lres['treinador'],
            'estadio' : lres['estadio'],
            'idclube' : id,
            'sigla': lres['sigla'],
            'nomeinc': lres['nomeclube'],
            'idliga': lres['liga'],
            'nomeliga': lres['nomeliga'],
        }
    return render(request, 'clube.html', tparams)


def jogador(request):
    if 'idjogador' in request.GET:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        try:
            input = """
                    import module namespace funcs="com.funcs.my.index" at "index.xqm";
                    funcs:showInfoJog('{}')
                    """.format(request.GET['idjogador'])
            query = session.query(input)
            res = query.execute()
            query.close()
        finally:
            if session:
                session.close()
        dres = xmltodict.parse(res)
        lres = dres['jogadores']['jogador']

    tparams = {
        'nome': lres['nomejogador'],
        'numero': lres['numerojogador'],
        'nacional': lres['nacionalidade'],
        'posicao': lres['posicaojogador'],
        'nacionalidade': lres['nacionalidade'],
        'idade': lres['idade'],
        'anteriores': lres['clubesanteriores'],
    }
    return render(request, 'jogador.html', tparams)

def addLiga(request):
    return render(request, 'novaliga.html', {})

def addLigaXML(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:addLiga()
                """
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    dres = xmltodict.parse(res)
    lres = dres['liga']['l']
    liga = request.POST.get('nomeliga')
    pais =request.POST.get('nomepais')
    id=lres[len(lres)-1]['idliga']
    id2=int(lres[len(lres)-1]['idliga'])+1
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    print(pais)
    try:
        input = """   
                let $c := doc('Ligas')/ligas/liga
                  for $e in $c
                  where $e/idliga/text() = """ + str(id) + """
                  return insert node (
                    <liga idliga='""" + str(id2) + """'>
                        <idliga>"""+ str(id2) + """</idliga>
                        <imagempais>bandeiras/""" + str(pais.lower()) + """.png</imagempais>
                        <nomeliga>""" + str(liga) + """</nomeliga>
                        <imagemliga>default.png</imagemliga>
                        <pais>"""+ str(pais) +"""</pais>
                    </liga>
                ) after $e
                """
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    response = redirect('/')
    return response

def edit_club(request):
    if ('idclube') in request.GET:
        id = str(request.GET['idclube'])
    else:
        id=1

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """<clube> {
                      let $id := """ + id + """
                      for $c in doc('Ligas')/ligas/liga/clube
                      where $c/idclube/text()=$id
                      return
                        <club>
                          <idclube>{$c/idclube/text()}</idclube>
                          <nomeclube>{$c/nomeclube/text()}</nomeclube>
                          <nomecompleto>{$c/nomecompleto/text()}</nomecompleto>
                          <sigla>{$c/sigla/text()}</sigla>
                          <pontos>{$c/pontos/text()}</pontos>
                          <posicaoclube>{$c/posicaoclube/text()}</posicaoclube>
                          <imagemclube>{$c/imagemclube/text()}</imagemclube>
                          <vitorias>{$c/vitorias/text()}</vitorias>
                          <empates>{$c/empates/text()}</empates>
                          <derrotas>{$c/derrotas/text()}</derrotas>
                          <golosmarcados>{$c/golosmarcados/text()}</golosmarcados>
                          <golossofridos>{$c/golossofridos/text()}</golossofridos>
                          <cidade>{$c/cidade/text()}</cidade>
                          <estadio>{$c/estadio/text()}</estadio>
                          <anofundacao>{$c/anofundacao/text()}</anofundacao>
                          <presidente>{$c/presidente/text()}</presidente>
                          <treinador>{$c/treinador/text()}</treinador>
                        </club>
                    }</clube>
                  """
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    dres = xmltodict.parse(res)
    lres = dres['clube']['club']
    tparams = {
        'clube' : lres['imagemclube'],
        'nomecompleto' : lres['nomecompleto'],
        'pontos' : lres['pontos'],
        'gm' : lres['golosmarcados'],
        'gs' : lres['golossofridos'],
        'pos' : lres['posicaoclube'],
        'vit' : lres['vitorias'],
        'derr' : lres['derrotas'],
        'emp' : lres['empates'],
        'cidade':lres['cidade'],
        'fundacao' : lres['anofundacao'],
        'presidente': lres['presidente'],
        'treinador': lres['treinador'],
        'estadio' : lres['estadio'],
        'idclube' : id,
        'sigla' : lres['sigla'],
        'nomeinc' : lres['nomeclube'],
    }
    return render(request, 'editar_club.html', tparams)


def edits_clube(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:editClube('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(request.GET['idclube'], request.POST.get('pontos'), request.POST.get('posicaoclube'), request.POST.get('vitorias'), request.POST.get('empates'), request.POST.get('derrotas'), request.POST.get('treinador'), request.POST.get('golossofridos'), request.POST.get('golosmarcados'), request.POST.get('estadio'), request.POST.get('presidente'), request.POST.get('cidade'), request.POST.get('anofund'), request.POST.get('nomecompleto'), request.POST.get('anofund'), request.POST.get('nomeclube'), request.POST.get('sigla'))
        query = session.query(input)
        query.execute()
        query.close()
    finally:
        if session:
            session.close()
    response = redirect('/clube?idclube=' + str(request.GET['idclube']))
    return response

def delete_jogador(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:deleteJogador('{}')
                """.format(request.GET['idjogador'])
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()
    dres = xmltodict.parse(res)
    lres = dres['jogadores']['jogador']

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:deleteJog('{}')
                """.format(request.GET['idjogador'])
        query = session.query(input)
        query.execute()
        query.close()
    finally:
        if session:
            session.close()
    response = redirect('/clube?idclube='+lres['idclube'])
    return response


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
