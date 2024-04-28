import unittest

from src.line_parser import LineParser, ParseError, ParseResults

class TestLineParser(unittest.TestCase):
    def test_comments(self):
        line = '# anime'
        with self.assertRaisesRegex(ParseError, r'.* line is empty'):
            LineParser.parse(line, 0, False)

    def test_malformed(self):
        with self.assertRaisesRegex(ParseError, r'.* line is empty'):
            LineParser.parse('', 0, False)
        
        with self.assertRaisesRegex(ParseError, r'.* unknown command'):
            LineParser.parse('P 1', 0, False)
        
        with self.assertRaisesRegex(ParseError, r'.* too few .*'):
            LineParser.parse('? 2', 0, False)
        
        with self.assertRaisesRegex(ParseError, r'.* too few .*'):
            LineParser.parse('>', 0, False)
        
        with self.assertRaisesRegex(ParseError, r'.* too many .*'):
            LineParser.parse('> 2 3', 0, False)
        
        with self.assertRaisesRegex(ParseError, r'.* too many .*'):
            LineParser.parse('? 2 3 4 5', 0, False)
        
        with self.assertRaisesRegex(ParseError, r'.* must be integers'):
            LineParser.parse('? cringe flex', 0, False)
        
        with self.assertRaisesRegex(ParseError, r'.* must be integers'):
            LineParser.parse('> >', 0, False)

    def test_commands(self):
        self.assertEqual(LineParser.parse('> 3', 5, False), ParseResults(1, 3, False))
        self.assertEqual(LineParser.parse('< 3', 5, False), ParseResults(-1, 3, False))
        self.assertEqual(LineParser.parse('1 3', 5, False), ParseResults(0, 3, True))
        self.assertEqual(LineParser.parse('0 3', 5, True), ParseResults(0, 3, False))
        self.assertEqual(LineParser.parse('? 3 4', 5, False), ParseResults(0, 4, False))
        self.assertEqual(LineParser.parse('? 3 4', 5, True), ParseResults(0, 3, True))
