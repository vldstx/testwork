import sqlite3


class NotesManager:  # инкапсуляция операций с базой данных
    def __init__(self, db_name='notes.db'):  #создание бд
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):   #создание таблицы в бд (ID, title, content)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()

    def add_note(self, title, content):  # добавление заметок в бд
        self.cursor.execute('SELECT id FROM notes')
        existing_ids = set(row[0] for row in self.cursor.fetchall())
        new_id = 1
        while new_id in existing_ids:
            new_id += 1

        self.cursor.execute('INSERT INTO notes (id, title, content) VALUES (?, ?, ?)', (new_id, title, content))
        self.conn.commit()

    def view_notes(self): #просмотр всех заметок
        self.cursor.execute('SELECT id, title FROM notes')
        notes = self.cursor.fetchall()

        if not notes:
            print("Нет заметок для просмотра.")
            return

        for note in notes:
            print(f"ID: {note[0]}, Заголовок: {note[1]}")

        choice = input(
            "Введите ID заметки для подробного просмотра (или 'D' для удаления, 'Enter' для возврата в меню): ")

        if choice.lower() == 'd':
            self.delete_note_menu()
        elif choice:
            self.view_note_details(choice)

    def delete_note_menu(self):
        note_id = input("Введите ID заметки, которую вы хотите удалить: ")
        self.delete_note(note_id)
        print("Заметка удалена.")

    def view_note_details(self, note_id):
        self.cursor.execute('SELECT id, title, content FROM notes WHERE id = ?', (note_id,))
        note = self.cursor.fetchone()

        if note:
            print(f"ID: {note[0]}, Заголовок: {note[1]}\nСодержание: {note[2]}")
        else:
            print("Заметка с указанным ID не найдена.")

    def search_notes(self, keyword): #поиск всех заметок в бд по ключевым словам/фразам

        keywords = keyword.lower().split()
        self.cursor.execute('SELECT id, title, content FROM notes')
        notes = self.cursor.fetchall()

        FILTRED_NOTES = []
        for note in notes:
            content = note[2].lower()
            if all(kw in content for kw in keywords):
                FILTRED_NOTES.append(note)

        for note in FILTRED_NOTES:
            print(f"ID: {note[0]}, Заголовок: {note[1]}, Содержание: {note[2]}")


    def delete_note(self, note_id): #удаление заметок из бд
        self.cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    notes_manager = NotesManager()

    while True:
        print("\nМеню:")
        print("1. Добавить заметку")
        print("2. Просмотреть список заметок")
        print("3. Поиск заметок")
        print("4. Удалить заметку")
        print("5. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Введите заголовок: ")
            content = input("Введите содержание: ")
            notes_manager.add_note(title, content)
            print("Заметка добавлена.")
        elif choice == '2':
            notes_manager.view_notes()
        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска: ")
            notes_manager.search_notes(keyword)
        elif choice == '4':
            note_id = input("Введите ID заметки, которую вы хотите удалить: ")
            notes_manager.delete_note(note_id)
            print("Заметка удалена.")
        elif choice == '5':
            notes_manager.close()
            break
        else:
            print("Неправильный выбор. Попробуйте еще раз.")
