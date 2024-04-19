import ipywidgets as widgets
import pandas as pd
import numpy as np
import os
import sys
from ipywidgets import Layout, Box, Label

# from utils_io import logger
from utils_io import Logger

logger = Logger().logger
logger.propagate = False

if len(logger.handlers) > 1:
    for handler in logger.handlers:
        logger.removeHandler(handler)
    # del logger
    logger = Logger().logger
    logger.propagate = False


class FormsPatternSearch:

    def __init__(self, data_source_dir):
        self.data_source_dir = data_source_dir
        self.form_01_to_null()
        self.fn_01 = None
        self.fn_02 = None
        self.form_02_to_null()
        self.form_03_to_null()
        self.form_04_to_null()

    def form_01_to_null(self):
        # self.sheets_01 = []
        # self.sheets_02 = []

        self.source_sheets = []
        self.selected_sheet = []
        self.fn_check_file1_drop_down = None
        # self.check_sheet_names_drop_down = None
        self.check_sheet_names_drop_down = None
        self.cols_file_01 = []
        self.form_01 = None

    def form_02_to_null(self):


        # self.сols_file_02 = []
        # self.observed_widgets = []
        # self.changed_widgets = []
        self.form_02 = None
        self.col_with_data = None
        self.col_with_filter = None
        # self.form_02_subforms = []
        # self.columns_values_01 = {'profile': None, 'tk_code': None, 'tk_name': None, 'model': None}
        # self.columns_values_02 = {'profile': None, 'tk_code': None, 'tk_name': None, 'model': None}
        # self.col_with_data_values = None
        self.col_with_filter_values = None
        self.filter_value = None

    def form_03_to_null(self):
        self.pttn_01_word_for_extract_enter = None
        self.pttn_01_word_for_extract_value = None
        self.form_03 = None

    def form_04_to_null(self):
        self.form_04_subforms = []
        self.form_04 = None
        self.cmp_cols_file_01 = []
        self.cmp_cols_file_02 = []

    def form_param_01(self, fn_list):

        self.fn_check_file1_drop_down = widgets.Dropdown( options=fn_list, value=None)
        form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
        check_box_file1 = Box([Label(value="Выберите Excel-файл с данными"), self.fn_check_file1_drop_down], layout=form_item_layout)
        # multi_select = Box([Label(value="Выберите разделы (Ctrl для мнж выбора) для сравнения: 'Услуги', 'ЛП', 'РМ':"), self.sections_drop_douwn], layout=form_item_layout) #, tips='&&&')

        self.check_sheet_names_drop_down = widgets.Dropdown(value=None)
        form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
        check_box_sheet_names = Box([Label(value="Выберите Лист Excel с данными"), self.check_sheet_names_drop_down], layout=form_item_layout)

        form_items = [check_box_file1, check_box_sheet_names ]

        self.form_01 = Box(form_items, layout=Layout(display='flex', flex_flow= 'column', border='solid 2px', align_items='stretch', width='75%')) #width='auto'))
        # return self.form_01, fn_check_file1_drop_douwn, fn_check_file2_drop_douwn, sections_drop_douwn

    def on_fn_check_file1_drop_douwn_change(self, change):
        self.fn_01 = self.fn_check_file1_drop_down.value
        # try:
        xl_01 = pd.ExcelFile(os.path.join(self.data_source_dir, self.fn_01))
        self.source_sheets = xl_01.sheet_names
        print(f"Листы файла: {str(self.source_sheets)}") # logger
        self.check_sheet_names_drop_down.options = self.source_sheets

        # except Exception as err:
        #     print(f"Ошибка чтения файла: {str(err)}")
        #     self.source_sheets = []

    @staticmethod
    def get_col_names_from_excel(path, fn, sheet):
        cols_file = []
        # for sheet in sheets:
        try:
            df = pd.read_excel(os.path.join(path, fn), sheet_name=sheet, nrows=5, header=0)
            cols_file = list(df.columns)
            # print(sheet, list(df.columns))
        except Exception as err:
            print(err)

        return cols_file


    def on_check_box_sheet_names_change(self, change):
        self.selected_sheet = self.check_sheet_names_drop_down.value
        try:
            self.cols_file_01 = self.get_col_names_from_excel(self.data_source_dir, self.fn_01, self.selected_sheet)
            print("Названия колонок в файле", self.cols_file_01)


        except Exception as err:
            self.cols_file_01 = []
            logger.error("Ошибка чтения колонок выбранных файлов. Не забывайте: навзания колонок должны быть в первой строке")
            sys.exit(2)

    def form_param_02(self, data_source_dir, fn_01):
        self.cols_with_data_drop_down = widgets.Dropdown( options=self.cols_file_01, value=None)
        if 'Характеристика значение' in self.cols_file_01:
                self.cols_with_data_drop_down.value = 'Характеристика значение'
        form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
        check_box_cols_with_data = Box([Label(value="Выберите Колонку с данными"),self.cols_with_data_drop_down], layout=form_item_layout)

        self.cols_with_filter_drop_down = widgets.Dropdown( options=self.cols_file_01, value=None)
        form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
        check_box_cols_with_filter = Box([Label(value="Выберите (при необходимости) Колонку с фильром"), self.cols_with_filter_drop_down], layout=form_item_layout)

        self.data_for_filter_drop_down = widgets.Dropdown(value=None)
        form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
        check_box_data_for_filter = Box([Label(value="Выберите значение для фильра"), self.data_for_filter_drop_down], layout=form_item_layout)

        form_items = [check_box_cols_with_data, check_box_cols_with_filter, check_box_data_for_filter]

        self.form_02 = Box(form_items, layout=Layout(display='flex', flex_flow= 'column', border='solid 2px', align_items='stretch', width='75%')) #width='auto'))

    def on_cols_with_data_drop_down_change(self, change):
        self.col_with_data = self.cols_with_data_drop_down.value
        print("self.col_with_data:", self.col_with_data)

    def on_cols_with_filter_drop_down_change(self, change):
        self.col_with_filter = self.cols_with_filter_drop_down.value
        try:
            unique = self.get_uniuque_by_col_name_from_excel(self.data_source_dir, self.fn_01, self.selected_sheet, self.col_with_filter)
            print("Уникальные значения для фильтра ", unique)
            self.data_for_filter_drop_down.options = unique

        except Exception as err:
            self.col_with_filter_values = None
            logger.error(str(err))
            sys.exit(2)

    def on_data_for_filter_drop_down_change(self, change):
        self.filter_value = self.data_for_filter_drop_down.value
        if (self.filter_value == 'Пусто'):
            self.filter_value = None

    def form_param_03(self):

        self.pttn_01_word_for_extract_enter = widgets.Text(placeholder='Слово...', value=None)
        form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
        text_for_pttn_01_word_for_extract = Box([Label(value="Введите слово для выделения"), self.pttn_01_word_for_extract_enter], layout=form_item_layout)
        # self.radio_btn_similary_headers = widgets.RadioButtons(options=['Повторяет значения 1-го файла', 'Не повторяет'], value= 'Не повторяет')

        form_items = [text_for_pttn_01_word_for_extract]

        self.form_03 = Box(form_items, layout=Layout(display='flex', flex_flow= 'column', border='solid 2px', align_items='stretch', width='75%')) #width='auto'))


    def on_pttn_01_word_for_extract_enter_change(self, change):
        self.pttn_01_word_for_extract_value = self.pttn_01_word_for_extract_enter.value


    @staticmethod
    def np_unique_nan(lst: np.array, debug = False)->np.array: # a la version 2.4
        lst_unique = None
        if lst is None or (((type(lst)==float) or (type(lst)==np.float64)) and np.isnan(lst)):
            # if debug: print('np_unique_nan:','lst is None or (((type(lst)==float) or (type(lst)==np.float64)) and math.isnan(lst))')
            lst_unique = lst
        else:
            data_types_set = list(set([type(i) for i in lst]))
            if debug: print('np_unique_nan:', 'lst:', lst, 'data_types_set:', data_types_set)
            if ((type(lst)==list) or (type(lst)==np.ndarray)):
                if debug: print('np_unique_nan:','if ((type(lst)==list) or (type(lst)==np.ndarray)):')
                if len(data_types_set) > 1: # несколько типов данных
                    if list not in data_types_set and dict not in data_types_set \
                          and tuple not in data_types_set and type(None) not in data_types_set\
                          and np.ndarray not in data_types_set: # upd 17/02/2023
                        lst_unique = np.array(list(set(lst)), dtype=object)
                    else:
                        lst_unique = lst
                elif len(data_types_set) == 1:
                    if debug: print("np_unique_nan: elif len(data_types_set) == 1:")
                    if list in data_types_set:
                        lst_unique = np.unique(np.array(lst, dtype=object))
                    elif  np.ndarray in data_types_set:
                        # print('elif  np.ndarray in data_types_set :')
                        lst_unique = np.unique(lst.astype(object))
                        # lst_unique = np_unique_nan(lst_unique)
                        lst_unique = np.asarray(lst, dtype = object)
                        # lst_unique = np.unique(lst_unique)
                    elif type(None) in data_types_set:
                        # lst_unique = np.array(list(set(lst)))
                        lst_unique = np.array(list(set(list(lst))))
                    elif dict in  data_types_set:
                        lst_unique = lst
                        # np.unique(lst)
                    elif type(lst) == np.ndarray:
                        if debug: print("np_unique_nan: type(lst) == np.ndarray")
                        if (lst.dtype.kind == 'f') or  (lst.dtype == np.float64) or  (float in data_types_set):
                            if debug: print("np_unique_nan: (lst.dtype.kind == 'f')")
                            lst_unique = np.unique(lst.astype(float))
                            # if debug: print("np_unique_nan: lst_unique predfinal:", lst_unique)
                            # lst_unique = np.array(list(set(list(lst))))
                            # if debug: print("np_unique_nan: lst_unique predfinal v2:", lst_unique)
                            # if np.isnan(lst).all():
                            #     lst_unique = np.nan
                            #     if debug: print("np_unique_nan: lst_unique predfinal v3:", lst_unique)
                        elif (lst.dtype.kind == 'S') :
                            if debug: print("np_unique_nan: lst.dtype == string")
                            lst_unique = np.array(list(set(list(lst))))
                            if debug: print(f"np_unique_nan: lst_unique 0: {lst_unique}")
                        elif lst.dtype == object:
                            if debug: print("np_unique_nan: lst.dtype == object")
                            if (type(lst[0])==str) or (type(lst[0])==np.str_) :
                                try:
                                    lst_unique = np.unique(lst)
                                except Exception as err:
                                    lst_unique = np.array(list(set(list(lst))))
                            else:
                                lst_unique = np.array(list(set(list(lst))))
                            if debug: print(f"np_unique_nan: lst_unique 0: {lst_unique}")
                        else:
                            if debug: print("np_unique_nan: else 0")
                            lst_unique = np.unique(lst)
                    else:
                        if debug: print('np_unique_nan:','else i...')
                        lst_unique = np.array(list(set(lst)))

                elif len(data_types_set) == 0:
                    lst_unique = None
                else:
                    # print('else')
                    lst_unique = np.array(list(set(lst)))
            else: # другой тип данных
                if debug: print('np_unique_nan:','другой тип данных')
                # lst_unique = np.unique(np.array(list(set(lst)),dtype=object))
                # lst_unique = np.unique(np.array(list(set(lst)))) # Исходим из того что все елеменыт спсика одного типа
                lst_unique = lst
        if type(lst_unique) == np.ndarray:
            if debug: print('np_unique_nan: final: ', "if type(lst_unique) == np.ndarray")
            if lst_unique.shape[0]==1:
                if debug: print('np_unique_nan: final: ', "lst_unique.shape[0]==1")
                lst_unique = lst_unique[0]
                if debug: print(f"np_unique_nan: final after: lst_unique: {lst_unique}")
                if (type(lst_unique) == np.ndarray) and (lst_unique.shape[0]==1):  # двойная вложенность
                    if debug: print('np_unique_nan: final: ', 'one more', "lst_unique.shape[0]==1")
                    lst_unique = lst_unique[0]
            elif lst_unique.shape[0]==0: lst_unique = None
        if debug: print(f"np_unique_nan: return: lst_unique: {lst_unique}")
        if debug: print(f"np_unique_nan: return: type(lst_unique): {type(lst_unique)}")
        return lst_unique

    @staticmethod
    def get_uniuque_by_col_name_from_excel(path, fn, sheet, col_name):
        try:
            df = pd.read_excel(os.path.join(path, fn), sheet_name=sheet, header=0, usecols=[col_name])
            # unique = df[col_name].unique()
            # не обрабатывает когда столбец со строковыми значениями и попадаются пустые значения - "не видит"
            unique = np.array(list(set(df[col_name].values)))
            if not ((unique.dtype=='float') or (unique.dtype=='float64')):
                # if np.isnan(unique).any(): #, casting='safe'
                # if 'nan' in unique :
                #     unique[unique=='nan'] = 'Пусто'
                unique = np.array(['Пусто' if u=='nan' else u for u in unique])
                # unique = np.unique(list(set(unique)))
                unique = np.unique(np.array(list(set(unique))))
            else:
                unique = np.unique(unique)
            # print(sheet, col_name, unique)
        except Exception as err:
            print(err)
            unique = None

        return unique

