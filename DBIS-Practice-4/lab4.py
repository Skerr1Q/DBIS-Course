'''Костенко Владислав Варіант 9
Порівняти найгірший бал з Математики у кожному регіоні
у 2020 та 2019 роках серед тих кому було зараховано тест'''

from pymongo import MongoClient
import csv
import logging
import time
import sys
import re

with open('results.log', 'w'):
    pass
with open('results.csv', 'w'):
    pass
logging.basicConfig(level=logging.DEBUG, filename='results.log',
                    format='%(asctime)s - %(message)s')


def parse(row, year):
    '''Parses rows deleting nulls and casting variables to needed types'''
    parsed_dict = {}
    for k, v in row.items():
        if v != 'null':
            k = k.lower().strip()
            v = v.strip().replace("'", "").replace(",", ".").replace('"', "")
            if k == 'birth':
                parsed_dict[k] = int(v)
            elif 'ball' in k:
                parsed_dict[k] = float(v)
            else:
                parsed_dict[k] = v

    parsed_dict['exam_year'] = int(year)
    return parsed_dict


def inserted_data(collection, filename, batch_size=1000):
    '''Insert data in batches to collection'''
    logging.info(f'Inserting data from {filename}')
    time_start = time.time()

    col_i = 0
    batch_arr = []

    try:
        with open(filename, "r", encoding="cp1251") as csv_file:

            year = re.findall(r'\d{4}', filename)[0]
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                parsed_row = parse(row, year)
                batch_arr.append(parsed_row)
                col_i += 1

                if col_i == batch_size:
                    try:
                        collection.insert_many(batch_arr)
                        batch_arr = []
                        col_i = 0

                    except:
                        return False

        # add the rest of documents
        if batch_arr:
            try:
                collection.insert_many(batch_arr)
            except:
                return False

        time_end = time.time()
        logging.info(
            f'Time to insert data from {filename}: {time_end - time_start}')

    except FileNotFoundError as err:
        logging.info("Error with opening files. Check their presence")
        return False

    return True


def query_agg(collection):
    '''Perform statistical query on data'''
    result = collection.aggregate([

        {"$match": {"mathteststatus": "Зараховано"}},

        {"$group": {
            "_id": {
                "region": "$regname",
                "year": "$exam_year"
            },
            "min_score": {
                "$min": "$mathball100"
            }
        }},

        {"$sort": {"_id": 1
        }}
    ])

    return result


def form_csv(query):
    '''Forms csv file'''
    with open('results.csv', 'w', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Область', 'Рік', 'Мін. бал з математики'])
        for row in query:
            csv_writer.writerow([row["_id"]["region"],
                                 row["_id"]["year"], row["min_score"]])

    logging.info('CSV file formed')

def try_connected(client):
    '''Checks connection to server'''
    try:
        client.admin.command('ismaster')
        return True
    except:
        logging.info("Can't connect to database. Trying again")
        return False

    return client
def main(db_name, collection_name, host, port):

    filenames = ['Odata2019File.csv', 'Odata2020File.csv']
    
    # Connecting to MongoDB
    connect_i = 0
    client = MongoClient(
        host, port)

    #trying to connect 10 times
    while not try_connected(client):
        time.sleep(3)
        if connect_i < 10:
            client = MongoClient(
                        host, port)
            connect_i +=1
        else:
            logging.info("Can't connect to database. Check connection")
            return

    logging.info("Connection created.")

    db = client[db_name]
    db[collection_name].drop()
    collection = db[collection_name]

    for f in filenames:
        if not inserted_data(collection, f):
            logging.info('Error while inserting files')
            return

    query = query_agg(collection)
    form_csv(query)

    #drops the collection, comment if needed
    collection.drop()

    client.close()
    logging.info('Connection closed')


if __name__ == "__main__":

    db_name = 'zno_db'
    collection_name = 'zno_collection'
    python_file, host, port = sys.argv
    port = int(port)

    main(db_name, collection_name, host, port)
