"""Regex that can extract a location from a query."""
QUERY_PHRASES = (
    r'^[W,w]hat\'?s the weather in (.+)',
    r'[W,w]eather in (.+)',
    r'(.+) weather',
)
