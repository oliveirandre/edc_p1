let $c := doc('Ligas')/ligas/liga
for $e in $c
return insert node (
  <liga>
    <idliga>3</idliga>
   </liga>
) after $e