import sys
import xlrd

def parse(filename):
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)

    product = None
    for idx in range(2, worksheet.nrows):
        regno = worksheet.cell_value(idx, 2)
        if regno.strip() != "":
            if product: yield product

            product = {
                "regno" : worksheet.cell_value(idx, 2).lower(),
                "applicant" : worksheet.cell_value(idx, 1).title(),
                "schedule" : worksheet.cell_value(idx, 5),
                "name" : worksheet.cell_value(idx, 6).title(),
                "dosage form" : worksheet.cell_value(idx, 10).title(),
                "pack size" : worksheet.cell_value(idx, 11) or None,
                "quantity" : worksheet.cell_value(idx, 12) or None,
                "sep" : worksheet.cell_value(idx, 16) or None,
                "generic" : worksheet.cell_value(idx, 19) or None,
                "ingredients" : []
            }

        product["ingredients"].append({
            "ingredient" : worksheet.cell_value(idx, 7).title(),
            "strength" : worksheet.cell_value(idx, 8),
            "unit" : worksheet.cell_value(idx, 9).lower(),
        })

if __name__ == "__main__":
    for p in parse(sys.argv[1]):
        print p
