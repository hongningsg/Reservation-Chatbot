import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def nameNormalize(name):
    name = name.split()
    normal_name = []
    for name_part in name:
        firstC = name_part[0].upper()
        normal_name.append(firstC + name_part[1:])
    return " ".join(normal_name)


def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute("select * from dentist")
    except:
        c.execute('''
            create table dentist (
            id integer primary key autoincrement,
            name text,
            location text,
            spec text)
        ''')
        c.execute("insert into dentist (name, location, spec) values ('Tony Stark', '10880 Malibu Point', 'Paediatric Dentistry')")
        c.execute("insert into dentist (name, location, spec) values ('Bruce Banner', '500 S. Buena Vista Street', 'Orthodontics')")
        c.execute("insert into dentist (name, location, spec) values ('Peter Parker', '20 Ingram Street', 'Oral Surgery')")
        conn.commit()
    conn.close()

def dentist_list(name, db_name = 'data.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    if name == '*':
        c.execute("select * from dentist")
    else:
        name = nameNormalize(name)
        c.execute("select * from dentist where name like '%%%s%%'" % name)
    return conn, c