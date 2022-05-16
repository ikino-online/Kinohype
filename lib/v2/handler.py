import sqlite3
import re
from aiogram.types import Message, CallbackQuery
from typing import List, Callable, Optional
from db.mydb import Database


class Handler:
    def __init__(self, db: Database):
        # database
        self._db = self._DataBrowser(db)

        # обработчики
        self._handlers_array = {}
        self._handlers_array['special'] = []
        self._query_handler_array = []

    async def handle_message(self, m: Message) -> None:
        """обработчик входящих сообщений"""
        user_path = self._db.get_user_path(m.from_user.id)
        m.text = '' if not m.text else m.text

        async def search_handler(_message: str, _handlers):
            _handlers = _handlers[0]
            for handler in _handlers:
                if re.match(handler[0], _message):
                    return handler[1]
            return None

        # middle
        m = self._middleware(m)

        func = await search_handler(m.text, self._handlers_array['special'])
        if func:
            await func(m)
            return

        handlers = self._handlers_array.get(user_path)
        if handlers:
            func = await search_handler(m.text, handlers)
            if func:
                await func(m)
                return

    async def handle_query(self, c: CallbackQuery) -> None:
        """обработчик callback запросов"""
        c = self._middleware(c)
        for query in self._query_handler_array:
            await query[1](c) if re.match(query[0], c.data) else 0

    def add(self, action_path: str, templates: dict) -> None:
        """добавить обработчик сообщений"""
        if not (self._handlers_array.get(action_path)):
            self._handlers_array[action_path] = []
        self._handlers_array[action_path].append(list(templates.items()))

    def add_query(self, template: str, func) -> None:
        """добавить обработчик callback запросов"""
        self._query_handler_array.append([template, func])

    def get_user_path(self, user_id: int) -> str:
        return self._db.get_user_path(user_id)

    def set_user_path(self, new_path: str, user_id: int) -> None:
        return self._db.set_user_path(new_path, user_id)

    def get_all_ids(self) -> List[int]:
        ids = self._db.get_all_ids()
        return [i[0] for i in ids]

    def get_all_count(self) -> int:
        return self._db.get_all_count()[0]

    def _middleware(self, m: Message):
        m.set_action_path = lambda p: self.set_user_path(p, m.from_user.id)
        m.get_action_path = lambda: self.get_user_path(m.from_user.id)
        return m

    class HMessage(Message):
        set_action_path: Callable[[str], None]
        get_action_path: Callable[[None], None]

    class _DataBrowser:
        def __init__(self, db: Database):
            self._connect = db.connect
            self._cursor = db.cursor

            # init table
            self._init_table_users()
            self._connect.commit()

        def _init_table_users(self) -> None:
            self._connect.execute(
                'CREATE TABLE IF NOT EXISTS "users" ('
                + '"telegram_id"	INTEGER NOT NULL UNIQUE,'
                + '"action_path"	TEXT NOT NULL DEFAULT "/",'
                + 'PRIMARY KEY("telegram_id"))'
            )

        def get_user_path(self, user_id: int) -> str:
            u = self._cursor.execute(
                'SELECT "action_path" FROM "main"."users" WHERE telegram_id = ?', (user_id,)).fetchone()
            if not u:
                self.add_user(user_id)
                return '/'
            return u[0]

        def add_user(self, user_id: int) -> None:
            self._cursor.execute(
                'INSERT INTO "main"."users" ("telegram_id") VALUES (?)', (user_id,))
            self._connect.commit()

        def set_user_path(self, new_path: str, user_id: int) -> None:
            self._cursor.execute(
                'UPDATE "main"."users" SET action_path = (?) WHERE telegram_id = (?)', (new_path, user_id))
            self._connect.commit()

        def get_all_ids(self) -> List[List[int]]:
            return self._cursor.execute('SELECT "telegram_id" FROM "main"."users"').fetchall()

        def get_all_count(self) -> int:
            return self._cursor.execute('SELECT COUNT("telegram_id") FROM "main"."users"').fetchone()
