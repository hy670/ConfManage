import sys
import difflib

def read_file(filename):
    try:
        with open(filename, 'r',encoding='UTF-8') as f:
            return f.readlines()
    except IOError:
        print("ERROR: 没有找到文件:%s或读取文件失败！" % filename)
        sys.exit(1)

def compare_file(file1, file2, out_file):
    file1_content = read_file(file1)
    file2_content = read_file(file2)
    d = difflib.HtmlDiff()
    result = d.make_file(file1_content, file2_content)
    with open(out_file, 'w',encoding='UTF-8') as f:
        f.writelines(result)

if __name__ == '__main__':
    compare_file('F1030.conf', 'F10301.conf', 'result.html')
