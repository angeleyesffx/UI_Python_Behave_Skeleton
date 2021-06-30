import pymysql,cgi,sys,threading,time,random

if  sys.version_info < (3,0):
    import HTMLParser
else:
    import html.parser as HTMLParser

def escape_html(s):
 '''
   function to return escaped html string
 '''
 return cgi.escape(s,quote=True)

def unescape_html(s,encoding="utf-8"):
 '''
   function to return unescaped html string
 '''
 return HTMLParser.HTMLParser().unescape(s).encode(encoding)

def escape_str(s):
    #this function is similar to PHP: mysql_escape_string()
    #it escapes any given string
     return pymysql.escape_string(s)

class session:
 def __init__(self,host,username,password,port=3306,database=None,timeout=5,charset='utf8',autocommit=True,ssl=None,cursorclass=pymysql.cursors.DictCursor,unix_socket=None,sql_mode=None, read_default_file=None, conv=None, use_unicode=None, client_flag=0, init_command=None, read_default_group=None, compress=None, named_pipe=None, db=None, passwd=None, local_infile=False, max_allowed_packet=16777216, defer_connect=False, auth_plugin_map=None, read_timeout=None, write_timeout=None, bind_address=None, binary_prefix=False, program_name=None, server_public_key=None):
    self.statement=None
    self.connection = pymysql.connect(host=host,port=port,user=username,password=password,ssl=ssl,database=database,cursorclass=cursorclass,autocommit=autocommit,connect_timeout=timeout,charset=charset,unix_socket=unix_socket,sql_mode=sql_mode,read_default_file=read_default_file,conv=conv,use_unicode=use_unicode,client_flag=client_flag,init_command=init_command,read_default_group=read_default_group,compress=compress,named_pipe=named_pipe,db=db,passwd=passwd,local_infile=local_infile,max_allowed_packet=max_allowed_packet,defer_connect=defer_connect,auth_plugin_map=auth_plugin_map,read_timeout=read_timeout,write_timeout=write_timeout, bind_address=bind_address, binary_prefix=binary_prefix, program_name=program_name, server_public_key=server_public_key)
    self.cursor = self.connection.cursor()
    self.statement=None
 def begin(self):
     self.connection.begin()
 def show_warnings(self):
     self.connection.show_warnings()
 def replace_connection(self,con):
     self.close()
     self.connection=con
     self.cursor = self.connection.cursor()
 def rollback(self):
     self.connection.rollback()
 def commit(self):
     self.connection.commit()
 def reconnect(self,new_cursor=False):
    self.connection.ping(reconnect=True)
    if new_cursor==True:
      if self.cursor:
          self.cursor.close()
      self.cursor = self.connection.cursor()
 def ping(self,reconnect=False):
    self.connection.ping(reconnect=reconnect)
 def set_max_connections(self,*args):
     if args:
      self.statement='''set global max_connections = {}'''.format(pymysql.escape_string(str(int(args[0]))))
     else:
      self.statement='''set global max_connections = 151'''
     self.cursor.execute(self.statement)
 def get_max_connections(self):
     self.statement='''SHOW VARIABLES LIKE "max_connections"'''
     self.cursor.execute(self.statement)
     return int(self.cursor.fetchall()[0][1])
 def set_wait_timeout(self,*args):
     if args:
      self.statement='''set global wait_timeout = {}'''.format(pymysql.escape_string(str(int(args[0]))))
     else:
      self.statement='''set global wait_timeout = 28800'''
     self.cursor.execute(self.statement)
 def get_wait_timeout(self):
     self.statement='''SHOW VARIABLES LIKE "wait_timeout"'''
     self.cursor.execute(self.statement)
     return int(self.cursor.fetchall()[0][1])
 def set_interactive_timeout(self,*args):
     if args:
      self.statement='''set global interactive_timeout = {}'''.format(pymysql.escape_string(str(int(args[0]))))
     else:
      self.statement='''set global interactive_timeout = 28800'''
     self.cursor.execute(self.statement)
 def get_interactive_timeout(self):
     self.statement='''SHOW VARIABLES LIKE "interactive_timeout"'''
     self.cursor.execute(self.statement)
     return int(self.cursor.fetchall()[0][1])
 def set_parameter_value(self,params):
     self.statement='''set global {}'''.format(self.dict_to_str(params,escape=False))
     self.cursor.execute(self.statement)
 def get_parameter_value(self,name):
     self.statement='''SHOW VARIABLES LIKE {}'''.format(self.real_escape_str(name))
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()
 def is_alive(self):
     if self.connection:
       return self.connection.open
     return False
 def add_parentheses(self,s):
     return " ( "+s+" ) "
 def real_escape_str(self,s):
     return self.connection.escape(s)
 def dict_to_str(self,data,in_seperator=' ',seperator=' , ',escape=True,parentheses=False):
    if escape==True:
      s= '''{}'''.format(seperator).join(['%s {} %s'.format(in_seperator) % (key, self.real_escape_str(value)) for (key, value) in data.items()])
    else:
      s= '''{}'''.format(seperator).join(['%s {} %s'.format(in_seperator) % (key, value) for (key, value) in data.items()])
    if parentheses==True:
        s=self.add_parentheses(s)
    return s
 def get_colums_format(self,row):
     return ''' , '''.join('{}'.format(pymysql.escape_string(col)) for col in row.keys())
 def get_values_format(self,row):
     return ''' , '''.join(self.real_escape_str(row[col]) for col in row.keys())
 def destroy(self):
     if self.cursor:
      self.cursor.close()
     if (self.connection) and ( self.is_alive()==True):
      self.connection.close()
     self.connection=None
     self.cursor=None
     self.statement=None
 def close(self,close_cursor=False):
     if (self.cursor) and (close_cursor==True):
         self.cursor.close()
     if (self.connection) and ( self.is_alive()==True):
      self.connection.close()
 def current_version(self):
     self.statement='''select version()'''
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()[0][0]
 def current_user(self):
     self.statement='''select CURRENT_USER()'''
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()[0]
 def change_password(self,user=None,password=""):
     if not user:
         user=self.current_user()[0]
     self.statement='''alter user {} identified by {}'''.format(user,self.real_escape_str(password))
     self.cursor.execute(self.statement)
 def create_user(self,user,password):
     self.statement='''create user if not exists {} identified by {}'''.format(user,self.real_escape_str(password))
     self.cursor.execute(self.statement)
 def drop_user(self,user):
     self.statement='''drop user if exists {}'''.format(user)
     self.cursor.execute(self.statement)
 def set_privileges(self,user,priv,db):
     self.statement='''grant {} on {} to {}'''.format(priv,db,user)
     self.cursor.execute(self.statement)
     self.cursor.execute('flush privileges')
 def revoke_privileges(self,user,priv,db):
     self.statement='''revoke {} on {} from {}'''.format(priv,db,user)
     self.cursor.execute(self.statement)
     self.cursor.execute('flush privileges')
 def show_privileges(self,user):
     self.statement='''show grants for {}'''.format(user)
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()
 def create_db(self,db):
     self.statement='''create database if not exists {}'''.format(db)
     self.cursor.execute(self.statement)
 def drop_db(self,db):
     self.statement='''drop database if exists {}'''.format(db)
     self.cursor.execute(self.statement)
 def use_db(self,db):
     self.statement='''use {}'''.format(db)
     self.cursor.execute(self.statement)
 def current_db(self):
     self.statement='''select database()'''
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()[0][0]
 def show_dbs(self):
     self.statement='''show databases'''
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()
 def show_tables(self):
     self.statement='''show tables'''
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()
 def describe_table(self,name):
     self.statement='''describe {}'''.format(name)
     self.cursor.execute(self.statement)
     return self.cursor.fetchall()
 def create_table(self,table,fields):
     self.statement='''create table if not exists {} ( {} )'''.format(table,self.dict_to_str(fields,escape=False))
     self.cursor.execute(self.statement)
 def rename_table(self,old,new):
     self.statement='''rename table {} to {}'''.format(old,new)
     self.cursor.execute(self.statement)
 def insert_into_table_format(self,table, row):
     cols = self.get_colums_format(row)
     vals = self.get_values_format(row)
     return '''insert into {} ( {} ) VALUES ( {} )'''.format(table, cols, vals)
 def insert_into_table(self,table,row):
     self.statement=self.insert_into_table_format(table,row)
     self.cursor.execute(self.statement)
 def reset_table(self,table):
     self.statement='''truncate table {}'''.format(table)
     self.cursor.execute(self.statement)
 def drop_table(self,table):
     self.statement='''drop table if exists {}'''.format(table)
     self.cursor.execute(self.statement)
 def add_column_format(self,table,columns):
     return '''alter table {} add {}'''.format(table,self.dict_to_str(columns,escape=False))
 def add_column(table,columns):
     self.statement=self.add_column_format(table,columns)
     self.cursor.execute(self.statement)
 def drop_column_format(self,table,column):
     return '''alter table {} drop column {}'''.format(table,column)
 def drop_column(table,column):
     self.statement=self.drop_column_format(table,columns)
     self.cursor.execute(self.statement)
 def rename_column_format(self,table,old,new):
     return '''alter table {} change {} {}'''.format(table,old,self.dict_to_str(new,escape=False))
 def rename_column(self,table,old,new):
     self.statement=self.rename_column_format(table,old,new)
     self.cursor.execute(self.statement)
 def modify_column_format(self,table,column):
     return '''alter table {} modify {}'''.format(table,self.dict_to_str(column,escape=False))
 def modify_column(self,table,old,new):
     self.statement=self.modify_column_format(table,old,new)
     self.cursor.execute(self.statement)
 def execute(self,statement,return_result=True):
     self.cursor.execute(statement)
     if return_result==True:
         return self.cursor.fetchall()
 def execute_many(self,statement,datalist,return_result=True):
     self.cursor.executemany(statement,datalist)
     if return_result==True:
         return self.cursor.fetchall()

def infos(host="localhost",username="root",password="",port=3306,timeout=5,ssl=None,database=None,cursorclass=pymysql.cursors.DictCursor,autocommit=True,charset='utf8',size=5,max_connections=10,keep_alive=True,check_interval=500,waiting=True,dynamic=True,blocking=True,unix_socket=None,sql_mode=None, read_default_file=None, conv=None, use_unicode=None, client_flag=0, init_command=None, read_default_group=None, compress=None, named_pipe=None, db=None, passwd=None, local_infile=False, max_allowed_packet=16777216, defer_connect=False, auth_plugin_map=None, read_timeout=None, write_timeout=None, bind_address=None, binary_prefix=False, program_name=None, server_public_key=None):#this function takes those values and return a dict which contains all necessary information to create a telnet session using those following class
  return {"host":host,"username":username,"password":password,"port":port,"timeout":timeout,"ssl":ssl,"database":database,"cursorclass":cursorclass,"autocommit":autocommit,"charset":charset,"size":size,"max_connections":max_connections,"keep_alive":keep_alive,"check_interval":check_interval,"waiting":waiting,"dynamic":dynamic,"blocking":blocking,"unix_socket":unix_socket,"sql_mode":sql_mode,"read_default_file":read_default_file,"conv":conv,"use_unicode":use_unicode,"client_flag":client_flag,"init_command":init_command,"read_default_group":read_default_group,"compress":compress,"named_pipe":named_pipe, "db":db, "passwd":passwd, "local_infile":local_infile, "max_allowed_packet":max_allowed_packet, "defer_connect":defer_connect, "auth_plugin_map":auth_plugin_map, "read_timeout":read_timeout, "write_timeout":write_timeout, "bind_address":bind_address, "binary_prefix":binary_prefix, "program_name":program_name, "server_public_key":server_public_key}

class pool:
 def __init__(self,info):
  self.pool=[]
  self.check_running=False
  self.used=0
  self.size=0
  self.configs=info
  self.rec=0
  self.available=0
  self.stop_conn_check=False
  self.th=None
  if (self.configs["size"]>self.configs["max_connections"]) or (self.configs["dynamic"]==False):
      self.configs["max_connections"]=self.configs["size"]
  for x in range(self.configs["size"]):
    t=threading.Thread(target=self.connect_to_host)#we are using threads to speed things up and connect to all hosts in a very short time (few seconds)
    t.start()
    time.sleep(0.001)
  while (self.size<self.configs["size"]):
      time.sleep(.01)
  self.available=len(self.pool)
  if self.configs["keep_alive"]==True:
    self.start_check()
 def connect_to_host(self):
  try:
   t=session(self.configs["host"],self.configs["username"],self.configs["password"],timeout=self.configs["timeout"],ssl=self.configs["ssl"],database=self.configs["database"],cursorclass=self.configs["cursorclass"],port=self.configs["port"],autocommit=self.configs["autocommit"],charset=self.configs["charset"],unix_socket=self.configs["unix_socket"], sql_mode=self.configs["sql_mode"], read_default_file=self.configs["read_default_file"], conv=self.configs["conv"], use_unicode=self.configs["use_unicode"], client_flag=self.configs["client_flag"], init_command=self.configs["init_command"], read_default_group=self.configs["read_default_group"], compress=self.configs["compress"], named_pipe=self.configs["named_pipe"], db=self.configs["db"], passwd=self.configs["passwd"], local_infile=self.configs["local_infile"], max_allowed_packet=self.configs["max_allowed_packet"], defer_connect=self.configs["defer_connect"], auth_plugin_map=self.configs["auth_plugin_map"], read_timeout=self.configs["read_timeout"], write_timeout=self.configs["write_timeout"],  bind_address=self.configs["bind_address"],  binary_prefix=self.configs["binary_prefix"],  program_name=self.configs["program_name"],  server_public_key=self.configs["server_public_key"])
   self.pool.append(t)
  except Exception as e:
   pass
  self.size+=1
 def get_connection(self,timeout=5):
  if len(self.pool)==0:
    if self.configs["blocking"]==True:
      if self.size==self.configs["max_connections"]:
        if self.configs["waiting"]==False:
            raise Exception("Maximum number of connections has been reached")
        else:
         ti=time.time()
         while(len(self.pool)==0):
              if int(time.time()-ti)==timeout:
                  raise Exception("Timed out")
              time.sleep(0.1)
         x=random.choice(self.pool)
         x.reconnect()
         self.pool.remove(x)
         self.used+=1
         self.available=len(self.pool)
         return x
      else:
          self.connect_to_host()
          x=random.choice(self.pool)
          x.reconnect()
          self.pool.remove(x)
          self.used+=1
          self.available=len(self.pool)
          return x
    else:
          self.connect_to_host()
          x=random.choice(self.pool)
          x.reconnect()
          self.pool.remove(x)
          self.used+=1
          self.available=len(self.pool)
          return x
  else:
      x=random.choice(self.pool)
      x.reconnect()
      self.pool.remove(x)
      self.used+=1
      self.available=len(self.pool)
      return x
 def start_check(self):
     if self.check_running==False:
      self.th=threading.Thread(target=self.keep_alive)
      self.th.daemon=True
      self.th.start()
      self.check_running=True
 def stop_check(self):
     self.check_running=False
     self.stop_conn_check=True
     del self.th
 def keep_alive(self):
    self.stop_conn_check=False
    while True:
     if self.stop_conn_check==True:
         break
     self.reconnect_all()
     ti=time.time()
     while True:
         if int(time.time()-ti)==self.configs["check_interval"]:
             break
         if self.pool==None:
             self.stop_conn_check=True
             break
         if self.stop_conn_check==True:
             break
         time.sleep(0.01)
 def reconnect_all(self):
    if self.pool:
      #if len(self.pool)>0:
       self.rec=0
       for x in self.pool:
         threading.Thread(target=self.reconnect_one,args=(x,)).start()
       while (self.rec<len(self.pool)):
          time.sleep(0.01)
 def reconnect_one(self,con):
    try:
      con.reconnect()
      self.rec+=1
    except:
        self.kill_connection()
        self.connect_to_host
        self.rec+=1
 def set_check_interval(self,interval):
     self.stop_check()
     self.configs["check_interval"]=interval
     self.start_check()
 def close_connection(self,con):
     if len(self.pool)>=self.configs["max_connections"]:
         self.kill_connection(con)
         return
     con.reconnect()
     self.used-=1
     self.pool.append(con)
     self.available=len(self.pool)
 def kill_connection(self,con):
     con.destroy()
     self.size-=1
     self.used-=1
     if con in self.pool:
         self.pool.remove(con)
     del con
     self.available=len(self.pool)
 def destroy(self):
     for x in self.pool:
         x.destroy()
         self.pool.remove(x)
         del x
     self.pool=None
     self.used=None
     self.size=None
     self.configs=None
     self.rec=None
     self.stop_check()
     self.stop_conn_check=None
     self.available=None
