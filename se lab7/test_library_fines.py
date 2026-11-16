from hypothesis import given, strategies as st
from library_fines import parse_member_id, total_fine, shelf_code

anything = st.one_of(st.none(), st.booleans(), st.integers(), st.floats(),
                     st.text(), st.binary(), st.lists(st.integers()))


# ---------------- parse_member_id ----------------
@given(st.text() | st.none())
def test_parse_member_id_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed with: {e!r}"


@given(anything)
def test_parse_member_id_result_shape(s):
    r = parse_member_id(s)
    assert r is None or (isinstance(r[0], str) and isinstance(r[1], int) and r[1] >= 0)


@given(st.text(alphabet="abcXYZ", min_size=1), st.integers(min_value=0, max_value=10**9))
def test_parse_member_id_valid_roundtrip(t, n):
    assert parse_member_id(f"{t}-{n}") == (t.upper(), n)


# ---------------- total_fine ----------------
@given(st.text() | st.none())
def test_total_fine_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed with: {e!r}"


@given(anything)
def test_total_fine_non_negative_int(s):
    f = total_fine(s)
    assert isinstance(f, int) and f >= 0


@given(st.lists(st.integers(min_value=0, max_value=10000), max_size=20))
def test_total_fine_matches_formula(days):
    expected = sum((d - 14) * 2 for d in days if d > 14)
    assert total_fine(",".join(map(str, days))) == expected


# ---------------- shelf_code ----------------
@given(st.text() | st.none())
def test_shelf_code_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed with: {e!r}"


@given(anything)
def test_shelf_code_returns_str(s):
    assert isinstance(shelf_code(s), str)


@given(st.text(alphabet="abcdefg", min_size=1), st.text(alphabet="hijklmn", min_size=1))
def test_shelf_code_two_words(a, b):
    assert shelf_code(f"{a} {b}") == (a[0] + b[0]).upper()
