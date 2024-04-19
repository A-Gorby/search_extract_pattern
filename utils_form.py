import ipywidgets as widgets
import pandas as pd
import numpy as np
import os
import sys
from ipywidgets import Layout, Box, Label
# self
from utils_io import logger
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

#     def form_param_cmp_03(self):
#         # fn_01, columns_values_01,
#         # fn_02, columns_values_02):

#         # print(self.columns_values_01)
#         # print(self.columns_values_02)

#         # self.profile_01_enter = widgets.Text(placeholder=columns_values_01['profile'], value=self.columns_values_01['profile'])
#         self.profile_01_enter = widgets.Text(value=self.columns_values_01['profile'])
#         self.tk_code_01_enter = widgets.Text(value=self.columns_values_01['tk_code'])
#         self.tk_name_01_enter = widgets.Text(value=self.columns_values_01['tk_name'])
#         self.model_01_enter = widgets.Text( placeholder='План/Факт/База/Техно...', value=self.columns_values_01['model'])

#         self.profile_02_enter = widgets.Text(value=self.columns_values_02['profile'])
#         self.tk_code_02_enter = widgets.Text(value=self.columns_values_02['tk_code'])
#         self.tk_name_02_enter = widgets.Text(value=self.columns_values_02['tk_name'])
#         self.model_02_enter = widgets.Text(placeholder='План/Факт/База/Техно...', value=self.columns_values_02['model'])

#         self.radio_btn_significance = widgets.RadioButtons(options=['Все строки', 'Только значимые'], value= 'Все строки', disabled=False) # description='Check me',    , indent=False
#         self.significance_threshold_slider = widgets.IntSlider(min=0, max=100, value=100)
#         self.radio_btn_same_headers = widgets.RadioButtons(options=['Повторяет значения 1-го файла', 'Не повторяет'], value= 'Не повторяет')
#         # self.radio_btn_similary_headers = widgets.RadioButtons(options=['Повторяет значения 1-го файла', 'Не повторяет'], value= 'Не повторяет')
#         self.checkbox_sign_serv_by_UET  = widgets.Checkbox(value=True, description='Значимость Услуг - по УЕТ', disabled=False, indent=False)

#         form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')

#         radio_btn_significance_box = Box([Label(value='Сравнение по всем строкам или по значимым:'), self.radio_btn_significance], layout=form_item_layout)
#         significance_threshold_box = Box([Label(value='Сравнение по строкам, составляющим __% значимости ТК:'), self.significance_threshold_slider], layout=form_item_layout)
#         checkbox_sign_serv_by_UET_box = Box([self.checkbox_sign_serv_by_UET], layout=form_item_layout)

#         radio_btn_same_headers_box = Box([Label(value='Профиль, Код и Наименование ТК 2-го файла:'), self.radio_btn_same_headers], layout=form_item_layout)
#         header_box = Box([radio_btn_same_headers_box],  layout=Layout(
#             display='flex', flex_flow='row', justify_content='space-between', border='solid 1px', padding='10px 0px 10px 0px'))

#         headers = ['', self.fn_01, self.fn_02 ]
#         headers = ['', r"<marquee><b>" + self.fn_01 + r"</b></marquee>" , r"<marquee><b>" + self.fn_02 + r"</b></marquee>" ]
#         form_items_flat = [Label('Уточните/Введите Профиль ТК'), self.profile_01_enter, self.profile_02_enter,
#                           Label('Уточните/Введите Код ТК'), self.tk_code_01_enter, self.tk_code_02_enter,
#                           Label('Уточните/Введите Название ТК'), self.tk_name_01_enter, self.tk_name_02_enter,
#                           Label('Уточните/Введите Модель'), self.model_01_enter, self.model_02_enter]

#         style={'font_weight': 'bold', 'font_size': '30px'}
#         grid_box = widgets.GridBox([widgets.HTML(s) for s in headers] + form_items_flat,
#                     layout=widgets.Layout(grid_template_columns="repeat(3, 30%)", border='solid 1px', padding='10px 0px 10px 0px'))
#         footer_box = Box([radio_btn_significance_box, significance_threshold_box, checkbox_sign_serv_by_UET_box],
#                         layout=Layout(display='flex', flex_flow='row', justify_content='space-between', border='solid 1px', padding='10px 0px 10px 0px'))
#         self.form_03 = Box([header_box, grid_box, footer_box],
#                       layout=Layout(display='flex', flex_flow= 'column', border='solid 2px', align_items='stretch', width='80%')) #width='auto', , margin='400px 0px 400px 0'
#         # return form_03, radio_btn_same_headers,\
#         # profile_01_enter, tk_code_01_enter, tk_name_01_enter, model_01_enter, \
#         #                 profile_02_enter, tk_code_02_enter, tk_name_02_enter, model_02_enter, \
#         #                 radio_btn_significance, significance_threshold_slider

#     def on_radio_btn_same_headers_change(self, change):
#         # print(change)
#         if change.new=='Повторяет значения 1-го файла':
#             self.profile_02_enter.value, self.tk_code_02_enter.value, self.tk_name_02_enter.value =\
#             self.profile_01_enter.value, self.tk_code_01_enter.value, self.tk_name_01_enter.value
#         else:
#             try:
#                 self.profile_02_enter.value, self.tk_code_02_enter.value, self.tk_name_02_enter.value =\
#                 self.columns_values_02['profile'], self.columns_values_02['tk_code'], self.columns_values_02['tk_name']
#             except:
#                 pass
#                 # The 'value' trait of a Text instance expected a unicode string, not the NoneType None

#     def on_change_value_copy(self, change):
#         # print(change)
#         widget_lst_01 = [self.profile_01_enter, self.tk_code_01_enter, self.tk_name_01_enter]
#         widget_lst_02 = [self.profile_02_enter, self.tk_code_02_enter, self.tk_name_02_enter]
#         if self.radio_btn_same_headers.value=='Повторяет значения 1-го файла':
#             widget_lst_02[widget_lst_01.index(change.owner)].value = change.new

#     def form_param_cmp_04(self, selected_sections, fn_01, fn_02, cols_file_01, cols_file_02):

#         sections = ['Услуги', 'ЛП', 'РМ']
#         tk_serv_cols = ['Код услуги по Номенклатуре медицинских услуг (Приказ МЗ № 804н)', 'Наименование услуги по Номенклатуре медицинских услуг (Приказ МЗ №804н)', #'Код услуги по Реестру МГФОМС',
#                 'Усредненная частота предоставления', 'Усредненная кратность применения', 'УЕТ 1', 'УЕТ 2']
#         tk_serv_cols_short = ['Код услуги', 'Наименование услуги', #'Код услуги по Реестру МГФОМС',
#                 'Частота', 'Кратность', 'УЕТ 1', 'УЕТ 2']
#         tk_lp_cols = ['Наименование лекарственного препарата (ЛП) (МНН)', 'Код группы ЛП (АТХ)', 'Форма выпуска лекарственного препарата (ЛП)',
#                   'Усредненная частота предоставления', 'Усредненная кратность применения', 'Единицы измерения', 'Кол-во']
#         tk_lp_cols_short = ['МНН', 'Код АТХ', 'Форма выпуска ЛП',
#                   'Частота', 'Кратность', 'Ед. измерения', 'Кол-во']
#         tk_rm_cols = ['Изделия медицинского назначения и расходные материалы, обязательно используемые при оказании медицинской услуги', 'Код МИ из справочника (на основе утвержденного Перечня НВМИ)',
#                   'Усредненная частота предоставления', 'Усредненная кратность применения', 'Ед. измерения', 'Кол-во']
#         tk_rm_cols_short = ['Код МИ/РМ', 'Название МИ/РМ',
#                   'Частота', 'Кратность', 'Ед. измерения', 'Кол-во']
#         tk_cols = [tk_serv_cols, tk_lp_cols, tk_rm_cols]
#         tk_cols_short = [tk_serv_cols_short, tk_lp_cols_short, tk_rm_cols_short]
#         # col_titles = ['Короткое название колонки', 'Колонка из файла 1', 'Колонка из файла 2']

#         col_titles = ["<b>Короткое название колонки</b>", "<b>"+fn_01+"</b>", "<b>"+fn_02+"</b>"]
#         pre_cols_01, pre_cols_02 = [], []
#         form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
#         form_items = []
#         # subforms = []
#         for i, section in enumerate(selected_sections):
#             pre_cols_01.append([])
#             pre_cols_02.append([])
#             pre_cols_01w = [widgets.Dropdown( options=cols_file_01[i], value=col if (col in cols_file_01[i]) else None) for col in tk_cols[i]]
#             pre_cols_02w = [widgets.Dropdown( options=cols_file_02[i], value=col if (col in cols_file_02[i]) else None) for col in tk_cols[i]]
#             pre_cols_01[i].extend(pre_cols_01w) #.append(pre_cols_01w)
#             pre_cols_02[i].extend(pre_cols_02w)
#             #
#             labels_w = [widgets.Label(value=col_sh) for col_sh in tk_cols_short[i]]
#             form_items_w = list(zip(labels_w, pre_cols_01w, pre_cols_02w))
#             # to flat list
#             form_items_flat = [v for r in form_items_w for v in r]
#             # grid_box = widgets.GridBox([Label(s) for s in col_titles] + form_items_flat, layout=widgets.Layout(grid_template_columns="repeat(3, 30%)"))
#             grid_box = widgets.GridBox([widgets.HTML(s) for s in col_titles] + form_items_flat, layout=widgets.Layout(grid_template_columns="repeat(3, 30%)"))

#             self.form_04_subforms.append(grid_box)
#         # form_04 = widgets.Accordion(children=self.form_04_subforms, titles=tuple(self.selected_sections)) # v8 ipywidgets
#         self.form_04 = widgets.Accordion(children = self.form_04_subforms) # v7.7.0 ipywidgets
#         for i, section in enumerate(selected_sections):
#             self.form_04.set_title(i, section)

#         # return form_04, subforms

#     def def_cmp_cols(self):
#         self.cmp_cols_file_01, self.cmp_cols_file_02 = [], []

#         # for i, section in enumerate(intersect_sheets):
#         for i, section in enumerate(self.selected_sections):
#             grid_box = self.form_04_subforms[i]
#             # print(section)
#             # divide into 3 lists
#             rez = [[ch.value for i_ch, ch in enumerate(grid_box.children[3:]) if i_ch%3==1],
#                   [ch.value for i_ch, ch in enumerate(grid_box.children[3:]) if i_ch%3==2]]
#             self.cmp_cols_file_01.append([ch.value for i_ch, ch in enumerate(grid_box.children[3:]) if i_ch%3==1])
#             self.cmp_cols_file_02.append([ch.value for i_ch, ch in enumerate(grid_box.children[3:]) if i_ch%3==2])
#             # print(grid_box.children[3:9])
#         return

# def def_filters(selected_sections, observed_widgets, changed_widgets):
#     # filters = list(zip([col.value for sections in observed_widgets for col in sections], [v.value for sections in changed_widgets for v in sections]))
#     filters = [col.value for sections in observed_widgets for col in sections], [v.value for sections in changed_widgets for v in sections]
#     # pprint(filters)
#     filters_01 = list(zip(filters[0][0::2], filters[1][0::2]))
#     # print(filters_01)
#     filters_02 = list(zip(filters[0][1::2], filters[1][1::2]))
#     # print(filters_02)

#     filters_01 = {section: {filters_01[i_s][0]:filters_01[i_s][1]} for i_s, section in enumerate(selected_sections)}
#     filters_02 = {section: {filters_02[i_s][0]:filters_02[i_s][1]} for i_s, section in enumerate(selected_sections)}
#     return filters_01, filters_02

# def read_tkbd_options_filter(path_tkbd_source, fn_tk_bd, cmp_sections, filters):
#     logger.info(f"Чтение '{fn_tk_bd}' ...")
#     print(cmp_sections)
#     xl = pd.ExcelFile(os.path.join(path_tkbd_source, fn_tk_bd))
#     # if not set(['Услуги', 'ЛП', 'РМ']).issubset(xl.sheet_names):
#     if not set(cmp_sections).issubset(xl.sheet_names):

#         logger.error(f"Обработка перкращена: в Excel файле со сводом ТК отсутсnвует все необходивмые листы: {str(cmp_sections)}")
#         sys.exit(2)
#     std_sections = ['Услуги', 'ЛП', 'РМ']
#     section = 'Услуги'
#     # df_services, df_LP, df_RM = None, None, None
#     # df_lst = [df_services, df_LP, df_RM]
#     df_lst = len(std_sections) * [None]

#     for i_section, section in enumerate(std_sections):
#         if section in cmp_sections:
#             # df_services = pd.read_excel(os.path.join(path_tkbd_source, fn_tk_bd), sheet_name = section)
#             df_section = pd.read_excel(os.path.join(path_tkbd_source, fn_tk_bd), sheet_name = section)
#             # print(filters[section].items())
#             # print(list(filters[section].items())[0])
#             # print(filters[section].keys())
#             # print(filters[section].values())
#             # print(cmp_sections.index(section))
#             key, value = list(filters[section].items())[0] # [cmp_sections.index(section)]
#             #print(section, key ,value)
#             if key is not None:
#                 logger.info(f"Filter: {key}: {value}")
#                 if value is not None:
#                     if (type(value)==str) and (value=='Пусто'):
#                         try:
#                             df_section = df_section[df_section[key].isnull()]
#                         except Exception as err:
#                             print(f"Read {section} ERROR:", err)
#                     else:
#                         try:
#                             df_section = df_section[df_section[key].notnull() & (df_section[key]==value)]
#                         except Exception as err:
#                             print(f"Read {section} ERROR:", err)
#                 else:
#                     try:
#                         df_section = df_section[df_section[key].isnull()]
#                     except Exception as err:
#                         print(f"Read {section} ERROR:", err)


#             logger.info(f"Получены данные с листа '{section}': {df_section.shape}")
#             #display(df_section.head(2))
#             df_lst[i_section] = df_section
#         # else: df_services = None

#     # df_LP, df_RM = None, None
#     df_services, df_LP, df_RM = df_lst
#     return df_services, df_LP, df_RM

# def try_get_headers(df_services, df_LP, df_RM):

#     try_columns = {'profile':'Профиль', 'tk_code':'Код ТК', 'tk_name': 'Наименование ТК', 'model':'Модель пациента'}
#     columns_values = {'profile': None, 'tk_code': None, 'tk_name': None, 'model': None}
#     fl_fill= False
#     for df in [df_services, df_LP, df_RM]:
#         if df is not None:
#             for val_name, col_name in try_columns.items():
#                 # print(val_name, col_name)
#                 if col_name in df.columns:
#                     if columns_values[val_name] is  None:
#                         # if df[col_name].dtype==float:
#                         #     df[col_name] = df[col_name].astype(object)
#                         values = df[col_name].unique()
#                         # print(values.dtype)
#                         # print(values)
#                         try:

#                             values = [x for x in values if str(x) != 'nan']
#                             values = np.array([str(x) for x in values])
#                             # print("try:", values)
#                         except Exception as err:
#                             print(err)
#                         if len(values)>0:
#                             columns_values[val_name] = values[0]
#                             fl_fill = True
#         if fl_fill: break

#     return columns_values

# def form_param_esklp_exist_dicts(esklp_dates):
#     esklp_dates_dropdown = widgets.Dropdown( options=esklp_dates) #, value=None)

#     form_item_layout = Layout(display='flex', flex_flow='row', justify_content='space-between')
#     check_box = Box([Label(value="Выберите дату сохраненного справочника ЕСКЛП:"), esklp_dates_dropdown], layout=form_item_layout)
#     form_items = [check_box]

#     #form_esklp_exist_dicts = Box(form_items, layout=Layout(display='flex', flex_flow= 'column', border='solid 2px', align_items='stretch', width='460%')) #width='auto')) #
#     form_esklp_exist_dicts = Box(form_items,
#     layout=Layout(display='flex', border='solid 2px', flex_flow= 'column', align_items='flex-start', justify_content='space-between', width='auto')) #width='60%'))   flex_flow= 'row',

#     # return form, fn_check_file_drop_douwn, fn_dict_file_drop_douwn, radio_btn_big_dict, radio_btn_prod_options, similarity_threshold_slider, max_entries_slider
#     return form_esklp_exist_dicts, esklp_dates_dropdown
