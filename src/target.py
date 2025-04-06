class target:
    def __init__(self, json_dict: dict[str: str]):
        self.surname = json_dict['Фамилия']
        self.fullname_short = json_dict['ФИО']
        self.organization_name = json_dict['Название организации']
        self.ogrn = json_dict['ОГРН']
        self.registration_number = json_dict['Регистрационный номер']
        self.date = json_dict['Дата выдачи']
        self.blank_series = json_dict['Серия бланка']
        self.blank_number = json_dict['Номер бланка']

class result:
    def __init__(self, fullname_short: str, ogrn: str, registration_number: str, result: int, date):
        self.fullname_short = fullname_short
        self.ogrn = ogrn
        self.registration_number = registration_number
        self.result = result
        self.date = date

    def to_dict(self) -> dict[str: str]:
        return {
            'ФИО': self.fullname_short,
            'ОГРН': self.ogrn,
            'Регистрационный номер': self.registration_number,
            'Результат': self.result,
            'ДатаВремя': self.date,
        }