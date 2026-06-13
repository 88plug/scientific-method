import sys
# minimal extract of the two modules' interaction
def apply_discount(price_str, pct, locale):
    # discount module: parses locale-formatted price, applies pct, RE-FORMATS with locale rules
    sep = ',' if locale in ('de_DE','fr_FR') else '.'
    v = float(price_str.replace(sep,'.'))
    v = v * (1 - pct/100.0)
    s = f"{v:.3f}"          # keeps 3 decimals internally
    return s.replace('.', sep)
def total_engine(line_strs, locale):
    # totals engine: parses each line, TRUNCATES to cents per line (assumes 2-decimal input), sums
    sep = ',' if locale in ('de_DE','fr_FR') else '.'
    total = 0
    for s in line_strs:
        v = float(s.replace(sep,'.'))
        cents = int(v * 100)      # truncation — correct IF input has 2 decimals
        total += cents
    return total / 100.0
if __name__=='__main__':
    locale, pct, n = 'de_DE', 10.0, 3
    lines = [apply_discount('7,40', pct, locale) for _ in range(n)]
    print('discounted line strings:', lines)
    print('engine total:', total_engine(lines, locale), '(expected:', round(7.40*0.9*n,2), ')')
