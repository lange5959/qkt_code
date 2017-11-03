# coding=utf-8

import sqlite3
import time
import random
import datetime


conn = sqlite3.connect("sg_data.db")
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS versionCheck(code TEXT, version_number INTEGER, data TEXT, status BOOLEAN)")


def data_entry():
    c.execute("INSERT INTO versionCheck VALUES('test.hip', 2, '2017-05-14 23:11:30', 0)")
    conn.commit()
    c.close()
    conn.close()

def dynamic_data_entry():
    current_time = time.time()


create_table()
data_entry()

