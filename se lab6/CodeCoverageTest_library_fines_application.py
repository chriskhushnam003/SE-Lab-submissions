import pytest
from library_fines import late_fine, can_borrow, renewal_status

# ---------- Starter tests ----------
def test_returned_on_time():
    assert late_fine("student", 10, False) == 0

def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

# ---------- late_fine: line coverage ----------
def test_unknown_member_raises():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 5, False)

def test_negative_days_raises():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)

def test_faculty_overdue_fine():
    # faculty loan = 30 days, 40 kept -> 10 overdue * 1
    assert late_fine("faculty", 40, False) == 10

def test_student_overdue_and_damaged():
    # student loan = 14 days, 20 kept -> 6 * 2 = 12, + 150 damage
    assert late_fine("student", 20, True) == 162

def test_fine_is_capped_at_200():
    # 115 days -> 101 overdue * 2 = 202 -> capped to 200
    assert late_fine("student", 115, False) == 200

# ---------- can_borrow: line coverage ----------
def test_cannot_borrow_with_high_pending_fine():
    assert can_borrow(0, 101, "student") is False

def test_faculty_can_borrow_below_limit():
    assert can_borrow(5, 0, "faculty") is True

# ---------- renewal_status: line coverage ----------
def test_renewal_denied_with_reservation():
    assert renewal_status(0, True, 5) == "denied"

def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"

def test_renewal_overdue():
    assert renewal_status(0, False, -1) == "overdue"

def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"
