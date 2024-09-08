from typing import TYPE_CHECKING
from typing import Any
from unittest import TestCase

from liberliber_rss_feed.cron import Cron

if TYPE_CHECKING:
    from collections.abc import Mapping


class StepError(BaseException):  # bypass except Exception
    ...


class Action:
    max: int
    invocations: 'list[tuple[tuple[Any, ...], Mapping[str, Any]]]'

    def __init__(self, max_: int) -> None:
        self.max = max_
        self.invocations = []

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        if len(self.invocations) >= self.max:
            raise StepError
        self.invocations.append((args, kwargs))


class TestCron(TestCase):
    def test_run_forever(self) -> None:
        action = Action(3)
        args = ('foo', 'bar')
        kwargs = {'key': 'value'}
        with self.assertRaises(StepError):
            Cron(action, args, kwargs).run_forever(
                replace_kwargs={},  # schedule following steps to "now"
                timedelta_kwargs={'milliseconds': 100.0},
            )
        self.assertEqual(
            action.invocations, [(args, kwargs), (args, kwargs), (args, kwargs)]
        )
