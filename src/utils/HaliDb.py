# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2010 Olle Johansson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import mapper, sessionmaker


class HaliData(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HaliDb(object):
    """
    SQLAlchemy wrapper class that sets up at simple key/value database.
    """

    def __init__(self, debug):
        self.engine = create_engine('sqlite:///extras/halidata.db', echo=debug)
        self.setup_session()
        self.setup_tables()

    def setup_session(self):
        """
        Start a SQLAlchemy db session.

        Saves the session instance in C{self.session}
        """
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def setup_tables(self):
        """
        Defines the tables to use for L{User} and L{Tell}.

        The Metadata instance is saved to C{self.metadata}
        """
        self.metadata = MetaData()
        halidata_table = Table('halidata', self.metadata,
            Column('key', String(50), primary_key=True),
            Column('value', String(255)),
        )
        mapper(HaliData, halidata_table)
        self.metadata.create_all(self.engine)

    def get(self, key):
        hd = self.session.query(HaliData).filter_by(key=key).first()
        if not hd:
            hd = HaliData(key, None)
            self.session.add(hd)
        return hd

    def get_value(self, key):
        hd = self.get(key)
        if hd:
            return hd.value
        return None

    def set_value(self, key, value):
        hd = self.get(key)
        hd.value = value
        self.session.commit()

    def del_key(self, key):
        hd = self.get(key)
        self.session.delete(hd)
        self.session.commit()

