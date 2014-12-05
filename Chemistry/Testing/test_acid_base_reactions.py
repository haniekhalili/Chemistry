"""
Copyright (c) 2014 Dan Obermiller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

You should have received a copy of the MIT License along with this program.
If not, see <http://opensource.org/licenses/MIT>
"""

try:
    import cStringIO as IO
except ImportError:
    import StringIO as IO
finally:
    import sys
    import unittest

    from Chemistry import compounds, base_reactions
    from Chemistry.base_reactions import Acid, Base, Reaction, Conditions
    from Chemistry.reactions.acid_base import AcidBase


class test_AcidBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls): pass

    @classmethod
    def tearDownClass(cls): pass

    def setUp(self):
        self.compound1 = compounds.Compound(
                                {"a1":"H", "a2":"H", "a3":"O"},
                                {"b1":("a1", "a3", {'order': 1,
                                                    'chirality': None}),
                                 "b2":("a2", "a3", {'order': 1,
                                                    'chirality': None})},
                                {"id":"Water"})
        self.compound2 = compounds.Compound(
                                {"a1":"H", "a2":"H", "a3":"O", "a4":"H"},
                                {"b1":("a1", "a3", {'order': 1,
                                                    'chirality': None}),
                                 "b2":("a2", "a3", {'order': 1,
                                                    'chirality': None}),
                                 "b3":("a3", "a4", {'order': 1,
                                                    'chirality': None})},
                                {"id":"Hydronium"})
        self.acid1 = Acid(self.compound2, 'a1', -1.74)
        self.base1 = Base(self.compound1, 'a2', -1.74)
        self.conditions1 = Conditions({})
        self.acidbase1 = AcidBase(self.acid1, self.base1, self.conditions1)

        self.hydroiodic = Acid(compounds.Compound(
                                {"a1":"H", "a2":"I"},
                                {"b1":("a1", "a2", {'order': 1,
                                                    'chirality': None})},
                                {"id":"Hydroiodic acid"}), 'a1', -10)
        self.conditions2 = Conditions({'pka': -10, 'acidic':True,
                                       'pka_molecule': self.hydroiodic})
        self.acidbase2 = AcidBase(self.acid1, self.base1, self.conditions2)

        self.hydroxide = Base(compounds.Compound(
                                {"a1":"H", "a2":"O", "a3":"Na"},
                                {"b1":("a1", "a2", {'order': 1,
                                                    'chirality': None}),
                                 "b2":("a2", "a3", {'order': 1,
                                                    'chirality': None})},
                                {"id":"Sodium Hydroxide"}), 'a2', 15.7)
        self.conditions3 = Conditions({'pka': -1.74, 'basic':True,
                                       'pka_molecule': self.hydroxide})
        self.acidbase3 = AcidBase(self.acid1, self.base1, self.conditions3)


    def tearDown(self): pass

    def test_constructor_not_raises_TE1(self):
        AcidBase(self.compound2, self.compound1, {})

    def test_constructor_not_raises_TE2(self):
        AcidBase(self.acid1, self.base1, self.conditions1)

    def test_constructor_raises_TE(self):
        with self.assertRaises(TypeError):
            AcidBase(self.compound2, self.compound1, [])

    def test_get_acid1(self):
        self.assertEqual(self.acidbase1.acid, (self.acid1, True))

    def test_get_acid2(self):
        self.assertEqual(self.acidbase2.acid,
                         (self.conditions2.pka_molecule, False))

    def test_get_base1(self):
        self.assertEqual(self.acidbase1.base, (self.base1, True))

    def test_get_base2(self):
        self.assertEqual(self.acidbase3.base,
                         (self.conditions3.pka_molecule, False))

    def test_get_basic_point1(self):
        self.assertEqual(self.acidbase1.basic_point, ('a2', True))

    def test_get_basic_point2(self):
        self.assertEqual(self.acidbase3.basic_point, ('a2', False))

    def test_get_acidic_point1(self):
        self.assertEqual(self.acidbase1.acidic_point, ('a1', True))

    def test_get_acidic_point2(self):
        self.assertEqual(self.acidbase2.acidic_point, ('a1', False))


if __name__ == '__main__':
    import types


    test_classes_to_run = [value for key, value in globals().items()
                           if (isinstance(value, (type, types.ClassType)) and
                               issubclass(value, unittest.TestCase))]

    loader = unittest.TestLoader()
    big_suite = unittest.TestSuite(loader.loadTestsFromTestCase(test_class)
                                   for test_class in test_classes_to_run)

    runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
    runner.run(big_suite)
