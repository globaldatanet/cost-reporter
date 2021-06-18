import datetime

from freezegun import freeze_time

import stacked_bar


@freeze_time('2020-12-23')
def test_generate_dates1(monkeypatch):
    """
    Given: A number of days = 5 and today being the FAKE_DATE
    When: The function is called
    Then: The function returns the last 5 days in reverse order
    """
    monkeypatch.setenv("DAYS", "5")

    assert stacked_bar.generate_dates() == ["19", "20", "21", "22", "23"]
