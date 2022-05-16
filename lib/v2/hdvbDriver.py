import re
import time
from db.mydb import Database
import aiohttp
from typing import List


class YaspellerResponse:
    uncorrect: str
    correct: str

    def __init__(self, uncorrect: str, correct: str):
        self.uncorrect = uncorrect
        self.correct = correct

    def __str__(self):
        return str({'uncorrect': self.uncorrect, 'correct': self.correct})


class Film:
    title: str
    iframe_url: str
    kinopoisk_id: int
    year: int
    quality: str
    poster: str
    rating: int
    ftype: str
    ftoken: str

    def __init__(self, title='', iframe_url='', kinopoisk_id=0, year=0, quality='', poster='', rating=0, ftype='', ftoken=''):
        self.title = title
        self.iframe_url = iframe_url
        self.kinopoisk_id = kinopoisk_id
        self.year = year
        self.quality = quality
        self.poster = poster
        self.rating = rating
        self.ftype = ftype
        self.ftoken = ftoken

    def __str__(self):
        return str({
            'title': self.title,
            'iframe_url': self.iframe_url,
            'kinopoisk_id': self.kinopoisk_id,
            'year': self.year,
            'quality': self.quality,
            'poster': self.poster,
            'rating': self.rating,
            'ftype': self.ftype,
            'ftoken': self.ftoken
        })


class KPResponse:

    filmID: int
    title: str
    year: str
    length: str
    description: str
    genres: list
    rating: str

    def __init__(self, obj: dict = {}):
        if obj:
            d = obj['data']
            t = obj['rating']
            self._obj = obj
            self.filmID = d['filmId']
            self.title = d['nameRu']
            self.year = d['year']
            self.length = d['filmLength']
            self.description = d['description']
            self.rating = t['rating']
            self.ratingImdb = t['ratingImdb']
            self.genres = [list(g.items())[0][1] for g in d['genres']]
            del d, obj
        else:
            self.filmID = 0
            self.title = ''
            self.year = ''
            self.length = ''
            self.description = ''
            self.genres = []
            self.rating = 0
            self.ratingImdb = 0

    def __str__(self):
        return str(self._obj)


async def _yaspeller(title: str) -> List[YaspellerResponse]:
    u, p = 'https://speller.yandex.net/services/spellservice.json/checkText', {
        'lang': 'ru', 'text': title}
    async with aiohttp.ClientSession() as session:
        async with session.get(u, params=p) as resp:
            resp_json = await resp.json()
            return [YaspellerResponse(uncorrect=i['word'], correct=i['s'][0]) for i in resp_json]


async def _sampling_films(films: list, film_title: str) -> List[List[int]]:
    """находит наибольшее кол-во совпадение в название фильма"""
    fts = re.split('\s|-|:|\.', film_title.lower().replace('ё', 'е'))
    len_fts, len_films = len(fts), len(films)

    result = [[] for _ in range(len_fts+1)]

    for film_index in range(len_films):
        f_title = re.split(
            '\s|-|:|\.', films[film_index]['title_ru'].lower().replace('ё', 'е'))

        k = 0
        for title_word in fts:
            if title_word in f_title:
                k += 1
        if k != 0:
            result[len_fts - k].append(film_index)

    return result


async def _sorted_films(films: List[Film]) -> List[Film]:
    """Сортировка фильмов по году выпуска"""
    return sorted(films, key=lambda film: film.year)


class HDVB:

    def __init__(self, hdvb_token: str, kp_token: str, db: Database):
        self._hdvb_token = hdvb_token
        self._kp_token = kp_token
        self._base_hdvb_url = 'https://apivb.info/api/'
        self._base_kp_films_url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/'
        self._db = self.DataBrowser(db)

    async def _fetch_hdvb(self, method: str, *args, **kwargs) -> dict:
        kwargs['token'] = self._hdvb_token
        async with aiohttp.ClientSession() as session:
            async with session.get(self._base_hdvb_url + method, params=kwargs) as resp:
                try:
                    return await resp.json()
                except Exception as e:
                    print(e)
                    return []

    async def _fetch_kp_films(self, method: str, kp_id: int) -> dict:
        async with aiohttp.ClientSession(headers={'X-API-KEY': self._kp_token}) as session:
            async with session.get(f'{self._base_kp_films_url}{kp_id}?append_to_response=RATING') as resp:
                try:
                    resp_json = await resp.json()
                    if not resp_json.get('data', 'rating'):
                        raise Exception(resp_json)
                    return resp_json
                except Exception as e:
                    print(e)
                    return {}

    async def find_by_title(self, title: str, limit: int = 25) -> List[Film]:
        films = []
        resp_json = await self._fetch_hdvb('videos.json', title=title)

        if type(resp_json) == list and not resp_json:
            speller_check = await _yaspeller(title)
            for word in speller_check:
                title = title.replace(word.uncorrect, word.correct)
            resp_json = await self._fetch_hdvb('videos.json', title=title)

        if type(resp_json) == list and resp_json:
            sort_films_index = await _sampling_films(resp_json, title)

            k = 0
            kp_ids = {}

            for films_index in sort_films_index:
                for i in films_index:
                    if k >= limit:
                        return await _sorted_films(films)

                    if not kp_ids.get(resp_json[i]['kinopoisk_id']):
                        films.append(
                            Film(
                                title=resp_json[i]['title_ru'],
                                iframe_url=resp_json[i]['iframe_url'],
                                kinopoisk_id=resp_json[i]['kinopoisk_id'],
                                year=resp_json[i]['year'],
                                quality=resp_json[i]['quality'],
                                poster=resp_json[i]['poster'],
                                ftype=resp_json[i]['type'],
                                ftoken=resp_json[i]['token'],
                            )
                        )
                        kp_ids[resp_json[i]['kinopoisk_id']] = 1
                        k += 1

        elif type(resp_json) == dict:
            print(resp_json)

        return await _sorted_films(films)

    async def find_by_kp_id(self, kp_id: int) -> Film:
        resp_json = await self._fetch_hdvb('videos.json', id_kp=kp_id)

        if type(resp_json) == list:
            return Film(
                title=resp_json[0]['title_ru'],
                iframe_url=resp_json[0]['iframe_url'],
                kinopoisk_id=resp_json[0]['kinopoisk_id'],
                year=resp_json[0]['year'],
                quality=resp_json[0]['quality'],
                poster=resp_json[0]['poster'],
                ftype=resp_json[0]['type'],
                ftoken=resp_json[0]['token'],
            )

        elif type(resp_json) == dict:
            print(resp_json)

        return Film()

    async def find_by_ftoken(self, ftype: str, ftoken: str) -> Film:
        resp_json = await self._fetch_hdvb(f'{ftype}.json', video_token=ftoken)

        if resp_json:
            return Film(
                title=resp_json['title_ru'],
                iframe_url=resp_json['iframe_url'],
                kinopoisk_id=resp_json['kinopoisk_id'],
                year=resp_json['year'],
                quality=resp_json['quality'],
                poster=resp_json['poster'],
                ftype=resp_json['type'],
                ftoken=resp_json['token'],
            )
        return Film()

    async def get_film_info(self, kp_id: int) -> KPResponse:
        resp_json = await self._fetch_kp_films('', kp_id)
        if resp_json:
            return KPResponse(resp_json)
        return KPResponse()

    async def get_popular_films(self) -> List[Film]:
        popular_films = await self._db.get_popular_films()
        films = [0]*len(popular_films)

        i = 0
        for f in popular_films:
            films[i] = Film(kinopoisk_id=f[0], rating=f[1],
                            title=f[2], poster=f[3], year=f[4], quality=f[5], ftoken=f[6])
            i += 1

        return films

    async def up_film_rating(self, film: Film) -> None:
        await self._db.up_film_rating(film)

    class DataBrowser:

        def __init__(self, db: Database):
            self._connect = db.connect
            self._cursor = db.cursor

            # init table
            self._init_table_movies()
            self._connect.commit()

        def _init_table_movies(self):
            self._cursor.execute(
                'CREATE TABLE IF NOT EXISTS "movies" ('
                + '"kinopoisk_id"	INTEGER NOT NULL UNIQUE,'
                + '"rating"	INTEGER NOT NULL DEFAULT 0,'
                + '"title"	TEXT NOT NULL DEFAULT "",'
                + '"poster_url"	TEXT NOT NULL DEFAULT "",'
                + '"year"	INTEGER NOT NULL DEFAULT 0,'
                + '"quality"	TEXT NOT NULL DEFAULT "",'
                + '"token"	TEXT NOT NULL DEFAULT "",'
                + 'PRIMARY KEY("kinopoisk_id"))'
            )

        async def add_film(self, film: Film) -> None:
            self._cursor.execute('INSERT INTO "main"."movies" VALUES (?, ?, ?, ?, ?, ?, ?)', (
                film.kinopoisk_id,
                film.rating,
                film.title,
                film.poster,
                film.year,
                film.quality,
                film.ftoken,
            ))
            self._connect.commit()

        async def get_film(self, kp_id: int) -> Film:
            r = self._cursor.execute(
                'SELECT * FROM "main"."movies" WHERE kinopoisk_id = (?)', (kp_id,)).fetchone()
            return Film(kinopoisk_id=r[0], rating=r[1], title=r[2], poster=r[3], year=r[4], quality=r[5], ftoken=r[6]) if r else Film()

        async def up_film_rating(self, film: Film) -> None:
            dbfilm = await self.get_film(film.kinopoisk_id)
            r = int(time.time()/60/60)/1000000

            if dbfilm.kinopoisk_id:
                self._cursor.execute('UPDATE "main"."movies" SET rating = (?) WHERE kinopoisk_id = (?)', (
                    dbfilm.rating + r,
                    dbfilm.kinopoisk_id
                ))

                if dbfilm.ftoken != film.ftoken:
                    self._cursor.execute('UPDATE "main"."movies" SET quality = (?) WHERE kinopoisk_id = (?)', (
                        film.quality,
                        film.kinopoisk_id
                    ))

                self._connect.commit()
            else:
                film.rating = r
                await self.add_film(film)

        async def get_popular_films(self) -> List[list]:
            return self._cursor.execute('SELECT * FROM "main"."movies" ORDER BY rating DESC LIMIT 7').fetchall()

