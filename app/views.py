from django.shortcuts import render
from lxml import etree as ET
from django.template.defaulttags import register
from django.shortcuts import render_to_response
from BaseXClient import BaseXClient
import xmltodict
from django.shortcuts import redirect
import feedparser
import webbrowser
from io import BytesIO


def ligas(request):
    with open("app/liga.xsd", 'r') as schema_file:
        schema_to_check = schema_file.read().encode('utf-8')
    with open("app/liga.xml", 'r') as xml_file:
        xml_to_check = xml_file.read().encode('utf-8')
    xmlschema_doc = ET.parse(BytesIO(schema_to_check))
    xmlschema = ET.XMLSchema(xmlschema_doc)
    try:
        doc = ET.parse(StringIO(xml_to_check))
        print('XML well formed, syntax ok')
    except IOError:
        print('Invalid File')
    except ET.XMLSyntaxError as err:
        print('XML Syntax Error')
    except:
        print('Unknown error')

    try:
        xmlschema.assertValid(doc)
        print('XML valid, schema validation ok.')
    except ET.DocumentInvalid as err:
        print('Schema validation error')
    except:
        print('Unknown error, exiting')

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

    print(feed)
    tparams = {
        'nomes': nomes,
        'paisn': paises,
        'pais': imagenspaises,
        'liga': imagensliga
    }
    return render(request, 'index.html', tparams)

def feed (request):
    feed = feedparser.parse('http://feeds.jn.pt/JN-Desporto')

    tparams = {
        'feed' : feed
    }
    return render(request, 'feed.html', tparams)

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
    if 'idliga' in request.GET:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        try:
            input = """
                        import module namespace funcs="com.funcs.my.index" at "index.xqm";
                        funcs:ligaInfo('{}')
                        """.format(request.GET['idliga'])
            query = session.query(input)
            res2 = query.execute()
            query.close()
        finally:
            if session:
                session.close()
    dres2 = xmltodict.parse(res2)
    nomeliga = dres2['liga']['nomeliga']
    imagemliga = dres2['liga']['imagemliga']

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
        print(dres)
        if(dres['liga']!= None):
            lres = dres['liga']['clube']
            print(isinstance(lres, dict))
            if isinstance(lres, dict):
                nomeclube[lres['idclube']] = lres['nomeclube']
                vitorias[lres['idclube']] = lres['vitorias']
                empates[lres['idclube']] = lres['empates']
                derrotas[lres['idclube']] = lres['derrotas']
                golosmarcados[lres['idclube']] = lres['golosmarcados']
                golossofridos[lres['idclube']] = lres['golossofridos']
                posicaoclube[lres['idclube']] = lres['posicaoclube']
                imagemclube[lres['idclube']] = lres['imagemclube']
                pontos[lres['idclube']] = lres['pontos']
            else:
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
                'idliga': request.GET['idliga']
            }
        else: tparams = {
            'imagemliga': imagemliga,
            'nomeliga': nomeliga,
            'idliga': request.GET['idliga']
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
    lres2 = dres2['jogadores']
    print(lres2)
    if dres2['jogadores']==None:
        info1 = []
    else:
        if isinstance(lres2['jogador'], dict):
            info1[lres2['jogador']['idjogador']] = lres2['jogador']['nomejogador']
        else:
            for c in lres2['jogador']:
                info1[c['idjogador']] = c['nomejogador']

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
    else:
        return redirect('/index')

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
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                    funcs:addNewLiga('{}', '{}', '{}', '{}', '{}', '{}')
                    """.format(id, id2, ("bandeiras/" + str(pais.lower())) + ".png",
                               liga,"default.png", pais)

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
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:edClube('{}')
                """.format(request.GET['idclube'])
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


def editar_jogador(request):
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
    else:
        return redirect('/index')
    tparams = {
        'id' : lres['idjogador'],
        'nome': lres['nomejogador'],
        'numero': lres['numerojogador'],
        'nacional': lres['nacionalidade'],
        'posicao': lres['posicaojogador'],
        'idade': lres['idade'],
        'anteriores': lres['clubesanteriores'],
        'imagem' : lres['imagemjogador']
    }
    return render(request, 'editar_jogador.html', tparams)

def edits_jogador(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                    import module namespace funcs="com.funcs.my.index" at "index.xqm";
                    funcs:updateJogador('{}', '{}', '{}', '{}', '{}', '{}', '{}')
                    """.format(request.GET['idjogador'], request.POST.get('nome'), request.POST.get('numero'),
                               request.POST.get('nacionalidade'), request.POST.get('posicao'), request.POST.get('idade'),
                               request.POST.get('clubes'))
        query = session.query(input)
        query.execute()
        query.close()
    finally:
        if session:
            session.close()
    response = redirect('/jogador?idjogador=' + str(request.GET['idjogador']))
    return response

def new_clube(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                import module namespace funcs="com.funcs.my.index" at "index.xqm";
                funcs:orderClube()
                """
        query = session.query(input)
        res=query.execute()
        query.close()
    finally:
        if session:
            session.close()
    dres = xmltodict.parse(res)
    lres = dres['clube']['l']
    print(lres[len(lres)-1])
    return render(request,'novoclube.html',{'id': int(lres[len(lres)-1]['idclube'])+1, 'idliga': request.GET['idliga']})

def news_clube(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                    import module namespace funcs="com.funcs.my.index" at "index.xqm";
                    funcs:addNewClube('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',
                                        '{}','{}','{}','{}','{}','{}','{}','{}')
                    """.format(request.GET['idliga'],request.GET['idclube'], request.POST.get('pontos'), request.POST.get('posicaoclube'), request.POST.get('vitorias'), request.POST.get('empates'), request.POST.get('derrotas'), request.POST.get('treinador'), request.POST.get('golossofridos'), request.POST.get('golosmarcados'), request.POST.get('cidade'), request.POST.get('anofund'), request.POST.get('estadio'), request.POST.get('presidente'), request.POST.get('sigla'), request.POST.get('nomecompleto'), request.POST.get('nomeclube'), "default-team.png")

        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    return redirect('/clube?idclube='+request.GET['idclube'])

def delete_clube (request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                   import module namespace funcs="com.funcs.my.index" at "index.xqm";
                   funcs:deleteClube('{}')
                   """.format(request.GET['idclube'])
        query = session.query(input)
        query.execute()
        query.close()
    finally:
        if session:
            session.close()

    return redirect('/')

def delete_liga(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                   import module namespace funcs="com.funcs.my.index" at "index.xqm";
                   funcs:deleteLiga('{}')
                   """.format(request.GET['idliga'])
        query = session.query(input)
        query.execute()
        query.close()
    finally:
        if session:
            session.close()

    return redirect('/')


def novo_jogador(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                   import module namespace funcs="com.funcs.my.index" at "index.xqm";
                   funcs:orderJogador()
                   """
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()
    dres = xmltodict.parse(res)
    lres = dres['jogador']['idjogador']
    print(lres[len(lres) - 1])

    return render(request, 'novojogador.html', {'idclube': request.GET['idclube'], 'id' : (int(lres[len(lres) - 1])+1)})

def new_jogador(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                        import module namespace funcs="com.funcs.my.index" at "index.xqm";
                        funcs:addNewJogador('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                        """.format(request.GET['idclube'],request.GET['idjogador'], request.POST.get('nome'), request.POST.get('numero'),
                                   request.POST.get('nacionalidade'), request.POST.get('posicao'),
                                   request.POST.get('idade'),
                                   request.POST.get('clubes'), "img/primeiraLiga/jogadores/ok.png" )
        query = session.query(input)
        query.execute()
        query.close()
    finally:
        if session:
            session.close()

    return redirect('/clube?idclube=' + request.GET['idclube'])

def trya(request):
    dom = ET.parse('app/liga.xml')
    xslt = ET.parse("app/ligas.xsl")
    transform = ET.XSLT(xslt)
    newdom = transform(dom)

    outfile = open('app/templates/ligas.html', 'wb')
    outfile.write(ET.tostring(newdom))
    webbrowser.open_new_tab('app/templates/ligas.html')
    return redirect('/')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
