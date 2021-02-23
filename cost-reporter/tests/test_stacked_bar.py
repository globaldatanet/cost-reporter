import datetime
import pytest
import stacked_bar

FAKE_DATE = datetime.datetime(2020, 12, 25, 17, 5, 55)


@pytest.fixture
def patch_datetime_today(monkeypatch):
    class MyDateTime:
        @classmethod
        def today(cls):
            return FAKE_DATE

    monkeypatch.setattr(datetime, 'datetime', MyDateTime)


def test_patch_datetime(patch_datetime_today):
    """ Make sure the fixture works
    """
    assert datetime.datetime.today() == FAKE_DATE


def test_generate_dates1(monkeypatch, patch_datetime_today):
    """
    Given: A number of days = 5 and today being the FAKE_DATE
    When: The function is called
    Then: The function returns the last 5 days in reverse order
    """
    monkeypatch.setenv("DAYS", "5")

    assert stacked_bar.generate_dates() == ["19", "20", "21", "22", "23"]
