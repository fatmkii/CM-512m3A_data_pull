
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
from prettytable import PLAIN_COLUMNS
from prettytable import RANDOM
from prettytable import DEFAULT
import csv

table = PrettyTable(['L25', 'L45', 'L75', 'a25', 'a45', 'a75', 'b25', 'b45', 'b75'])
table.add_row([1, 2, 3, 4, 5, 6, 7, 8, 9])
table.vertical_char  = ","
table.set_style(PLAIN_COLUMNS)
print(table)

with open('./2.csv','wt') as fout:
    csvout = csv.writer(fout)
    csvout.writerows(table)