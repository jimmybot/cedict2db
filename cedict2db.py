import re
import sqlite3

from pinyin import decode_pinyin

INPUT_FILENAME = 'data/source/cedict_ts.u8'
DB_FILENAME = 'data/derived/cedict.db'
CE_TABLE_NAME = 'cedict'
EC_TABLE_NAME = 'ecdict'

entryRE = re.compile('(\S+) (\S+) \[([^\]]+)\] (.+)')

def parse_entry(line):
    result = entryRE.findall(line)
    if len(result) == 1:
        traditional, simplified, raw_pinyin, definitions = result[0]

        pinyin = decode_pinyin(raw_pinyin)

        # remove the '/' that separates and bookends the definitions
        definitions = definitions[1:-1]
        definition_list = definitions.split('/')

        return (traditional, simplified, pinyin, definition_list)
    else:
        raise Exception('Error parsing entry: original=%s result=%s' % (line, result))

def read_file(filename, parse_fn):
    entries = []
    with open(filename) as infile:
        for line in infile:
            if not line.startswith('#'):
                entries.append(parse_fn(line))
    return entries

def write_data(entries, db_filename, ce_table_name, ec_table_name):
     with sqlite3.connect(db_filename) as conn:
         conn.execute('DROP TABLE IF EXISTS %s' % ce_table_name)
         conn.execute('DROP TABLE IF EXISTS %s' % ec_table_name)
         conn.execute('CREATE TABLE %s(traditional TEXT, simplified TEXT, pinyin TEXT, definitions TEXT)' % ce_table_name)
         conn.execute('CREATE TABLE %s(english TEXT, traditional TEXT, simplified TEXT, pinyin TEXT)' % ec_table_name)
         for traditional, simplified, pinyin, definition_list in entries:
             conn.execute('INSERT INTO %s VALUES(?, ?, ?, ?)' % ce_table_name, (traditional, simplified, pinyin, ' | '.join(definition_list)))
             for definition in definition_list:
                 conn.execute('INSERT INTO %s VALUES(?, ?, ?, ?)' % ec_table_name, (definition, traditional, simplified, pinyin))

if  __name__ == '__main__':
    entries = read_file(INPUT_FILENAME, parse_entry)
    write_data(entries, DB_FILENAME, CE_TABLE_NAME, EC_TABLE_NAME)

