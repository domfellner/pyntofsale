from tools.add_ean_to_csv import append_checkdigit, create_ean_13


def test_ean_13_checksum():
    validated_eans = [
        "1234567890180",
        "1234567890401",
        "1234567890142",
        "1234567890173",
        "1234567890104",
        "1234567890135",
        "1234567890166",
        "1234567890197",
        "1234567890128",
        "1234567890159",
    ]
    eans_under_test = [append_checkdigit(ean[:-1]) for ean in validated_eans]
    assert validated_eans == eans_under_test


def test_ean_8_checksum():
    validated_eans = [
        "12267170"
        "12345472"
        "12345373"
        "12345274"
        "12345175"
        "12345076"
        "12345977"
        "12345878"
        "12345779"
    ]
    eans_under_test = [append_checkdigit(ean[:-1]) for ean in validated_eans]
    assert validated_eans == eans_under_test


def test_ean_leading_zero():
    validated_eans = ["01234565", "00000017", "0123456789128", "0000000000017"]
    eans_under_test = [append_checkdigit(ean[:-1]) for ean in validated_eans]
    assert validated_eans == eans_under_test


def test_ean_13_valid_length():
    seeds = [i for i in range(1000)]
    eans = [create_ean_13(s) for s in seeds]
    is_13_digits = [len(ean) == 13 for ean in eans]
    assert all(is_13_digits)


def test_ean_13_no_duplicates():
    seeds = [i for i in range(1000)]
    eans = [create_ean_13(s) for s in seeds]
    assert len(eans) == len(set(eans))
