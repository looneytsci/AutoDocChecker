import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Config:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('config.ini')

    def read_config(self):
        self.url = self.config_parser['app']['url']
        
        self.open_button = self.config_parser['app']['open_button']
        self.form_iframe = self.config_parser['app']['form_iframe']
        self.training_level_select = self.config_parser['app']['training_level_select']
        self.find_organization_button = self.config_parser['app']['find_organization_button']
        self.modal_window = self.config_parser['app']['modal_window']
        self.organization_name_input = self.config_parser['app']['organization_name_input']
        self.ogrn_input = self.config_parser['app']['ogrn_input']
        self.surname_input = self.config_parser['app']['surname_input']
        self.blank_series_input = self.config_parser['app']['blank_series_input']
        self.blank_number_input = self.config_parser['app']['blank_number_input']
        self.registration_number = self.config_parser['app']['registration_number']
        self.date_input = self.config_parser['app']['date_input']
        self.captcha_image = self.config_parser['app']['captcha_image']
        self.captcha_input = self.config_parser['app']['captcha_input']
        self.search_button = self.config_parser['app']['search_button']
        self.result_modal_window = self.config_parser['app']['result_modal_window']
        self.result_header = self.config_parser['app']['result_header']
        self.wrong_captcha_label = self.config_parser['app']['wrong_captcha_label']
        self.download_button = self.config_parser['app']['download_button']

        self.find_organization_panel_css_selector = self.config_parser['app']['find_organization_panel_css_selector']

        self.waiter_timeout = self.config_parser['app']['waiter_timeout']

        self.output_folder = self.config_parser['app']['output_folder']

        self.captcha_retries = int(self.config_parser['app']['captcha_retries'])
        self.captcha_error_text = self.config_parser['app']['captcha_error_text']
    
    def validate_config(self):
        properties = [
            'url',
            'open_button',
            'form_iframe',
            'training_level_select',
            'find_organization_button',
            'modal_window',
            'organization_name_input',
            'ogrn_input',
            'surname_input',
            'blank_series_input',
            'blank_number_input',
            'registration_number',
            'date_input',
            'captcha_image',
            'search_button',
            'result_modal_window',
            'result_header',
            'wrong_captcha_label',
            'find_organization_panel_css_selector',
            'waiter_timeout',
            'output_folder',
            'captcha_retries',
            'captcha_error_text',
            'download_button',
        ]

        for property in properties:
            if not hasattr(self, property):
                raise ValueError(f'❌ {property} не установлена в Config.ini')
        
        print('🟢 Успешно проинициализировали конфигурацию')
    
    def set_input_file(self, file):
        self.input_file_path = file

    def is_input_file_setted(self) -> bool:
        hasattr(self, 'input_file_path')