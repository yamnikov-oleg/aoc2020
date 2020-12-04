import re
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Passport:
    fields: Dict[str, str] = field(default_factory=OrderedDict)


def parse_passport_field(s: str) -> Tuple[str, str]:
    values = s.strip().split(':')
    if len(values) != 2:
        raise ValueError(f"Invalid passport field: {s:!r}")

    return values[0], values[1]


def parse_passport(s: str) -> Passport:
    field_strs = re.split(r"[ \n]", s)
    field_strs = [s.strip() for s in field_strs]
    field_strs = [s for s in field_strs if s]

    passport = Passport()
    for field_str in field_strs:
        key, value = parse_passport_field(field_str)
        passport.fields[key] = value

    return passport


def parse_passports_file(content: str) -> List[Passport]:
    passport_strs = content.split('\n\n')
    passports = [parse_passport(s) for s in passport_strs]
    return passports


def passport_has_required_fields(passport: Passport) -> bool:
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for key in required_fields:
        if key not in passport.fields.keys():
            return False

    return True


def is_valid_birth_year(byr: str) -> bool:
    try:
        byr_int = int(byr)
    except (ValueError, TypeError):
        return False

    return 1920 <= byr_int <= 2002


def is_valid_issue_year(iyr: str) -> bool:
    try:
        iyr_int = int(iyr)
    except (ValueError, TypeError):
        return False

    return 2010 <= iyr_int <= 2020


def is_valid_expiration_year(eyr: str) -> bool:
    try:
        eyr_int = int(eyr)
    except (ValueError, TypeError):
        return False

    return 2020 <= eyr_int <= 2030


def is_valid_height(hgt: str) -> bool:
    match = re.match(r"^(\d+)(cm|in)$", hgt)
    if not match:
        return False

    hgt_value = int(match.group(1))
    hgt_unit = match.group(2)

    if hgt_unit == 'cm':
        return 150 <= hgt_value <= 193
    elif hgt_unit == 'in':
        return 59 <= hgt_value <= 76
    else:
        raise ValueError(f"Invalid height unit: {hgt_unit}")


def is_valid_hair_color(hcl: str) -> bool:
    match = re.match(r"^#[0-9a-f]{6}$", hcl)
    return match is not None


def is_valid_eye_color(ecl: str) -> bool:
    return ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def is_valid_passport_id(pid: str) -> bool:
    match = re.match(r"^\d{9}$", pid)
    return match is not None


def passport_is_valid(passport: Passport) -> bool:
    validators = {
        'byr': is_valid_birth_year,
        'iyr': is_valid_issue_year,
        'eyr': is_valid_expiration_year,
        'hgt': is_valid_height,
        'hcl': is_valid_hair_color,
        'ecl': is_valid_eye_color,
        'pid': is_valid_passport_id,
    }

    for key, validate in validators.items():
        if key not in passport.fields.keys():
            return False

        value = passport.fields[key]
        if not validate(value):
            return False

    return True


def main():
    with open('./input.txt') as f:
        passports = parse_passports_file(f.read())

    count_no_missing_fields = 0
    count_valid = 0
    for p in passports:
        if passport_has_required_fields(p):
            count_no_missing_fields += 1

        if passport_is_valid(p):
            count_valid += 1

    print(f"Passports without missing fields: {count_no_missing_fields}")
    print(f"Passports with valid data: {count_valid}")


if __name__ == "__main__":
    main()
