let $c := doc('Ligas')/ligas/liga
let $i := '3'
for $e in $c
where $e/idliga = $i
return delete node $e