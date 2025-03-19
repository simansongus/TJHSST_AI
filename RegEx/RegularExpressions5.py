import sys; args = sys.argv[1:]
idx = int(args[0])-70

myRegexLst = [
    r"/^(?=.*a)(?=.*i)(?=.*e)(?=.*u)(?=.*o)[a-z]*$/m", 
    r"/^([bcdfghj-np-tv-z]*[aeiou]){5}[bcdfghj-np-tv-z]*$/m",
    r"/^[bcdfghj-np-tvxyz]w[bcdfghj-np-tvxyz]$|^[a-z]*[bcdfghj-np-tvxyz]w[bcdfghj-np-tvxyz]{2}[a-z]*$/m",
    r"/^a$|^([a-z])\1$|^(?=([a-z])([a-z])([a-z])?)(?=.*\4\3\2$)[a-z]*$/m",
    r"/^[ac-su-z]*(bt|tb)+[ac-su-z]*$/m",
    r"/^[a-z]*([a-z])\1[a-z]*$/m",
    r"/^[a-z]*([a-z])([a-z]*\1){5}[a-z]*$/m",
    r"/^[a-z]*(([a-z])\2){3}[a-z]*$/m",
    r"/^([aeiou]*[bcdfghj-np-tv-z]){13}[aeiou]*$/m",
    r"/^(([a-z])(?![a-z]*\2[a-z]*\2))*$/m",
  ]
if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Gus Simanson, period 2, 2025