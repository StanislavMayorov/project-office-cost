import cx_Oracle

#con = cx_Oracle.connect('STAS/1234@127.0.0.1/orcl')
con = cx_Oracle.connect('jdbc:oracle:thin:@//localhost:1521/XE')
print(con.version)
con.close()
