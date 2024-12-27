from main import dir_sort_key, direction_to_delta

def test_dir_sort_key_up():
    # For upward movement (^), should sort by:
    # - Primary: highest row first (negative row * -1)
    # - Secondary: leftmost column first
    positions = [(2, 1), (1, 2), (2, 2), (1, 1)]
    sort_key = dir_sort_key("^")
    sorted_positions = sorted(positions, key=sort_key)
    assert sorted_positions == [(1, 1), (1, 2), (2, 1), (2, 2)]

def test_dir_sort_key_down():
    # For downward movement (v), should sort by:
    # - Primary: lowest row first (negative row * 1)
    # - Secondary: leftmost column first
    positions = [(1, 2), (2, 1), (1, 1), (2, 2)]
    sort_key = dir_sort_key("v")
    sorted_positions = sorted(positions, key=sort_key)
    assert sorted_positions == [(2, 1), (2, 2), (1, 1), (1, 2)]

def test_dir_sort_key_left():
    # For leftward movement (<), should sort by:
    # - Primary: rightmost column first (negative col * -1)
    # - Secondary: topmost row first
    positions = [(2, 1), (1, 2), (2, 2), (1, 1)]
    sort_key = dir_sort_key("<")
    sorted_positions = sorted(positions, key=sort_key)
    assert sorted_positions == [(1, 1), (2, 1), (1, 2), (2, 2), ]

def test_dir_sort_key_right():
    # For rightward movement (>), should sort by:
    # - Primary: leftmost column first (negative col * 1)
    # - Secondary: topmost row first
    positions = [(2, 2), (1, 1), (2, 1), (1, 2)]
    sort_key = dir_sort_key(">")
    sorted_positions = sorted(positions, key=sort_key)
    assert sorted_positions == [(1, 2), (2, 2), (1, 1), (2, 1)]

def test_dir_sort_key_empty_list():
    # Should handle empty lists without error
    positions = []
    sort_key = dir_sort_key(">")
    sorted_positions = sorted(positions, key=sort_key)
    assert sorted_positions == []

def test_dir_sort_key_single_position():
    # Should handle single-element lists
    positions = [(1, 1)]
    sort_key = dir_sort_key("^")
    sorted_positions = sorted(positions, key=sort_key)
    assert sorted_positions == [(1, 1)]
