from .target import target
import os
import json

class JSON_service:
    def __init__(self, input_json_path: str, output_json_path: str):
        self.input_json_path = input_json_path
        self.output_json_path = output_json_path

    def get_input_targets(self) -> list[target]:
        with open(self.input_json_path, 'r', encoding='utf-8') as openfile:
            items = json.load(openfile)
            targets = []

            for item in items:
                targets.append(target(item))
            
            return targets
    
    def save_results(self, results: dict[str: str]):
        try:
            os.makedirs(self.output_json_path, exist_ok=True)

            file_path = f'{self.output_json_path}/output.json'
            self.create_empty_json_file(file_path)

            dumped = json.dumps(results, indent=4, ensure_ascii=False)

            with open(file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(dumped)

            print('🟢 Успешно сохранили результаты.')
        except Exception as error:
            print(f'❌ Произошла ошибка при сохранении результатов.\nError: {error}')
    
    def create_empty_json_file(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({}, f)