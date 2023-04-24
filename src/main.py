import argparse
import sys
from dependency_parser import DependencyParser
from vulnerability_mapper import VulnerabilityMapper
from report import Report


def os_specific():
    if sys.platform.startswith('win'):
        return '\\'
    elif sys.platform.startswith('linux'):
        return '/'
    else:
        print('Неизвестная операционная система, возможны проблемы совместимости параметров. Смотри main.py')
        return '/'

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs=1, help='Путь до корневой папки анализируемого проекта')
    parser.add_argument('--venv', default=None, help='Путь до папки виртуального окружения. Если не указана, папка ищется в корне проекта')
    return parser

def main():
    delimiter = os_specific()

    parser = arg_parser()
    args = parser.parse_args()
    path = args.path[0]
    venv = args.venv

    if path[-1] != delimiter:
        path = path + delimiter

    dependency_parser = DependencyParser(path, venv, delimiter)
    project, reqs, fixed_reqs = dependency_parser.parse()
    
    '''vulnerability_mapper = VulnerabilityMapper()
    vul_list = vulnerability_mapper.vuln_scan(fixed_reqs)

    report = Report(project, reqs, fixed_reqs, vul_list)
    report.make_report(vul_list)'''

if __name__ == "__main__":
    main()