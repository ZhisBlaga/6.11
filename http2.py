from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine("sqlite:///albums.sqlite3")
Base = declarative_base()

#Описание таблицы

class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.Integer, primary_key=True)
    year = sa.Column(sa.Integer)
    artist = sa.Column(sa.String)
    genre = sa.Column(sa.String)
    album = sa.Column(sa.String)


Sessions = sessionmaker(engine)

session = Sessions()


#Описание GET запросов
@route('/albums/<artist>', method='GET')
def get_albums(artist):
    string=''
    count = session.query(Album).filter_by(artist=artist).count()
    for row in session.query(Album).filter_by(artist=artist).all():
            string += row.album+'<br>'                  #BR для вывода по строчно
    return ' Всего альбомов: <strong>{}</strong>'.format(count)+'<br><br> Список всех альбомов группы <strong>{}</strong>:<br>'.format(artist),string

#Описание POST запросов
@route("/albums", method="POST")
def add_albums():
    year = (request.forms.get("year"))
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album = request.forms.get("album")

    #Проверяем что год валидный, если будет ошибка преобразованя в чило отловим ошибку ValueError
    try:
        year = int(year)
        if 1800 <= year <= 2020:
            #Проверяем наличние альбома не только по имени альбома но и по артисту.
            count = session.query(Album).filter_by(artist=artist,album=album).count()
            
            if count==0:
                new_album =Album(
                    year = year,
                    artist=artist,
                    genre=genre,
                    album=album
                  )
                session.add(new_album)
                session.commit()
                result = 'Данные добавленны в БД'
            else:
                result = HTTPError(409, 'Такой альбом есть в БД')

        else:
            result = HTTPError(409, 'Проверьте год выпуска альбома')
        return result
    except ValueError as err:
        result = HTTPError(409, err)
        return result

if __name__ == "__main__":

    run(host="localhost", port=8080, debug=True)
