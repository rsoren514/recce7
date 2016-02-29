# Creates a test sqlite DB for use in the 'jsontest' and 'jsontest2' tests.
# NOTE: Need to run this to create the DB before running the other two tests!

import sqlite3

# Creates a SQLite DB with 2 tables for test purposes

def addcv(c):
    c.execute('''CREATE TABLE Castlevania (title text, system text, datetime text)''')

    c.execute("INSERT INTO Castlevania VALUES ('Castlevania','NES','1987-05-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania II: Simons Quest','NES','1988-12-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Haunted Castle','Arcade','1988-09-22T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: The Adventure','Game Boy','1989-12-15T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania III: Draculas Curse','NES','1990-09-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania II: Belmonts Revenge','Game Boy','1991-08-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Super Castlevania IV','SNES','1991-12-04T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Kid Dracula','Game Boy','1993-03-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Bloodlines','Sega Genesis','1994-03-17T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Dracula X','SNES','1995-09-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Symphony of the Night','PlayStation',"
              "'1997-10-02T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania Legends','Game Boy','1998-03-11T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania 64','N64','1998-12-31T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Legacy of Darkness','N64','1999-11-30T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Circle of the Moon','GBA','2001-06-11T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania Chronicles','PlayStation','2001-10-08T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Harmony of Dissonance','GBA','2002-09-16T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Aria of Sorrow','GBA','2003-05-06T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Lament of Innocence','PlayStation 2',"
              "'2003-10-21T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Dawn of Sorrow','DS','2005-10-04T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Curse of Darkness','PlayStation 2','2005-11-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Curse of Darkness','Xbox','2005-11-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Portrait of Ruin','DS','2006-12-05T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: The Dracula X Chronicles','PSP','2007-10-23T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Rondo of Blood','Virtual Console','2008-01-01T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Order of Ecclesia','DS','2008-10-21T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania Judgment','Wii','2008-11-18T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: The Adventure ReBirth','WiiWare','2009-12-28T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania Puzzle: Encore of the Night','iOS','2010-07-16T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Harmony of Despair','Xbox Live Arcade',"
              "'2010-08-04T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Lords of Shadow','Playstation 3','2010-10-05T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Lords of Shadow','Xbox 360','2010-10-05T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Lords of Shadow - Mirror of Fate','3DS',"
              "'2013-03-05T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Lords of Shadow 2','PlayStation 3','2014-02-25T00:00:00')")
    c.execute("INSERT INTO Castlevania VALUES ('Castlevania: Lords of Shadow 2','Xbox 360','2014-02-25T00:00:00')")

def addloz(c):
    c.execute('''CREATE TABLE Zelda (title text, system text, year text)''')

    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda','NES','1987')")
    c.execute("INSERT INTO Zelda VALUES ('Zelda II: The Adventure of Link','NES','1988')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: A Link to the Past','SNES','1992')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Links Awakening','Game Boy','1993')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Ocarina of Time','N64','1998')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Majoras Mask','N64','2000')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Oracle of Ages','Game Boy Color','2001')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Oracle of Seasons','Game Boy Color','2001')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: The Wind Waker','GameCube','2003')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Four Swords Adventures','GameCube','2004')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: The Minish Cap','GBA','2005')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Twilight Princess','GameCube','2006')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Twilight Princess','Wii','2006')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Phantom Hourglass','DS','2007')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Spirit Tracks','DS','2009')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Skyward Sword','Wii','2011')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: A Link Between Worlds','3DS','2013')")
    c.execute("INSERT INTO Zelda VALUES ('The Legend of Zelda: Tri Force Heroes','3DS','2015')")

def main():
    print("Starting Main.")
    conn = sqlite3.connect('GameSeries.db')
    c = conn.cursor()
    addcv(c)
    addloz(c)
    conn.commit()
    y = ('NES',)
    c.execute("SELECT * FROM Castlevania WHERE system=?", y)
    print("Castlevania NES games")
    print(c.fetchall())

    c.execute("SELECT * FROM Zelda WHERE system=?", y)
    print("Zelda NES games")
    print(c.fetchall())

    conn.close()

if __name__ == "__main__": main()