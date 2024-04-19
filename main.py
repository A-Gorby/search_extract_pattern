import re
from tqdm import tqdm
tqdm.pandas()
import os
import sys
import glob
import openpyxl
import datetime
import pandas as pd
import numpy as np
import humanize
import re
import xlrd

from utils_io import get_humanize_filesize

def read_filter_data(data_source_dir, fn = None,
    sh_n = None, filter_col=None, filter_value=None,
    n_rows=None):
    """
    """
    df_01 = None
    df_02 = None
    # print(f"data_source_dir: '{data_source_dir}', fn: '{fn}', sheet_name: '{sh_n}'")
    try:
        if n_rows is None:
            df_01 = pd.read_excel(os.path.join(data_source_dir, fn), sheet_name=sh_n)
        else:
            df_01 = pd.read_excel(os.path.join(data_source_dir, fn), sheet_name=sh_n, nrows=n_rows)
        print("Входной файл: (строк, колонок):", df_01.shape)
        # print(df_01.columns)
        print(f"Колонка для фильтра _00: '{filter_col}', Значение фильтра: '{filter_value}'")
        if not ((filter_col is None ) or (filter_col ==' ') or (filter_col == 'None')):
            print(f"Колонка для фильтра: '{filter_col}', Значение фильтра: '{filter_value}'")
            try:
                mask = (df_01[filter_col].notnull() & (df_01[filter_col]==filter_value))
                df_02 = df_01[mask]
                print("Входной файл с учетом фильтра: (строк, колонок):", df_02.shape)
            except Exception as err:
                print(err)
        else:
            df_02 = df_01.copy()

    except Exception as err:
        print(err)


    return df_01, df_02

def get_xlsx_sheet_cols_widths(data_source_dir, fn, sheet_name):
    worksheet = openpyxl.load_workbook(os.path.join(data_source_dir, fn))
    # sheet = worksheet.active
    sheet = worksheet[sheet_name]
    # print(fn)
    # print(sheet_name, sheet)
    # print(list(sheet.column_dimensions))
    cols_widths_lst = [round(sheet.column_dimensions[c].width) for c in list(sheet.column_dimensions)]
    # print(cols_widths_lst)
    return cols_widths_lst


def save_to_excel(
    data_processed_dir,
    fn_main,
    df_lst,
    sh_n_lst,
    widths_lsts_list,
    ):
    offset = datetime.timezone(datetime.timedelta(hours=3))
    dt = datetime.datetime.now(offset)
    str_date = dt.strftime("%Y_%m_%d_%H%M")
    fn_save = fn_main + '_' + str_date + '.xlsx'
    with pd.ExcelWriter(os.path.join(data_processed_dir, fn_save), engine='xlsxwriter') as writer:
        workbook = writer.book
        format_float = workbook.add_format({"num_format": "# ### ##0.00"})
        format_int = workbook.add_format({"num_format": "# ### ##0"})
        header_format = workbook.add_format({'bold': True,"text_wrap": 1,"valign": "top", "align": "left",}) #'fg_color': '#D7E4BC','border': 1})

        for sh_n, data_df, cols_width  in zip(sh_n_lst, df_lst, widths_lsts_list):
            data_df.to_excel(writer, sheet_name = sh_n, float_format="%.2f", index=False) #
            worksheet = writer.sheets[sh_n]
            # print(cols_width)
            for i_w, w in enumerate(cols_width):
                worksheet.set_column(i_w, i_w, w, None)
            worksheet.autofilter(0, 0, data_df.shape[0], data_df.shape[1]-1)
    print(fn_save)
    print(get_humanize_filesize(data_processed_dir, fn_save))
    return fn_save

def extract_words(s, preposition):
    """
    v01.02 18.04.2024
    """
    s_cut = s
    words_part = None
    if s is None or (type(s)!=str):
        return None, s
    pttn_re_single = fr"{preposition}"
    try:
        m = re.search(pttn_re_single, s, flags=re.I)
    except Exception as err:
        print(err)
        m = re.search(re.escape(pttn_re_single), s, flags=re.I)
    if m is not None:
        words_part = m.group()
        s_cut = s.replace(words_part,'', 1)

    return words_part, s_cut

def apply_extract_words_split_rows(df_input, preposition, col_source='Характеристика значение', col_target='Характеристика значение'):
    """
    v 01.01 18.04.2024
    """
    df_output = df_input.copy()
    output_lst = []
    print(f"apply_extract_words_split_rows: col_source: '{col_source}'")
    col_source_new = col_source
    if col_source==col_target:
        if col_source + ' pred' in df_output.columns:
            cnt = 0
            for col in df_output.columns:
                if col_source + ' pred' in col:
                    cnt += 1
            col_source_new = col_source + f' pred_{cnt+1:02d}'

        else:
            col_source_new = col_source + ' pred'
            # df_output.rename(columns={col_source: }, inplace=True)
        df_output.rename(columns={col_source: col_source_new}, inplace=True)

    for i_row, row in tqdm(df_output.iterrows(), total = df_output.shape[0]):
        d_source = dict(row)
        words_part, s_cut = extract_words(row[col_source_new], preposition)
        if words_part is not None:
            d_source.update({col_target: words_part})
            output_lst.append(d_source)
        d_source = dict(row)
        # if s_cut is not None:
        if (type(s_cut)==str):
            s_cut = s_cut.strip()   # обрехать пробелы с краев
            # s_cut = re.sub(r"\s+", r"\s", s_cut) # сократить  "внутренние" пробелы от двух и больше до одного
            s_cut = re.sub(r" +", r" ", s_cut) # сократить  "внутренние" пробелы от двух и больше до одного
        d_source.update({col_target: s_cut})
        output_lst.append(d_source)

    df_output = pd.DataFrame(output_lst)
    return df_output

def combine_sheet_name(sheet_name: str, preposition: str) -> str : 
    """
    v 01.01 19.04.2024
    """
    if sheet_name is None or preposition is None:
        return None
    max_sheet_name_length = 31
    sheet_name_len = len(sheet_name )
    preposition_len = len(preposition)
    ratio = max_sheet_name_length/(sheet_name_len + preposition_len)
    # print(ratio)
    new_sheet_name = sheet_name[:int(ratio*sheet_name_len)] + '_' + preposition[:int(ratio*preposition_len)]

    return new_sheet_name[:max_sheet_name_length]

def search_extract_pattern(
    data_source_dir, data_processed_dir,
    fn, sheet_name,
    col_source='Характеристика значение', col_target='Характеристика значение',
    col_with_filter=None, filter_value=None,
    preposition='для аппарата', 
):
    """
    v01.01 19.04.2024 
    """

    df_01, df_02 = read_filter_data(data_source_dir, fn, sheet_name, col_with_filter, filter_value, n_rows=None)
    display(df_02.head())
    df_04 = apply_extract_words_split_rows(df_02, preposition=preposition, col_source=col_source, col_target=col_target)
    # apply_extract_words_split_rows(df_input, preposition, col_source='Характеристика значение', col_target='Характеристика значение')
    print(); print()
    print(f"Выходной файл: (строк, колонок): {df_04.shape}")
    display(df_04.head())
    cols_widths_lst = get_xlsx_sheet_cols_widths(data_source_dir, fn=fn, sheet_name=sheet_name)
    new_sheet_name = combine_sheet_name(sheet_name, preposition)
    save_to_excel(
          data_processed_dir=data_processed_dir,
          fn_main = fn.split('.xlsx')[0],
          df_lst = [df_04],
          sh_n_lst = [new_sheet_name],
          widths_lsts_list = [cols_widths_lst + [40]],
          )
    return df_01, df_02, df_04

