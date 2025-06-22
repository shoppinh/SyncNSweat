def safe_int_convert(value, default=0):
    try:
        return int(float(value)) if '.' in str(value) else int(value)
    except (ValueError, TypeError):
        return default