from pathlib import PurePosixPath, PureWindowsPath

import pytest

from datamodel_code_generator.reference import camel_to_snake, get_relative_path


@pytest.mark.parametrize(
    'base_path,target_path,expected',
    [
        ('/a/b', '/a/b', '.'),
        ('/a/b', '/a/b/c', 'c'),
        ('/a/b', '/a/b/c/d', 'c/d'),
        ('/a/b/c', '/a/b', '..'),
        ('/a/b/c/d', '/a/b', '../..'),
        ('/a/b/c/d', '/a', '../../..'),
        ('/a/b/c/d', '/a/x/y/z', '../../../x/y/z'),
        ('/a/b/c/d', 'a/x/y/z', 'a/x/y/z'),
        ('/a/b/c/d', '/a/b/e/d', '../../e/d'),
    ],
)
def test_get_relative_path_posix(
    base_path: str, target_path: str, expected: str
) -> None:
    assert PurePosixPath(
        get_relative_path(PurePosixPath(base_path), PurePosixPath(target_path))
    ) == PurePosixPath(expected)


@pytest.mark.parametrize(
    'base_path,target_path,expected',
    [
        ('c:/a/b', 'c:/a/b', '.'),
        ('c:/a/b', 'c:/a/b/c', 'c'),
        ('c:/a/b', 'c:/a/b/c/d', 'c/d'),
        ('c:/a/b/c', 'c:/a/b', '..'),
        ('c:/a/b/c/d', 'c:/a/b', '../..'),
        ('c:/a/b/c/d', 'c:/a', '../../..'),
        ('c:/a/b/c/d', 'c:/a/x/y/z', '../../../x/y/z'),
        ('c:/a/b/c/d', 'a/x/y/z', 'a/x/y/z'),
        ('c:/a/b/c/d', 'c:/a/b/e/d', '../../e/d'),
    ],
)
def test_get_relative_path_windows(
    base_path: str, target_path: str, expected: str
) -> None:
    assert PureWindowsPath(
        get_relative_path(PureWindowsPath(base_path), PureWindowsPath(target_path))
    ) == PureWindowsPath(expected)


@pytest.mark.parametrize(
    'camel_case,disallow_single_symbols,snake_case',
    [
        ('IP', True, 'ip'),
        ('someCamelCased', True, 'some_camel_cased'),
        ('podIPs', True, 'pod_ips'),
        ('IP', False, 'ip'),
        ('someCamelCased', False, 'some_camel_cased'),
        ('podIPs', False, 'pod_i_ps'),
    ],
)
def test_camel_to_snake(camel_case, disallow_single_symbols, snake_case) -> None:
    assert (
        camel_to_snake(camel_case, disallow_single_symbols=disallow_single_symbols)
        == snake_case
    )
