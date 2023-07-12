import datetime


def get_args(record: str) -> list[str] | None:
    args = record.split()
    return args if len(args) == 3 else None


def is_date_valid(date_string: str) -> bool:
    try:
        birthday_date = str_to_date(date_string)
        current_date = datetime.datetime.today()
        if birthday_date > current_date:
            raise ValueError
        return True
    except ValueError:
        return False


def is_record_valid(record: str) -> bool:
    args = get_args(record)
    if not args:
        return False
    return is_date_valid(args[-1])


def str_to_date(date_string) -> datetime:
    date_format = "%d-%m-%Y"
    return datetime.datetime.strptime(date_string, date_format)
