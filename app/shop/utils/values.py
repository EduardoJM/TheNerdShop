import babel.numbers
import decimal

def brl(value):
    val_aux = str(value)
    return babel.numbers.format_currency(decimal.Decimal(val_aux), "BRL" )
