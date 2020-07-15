import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class  Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album" 

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums



@route("/albums/<artist>")
def albums(artist):

    album_l = find(artist)
    album_n=[album.album for album in album_l]
    res=("Количество Альбомов исполнителя {} - {} <br>".format(artist,len(album_n)))
    res += "<br>".join(album_n)
    return res









def find_a(album):
    """
    Находит альбомы в базе данных по заданному имени
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.album == album).all()
    return albums
    
        



@route("/albums", method="POST")
def albums_add():
   
        
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album = request.forms.get("album")
 
        



    try:
        int(year)
    except(ValueError):
        result = HTTPError(404, "Год необходимо указать цифрами")
    else:
        if len(year)!=4:
            result = HTTPError(404, "Некорректно указан год")
        else:
            if(find_a(album)):
                result = HTTPError(409, "Такой Альбом уже существует")
            else:
                session=connect_db()
                new_alb=Album(year=year,artist=artist, genre=genre, album=album)
                session.add(new_alb)
                session.commit()

                result = "альбом {} добавлен".format(album)  
    
    return result    


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)    