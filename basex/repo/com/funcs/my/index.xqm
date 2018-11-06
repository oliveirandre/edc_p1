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