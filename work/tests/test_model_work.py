import datetime
import pytest

from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


@pytest.fixture()
def make_one():
    from work.models import WorkItem, DataSet

    def _make_one(key, dataset="test_dataset", queued_at=None):
        if queued_at is None:
            queued_at = datetime.datetime.now() - datetime.timedelta(days=30)
        d = DataSet(name=dataset, slug=dataset)
        d.save()
        w = WorkItem(
            key=key,
            dataset=d,
            queued_at=queued_at
        )
        return w
    return _make_one


def test_setup(make_one):
    w = make_one("TEST-1")
    w.full_clean()


def test_str(make_one):
    w = make_one("TEST-1")
    expected = "test_dataset / TEST-1"
    assert expected == str(w)


def test_dates_must_be_in_order_happy(make_one):
    """Queued >= started >= ended"""
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.started_at = datetime.datetime.now() - datetime.timedelta(days=4)
    w.ended_at = datetime.datetime.now()

    w.check_dates()


def test_dates_must_be_in_order_started(make_one):
    """Queued >= started >= ended"""
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.started_at = datetime.datetime.now() - datetime.timedelta(days=20)

    with pytest.raises(ValidationError):
        w.check_dates()


def test_dates_must_be_in_order_ended(make_one):
    """Queued >= started >= ended"""
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.ended_at = datetime.datetime.now() - datetime.timedelta(days=20)

    with pytest.raises(ValidationError):
        w.check_dates()


def test_dates_must_be_in_order_ended_before_started(make_one):
    """Queued >= started >= ended"""
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.started_at = datetime.datetime.now() - datetime.timedelta(days=10)
    w.ended_at = datetime.datetime.now() - datetime.timedelta(days=11)

    with pytest.raises(ValidationError):
        w.check_dates()


def test_cycle_time(make_one):
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.started_at = datetime.datetime.now() - datetime.timedelta(days=4)
    w.ended_at = datetime.datetime.now()

    assert w.cycle_time.days == 4


def test_cycle_time_in_progress(make_one):
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.started_at = datetime.datetime.now() - datetime.timedelta(days=4)

    with pytest.raises(ValueError):
        w.cycle_time.days

def test_lead_time(make_one):
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.started_at = datetime.datetime.now() - datetime.timedelta(days=4)
    w.ended_at = datetime.datetime.now()

    assert w.lead_time.days == 14


def test_lead_time_in_progress(make_one):
    w = make_one("TEST-1")
    w.queued_at = datetime.datetime.now() - datetime.timedelta(days=14)
    w.started_at = datetime.datetime.now() - datetime.timedelta(days=4)

    with pytest.raises(ValueError):
        w.lead_time.days
