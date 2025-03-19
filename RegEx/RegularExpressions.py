import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
  r"/^0$|^10[01]$/i",
  r"/^[01]*$/i",
  r"/0$/i",
  r"/\w*[aeiou]\w*[aeiou]\w*/i",
  r"/^0$|^1[01]*0$/",  
  r"/^[01]*110[01]*$/i",
  r"/^.{2,4}$/is",
  r"/^\d{3} *-? *\d{2} *-? *\d{4}$/",
  r"/^.*?d\w*/im",
  r"/^[01]?$|^1[01]*1$|^0[01]*0$/i",
  ... ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])


#Gus Simanson, period 2, 2025