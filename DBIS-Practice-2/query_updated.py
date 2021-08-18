'''Костенко Владислав КМ-82 Варіант 9
Порівняти найгірший бал з Математики у кожному регіоні у 2020 та 2019 роках серед тих кому було зараховано тест'''
import logging
import psycopg2
import csv

with open('results.log', 'w'):
    pass
logging.basicConfig(level=logging.DEBUG, filename='results.log', format='%(asctime)s - %(message)s')

def query_data(cur):
    '''Gets data from database'''
    
    query= '''
        SELECT L.REGION,
            Z.EXAM_YEAR,
            MIN(Z.BALL100) AS MINMATHBALL
        FROM ZNORESULT Z
        INNER JOIN PERSON P ON Z.PERSON_ID = P.PERSON_ID
        INNER JOIN LOCATION L ON L.LOCATION_ID = P.LOCATION_ID
        WHERE Z.TEST_NAME = 'Математика'
                        AND TEST_STATUS = 'Зараховано'
        GROUP BY L.REGION,
            Z.EXAM_YEAR
        ORDER BY MINMATHBALL;
        '''
    
    cur.execute(query)
    
    return cur

def form_csv(cur):
    '''Forms csv file'''
    with open('result.csv', 'w', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Область', 'Рік', 'Мін. бал з математики'])
        for row in cur:
            csv_writer.writerow(row)
    logging.info('CSV file formed')

if __name__ == '__main__':

    try:

        # connect to the PostgreSQL server
        logging.info('Connecting to the PostgreSQL database')
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres")

    except psycopg2.OperationalError as e:

        logging.info("Can't connect to database. Trying again")
        restored = False
        while not restored:
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        database="postgres",
                        user="postgres",
                        password="postgres")
                    cur = conn.cursor()
                    logging.info('Connection restored')
                    restored = True
                except psycopg2.OperationalError as err:
                    pass

    cur = conn.cursor()

    form_csv(query_data(cur))
    
    cur.close()
    conn.close()
    logging.info('Database connection closed.')
