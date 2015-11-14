from django.http import HttpResponse
import os
import xlwt


def exportDataAsExcelFile(filename, sheets):
    """
    Write an excel file with the data.
    """
    file = "{}.xls".format(filename)
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % file

    book = xlwt.Workbook(encoding="UTF-8")
    for s in sheets:
        sht = book.add_sheet(s['name'])
        header = s['header']
        data = s['data']
        if isinstance(header, dict):
            header = [(k, v) for k, v in sorted(header.iteritems())]

        if header and data:
            col = 0
            for h in header:
                row = 0
                if h[1]:
                    sht.write(row, col, h[1])
                if h[0]:
                    for key in data:
                        row += 1
                        sht.write(row, col, u"{}" .format(key.get(h[0], '')))
                col += 1

    book.save(response)
    return response