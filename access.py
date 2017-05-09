#!/usr/bin/python
#coding: utf-8

import actions
from init import Init

if __name__ == '__main__':
    try:
        loader = Init()
        config = loader.getConfig()

        action = getattr(actions, config.action)(config)
        action.run()
    except Exception as e:
        error = 'ERROR: \033[1m{}\033[0m'.format(e)
        print(error)
