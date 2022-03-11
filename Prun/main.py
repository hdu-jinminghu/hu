'''
Author: your name
Date: 2021-03-25 10:33:56
LastEditTime: 2021-03-25 10:42:39
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\main.py
'''
from absl import app, flags
import manage
import sys
# FLAGS = flags.FLAGS
# flags.DEFINE_string("port", None, "Specify django port.")

# # 指定必须输入的参数
# flags.mark_flag_as_required("port")


# def run_migrate(argv):
#     argvs = [
#         FLAGS.port,
#         "migrate",
#     ]
#     manage.main(argvs)


def run_main(argv):
    argvs = [
        "main.py",
        "runserver",
        "0.0.0.0:8000" , 
        "--noreload",
    ]
    manage.main(argvs)


if __name__ == "__main__":
    # app.run(run_migrate)
    app.run(run_main)