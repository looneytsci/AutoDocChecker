from .target import target, result
from .config_parser import Config
from .parse_flow import Flow
from .website_data_parser import website_data_parser
from selenium.webdriver.safari.webdriver import WebDriver
from .json_service import JSON_service

class Runner:
    def __init__(self, targets: list[target], driver: WebDriver, config: Config, json_service: JSON_service):
        self.config = config
        self.retries_count = config.captcha_retries
        self.targets = targets
        self.parser = website_data_parser(driver, config.url, config.waiter_timeout)
        self.driver = driver
        self.json_service = json_service

    outputs: list[result] = []

    def start(self):
        for target in self.targets:
            # Обновляем кол-во попыток для скрипта
            self.retries_count = self.config.captcha_retries
            # Запускаем скрипт
            self.run_flow(target, self.retries_count > 0)

        self.driver.quit()
        self.save_output()

    def run_flow(self, target: target, auto_mode: bool):
        try:
            self.call_script(target, auto_mode)
        except RuntimeError as error:
            self.retries_count -= 1
            mode = True if self.retries_count > 0 else False
            self.run_flow(target, mode)

    def call_script(self, target: target, mode: bool):
        flow = Flow(self.parser, self.config, target)
        output = flow.run_flow(mode)
        self.outputs.append(output)
    
    def save_output(self):
        print('🥷🏻 Закончили прогон. Сохраняем результаты.')

        if len(self.outputs) == 0:
            print('❌ Не получено ни одного отчета.')
            return
    
        results = []

        for output in self.outputs:
            results.append(output.to_dict())

        self.json_service.save_results(results)