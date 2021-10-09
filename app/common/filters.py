def format_datetime(value, format='short'):
    value_str = None
    if not value:
        value_str = ''
    if format == 'short':
        value_str = value.strftime('%d de %b de %Y')
    elif format == 'full':
        value_str = value.strftime('%d de %b de %Y - %H:%M')
    else:
        value_str = ''
    return value_str

