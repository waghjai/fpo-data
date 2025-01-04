import json
import pdfplumber

fpo_list = {"data": []}

def process_string(value):
    return value.replace('\n', ' ') if value else 'null'

with pdfplumber.open("data/statewise-fpo-list.pdf") as pdf:
    total_pages = len(pdf.pages)
    total_rows = 0
    
    for page_number, page in enumerate(pdf.pages, start=1):
        print(f'\rProcessing page {page_number}/{total_pages}', end='', flush=True)

        table = page.extract_table()

        if not table:
            continue

        for row in table[1:]:
            try:
                serial_number = int(row[0])

                total_rows += 1

                fpo_data = {
                    'serialNumber': serial_number,
                    'state': process_string(row[1]),
                    'district': process_string(row[2]),
                    'block': process_string(row[3]),
                    'cbbo': process_string(row[4]),
                    'name': process_string(row[5]),
                    'registrationNumber': process_string(row[6]),
                    'registrationAct': process_string(row[7]),
                    'dateOfIncorporation': process_string(row[8]),
                    'officeAddress': process_string(row[9])
                }

                fpo_list['data'].append(fpo_data)

            except (IndexError, ValueError) as e:
                continue

    with open('data/statewise-fpo-list.json', 'w', encoding='utf-8') as json_file:
        json.dump(fpo_list, json_file, ensure_ascii=False, indent=4)

    print(f'\nExtracted {total_rows} rows from {total_pages} pages')
