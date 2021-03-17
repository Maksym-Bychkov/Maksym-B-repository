from flask import Flask, render_template, url_for, request, redirect
import re


app = Flask(__name__)


def parser(filename):

    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.rstrip('\n').strip() for line in file]

    id = 1
    table_list = []
    transaction_dict = {}
    marker = False
    cassette_count = ('Cassette_1_count', 'Cassette_2_count', 'Cassette_3_count', 'Cassette_4_count',)

    for line in lines:
        if marker:
            match = re.search(r'\d{6}X{6}\d{4}', line)
            if match:
                transaction_dict['PAN'] = match[0]
                transaction_dict['ID'] = id
            match = re.search(r'\d\d:\d\d:\d\d CASH WITHDRAWAL\D+\d+,*\d+\.\d{2}', line)
            if match:
                transaction_dict['Amount'] = re.search(r'\d+,*\d+\.\d{2}', match[0])[0]
                transaction_dict['Time'] = re.search(r'\d\d:\d\d:\d\d', match[0])[0]
            match = re.search(r'AUTH\. CODE: +\d{6}', line)
            if match:
                transaction_dict['Auth_code'] = re.search(r'\d{6}', match[0])[0]
            match = re.search(r'\d+ - +\d+ - +\d+ - +\d+', line)
            if match:
                cassette_count_list = match[0].split('-')
                for i in range(4):
                    transaction_dict[cassette_count[i]] = cassette_count_list[i].strip()

        if re.search('CASH TAKEN', line):
            marker = True
            transaction_dict = {}
        if re.search('TRANSACTION END', line) and marker:
            marker = False
            if transaction_dict:
                table_list.append(transaction_dict)
                id = id + 1
                transaction_dict = {}
    # print(table_list)
    # print(len(table_list))
    return table_list


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        content = parser('4508 8464-20161125-065747-231211-TOP.ENC[2].txt')
        return render_template('index.html', content=content)
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

