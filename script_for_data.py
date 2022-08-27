import csv
from pprint import pprint


class Taker:
    __instance = None
    GREETING = [
        'здравствуйте',
        'добрый день',
        'доброе утро',
        'добрый вечер',
        'добрый']
    VALEDICTION = [
        'всего хорошего',
        'до свидания',
        'хорошего вечера',
        'хорошего дня',
        'всего доброго']
    SAY_NAME = [
        'зовут',
        'меня',
        'это'
    ]

    PLACE_OF_GREETING = range(5)

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, data):
        self.data = data
        self.cleaned_data = {}
        self.task_data = {}

    def read_data(self):
        '''
        Извлекает данные из csv файла.
        '''
        with open(self.data, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    num_of_dialogue, line, person, phrase = row
                    num_of_dialogue = int(num_of_dialogue)
                    phrase = phrase.lower()
                    if self.cleaned_data.get(num_of_dialogue) is None:
                        self.cleaned_data[num_of_dialogue] = {}
                    self.cleaned_data[num_of_dialogue][int(line)] = {
                            person: phrase
                            }
                    line_count += 1

    def show_data(self):
        pprint(self.task_data)

    def take_greeting(self):
        '''
        Проверяет поприветствовал ли оператор клиента.
        Результат записывает под ключ - is_greeting.
        '''
        for dialogue in self.cleaned_data:

            if self.task_data.get(dialogue) is None:
                self.task_data[dialogue] = {}
            self.task_data[dialogue]['is_greeting'] = False

            for line in self.PLACE_OF_GREETING:
                for greet in self.GREETING:
                    manager_greet = self.cleaned_data[dialogue][
                        line
                        ].get('manager')
                    if manager_greet is not None:
                        if greet in manager_greet:
                            self.task_data[dialogue]['is_greeting'] = True
                            break

    def take_valediction(self):
        '''
        Проверяет поприветствовал ли оператор клиента.
        Результат записывает под ключ - is_valediction.
        '''
        for dialogue in self.cleaned_data:
            len_dialogue = len(self.cleaned_data[dialogue])

            if self.task_data.get(dialogue) is None:
                self.task_data[dialogue] = {}
            self.task_data[dialogue]['is_valediction'] = False

            for line in range(len_dialogue - 5, len_dialogue):
                for valediction in self.VALEDICTION:
                    manager_valediction = self.cleaned_data[dialogue][
                            line
                            ].get('manager')
                    if manager_valediction is not None:
                        if valediction in manager_valediction:
                            self.task_data[dialogue]['is_valediction'] = True
                            break

    def is_small_talk(self):
        '''
        Проверяет является ли take_greeting и take_valediction для сессии.
        Результат записывает под ключ - is_small_talk.
        '''
        for dialogue in self.cleaned_data:
            if (self.task_data.get(dialogue).get('is_valediction') is None and
                self.task_data.get(dialogue).get('is_greeting') is None):
                print('Отсутствуют необходимые, сначала вызовите'
                      'функции take_greeting и take_valediction')
            self.task_data[dialogue]['is_small_talk'] = (
                self.task_data.get(dialogue).get('is_valediction') and
                self.task_data.get(dialogue).get('is_greeting'))

    def is_good_manager(self):
        '''
        Проверяет сказал ли своё имя оператор.
        '''
        for dialogue in self.cleaned_data:

            if self.task_data.get(dialogue) is None:
                self.task_data[dialogue] = {}
            self.task_data[dialogue]['is_said_name'] = False

            for line in self.PLACE_OF_GREETING:
                for greet in self.SAY_NAME:
                    manager_greet = self.cleaned_data[dialogue][
                        line
                        ].get('manager')
                    if manager_greet is not None:
                        if greet in manager_greet:
                            self.task_data[
                                dialogue][
                                    'manager'] = self.take_name_of_the_manager(
                                        manager_greet)
                            self.task_data[
                                dialogue][
                                    'company'] = self.take_name_of_the_company(
                                        manager_greet)
                            if self.task_data[
                                dialogue][
                                    'manager'] != 'Имя неизвестно':
                                self.task_data[
                                    dialogue][
                                        'is_said_name'] = manager_greet
                            else:
                                self.task_data[
                                    dialogue][
                                        'is_said_name'] = 'Имя не было сказано'
                            break

    @staticmethod
    def take_name_of_the_manager(phrase):
        """
        Извлекает имя менеджера.
        """
        words = phrase.split()
        length = len(words)
        for i in range(length):
            if words[i] == 'меня':
                if words[i] == 'зовут':
                    return words[i+2]
                return words[i+1]
            if words[i] == 'это':
                return words[i+1]
        return 'Имя неизвестно'

    @staticmethod
    def take_name_of_the_company(phrase):
        """
        Извлекает название компании.
        """
        words = phrase.split()
        length = len(words)
        for i in range(length):
            if words[i] == 'компания':
                return words[i+1]
        return 'Название неизвестно'


dialogs = Taker('test_data.csv')
dialogs.read_data()
dialogs.take_greeting()
dialogs.take_valediction()
dialogs.is_small_talk()
dialogs.is_good_manager()
dialogs.show_data()
