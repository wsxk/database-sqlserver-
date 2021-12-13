from my_sql_homework import wsxk_cmd
import os

if __name__ == "__main__":
    try:
        os.system('cls')
        wxk = wsxk_cmd()
        wxk.cmdloop()
    except:
        exit()