#encoding:utf8
#功能处理原始豆瓣图书数据
import os
import xlrd
import json

#遍历文件
def get_filelist():
    file_list = []
    base_uri = "../raw_data/"
    for files in os.listdir(base_uri):
        file_list.append(os.path.join(base_uri,files))
    return file_list

def get_data(file_list):
    book_list = []
    #遍历文件
    for files in file_list:
        book = xlrd.open_workbook(files)
        print("processing book %s" % files)
        #遍历sheet
        for sheet_names in book.sheet_names():
            sheet = book.sheet_by_name(sheet_names)
            #row
            for row in range(sheet.nrows):
                if row == 0:
                    continue
                item = {}
                item['cat'] = sheet_names
                #column
                for col in range(sheet.ncols):
                    val = sheet.cell(row,col).value
                    if col == 0:
                        item["index"] = val
                    if col == 1:
                        item['name'] = val
                    if col == 2:
                        item['score'] = val
                    if col == 3:
                        item['score_count'] = val
                    if col == 4:
                        item['author'] = val.split("：")[1]
                    if col == 5:
                        if len(val.split("：")[1].split("/")) < 3:
                            print("len < 3")
                            print(val)
                            continue
                        else:
                            publisher,year,price = val.split("：")[1].split("/")
                            item['publisher'] = publisher
                            item['year'] = year
                            item['price'] = price
                    book_list.append(item)

    with open('../db/douban.db','wt',encoding='utf8') as f:
        json.dump(book_list,f)



def process():
    #获取原始文件列表
    file_list = get_filelist()
    #生成db数据
    get_data(file_list)
    #

if __name__ == "__main__":
    process()


