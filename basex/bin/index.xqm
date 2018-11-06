module namespace funcs = "com.funcs.my.index";
declare namespace map = "http://www.w3.org/2005/xpath-functions/map";

declare updating function funcs:editClube($id, $pontos, $posicao, $vitorias, $empates, $derrotas, $treinador, $golossofridos, $golosmarcados,
                                          $cidade, $anofund, $estadio, $presidente, $sigla, $nomecompleto, $nomeinc) {
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
};


declare function funcs:deleteJogador($id) as node(){
  <jogadores> {
   let $idjogador := $id
   for $c in doc('Ligas')/ligas/liga/clube/jogadores
   return
   for $a in $c//jogador
     where $a/idjogador/text() = $idjogador
     return
     <jogador>
       <idclube>{$a/../../idclube/text()}</idclube>
     </jogador>
  } </jogadores>
};

declare function funcs:listLigas() as node () {
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
};

declare function funcs:showLiga($id) as node() {
  <liga> {
  let $idliga := $id
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
};

declare function funcs:showClube($idclube) as node() {
  <clube> {
    let $id := $idclube
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
};

declare function funcs:showJogadores($idclube) as node() {
  let $s := $idclube
  for $c in doc('Ligas')/ligas/liga/clube
  where $c/idclube/text()=$s
  return
    for $d in $c//jogadores
    return $d  
};

declare function funcs:showInfoJog($idjog) as node() {
  <jogadores> {
      let $idjogador := $idjog
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
};

declare function funcs:addLiga() as node() {
  <liga>{
  for $c in doc('Ligas')/ligas/liga
  order by $c/idliga
    return
    <l>
      <idliga>{$c/idliga/text()}</idliga>
      </l>
  }</liga>
};

declare updating function funcs:deleteJog($id) {
  let $c := doc('Ligas')/ligas/liga/clube
  let $j := $id
  for $e in $c
  return
  for $d in $e//jogadores/jogador
  where $d/idjogador/text() = $j
  return delete node $d
};
