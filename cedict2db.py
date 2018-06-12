import re
import sqlite3

INPUT_FILENAME = 'data/source/cedict_ts.u8'
DB_FILENAME = 'data/derived/cedict.db'
TABLE_NAME = 'cedict'

entryRE = re.compile('(\S+) (\S+) \[([^\]]+)\] (.+)')

def parse_entry(line):
    result = entryRE.findall(line)
    if len(result) == 1:
        return result[0]
    else:
        raise Exception('Error parsing entry: original=%s result=%s' % (line, result))

def read_file(filename, parse_fn):
    entries = []
    with open(filename) as infile:
        for line in infile:
            if not line.startswith('#'):
                entries.append(parse_fn(line))
    return entries

def write_data(entries, db_filename, table_name):
     with sqlite3.connect(db_filename) as conn:
         conn.execute('DROP TABLE IF EXISTS %s' % table_name)
         conn.execute('CREATE TABLE %s(traditional TEXT, simplified TEXT, pinyin TEXT, definitions TEXT)' % table_name)
         for entry in entries:
             conn.execute('INSERT INTO cedict VALUES(?, ?, ?, ?)', entry)

if  __name__ == '__main__':
    entries = read_file(INPUT_FILENAME, parse_entry)
    write_data(entries, DB_FILENAME, TABLE_NAME)

