def parse_duration(s):
    """legacy: '2h30m', '90s', '1d2h', integers=seconds. Quirks preserved."""
    s=s.strip()
    if not s: return 0
    if s.isdigit(): return int(s)
    units={'d':86400,'h':3600,'m':60,'s':1}
    total=0; num=''
    for ch in s:
        if ch.isdigit(): num+=ch
        elif ch in units and num:
            total+=int(num)*units[ch]; num=''
        else: return -1   # quirk: invalid => -1, not exception
    if num: total+=int(num)  # quirk: trailing bare number = seconds
    return total
