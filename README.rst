in_memory_ip_to_location_look_up
================================

Query mysql database, create in-memory database for fast lookup.

This project aims to be model of ip to location services, used to create localized CDN.

    :: TO BUILD 

- Collect IP address, location and use example ipparser.py to create a csv file to import to mysql database
- create a mysql database name geoip, have just one table with structure:

::

    mysql> desc ip_detail 
    -> ;
    +----------+----------+------+-----+---------+-------+
    | Field    | Type     | Null | Key | Default | Extra |
    +----------+----------+------+-----+---------+-------+
    | beginIP  | char(20) | NO   |     | NULL    |       |
    | endIP    | char(20) | NO   |     | NULL    |       |
    | beginNUM | int(15)  | NO   |     | NULL    |       |
    | endNUM   | int(15)  | NO   | PRI | NULL    |       |
    | ISP      | char(10) | NO   |     | NULL    |       |
    | location | char(20) | NO   |     | NULL    |       |
    | service  | char(20) | NO   |     | NULL    |       |
    +----------+----------+------+-----+---------+-------+
    7 rows in set (0.03 sec)

:: 

- Modify configuration and start using this project. 




HomePage: http://blog.tinytechie.net 


