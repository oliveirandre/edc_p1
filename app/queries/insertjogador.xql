let $c := doc('Ligas')/ligas/liga/clube
let $i := '1000'
for $e in $c
  where $e/idclube = $i
    return insert node (
      <jogador>
        <idjogador>2000</idjogador>
      </jogador>
    ) into $e/jogadores