import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
  r"/\w*(\w)\w*\1\w*/i",
  r"/\w*(\w)(\w*\1\w*){3}/i",
  r"/^([10])([10]*\1)?$/",
  r"/\b(?=\w*cat)\w{6}\b/i",
  r"/\b(?=\w*bri)(?=\w*ing)\w{5}(\w?){4}\b/i",  
  r"/\b(?!\w*cat)\w{6}\b/i",
  r"/\b(?!\w*(\w)\w*\1\w*)\w+/i",
  r"/^(?!.*10011)[10]*$/",
  r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
  r"/^(?!.*(101|111))[10]*$/",]
if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Gus Simanson, period 2, 2025