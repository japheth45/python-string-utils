from unittest import TestCase

from string_utils import slugify


class SlugifyTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            slugify(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            slugify(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            slugify(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            slugify([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            slugify({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_slugify_lowercase_strings(self):
        self.assertEqual(slugify('BANANA'), 'banana')

    def test_slugify_trim_strings_and_extra_white_spaces(self):
        self.assertEqual(slugify('hello '), 'hello')
        self.assertEqual(slugify(' hello'), 'hello')
        self.assertEqual(slugify(' hello '), 'hello')
        self.assertEqual(slugify(' hello world '), 'hello-world')
        self.assertEqual(slugify('''
            \n\t
            hello \n\t world
            \n\t
        '''), 'hello-world')

    def test_slugify_removes_signs(self):
        self.assertEqual(slugify('(this is a "test")'), 'this-is-a-test')
        self.assertEqual(slugify('<<wow>> :: [yeah]'), 'wow-yeah')
        self.assertEqual(slugify('c++'), 'c')
        self.assertEqual(slugify('?#foo+bar+baz!'), 'foo-bar-baz')

    def test_slugify_use_given_join_sign(self):
        self.assertEqual(slugify('Slugify this string please!', '-'), 'slugify-this-string-please')
        self.assertEqual(slugify('Slugify this string please!', '_'), 'slugify_this_string_please')
        self.assertEqual(slugify('Slugify this string please!', '.'), 'slugify.this.string.please')

    def test_slugify_converts_non_ascii_letters(self):
        self.assertEqual(slugify('Mönstér Mägnët'), 'monster-magnet')

    def test_slugify_preserves_numbers(self):
        self.assertEqual(slugify('12 eggs, 1 gallon of milk, 4 bananas'), '12-eggs-1-gallon-of-milk-4-bananas')

    def test_slugify_removes_dash_duplicates(self):
        self.assertEqual(slugify('-hello world too--much --dashes---here--'), 'hello-world-too-much-dashes-here')

    def test_slugify_rejects_empty_separator(self):
        with self.assertRaises(ValueError) as raised:
            slugify('hello world', separator='')

        self.assertEqual(str(raised.exception), 'separator must be a non-empty string')

    def test_slugify_rejects_non_string_separator(self):
        for invalid_separator in (None, 7, ['-'], True):
            with self.assertRaises(TypeError) as raised:
                # noinspection PyTypeChecker
                slugify('hello world', separator=invalid_separator)

            self.assertEqual(
                str(raised.exception),
                'Expected "str", received "{}"'.format(type(invalid_separator).__name__)
            )
