import sys; args = sys.argv[1:]
idx = int(args[0])-40


myRegexLst = [
  r"/^[x.o]{64}$/i",
  r"/^[xo]*\.[xo]*$/i",
  r"/^\.|^x+o*\.|\.o*x+$|\.$/i",
  r"/^(..)*.$/s",
  r"/^0([10][10])*$|^1([10][10])*[10]$/",  
  r"/\w*a[eiou]\w*|\w*e[aiou]\w*|\w*i[aeou]\w*|\w*o[aeiu]\w*|\w*u[aeio]\w*/i",
  r"/^(1?0)*1*$/",
  r"/^[bc]*[abc][bc]*$/",
  r"/^([bc]+|([bc]*a[bc]*a[bc]*)+)$/",
  r"/^(2[02]*|((1[02]*1)[02]*))+$/",]

if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Gus Simanson, period 2, 2025