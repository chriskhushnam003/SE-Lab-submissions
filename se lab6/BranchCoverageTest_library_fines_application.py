import pytest
from library_fines import late_fine, can_borrow, renewal_status

# ---------- Starter tests ----------
def test_returned_on_time():
    assert late_fine("student", 10, False) == 0

def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

# ---------- late_fine: every decision True and False ----------
def test_unknown_member_raises():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 5, False)

def test_negative_days_raises():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)

def test_zero_days_is_valid():
    assert late_fine("guest", 0, False) == 0

def test_faculty_within_loan_period():
    assert late_fine("faculty", 30, False) == 0          # boundary: overdue == 0

def test_faculty_overdue_fine():
    assert late_fine("faculty", 40, False) == 10

def test_student_exactly_at_loan_limit():
    assert late_fine("student", 14, False) == 0          # boundary: overdue == 0

def test_student_one_day_overdue():
    assert late_fine("student", 15, False) == 2          # boundary: overdue == 1

def test_guest_overdue_fine():
    assert late_fine("guest", 20, False) == 30           # 6 * 5

def test_fine_exactly_200_not_capped_further():
    assert late_fine("student", 114, False) == 200       # 100*2 = 200, not > 200

def test_fine_above_200_is_capped():
    assert late_fine("student", 115, False) == 200       # 202 -> 200

def test_damaged_only_adds_150():
    assert late_fine("student", 5, True) == 150

def test_damaged_and_overdue():
    assert late_fine("student", 20, True) == 162

def test_damaged_and_capped():
    assert late_fine("guest", 100, True) == 350          # 200 cap + 150

# ---------- can_borrow ----------
def test_cannot_borrow_with_high_pending_fine():
    assert can_borrow(0, 101, "student") is False

def test_can_borrow_with_fine_exactly_100():
    assert can_borrow(0, 100, "student") is True

def test_faculty_below_limit():
    assert can_borrow(9, 0, "faculty") is True

def test_faculty_at_limit():
    assert can_borrow(10, 0, "faculty") is False

def test_student_below_limit():
    assert can_borrow(2, 0, "student") is True

def test_student_at_limit():
    assert can_borrow(3, 0, "student") is False

def test_guest_uses_default_limit():
    assert can_borrow(3, 0, "guest") is False

# ---------- renewal_status ----------
def test_renewal_denied_with_reservation():
    assert renewal_status(0, True, 5) == "denied"

def test_reservation_overrides_limit():
    assert renewal_status(5, True, -3) == "denied"

def test_renewal_limit_reached_at_two():
    assert renewal_status(2, False, 5) == "limit reached"

def test_renewal_limit_exceeded():
    assert renewal_status(3, False, 5) == "limit reached"

def test_renewal_overdue():
    assert renewal_status(1, False, -1) == "overdue"

def test_renewal_zero_days_left_ok():
    assert renewal_status(0, False, 0) == "renewed"

def test_renewal_success():
    assert renewal_status(1, False, 5) == "renewed"
