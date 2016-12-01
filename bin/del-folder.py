#!/usr/bin/python3.5
# -*- coding:utf8 -*-

import shutil
import os
import sys
import logging
import datetime
import configparser

logging.basicConfig(filename='/var/log/del_folder.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(funcName)s: %(message)s')


class FolderClear:
    def __init__(self, root_dir, **kwargs):
        self.root_dir = root_dir
        self.save_day = int(kwargs['save_day'])
        self.save_copies = int(kwargs['save_copies'])
        self.cut_time = (datetime.datetime.today() - datetime.timedelta(self.save_day)).strftime('%Y%m%d')
        self.file_list = []

    def sort_for_timestamp(self):
        files = os.listdir(self.root_dir)
        file_dict = {}
        for file in files:
            file_path = self.root_dir + '/' + file
            file_timestamp = os.path.getctime(file_path)
            file_dict[file_timestamp] = file_path
        sort_list = sorted(file_dict.items(), key=lambda x: x[0], reverse=False)
        for absolute_path in sort_list:
            self.file_list.append(absolute_path[1])

    def del_file(self):
        self.sort_for_timestamp()
        while len(self.file_list) > self.save_copies:
            file = self.file_list.pop(0)
            file_timestamp = os.path.getctime(file)
            file_ctime = datetime.datetime.fromtimestamp(file_timestamp).strftime('%Y%m%d')
            # print('{}==>{}'.format(file_ctime, self.cut_time))
            if file_ctime > self.cut_time:
                break
            if os.path.isfile(file):
                os.remove(file)
            shutil.rmtree(file)
        else:
            logging.info('{} folder le {} directory or file'.format(self.root_dir, self.save_copies))


if __name__ == '__main__':
    program_path = os.path.dirname(sys.path[0])
    config = configparser.ConfigParser()
    config.read(program_path + '/' + 'conf/del-folder.conf')
    default_parameter = config['default']
    default_day = default_parameter['save_day']
    default_copies = default_parameter['save_copies']
    paths = config.sections()[1:]
    for path in paths:
        if os.path.exists(path) and not str(path).endswith('/'):
            save_day = config.get(path, 'save_day', fallback=default_day)
            save_copies = config.get(path, 'save_copies', fallback=default_copies)
            fc = FolderClear(path, save_day=save_day, save_copies=save_copies)
            fc.del_file()
        else:
            logging.info('Path {0} defined error!!!'.format(path))
