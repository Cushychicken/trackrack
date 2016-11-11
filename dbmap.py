from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Board(Base):
    __tablename__ = 'boards'

    id          = Column(Integer, primary_key=True)
    owner       = Column(Text)
    mac_addr    = Column(Text)
    board_no    = Column(Text)
    last_update = Column(Text) 

    def __repr__(self):
        return "<Board(owner='%s', mac_addr='%s', board_no='%s', last_update='%s')>" % (self.owner, self.mac_addr, self.board_no, self.last_update)
   
class Note(Base):
    __tablename__ = 'notes'

    id          = Column(Integer, primary_key=True)
    info        = Column(Text)
    board_no    = Column(Text)
    time        = Column(Text)

    def __repr__(self):
        return "<Note(info='%s', board_no='%s', time='%s')>" % (self.info, self.board_no, self.time)

engine = create_engine('sqlite:///tests/demo_board.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


