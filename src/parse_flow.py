from .target import target, result
from .website_data_parser import website_data_parser
from .config_parser import Config
from .solve_captcha import captcha_resolver
from selenium.webdriver.support.ui import Select
from datetime import datetime
import os

class Flow:
    def __init__(self, parser: website_data_parser, config: Config, target: target):
        self.parser = parser
        self.config = config
        self.target = target
    
    def open_and_find_iframe(self):
        open_button_elem = self.parser.find_simple_element_with_xpath('open_button', self.config.open_button)
        open_button_elem.click()
        
        self.parser.find_and_switch_to_new_frame(self.config.form_iframe)
    
    def select_training_level(self):
        training_level_element = self.parser.wait_and_find_element('select', self.config.training_level_select)

        dropdown = Select(training_level_element)
        dropdown.select_by_value('dpo')

    def find_organization(self):
        find_org_button = self.parser.find_simple_element_with_xpath('find_organization_button', self.config.find_organization_button)
        find_org_button.click()

        modal = self.parser.wait_visibility_and_find_element('modal_window', self.config.modal_window)

        organization_name_input = self.parser.wait_and_find_element('organization_name_input', self.config.organization_name_input)
        organization_name_input.send_keys(self.target.organization_name)

        input_ogrn = self.parser.wait_and_find_element('input_dpo', self.config.ogrn_input)
        input_ogrn.send_keys(self.target.ogrn)

        self.parser.wait_until_clickable_and_click_element('find_organization_panel', self.config.find_organization_panel_css_selector)

    def fill_input_fields(self):
        surname_input = self.parser.find_simple_element_with_xpath('surname_input', self.config.surname_input)
        surname_input.send_keys(self.target.surname)

        blank_series_input = self.parser.find_simple_element_with_xpath('blank_series_input', self.config.blank_series_input)
        blank_series_input.send_keys(self.target.blank_series)

        blank_number_input = self.parser.find_simple_element_with_xpath('blank_number_input', self.config.blank_number_input)
        blank_number_input.send_keys(self.target.blank_number)

        registration_number = self.parser.find_simple_element_with_xpath('registration_number', self.config.registration_number)
        registration_number.send_keys(self.target.registration_number)

        date_input = self.parser.find_simple_element_with_xpath('date_input', self.config.date_input)
        date_input.send_keys(self.target.date)

    def resolve_captcha(self, auto_mode: bool):
        os.makedirs('captcha/', exist_ok=True)
        
        captcha_img = self.parser.wait_and_find_element('captcha_img', self.config.captcha_image)
        captcha_img.screenshot('captcha/captcha.png')

        captcha_value = ''

        if auto_mode:
            resolver = captcha_resolver('captcha/captcha.png')
            captcha_value = resolver.extract_value_from_captcha()
        else:
            captcha_value = input('Введите значение капчи: ')
        
        print(f"🟢 Считали значение капчи: {captcha_value}")

        captcha_input = self.parser.find_simple_element_with_xpath('captcha_input', self.config.captcha_input)
        captcha_input.send_keys(captcha_value)

    def valid_captcha(self) -> bool:
        wrong_captcha_label = self.parser.find_simple_element_with_xpath('wrong_captcha_label', self.config.wrong_captcha_label)
        return False if wrong_captcha_label and wrong_captcha_label.text == self.config.captcha_error_text else True

    def search_and_get_result(self) -> int:
        search_button = self.parser.find_simple_element_with_xpath('search_button', self.config.search_button)
        self.parser.execute_script("arguments[0].click();", search_button, 'search_button') 

        result_modal = self.parser.wait_visibility_and_find_element('result_modal_window', self.config.result_modal_window)

        if not self.valid_captcha():
            print('❌ Бот не смог распознать капчу')
            raise RuntimeError('Wrong captcha')

        result_header = self.parser.wait_and_find_element('result_header', self.config.result_header)
        download_button = self.parser.wait_and_find_element('download_button', self.config.download_button)
        
        if download_button:
            download_button = self.parser.wait_until_clickable_and_click_element_xpath('download_button', self.config.download_button)
            print('🟢 Начинаем загрузку документа.')
            return 1

        if result_header.text == 'Данные не найдены':
            print('❌ Документ не найден')
            return 0

        return 0

    def prepare_output(self, target: target, is_success: int) -> result:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return result(
            fullname_short=target.fullname_short,
            ogrn=target.ogrn,
            registration_number=target.registration_number,
            result=is_success,
            date=date
        )

    def run_flow(self, captcha_auto_mode: bool) -> result:
        print('======================        Открываем url       ========================================')
        self.parser.open_url(self.config.url)
        print('====================== Открываем форму для поиска ========================================')
        self.open_and_find_iframe()
        print('======================   Выбираем форму обучения  ========================================')
        self.select_training_level()
        print('======================      Ищем организацию      ========================================')
        self.find_organization()
        print('======================       Заполняем форму      ========================================')
        self.fill_input_fields()
        print('======================       Проходим капчу       ========================================')
        self.resolve_captcha(auto_mode=captcha_auto_mode)
        print('======================       Выполняем поиск      ========================================')
        _result = self.search_and_get_result()
        return self.prepare_output(self.target, _result)
