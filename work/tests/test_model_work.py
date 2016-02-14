import datetime
import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture()
def make_one():
    from work.models import WorkItem, DataSet

    def _make_one(key, dataset="test_dataset", queued_at=None):
        if queued_at is None:
            queued_at = datetime.datetime.now()
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
