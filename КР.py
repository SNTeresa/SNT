import sqlite3


def создать_базу_данных():
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS книги (
            книга_id INTEGER PRIMARY KEY AUTOINCREMENT,
            название TEXT NOT NULL,
            автор TEXT NOT NULL,
            год INTEGER,
            доступно INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS читатели (
            читатель_id INTEGER PRIMARY KEY AUTOINCREMENT,
            имя TEXT NOT NULL,
            телефон TEXT,
            книга_id INTEGER,
            FOREIGN KEY (книга_id) REFERENCES книги (книга_id)
        )
    ''')

    conn.commit()
    conn.close()

def добавить_книгу(название, автор, год):
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO книги (название, автор, год) VALUES (?, ?, ?)', (название, автор, год))
    conn.commit()
    conn.close()

def добавить_читателя(имя, телефон):
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO читатели (имя, телефон) VALUES (?, ?)', (имя, телефон))
    conn.commit()
    conn.close()

def выдать_книгу(читатель_id, книга_id):
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()

    cursor.execute('SELECT доступно FROM книги WHERE книга_id = ?', (книга_id,))
    доступно = cursor.fetchone()

    if доступно and доступно[0] == 1:
        cursor.execute('UPDATE книги SET доступно = 0 WHERE книга_id = ?', (книга_id,))
        cursor.execute('UPDATE читатели SET книга_id = ? WHERE читатель_id = ?', (книга_id, читатель_id))
        conn.commit()

    conn.close()


def вернуть_книгу(книга_id):
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE книги SET доступно = 1 WHERE книга_id = ?', (книга_id,))
    cursor.execute('UPDATE читатели SET книга_id = NULL WHERE книга_id = ?', (книга_id,))

    conn.commit()
    conn.close()


def получить_доступные_книги():
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM книги WHERE доступно = 1')
    книги = cursor.fetchall()
    conn.close()
    return книги


def получить_книги_читателя(читатель_id):
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT k.название, k.автор FROM книги k JOIN читатели r ON k.книга_id = r.книга_id WHERE r.читатель_id = ?',
        (читатель_id,))
    книги = cursor.fetchall()
    conn.close()
    return книги


def искать_книги(ключевое_слово):
    conn = sqlite3.connect('библиотека.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM книги WHERE название LIKE ? OR автор LIKE ?',
                   ('%' + ключевое_слово + '%', '%' + ключевое_слово + '%'))
    книги = cursor.fetchall()
    conn.close()
    return книги

if __name__ == '__main__':
    создать_базу_данных()

    добавить_книгу("1984", "Джордж Оруэлл", 1949)
    добавить_книгу("Убить пересмешника", "Харпер Ли", 1960)
    добавить_книгу("Великий Гэтсби", "Фрэнсис Скотт Фицджеральд", 1925)

    добавить_читателя("Влад", "8923412")
    добавить_читателя("Андрей", "892341432")

    выдать_книгу(1, 1)

    print("Доступные книги:", получить_доступные_книги())

    вернуть_книгу(1)

    print("Доступные книги после возврата:", получить_доступные_книги())
