import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def make_one():
    from work.models import DataSet
    def _make_one(*args, **kwargs):
        d = DataSet(*args, **kwargs)
        return d
    return _make_one


def test_setup(make_one):
    d = make_one(name="Test Dataset")
    assert d
    d.full_clean()


def test_name(make_one):
    name = "Test Dataset"
    d = make_one(name=name)
    assert str(d) == name


def test_auto_slugification_long(make_one):
    """The slug should be shrunk to 75 characters"""
    name = "a"*76
    expected = "a"*75
    d = make_one(name=name)
    d.full_clean()
    assert d.slug == expected


def test_auto_slugification_sticks(make_one):
    """A slug, once generated automatically, shouldn't change."""
    name = "Test Dataset"
    d = make_one(name=name)
    d.full_clean()
    assert d.slug == "test-dataset"

    d.name = "Another Dataset"
    d.full_clean()
    assert d.slug == "test-dataset"


def test_manual_slugs(make_one):
    """A slug provided should be kept."""
    name = "Test Dataset"
    slug = "remember-the-cant"
    d = make_one(name=name, slug=slug)
    d.full_clean()
    assert d.slug == slug
