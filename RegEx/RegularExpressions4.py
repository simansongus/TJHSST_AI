import sys; args = sys.argv[1:]
idx = int(args[0])-60

myRegexLst = [
  r"/^((?!010)[10])*$/", #good
  r"/^((?!010)(?!101)[10])*$/", #good
  r"/^([10])([10]*\1)?$/", #good
  r"/\b((\w)(?!\w*\2\b))+\b/i", #good
  r"/(?=\w*?(\w)\w*\1\w*)(?=\w*(?!\1)(\w)\w*\2\w*)\w*|\w*?(\w)\w*(\3\w*)(\3\w*)(\3\w*)/i", #good
  r"/\b((\w)(?!\w*\2))*(\w)((\w)(?!\w*\5))*\3((\w)(?!\w*\7))*\3((\w)(?!\w*\9))*\b/i", #good
  r"/\b(?=\w*?a)(?=\w*?e)(?=\w*?i)(?=\w*?o)(?=\w*?u)(?!(\w*?[aeiou]){6,})\w*\b/i", #good
  r"/^(?=^(0*(10*1)?)*$)[10]([10]{2})*$/", #good
  r"/^0$|(?!^0)^(0|1(01*0)*1)+$/",    #good
  r"/(?!^0)(?!^(0|1(01*0)*1)+$)^[10]+$/"   #good
  ,]
if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Gus Simanson, period 2, 2025