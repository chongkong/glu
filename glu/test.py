from glu import create_scope
import unittest


class CoreTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scope = create_scope(set_basic=False)
        
    def setUp(self):
        self.scope.reset(set_basic=False)

    def test_interpolation(self):
        self.scope.load({
            'name': 'World'
        })

        self.assertEqual(
            self.scope.glue('hello, {{ name }}'),
            'hello, World')

    def test_interpolation_fail(self):
        self.scope.load({
            'int_value': 123,
            'array_value': [1, 2, 3],
            'dict_value': {'foo': 'bar'}
        })

        self.assertEqual(
            self.scope.glue('int: {{ int_value }}'),
            'int: 123')

        with self.assertRaises(AssertionError):
            self.scope.glue('array: {{ array_value }}')

        with self.assertRaises(AssertionError):
            self.scope.glue('dict: {{ dict_value }}')

    def test_load_from_to(self):
        self.scope.load({
            'score': {
                'math': 93
            }
        }, load_from='score', load_to='midterm_score')

        self.assertEqual(self.scope.glue('{{ midterm_score.math }}'), 93)

    def test_fallback(self):
        self.scope.load({
            'score': {
                'math': 93
            }
        })

        self.assertEqual(
            self.scope.glue('{{ score.science ?? score.history ?? score.math }}'), 93)

    def test_string_filters(self):
        self.scope.load({
            'foo': 'This_isREALLYAmazing'
        })

        self.assertEqual(
            self.scope.glue({
                'display': '{{ foo | display }}',
                'camel_case': '{{ foo | camel_case }}',
                'pascal_case': '{{ foo | pascal_case }}',
                'snake_case': '{{ foo | snake_case }}',
                'lisp_case': '{{ foo | lisp_case }}',
                'uppercase': '{{ foo | uppercase }}',
                'uppercase_dash': '{{ foo | uppercase_dash }}',
                'capitalize_dash': '{{ foo | capitalize_dash }}',
            }),
            {
                'display': 'This Is Really Amazing',
                'camel_case': 'thisIsReallyAmazing',
                'pascal_case': 'ThisIsReallyAmazing',
                'snake_case': 'this_is_really_amazing',
                'lisp_case': 'this-is-really-amazing',
                'uppercase': 'THIS_IS_REALLY_AMAZING',
                'uppercase_dash': 'THIS-IS-REALLY-AMAZING',
                'capitalize_dash': 'This-Is-Really-Amazing',
            }
        )

    def test_mute(self):
        self.scope.load({
            'empty_array': [],
            'empty_string': '',
            'empty_dict': {}
        })

        self.assertEqual(
            self.scope.glue({
                'foo': '{{ empty_array | mute_if_empty }}',
                'bar': '{{ empty_string | mute_if_empty }}',
                'zoo': '{{ empty_dict | mute_if_empty }}',
                'coz': '{{ undefined_var | mute }}'
            }), {})

    def test_scope(self):
        self.scope.load({
            'greeting': 'hello, {{ name }}'
        })
        self.scope.load({
            'foo_scope': {
                'name': 'foo'
            },
            'bar_scope': {
                'name': 'bar'
            }
        })

        self.assertEqual(
            self.scope.glue({
                'hello_foo': '{{ greeting < foo_scope }}',
                'hello_bar': '{{ greeting < bar_scope }}'
            }), {
                'hello_foo': 'hello, foo',
                'hello_bar': 'hello, bar'
            })
