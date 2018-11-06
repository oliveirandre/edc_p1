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
                    <liga> {
                      let $idliga := """ + str(request.GET['idliga']) + """
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
        input = """<clube> {
                      let $id := """+ id + """
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
                           <liga>{$c/../idliga/text()}</liga>
                           <nomeliga>{$c/../nomeliga/text()}</nomeliga>
                        </club>
                    }</clube>
                  """
        query = session.query(input)
        res = query.execute()
        query.close()
    finally:
        if session:
            session.close()

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                  let $s := """+ id + """
                  for $c in doc('Ligas')/ligas/liga/clube
                  where $c/idclube/text()=$s
                  return
                    for $d in $c//jogadores
                    return $d    
                """
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
                    <jogadores> {
                        let $idjogador := """ + str(request.GET['idjogador']) + """
                        for $c in doc('Ligas')/ligas/liga/clube/jogadores
                        return
                        for $a in $c//jogador
                          where $a/idjogador/text() = $idjogador
                          return
                          <jogador>
                            <idjogador>{$a/idjogador/text()}</idjogador>
                            <nomejogador>{$a/nomejogador/text()}</nomejogador>
                            <imagemjogador>{$a/imagemjogador/text()}</imagemjogador>
                            <numerojogador>{$a/numerojogador/text()}</numerojogador>
                            <idade>{$a/idade/text()}</idade>
                            <nacionalidade>{$a/nacionalidade/text()}</nacionalidade>
                            <posicaojogador>{$a/posicaojogador/text()}</posicaojogador>
                            <clubesanteriores>{$a/clubesanteriores/text()}</clubesanteriores>
                          </jogador>
                    } </jogadores>
                    """
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
        input = """        <liga>{
                            for $c in doc('Ligas')/ligas/liga
                            order by $c/idliga
                              return
                              <l>
                                <idliga>{$c/idliga/text()}</idliga>
                                </l>
                                }</liga>
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
        input = """   let $c := doc('Ligas')/ligas/liga
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
                let $id := """ + "'" + str(request.GET['idclube']) + "'" + """
                let $pontos := """ + "'" + str(request.POST.get('pontos')) + "'" + """
                let $posicao := """ + "'" + str(request.POST.get('posicaoclube')) + "'" + """  
                let $vitorias := """ + "'" + str(request.POST.get('vitorias')) + "'" + """
                let $empates := """ + "'" + str(request.POST.get('empates')) + "'" + """
                let $derrotas := """ + "'" + str(request.POST.get('derrotas')) + "'" + """
                let $treinador := """ + "'" + str(request.POST.get('treinador')) + "'" + """ 
                let $golossofridos := """ + "'" + str(request.POST.get('golossofridos')) + "'" + """ 
                let $golosmarcados := """ + "'" + str(request.POST.get('golosmarcados')) + "'" + """ 
                let $estadio := """ + "'" + str(request.POST.get('estadio')) + "'" + """ 
                let $presidente := """ + "'" + str(request.POST.get('presidente')) + "'" + """ 
                let $cidade := """ + "'" + str(request.POST.get('cidade')) + "'" + """ 
                let $anofund := """ + "'" + str(request.POST.get('anofund')) + "'" + """ 
                let $nomecompleto := """ + "'" + str(request.POST.get('nomecompleto')) + "'" + """ 
                let $anofund := """ + "'" + str(request.POST.get('anofund')) + "'" + """ 
                let $nomeinc := """ + "'" + str(request.POST.get('nomeclube')) + "'" + """ 
                let $sigla := """ + "'" + str(request.POST.get('sigla')) + "'" + """ 

                
                
                for $c in doc('Ligas')/ligas/liga/clube
                where $c/idclube/text() = $id
                return (replace value of node $c/pontos with $pontos,
                        replace value of node $c/posicaoclube with $posicao,
                        replace value of node $c/vitorias with $vitorias,
                        replace value of node $c/empates with $empates,
                        replace value of node $c/derrotas with $derrotas,
                        replace value of node $c/treinador with $treinador,
                        replace value of node $c/golossofridos with $golossofridos,
                        replace value of node $c/golosmarcados with $golosmarcados,
                        replace value of node $c/cidade with $cidade,
                        replace value of node $c/anofundacao with $anofund,
                        replace value of node $c/estadio with $estadio,
                        replace value of node $c/presidente with $presidente,
                        replace value of node $c/sigla with $sigla,
                        replace value of node $c/nomecompleto with $nomecompleto,
                        replace value of node $c/nomeclube with $nomeinc) 
                """
        print(input)
        query = session.query(input)
        query.execute()
        query.close()
    finally:
        if session:
            session.close()
    response = redirect('/clube?idclube=' + str(request.GET['idclube']))
    return response

def delete_jogador(request):
    if ('idjogador') in request.GET:
        id = str(request.GET['idjogador'])
    else:
        id = 1

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = """
                       <jogadores> {
                           let $idjogador := """ + id + """
                           for $c in doc('Ligas')/ligas/liga/clube/jogadores
                           return
                           for $a in $c//jogador
                             where $a/idjogador/text() = $idjogador
                             return
                             <jogador>
                               <idclube>{$a/../../idclube/text()}</idclube>
                             </jogador>
                       } </jogadores>
                       """
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
                let $c := doc('Ligas')/ligas/liga/clube
                let $j := """ + id +"""
                for $e in $c
                return
                for $d in $e//jogadores/jogador
                where $d/idjogador/text() = $j
                return delete node $d
        """
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
