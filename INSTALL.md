Rough Guide to Informix Environment on Linux (Ubuntu 12.04)
-----------------------------------------------------------

1) install pyodbc and unixodbc

http://code.google.com/p/pyodbc/
http://www.unixodbc.org/

In order to install InformixDB, we need the Informix drivers and SD:

2) install informix client sdk

search for

Informix Downloads Client Software Development Kit

http://www14.software.ibm.com/webapp/download/search.jsp?rs=ifxdl

chose:

Informix Downloads (Informix Client SDK Developer Edition for Linux x86_64, 64-bit)

A single packaging of several application programming interfaces (APIs) for rapid, cost-effective development of applications for IBM Informix servers.
    4.10.FC1DE  Released product    26 Mar 2013     1KB     Linux for System x86-64

extract tarball into a temp dir (otherwise tar xvf puts everything into current directory)

execute ./installclientsdk

3) add hosts to /opt/ibm/informix/etc/sqlhosts

wilson  onsoctcp    wilson  informix

4) install informixdb, which SQLAlchemy needs to communicate with informix databases.

see:
http://docs.sqlalchemy.org/en/rel_0_8/dialects/informix.html

download:

https://pypi.python.org/pypi/InformixDB/

or

http://informixdb.sourceforge.net/

5) fail

python setup.py build_ext

running build_ext
sh: /usr/informix/bin/esql: not found
sh: /usr/informix/bin/esql: not found
error:
Can''t find esql. Please set INFORMIXDIR correctly.

6) Declare the informix directory with esql-informixdir flag:

python setup.py build_ext --esql-informixdir=/opt/ibm/informix/

7) sudo su - root

export INFORMIXDIR=/opt/ibm/informix

python setup.py install

8) error

Sqlhosts file not found or cannot be opened.

9) create user/group

sudo groupadd informix ; sudo useradd -g informix -d /dev/null informix

chown -R informix:informix /opt/ibm/informix/

10) export ODBCINI=/opt/ibm/informix/etc/odbc.ini

from command line and put in .bash_aliases

11) Cannot locate informix service/tcp service in /etc/services.

12) add to /etc/services

informix    18001/tcp           # informix

just after port 17004 entry
