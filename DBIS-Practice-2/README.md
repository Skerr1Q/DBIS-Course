## DBIS-Practice-2 Костенко Владислав КМ-82 Варіант 9

### Інструкція до запуску
Додати в папку проекта csv-файли з даними ЗНО: "Odata2019File.csv" та "Odata2020File.csv".\
Запустити через консоль файл query.py за допомогою команди: `python query.py` для отримання бази даних з КП1\
Почати міграцію за допомогою команди: `flyway migrate -url=<url> -user=<user> -password=<password>`\
( за замовчуванням `-url=jdbc:postgresql://localhost:5432/postgres -user=postgres -password=postgres` )\
Запустити через консоль файл query_updated.py за допомогою команди: `python query_updated.py` для отримання файлу csv

### Директорія до запуску
 - sql
     - drop_table.sql
     - V1__create_table.sql
     - V2__insert_data.sql
 - Odata2019File.csv
 - Odata2020File.csv
 - query.py
 - physicalerd.png
 - logicalerd.png
 - query_updated.py
 - flyway.conf

### Директорія після запуску
 - sql
     - drop_table.sql
     - V1__create_table.sql
     - V2__insert_data.sql
 - Odata2019File.csv
 - Odata2020File.csv
 - query.py
 - physicalerd.png
 - logicalerd.png
 - query_updated.py
 - flyway.conf
 - result.csv
 - results.log
