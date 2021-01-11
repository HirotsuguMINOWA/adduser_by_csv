#!/usr/bin/env python3
MAX_PW = 12
d = {
    "email": "メールアドレス",
    "uid": "学籍番号 ※RemoteServerのIDになるので間違えないように。",
    "name": "ユーザフルネーム"
}
import csv
import subprocess
import crypt
import sys
from pathlib import Path
import string
import secrets


def pass_gen(size=12):
    """パスワード生成
    https://gammasoft.jp/blog/generate-password-by-python/
    """
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # 記号を含める場合
    # chars += '%&$#()'

    return ''.join(secrets.choice(chars) for x in range(size))


def input_name(name):
    while True:
        uid = input(f"{name}のUIDを決めて下さい。学生番号が無いため。")
        print("UIDは次:", uid)
        ans = input("決定(y/N)")
        if ans.lower() in ("y", "yes"):
            return uid


def parse_row(a_row: csv.DictReader):
    password = pass_gen(MAX_PW)
    encpt_passwd = crypt.crypt(password, '2b')
    if a_row[d["uid"]] != "":
        uid = a_row[d["uid"]]
    else:
        uid = input_name(a_row[d["name"]])
    # useraddコマンドの実行
    # -m : ホームディレクトリ作成
    command = f'useradd -s /bin/bash -m -p {encpt_passwd} -u {uid} -c'.split()
    command.append(a_row[d["name"]])
    subprocess.call(command)


def parse_reader(reader: csv.DictReader):
    for i, a_row in enumerate(reader):
        parse_row(a_row)


print("sys.argv:", sys.argv)

if len(sys.argv) == 1:
    """ pyコードのみ"""
    print("将来GUI(Toga)起動。今は何も動作しない")
elif len(sys.argv) == 2:
    p_path = Path(sys.argv[1])
    if p_path.exists() and p_path.suffix == ".csv":
        with open(p_path, encoding='utf-8-sig') as f:  # 'utf-8-sig'でなければ`\ufeff`が残る。
            reader = csv.DictReader(f)
            parse_reader(reader)
            # data = [row for row in reader]
        # with open(p_path) as f:
        #     for line in f:
        #         i = line.find(',')
        #         name = line[:i]
        #         password = line.rstrip()[i + 1:]
        #         encpt_passwd = crypt.crypt(password, '2b')
        #         command = 'useradd -m -p {0} {1}'.format(encpt_passwd, name).split()
        #         subprocess.call(command)
else:
    print("CLI/GUI起動条件とは異なります")

# # テキトーに表示してるだけです
# print(data[0]['title'])
# print(data[0]['version'])
# print(data[2]['price'])
# print(data[3]['stock'])
