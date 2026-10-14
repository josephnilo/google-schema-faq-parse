import contextlib
import io
import json
import unittest
from unittest.mock import Mock, patch

import FAQ_parse as faq


class FAQTests(unittest.TestCase):
    def test_questions_and_paragraph_boundaries(self):
        result = faq.faq_schema('<h3>First?</h3><p>One <b>bold</b>.</p><p>Two.</p>'
                                '<h3>Not a question</h3><p>Ignored.</p><h3>Second?</h3><p>Three.</p>')
        self.assertEqual(len(result['mainEntity']), 2)
        self.assertEqual(result['mainEntity'][0]['acceptedAnswer']['text'], 'One bold. Two.')
        self.assertEqual(result['mainEntity'][1]['acceptedAnswer']['text'], 'Three.')

    def test_json_escaping_and_script_termination(self):
        html = '<h3>Is "café" valid?</h3><p>A &quot;quote&quot;, newline\n and &lt;/script&gt;.</p>'
        rendered = faq.render_faq(html)
        payload = rendered.split('>', 1)[1].rsplit('</script>', 1)[0]
        result = json.loads(payload)
        self.assertEqual(result['mainEntity'][0]['name'], 'Is "café" valid?')
        self.assertIn('</script>', result['mainEntity'][0]['acceptedAnswer']['text'])
        self.assertEqual(rendered.count('</script>'), 1)

    def test_empty_faq_is_valid(self):
        self.assertEqual(faq.faq_schema('<h3>Title</h3>')['mainEntity'], [])

    def test_json_validation(self):
        self.assertTrue(faq.validateJSON('{}'))
        self.assertFalse(faq.validateJSON('<script>{}</script>'))

    def test_cli_uses_bounded_request(self):
        response = Mock(text='<h3>Ready?</h3><p>Yes.</p>')
        with patch('builtins.input', return_value='https://example.invalid/faq'), \
             patch.object(faq.requests, 'get', return_value=response) as get, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            faq.main()
        get.assert_called_once_with('https://example.invalid/faq', timeout=30)
        response.raise_for_status.assert_called_once()
        self.assertIn('FAQPage', output.getvalue())

    def test_http_failure_propagates(self):
        response = Mock(); response.raise_for_status.side_effect = faq.requests.HTTPError('synthetic')
        with patch('builtins.input', return_value='https://example.invalid'), \
             patch.object(faq.requests, 'get', return_value=response):
            with self.assertRaises(faq.requests.HTTPError):
                faq.main()
