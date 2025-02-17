import os

import pandas
import peewee

from models import Person, SqliteDatabase


class CSVToDB():
    """Класс создает базу данных db_name на основе данных прочитанных
    из CSV-файла csv_file_name.
    """

    def __init__(self, csv_file_name, db_name, model):
        """Конструктор класса. При создании экземпляра данные из CSV-файла
            читаются в объект pandas.DataFrame. После этого, на основе данных
            из этого объекта создается база данных sqlite с аналогичной
            структурой.

        Args:
            csv_file_name (str): имя CSV-файла с исходными данными
            db_name (str): имя файла создаваемой базы данных sqlite
            model (peewee.ModelBase): Имя модели
        """

        self.model = model

        if os.path.isfile(csv_file_name):
            self.csv_data_df = pandas.read_csv(csv_file_name, encoding='utf-8').fillna(False)
        else:
            raise FileNotFoundError(
                "The file itr_list.xlsx does not exist!!!")

        self.connect = SqliteDatabase(db_name)

        try:
            self.connect.connect()
            self.model.create_table(safe=True)
        except peewee.InternalError as px:
            print(str(px))

        self.model.delete().execute()

        self.fields = list(self.model._meta.fields.keys())[1:]
        self.data = [tuple(self.csv_data_df.values[index])
                     for index in
                     range(self.csv_data_df.shape[0])]
        self.model.insert_many(
            self.data,
            fields=self.fields).execute()

    def get_name_list(self, status, initials=True) -> str:
        """Возвращает список допускающих, выдающих или согласующих
        наряд-допуск. Если параметр initials равен True будет
        возвращен список имен состоящий из фамилии и инициалов.
        В противном случае имя и отчество будут переданы полностью.

        Returns:
            str: Список имен.
        """

        if initials:
            return [f'{record.last_name} '
                    f'{record.name[0]}. '
                    f'{record.patronymic[0]}.'
                    for record in self.model.select().where(
                        getattr(self.model, status)
                    )]

        return [f'{record.last_name} '
                f'{record.name} '
                f'{record.patronymic}'
                for record in self.model.select().where(
                    getattr(self.model, status)
                )]


def main() -> None:
    db_inst = CSVToDB('itr_list.csv', 'itr.sqlite', Person)
    print(db_inst.get_name_list('is_admitting'))
    print(db_inst.get_name_list('is_issuing', False))
    print(db_inst.get_name_list('is_approving'))


if __name__ == '__main__':
    main()
