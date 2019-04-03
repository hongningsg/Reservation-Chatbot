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
        c.execute('''
            create table timeslot (
            id integer primary key autoincrement,
            doc_id integer,
            start integer,
            status integer,
            reserved_by text,
            foreign key (doc_id) references dentist (id))
        ''')
        for id in range(1, 4):
            for i in range(9, 18):
                c.execute("insert into timeslot (doc_id, start, status, reserved_by) values (?, ?, ?, ?)", (id, i, 0, None))
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

def getDocTime(id, db_name = 'data.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from timeslot where doc_id = %s" % id)
    return conn, c

def timeNormal(time):
    available_time = [
        '9', '10', '11', '12', '13', '14', '15', '16', '17'
    ]
    availability = True
    if time not in available_time:
        availability = False
    return availability


def book(id, time, current_user, db_name = 'data.db'):
    availability = timeNormal(time)
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from timeslot where doc_id = %s and start = %s and status = 0" % (id, time))
    reserve = c.fetchone()
    if reserve == None:
        conn.close()
        return False, -1
    if availability:
        c.execute("update timeslot set status = 1, reserved_by = '%s' where doc_id = %s and start = %s" % (current_user, id, time))
        conn.commit()
    conn.close()
    return availability, reserve['id']

def cancel(id, time, current_user, db_name = 'data.db'):
    availability = timeNormal(time)
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from timeslot where doc_id = %s and start = %s and status = 1 and reserved_by = '%s'" % (id, time, current_user))
    if c.fetchone() == None:
        conn.close()
        return False
    if availability:
        c.execute("update timeslot set status = 0, reserved_by = null where doc_id = %s and start = %s" % (id, time))
        conn.commit()
    conn.close()
    return availability

def closestTime(id, db_name = 'data.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from timeslot where doc_id = %s and status = 0" % id)
    return conn, c.fetchone()

def cancelID(id, current_user, db_name = 'data.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from timeslot where (id = %s and status = 1 and reserved_by = '%s')" % (id, current_user))
    if c.fetchone() == None:
        conn.close()
        return False
    else:
        c.execute("update timeslot set status = 0, reserved_by = null where id = %s" % id)
        conn.commit()
    conn.close()
    return True
