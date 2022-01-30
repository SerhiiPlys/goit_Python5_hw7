"""Скрипт написан под мои личные предпочтения с учетом требований ДЗ
   Поскольку наиболее точные требования заказчика (который я сам!!!) знаю только я
   постольку под себя его и сделал. Конечно логика его может меняться. Это версия 4.2022
   Иправлены баги удаления пустых папок и ошибки создания папки архива (если она уже есть
   при повторном вызове.
   Также использована логика входа через комстроку или ручной ввод 
"""

import os  # work with file system
import sys # for command line
import shutil # for func copy
import re # string func
import time

path_test = "C:\\Users\\Ultra\\Desktop\\garbage"
log_list = []

TRANS = {}
def make_trans_dict():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l",
                   "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "",
                   "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    global TRANS
    CYR = []
    for i in CYRILLIC_SYMBOLS:
        CYR.append(i)
    for i,j in zip(CYR, TRANSLATION):
        TRANS[ord(i)] = j
        TRANS[ord(i.upper())] = j.upper()

def check_name(name_a):
    name_a_a = name_a.translate(TRANS)
    return re.sub(r'[^a-zA-Z0-9.]', '_', name_a_a)

def empty_dir(path_a):
    """Проверка что директория пуста - тогда возврат True
       если путь ошибочен или папка не пустая возврат False
    """
    if os.path.exists(path_a):
        sz = os.path.getsize(path_a)
        if sz == 0:
            return True
        else:
            return False
    else:
        return False

def del_empty_dir(path_b):
    """Удаление пустой папки и подпапок, фугкция рекурсивная, ппосокльку
       функция os.rmdir() удаляет только папку без вложенных обьектов,
       поэтому нужно рекусрсивно проходить по поути до нижнего уровня и удалять
       Входя сюда мы уже точно знаем что размер обьекта = 0
    """
    ls_1 = os.listdir(path_b)
    if bool(ls_1) == True:    
        path_b_a = os.path.join(path_b, ls_1[0]) # путь к подобьекту
        del_empty_dir(path_b_a)            # рекурсивный вызов по дочернему пути 
        ls_1.pop(0)
        if bool(ls_1) == True:
            del_empty_dir(path_b)
        else:
            os.rmdir(path_b) # и удаляем саму родительскую папку - она осталась единственная
            return
    else:
        os.rmdir(path_b)  # удаляем папку - она одна без вложенных обьектов

def main():      
    """ вход в программу  - проверка пути из командной строки, наличие каталога и предложение
        на ввод вручную если ошибки через комстроку
        проверяем существование каталога и создаем все папки, если путь входа корректен
    """
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        if os.path.exists(path):
            print(path)
            print("Папка существует, продолжаем")
        else:    # путь есть но он кривой - вводим вручную
            print("Ошибка в комстроке пути к папке либо папки не существует")
            path = input("Введите путь к папке:\nИспользуйте двойной Бэкслеш \\\ как разделитель\n")
            print(path)
            log_list.append(f"Папка для расхламления {path}\n")
    else:  # пути нет в комстроке - вводим вручную
         print("Путь в комстроке пуст")
         path = input("Введите путь к папке:\nИспользуйте двойной Бэкслеш \\\ как разделитель\n")
         print(path)
         log_list.append(f"Папка для расхламления {path}\n")

     # делаем словарь для транслитерализации - путь существует, впустую память не займем
    make_trans_dict()
        
    if not os.path.isdir(path):
        print("Ошибка в пути к папке")
        os._exit(-1)  # код ошибки
    else:
        if not os.path.exists(path+'\\images'):
            os.mkdir(path+'\\images')
        if not os.path.exists(path+'\\documents'):
            os.mkdir(path+'\\documents')
        if not os.path.exists(path+'/audio'):
            os.mkdir(path+'/audio')
        if not os.path.exists(path+'/video'):
            os.mkdir(path+'/video')
        if not os.path.exists(path+'/archives'):
            os.mkdir(path+'/archives')
        if not os.path.exists(path+'/others'):
            os.mkdir(path+'/others')
            
     #получаем все пути к существующим файлам
    ls_files = []
    print("Список существующих файлов в выбранной папке:")
    log_list.append("Список существующих файлов в выбранной папке:\n")
    for root,dirs,files in os.walk(path):
        for f in files:
            full_adr = os.path.join(root, f)
            print(full_adr)
            log_list.append(full_adr+'\n')
            ls_files.append(full_adr)
    print(' ')

      #раскидываем файлы по папкам назначения согласно расширения
    for full_adr_s in ls_files:
        try:
            if (("images" in full_adr_s) or ("documents" in full_adr_s) or
                ("video" in full_adr_s) or ("audio" in full_adr_s) or
                ("archives" in full_adr_s) or ("other" in full_adr_s)):
                continue #пропускаем файлы и пути в сущетствующих папках назначения
            elif ((".xlsx" in full_adr_s) or (".txt" in full_adr_s) or
                (".doc" in full_adr_s) or (".docx" in full_adr_s) or
                (".pdf" in full_adr_s) or (".pptx" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\documents', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} в \n{full_adr_d}\n")
            elif ((".jpeg" in full_adr_s) or (".bmp" in full_adr_s) or
                (".jpg" in full_adr_s) or (".png" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\images', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} в \n{full_adr_d}\n")
            elif ((".avi" in full_adr_s) or (".mpeg" in full_adr_s) or
                (".mp4" in full_adr_s) or (".mov" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\video', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} в \n{full_adr_d}\n")
            elif ((".mp3" in full_adr_s) or (".ogg" in full_adr_s) or
                (".wav" in full_adr_s) or (".amr" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\audio', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} в \n{full_adr_d}\n")
            elif ((".zip" in full_adr_s) or (".rar" in full_adr_s) or
                (".tar" in full_adr_s) or (".gz" in full_adr_s)):
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\archives', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} в \n{full_adr_d}\n")
            else:
                normal_name = check_name(os.path.basename(full_adr_s))
                full_adr_d = os.path.join(path+'\\others', normal_name)
                shutil.copyfile(full_adr_s, full_adr_d)
                os.remove(full_adr_s)
                print(f"Перемещение \n{full_adr_s} в \n{full_adr_d}")
                log_list.append(f"Перемещение \n{full_adr_s} в \n{full_adr_d}\n")
        except:
            print("Ошибка в путях либо копировании файлов")
            log_list.append("Ошибка в путях либо копировании файлов\n")
            os._exit(-2)

       #удаляем пустые папки
    print("Список удаляемых пустых папок:")
    log_list.append("Список удаляемых пустых папок:\n")
    ls_dirs_1 = os.listdir(path)    # список из папок первого уровня
    for d in ls_dirs_1:             #
        full_adr = os.path.join(path, d) 
        if empty_dir(full_adr):
            try:
                if (("images" in full_adr) or ("documents" in full_adr) or
                    ("video" in full_adr) or ("audio" in full_adr) or
                    ("archives" in full_adr) or ("other" in full_adr)):
                    continue #пропускаем папки в сущетствующих папках назначения
                else:
                    print(f"Удаление пустой папки\n{full_adr}")
                    log_list.append(f"Удаление пустой папки\n{full_adr}\n")
                    del_empty_dir(full_adr) #удаляем папку и подпапки - рекурсия - указываем родительскую папку
            except:
                print("Ошибка в удалении пустых папок")
    print(' ')

       # распаковываем архивы в подпапки
    print("Перемещение и распаковка архивов:")
    log_list.append("Перемещение и распаковка архивов:\n")
    ls_archives = os.listdir(path+'/archives')
    for arc in ls_archives:
        if (".zip" in arc) or (".rar" in arc) or (".tar" in arc):
            arc_n = arc[0:len(arc) - 4]
            if not os.path.exists(os.path.join(path+'/archives', arc_n)):
                 os.mkdir(os.path.join(path+'/archives', arc_n))
            try:
                shutil.unpack_archive(arc, os.path.join(path+'/archives', arc_n))
                os.remove(os.path.join(path+'/archives', arc))
                print(f"Архив {arc} распакован в папку {arc}")
                log_list.append(f"Архив {arc} распакован в папку {arc}\n")
            except:
                print(f"{arc} архив неопознан или поврежден")
                log_list.append(f"{arc} архив неопознан или поврежден\n")
        elif (".gz" in arc):
            arc_n = arc[0:len(arc) - 3]
            if not os.path.exists(os.path.join(path+'/archives', arc_n)):
                 os.mkdir(os.path.join(path+'/archives', arc_n))
            try:
                shutil.unpack_archive(arc, os.path.join(path+'/archives', arc_n))
                os.remove(os.path.join(path+'/archives', arc))
                print(f"Архив {arc} распакован в папку {arc}")
                log_list.append(f"Архив {arc} распакован в папку {arc}\n")
            except:
                print(f"{arc} архив неопознан или поврежден")
                log_list.append(f"{arc} архив неопознан или поврежден\n")

      # логирование нормальной работы приложения
    local_time = time.asctime()
    print(f"Создан логфайл {local_time}.txt")
    with open(path+"\\log.txt", 'x') as file_log:
        file_log.write((f"Файл логирования сортировки папки {path}\
                       \nсоздан {local_time} \n"))
        s_log = ''
        for item in log_list:
            s_log += item 
        file_log.write(s_log)

        

if __name__ == "__main__":
    main()
    



