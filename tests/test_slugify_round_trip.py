from unittest import TestCase

from string_utils import is_slug, slugify


class SlugifyRoundTripTestCase(TestCase):
    def test_slugify_output_is_accepted_by_is_slug(self):
        separators = ['-', '_', '.', '+', '..']
        inputs = ['hello world', 'Top 10 Tips!', '  spaces   and   runs  ']

        for separator in separators:
            for input_string in inputs:
                with self.subTest(separator=separator, input_string=input_string):
                    slug = slugify(input_string, separator)
                    self.assertNotEqual(slug, '')
                    self.assertTrue(
                        is_slug(slug, separator),
                        'is_slug rejected {!r} with separator {!r}'.format(slug, separator)
                    )
