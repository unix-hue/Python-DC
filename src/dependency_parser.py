import sys
import os
import entities

class DependencyParser:

    _SIGNS = ('==', '===', '>=', '<=', '>', '<', '~=')

    def __init__(self, path, venv):
        self.path = path
        self.project = None
        self.reqs = None
        self.fixed_reqs = None

        if venv is None:
            self.venv = f'{path}.venv'
        else:
            self.venv = venv

    def parse(self):
        try:
            with open(f'{self.path}pyproject.toml', 'r') as file:
                self.project = self._pyproj_info_parse(file)
                self.reqs = self._pyproj_parse(file)
        except FileNotFoundError:
            try:
                with open(f'{self.path}requirements.txt', 'r') as file:
                    self.reqs = self._req_parse(file)
            except FileNotFoundError:
                sys.exit('В директории проекта не найдены файлы pyproject.toml и requirements.txt\n'\
                        'Создайте хотя бы один из этих файлов и добавьте туда данные о зависимостях')
                
        if os.path.exists(self.venv):
            self.fixed_reqs = self._venv_parse(self.venv)
        else:
            try:
                with open(f'{self.path}poetry.lock', 'r') as file:
                    self.fixed_reqs = self._lock_parse(file)
            except FileNotFoundError:
                sys.exit('В директории проекта не найдена директория venv и файл poetry.lock\n'\
                        'Создайте файл poetry.lock или создайте/укажите путь к виртуальному окружению'\
                        'Указать абсолютный путь к виртуальному окружению можно через опцию --venv')
        
        return self.project, self.reqs, self.fixed_reqs

    def _recieve_data(self, value):
        begin = value.find('"')
        return value[begin+1:-1]

    def _pyproj_info_parse(self, file):
        project = entities.Project()
        start_parse = False

        for line in file:
            line_ = line.rstrip(' \n\r')

            if line_ == '[tool.poetry]':
                start_parse = True
            elif start_parse and line_.startswith('name'):
                project.name = self._recieve_data(line_)
            elif start_parse and line_.startswith('version'):
                project.version = self._recieve_data(line_) 
            elif start_parse and line_.startswith('description'):
                project.description = self._recieve_data(line_)
            elif start_parse and line_.startswith('authors'):
                project.authors = self._recieve_data(line_)
            elif start_parse and line_.startswith('license'):
                project.license = self._recieve_data(line_)
            elif start_parse and line in ['\n', '', '\r\n']:
                break
            else:
                continue

        return project

    def _pyproj_parse(self, file):
        reqs = dict()
        start_parse = False

        for line in file:
            line_ = line.rstrip(' \n\r')

            if line_ == '[tool.poetry.dependencies]':
                start_parse = True
            elif start_parse and line in ['\n', '', '\r\n']:
                break
            elif start_parse:
                try:
                    name, _, version = line_.split()
                    reqs[name] = [('pyproject.toml', version[1:-1])]
                except BaseException:
                    print(f'Неподдерживаемый формат описания зависимости : {line_}\n'\
                          'Приведите запись в формат \'name = "version"\'')
            else:
                continue

        return reqs

    def _req_parse(self, file):#todo
        reqs = dict()

        for line in file:
            line_ = line.rstrip(' \n\r')

            line_ = line_.replace(' ', '')

            sign = line_.find(';')
            if sign != -1:
                line_ = line_[0:sign]
            else:
                sign = line_.find('#')
                if sign != -1:
                    line_ = line_[0:sign]

            sign = line_.find('[')
            if sign != -1:
                sign_2 = line_.find(']')
                sub = line_[sign+1:sign_2]
                line_ = line_[0:sign] + line_[sign_2+1:]
                print(f'Опциональная библиотека [{sub}] для {line_[0:sign]} не будет учтена как зависимость и проверена\n'\
                      'Пожалуйста, добавьте ее в файл зависимостей в подходящем формате или уберите\n'\
                        'Подходящие форматы:\n'\
                        'library\n'\
                        'library==1.1.1, знак может быть любой\n'\
                        'library>=1.1.1,<2.0.0\n')

            single = True
            for sign in self._SIGNS:
                delim = line_.find(sign)
                if delim != -1:
                    single = False
                    name = line_[0:delim]
                    version = line_[delim:]
                    reqs[name] = [('requirements.txt', version)]
                
            if single:
                reqs[line_] = [('requirements.txt', '*')]
            
        return reqs

    def _venv_parse(self, venv):#todo
        pass

    def _lock_parse(self, file):#todo
        pass
