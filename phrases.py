"""Regex that can extract a location from a query."""
QUERY_PHRASES = (
    r'^[W,w]hat\'?s the weather(?P<time> tomorrow)? in (?P<location>.+)',
    r'[W,w]eather (?P<time>tomorrow)? in (?P<location>.+)',
    r'(?P<location>.+) weather (?P<time>tomorrow)?',
)
