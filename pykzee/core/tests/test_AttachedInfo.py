import unittest

from pyimmutable import ImmutableDict, ImmutableList

from pykzee.core import AttachedInfo
from pykzee.core.common import sanitize

# Instantiante an empty ImmutableDict, since pykzee modules may or may not do
# that anyway. This way we know what instance counts to expect in the tests
# below.
empty_immutable_dict = ImmutableDict()


class TestResolved(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(immutables_count(), 1)
        data = sanitize(
            {
                "foo": "bar",
                "x1": [0, 1, 2, {"__symlink__": "x2"}, 4],
                "x2": {
                    "y1": 123,
                    "y2": {"__symlink__": "foo"},
                    "y3": {"__symlink__": "/x1/[3]/y1"},
                    "y4": {"__symlink__": ["x2", "y2"]},
                },
            }
        )
        data_resolved = sanitize(
            {
                "foo": "bar",
                "x1": [
                    0,
                    1,
                    2,
                    {"y1": 123, "y2": "bar", "y3": 123, "y4": "bar"},
                    4,
                ],
                "x2": {"y1": 123, "y2": "bar", "y3": 123, "y4": "bar"},
            }
        )
        self.assertEqual(immutables_count(), 12)
        resolved = AttachedInfo.resolved(data)
        self.assertTrue(resolved is data_resolved)
        self.assertEqual(immutables_count(), 25)
        data_resolved = resolved = None
        self.assertEqual(immutables_count(), 25)
        data = None
        self.assertEqual(immutables_count(), 1)


def immutables_count():
    return (
        ImmutableDict._get_instance_count()
        + ImmutableList._get_instance_count()
    )


if __name__ == "__main__":
    unittest.main()
