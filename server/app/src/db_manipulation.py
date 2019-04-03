#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute("select * from user")
    except:
        c.execute('''
            create table user (
            username text primary key,
            password text)
        ''')
        c.execute("insert into user values ('admin', 'password')")
        conn.commit()
    conn.close()

def validate(username, password, db_name = 'data.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from user where username = '%s' and password = '%s'" % (username, password))
    v = c.fetchone()
    conn.close()
    if v == None:
        return False
    else:
        return True

def register(username, password, db_name = 'data.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from user where username = '%s'" % username)
    v = c.fetchone()
    if v == None:
        c.execute("insert into user values ('%s', '%s')" % (username, password))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
