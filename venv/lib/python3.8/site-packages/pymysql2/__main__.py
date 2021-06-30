import sys
if  sys.version_info < (3,0):
    input=raw_input
from pymysql2.__init__ import session

msg="""Usage:

xmysql [options...]

options:

-s: server to connect to (default: localhost)
-u: username (default: root)
-p: password (default: "")
-c: commands to execute seperated by ";"
-db: database to use
-h: display this help message
-t: timeout (default: 5)
-ch: charset (default: utf8)

Examples:

xmysql localhost:3306 -u root -p ""

xmysql localhost -u root -p root -db shop -c "select username,password from users"

"""
c=sys.argv
user="root"
pwd=""
host="localhost"
port=3306
db=None
commands=[]
timeout=5
charset="utf8"

if len(c)<2:
    print(msg)
    sys.exit()

i=0
while(i<(len(c))):
    x=c[i]
    if (x=="-h"):
        print(msg)
        sys.exit()
    if (x=="-s"):
        host=c[i+1]
        i+=1
    if (x=="-u"):
        user=c[i+1]
        i+=1
    if (x=="-p"):
        pwd=c[i+1]
        i+=1
    if (x=="-db"):
        db=c[i+1]
        i+=1
    if (x=="-c"):
        commands=c[i+1].split(';')
        i+=1
    if (x=="-t"):
        timeout=int(c[i+1])
        i+=1
    if (x=="-ch"):
        charset=c[i+1]
        i+=1
    i+=1

if ":" in host:  
  ip=host.split(':')[0]
  port=int(host.split(':')[1])
else:
    ip=host

def run():
 try:
  s=session(ip,user,pwd,database=db,port=port,timeout=timeout,charset=charset)
  if len(commands)>0:
      for i in commands:
        try:
          print("mysql> "+i)
          r=s.execute(i)
          for x in r:
             print(x)
        except Exception as xc:
          print(xc)
      s.close()
      sys.exit()
  else:
   while True:
    try:
      cmd=input("mysql> ")
      if (cmd.lower().strip()in ["exit","quit"]):
        s.close()
        sys.exit()
      r=s.execute(cmd)
      for x in r:
          print(x)
    except KeyboardInterrupt:
        s.close()
        sys.exit()
    except Exception as e:
        print(e)
 except Exception as ex:
  print(ex)
  sys.exit()

run()
