import configparser
import os
import time

import eel
from docxtpl import DocxTemplate

from create_db import CSVToDB
from models import Person

# Чтение значений констант из settings.ini
config = configparser.ConfigParser()
config.read("settings.ini", encoding='utf-8')

SAVE_FOLDER_NAME = config["Settings"]["SAVE_FOLDER_NAME"]
SKIP = config["Settings"]["SKIP"]
APPROVER_POSITION = config["Settings"]["APPROVER_POSITION"]
ENGINEERS_LIST_FILENAME = config["Settings"]["ENGINEERS_LIST_FILENAME"]
DB_FILENAME = config["Settings"]["DB_FILENAME"]
TEMPLATES_PATHNAME = config["Settings"]["TEMPLATES_PATHNAME"]
EXTRA_KEYS_FILENAME = config["Settings"]["EXTRA_KEYS_FILENAME"]

ROWS = {
    '1': 'A - D',
    '2': 'D - F',
    '3': 'F - H',
    '4': 'H - K'
}

SKIP_ADMITTING_VALUE = ''
SKIP_ISSUING_VALUE = ' ' * 60
SKIP_APPROVING_VALUE = ' ' * 100

db_inst = CSVToDB(ENGINEERS_LIST_FILENAME, DB_FILENAME, Person)


def get_templates_list() -> list:
    '''
    Возвращает список файлов в папке TEMPLATES_PATHNAME
    с расширениями 'doc' и 'docx'
    '''

    path = os.getcwd()
    try:
        with os.scandir(path+'/'+TEMPLATES_PATHNAME) as listofentries:
            templates_list = [entry.name for entry in listofentries
                              if os.path.splitext(entry)[1] in
                              ('.doc', '.docx')]
    except FileNotFoundError:
        raise FileNotFoundError

    eel.progress_bar(f'Найдено шаблонов - {len(templates_list)}')
    time.sleep(0.5)
    return templates_list


def format_date(date: str) -> str:
    '''
    Преобразует и возвращает дату в формате ДД:ММ:ГГГГ
    '''

    date = [symbol for symbol in date]
    return f'{"".join(date[8:])}.{"".join(date[5:7])}.{"".join(date[:4])}'


def get_extra_keys() -> dict:
    '''
    Возвращает словарь из дополнительных ключей найденных
    в файле EXTRA_KEYS_FILENAME
    '''

    with open(EXTRA_KEYS_FILENAME, encoding="utf-8") as data_file:
        raw_data = data_file.readlines()
    data = [row for row in raw_data if ': ' in row and '#' not in row]
    extra_context = {}
    for row in data:
        key, value = row.split(': ')
        extra_context[key] = value.replace('\n', '')

    print('Дополнительные ключи:\n')
    for key, value in extra_context.items():
        print(key, ': ', value)
    return extra_context


def get_context(dsp: str,
                date: str,
                admitting: str,
                issuing: str,
                approving: str) -> dict:
    '''
    Возвращает словарь содержащий переданные значения,
    а так же ключи и значения из файла  EXTRA_KEYS_FILENAME
    '''

    context = {}

    context['ДСП'] = dsp

    if date == '':
        context['Дата'] = '01.01.1990'
    else:
        context['Дата'] = format_date(date)

    admitting_list = db_inst.get_name_list('is_admitting', False)
    try:
        admitting_list.remove(issuing)
    except ValueError:
        pass

    context['СписокДопускающих'] = ', '.join(admitting_list)

    if admitting != SKIP_ADMITTING_VALUE:
        admitting = admitting.split()
        context['Допускающий'] = (
            f'{admitting[0]} {admitting[1][0]}.{admitting[2][0]}.'
        )
    else:
        context['Допускающий'] = admitting

    context['Выдающий'] = issuing

    if approving != SKIP_APPROVING_VALUE:
        approving = approving.split()
        approving = (f'{APPROVER_POSITION} '
                     f'{approving[0]} {approving[1][0]}.{approving[2][0]}.')

    context['Согласующий'] = approving
    context['Ряды'] = ROWS[context['ДСП']]
    dsp_number = int(context['ДСП'])
    context['Конвейеры'] = f'{dsp_number*2-1}, {dsp_number*2}'

    return {**context, **get_extra_keys()}


def get_save_folder_name(date: str, dsp: str) -> str:
    '''
    Создает и возвращает уникальное имя папки с готовыми документами
    '''
    prefix = ''
    prefix_number = 1
    while 1:
        if not os.path.isdir(f'{SAVE_FOLDER_NAME}{dsp} {date}{prefix}/'):
            return f'{SAVE_FOLDER_NAME}{dsp} {date}{prefix}/'
        else:
            prefix = '_' + str(prefix_number)
            prefix_number += 1


def make_documents(templates_list: list, context: dict) -> None:
    '''
    Создает документы на основе списка шаблонов templates_list
    и словаря ключей context
    '''

    save_folder = get_save_folder_name(context['Дата'], context['ДСП'])
    os.mkdir(save_folder)
    os.startfile(f'{os.getcwd()}\\{save_folder}')
    print('\nСоздание НД\n')
    templates_count = len(templates_list)
    for number, template in enumerate(templates_list):
        document = DocxTemplate('templates/'+template)
        document.render(context)
        document.save(save_folder+template)
        print(f'{number+1}/{templates_count} {template} - сохранен')
        eel.progress_bar(f'{number+1}/{templates_count}')
    time.sleep(0.5)
    print('Все файлы успешно сохранены!')
    eel.progress_bar('Все файлы успешно сохранены!')


def main():
    '''
    Создает окно графического интерфейса программы
    на основе HTML-шаблона в папке 'wui' и базы данных DB_FILENAME
    '''

    eel.init('wui')

    admitting_list = db_inst.get_name_list('is_admitting', False)
    admitting_value_list = db_inst.get_name_list('is_admitting', False)
    issuing_list = db_inst.get_name_list('is_issuing', False)
    issuing_value_list = db_inst.get_name_list('is_issuing', False)
    approving_list = db_inst.get_name_list('is_approving', False)
    approving_value_list = db_inst.get_name_list('is_approving', False)
    admitting_list.append(SKIP)
    admitting_value_list.append(SKIP_ADMITTING_VALUE)
    issuing_list.append(SKIP)
    issuing_value_list.append(SKIP_ISSUING_VALUE)
    approving_list.append(SKIP)
    approving_value_list.append(SKIP_APPROVING_VALUE)

    eel.generate_forms(admitting_list,
                       admitting_value_list,
                       issuing_list,
                       issuing_value_list,
                       approving_list,
                       approving_value_list)
    try:
        eel.start('ui.html',
                  mode='default',
                  size=(500, 850),
                  position=(100, 200))
    except Exception:
        return


@eel.expose
def make_nd(dsp: str,
            date: str,
            admitting: str,
            issuing: str,
            approving: str) -> None:
    '''
    Функция реализует основную логику программы
    на основе данных полученных из форм окна графического интерфейса
    '''

    templates_list = get_templates_list()
    context = get_context(dsp, date, admitting, issuing, approving)
    make_documents(templates_list, context)


if __name__ == '__main__':
    main()
