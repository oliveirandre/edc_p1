let $c := doc('Ligas')/ligas/liga
let $j := '1000'
let $m := '2000'
for $e in $c
  where $e/clube/idclube = $j
  for $n in $e/clube/jogadores
    where $e/clube/jogadores/jogador/idjogador = $m
    return delete node $e/clube/jogadores/jogador