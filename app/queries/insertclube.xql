let $c := doc('Ligas')/ligas/liga
let $i := '3'
for $e in $c
  where $e/idliga = $i
    return insert node (
      <clube>
        <idclube>1000</idclube>
        <jogadores></jogadores>
      </clube>
    ) into $e