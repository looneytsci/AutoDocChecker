import sys
from selenium import webdriver
from src.config_parser import Config
from src.runner import Runner
from src.json_service import JSON_service
from selenium.webdriver.chrome.options import Options
import os

def create_config() -> Config:
    config = Config()
    config.read_config()
    config.validate_config()

    return config

if __name__ == '__main__':
    config = create_config()
    args = sys.argv[1:]
    options = Options()

    download_dir = os.path.dirname(os.path.abspath(__file__)) + '/' + config.output_folder
    options.add_experimental_option('prefs', {
        'download.default_directory': download_dir,
    })

    for arg in args:
        if '.json' in arg:
            config.set_input_file(arg)

        if '--silent' in arg:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    json_service = JSON_service('input.json', config.output_folder)
    targets = json_service.get_input_targets()
    runner = Runner(targets, driver, config, json_service)
    runner.start()