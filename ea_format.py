from openpyxl import load_workbook
import attr


@attr.s
class Record(object):
    ref_no = attr.ib()
    cpd_type = attr.ib()
    start_date = attr.ib()
    end_date = attr.ib()
    activity = attr.ib()
    topic = attr.ib()
    provider= attr.ib()
    division= attr.ib()
    location = attr.ib()
    total_hrs = attr.ib()
    risk_hrs = attr.ib()
    bus_hrs = attr.ib()
    area_hrs = attr.ib()
    notes = attr.ib()
    learning_outcome = attr.ib()


def read_workbook(filename: str):

    wb =  load_workbook(filename)
    sheet = wb['CPD Records']
    
    data = []
    for i in range(1, sheet.max_row+1):
        row = []
        for j in range(1,sheet.max_column+1):
            cell = sheet.cell(row=i,column=j).value
            row.append(cell)
        data.append(row)

    return data

def parse_ea_records(filename):

    data = read_workbook(filename)
    data.pop(0) # Remove first row
    data.pop(0) # Remove headings row
 
    new_rows = list()
    for row in data[0::2]:
        new_rows.append(row)

    for i, row in enumerate(data[1::2]):
        cell = row[3]
        new_rows[i].append(cell)


    records = list()

    for row in new_rows:
        print(row)
        records.append(Record(*row))
    return records
        


if __name__ == '__main__':
    records = parse_ea_records(filename='example.xlsx')
    for record in records:
        print(record)
