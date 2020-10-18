import lambda_function

TEST_DATA = {
    "lambda": [1, 2, 3, 4, 5, 6],
    "ecs": [1, 2, 3, 1, 2, 1],
    "cloudwatch": [0, 0, 0, 0, 0, 0]
}


def test_notify1(monkeypatch):
    """
    Given: Cost increased
    When: ONLY_NOTIFY_ON_INCREASE is True and MIN_DAILY_COST is breached
    Then: Notify
    """
    monkeypatch.setenv("ONLY_NOTIFY_ON_INCREASE", "True")
    monkeypatch.setenv("MIN_DAILY_COST", "0")

    for service in TEST_DATA.keys():
        TEST_DATA[service][-2] = 0
        TEST_DATA[service][-1] = 10

    assert lambda_function.trigger_notification(TEST_DATA)


def test_notify2(monkeypatch):
    """
    Given: Cost decreased
    When: ONLY_NOTIFY_ON_INCREASE is True and MIN_DAILY_COST is breached
    Then: Dont Notify
    """
    monkeypatch.setenv("ONLY_NOTIFY_ON_INCREASE", "True")
    monkeypatch.setenv("MIN_DAILY_COST", "0")

    for service in TEST_DATA.keys():
        TEST_DATA[service][-2] = 10
        TEST_DATA[service][-1] = 0

    assert not lambda_function.trigger_notification(TEST_DATA)
