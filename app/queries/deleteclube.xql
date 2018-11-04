let $c := doc('Ligas')/ligas/liga
let $j := '1000'
for $e in $c
where $e/clube/idclube = $j
return delete node $e/clube