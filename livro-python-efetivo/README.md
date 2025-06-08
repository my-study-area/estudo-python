# Anotações do livro Effective Python

Site do livro: https://effectivepython.com/

Repositório do livro: https://github.com/bslatkin/effectivepython/tree/main


## Item 76: Verify Related Behavior in Testcase Subclasses
- Utilize `unittest.TestCase` para criar subclasses de teste. Mensagem de erro de falha são mais amigáveis.
```python
import unittest

# BOM
class TestMyClass(unittest.TestCase):
    def test_assert_helper(self):
        expected = 12
        found = 2 * 5
        self.assertEqual(expected, found)

# RUIM
def test_assert_statement(self):
    expected = 12
    found = 2 * 5
    assert expected == found
```
