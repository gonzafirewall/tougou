* tougou ejecutable desde Linea de comandos 
  con Settings para preguntar sobre hosts en los plugins.
  Detalles:
     referencia:  http://docopt.org/
               tougou -s SETTINGS.conf -h [default: all]
               Por default intenta configurarse buscando un archivo settings.conf
               en el directorio de ejecución. O en /etc/tougou/settings.conf en ese orden.

    SETTINGS.conf --
        [MODULO]_URL
        [MODULO]_PORT default: 80
        [MODULO]_USER
        [MODULO]_PWD

    ejemplo de settings.conf
        NAGIOS3_URL: http://intranet.quicuo.com.ar
        NAGIOS3_USER: nagiosadmin
        NAGIOS3_PWD: AlgunaPass
