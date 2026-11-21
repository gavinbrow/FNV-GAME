"""Safety checks for the anchored native class/override source transformation."""
import unittest

from tescontainer_experiment import transform


SOURCE = '''class TESContainer : public BaseFormComponent
{
  public:
    virtual void CopyFromBase(BaseFormComponent* component);
};
struct FUN_00481d10_shell : TESContainer
{
    bool FUN_00481d10(BaseFormComponent* other);
};
bool FUN_00481d10_shell::FUN_00481d10(BaseFormComponent* other)
{
    return other == 0;
}
'''


class TransformTests(unittest.TestCase):
    def test_moves_declaration_and_preserves_body(self):
        source, header = transform(SOURCE)
        self.assertIn('#include "TESContainer.h"', source)
        self.assertIn('virtual bool CompareWithBase(BaseFormComponent* other);', header)
        self.assertIn('bool TESContainer::CompareWithBase(BaseFormComponent* other)', source)
        self.assertIn('    return other == 0;', source)
        self.assertNotIn('FUN_00481d10_shell', source)

    def test_duplicate_class_rejected(self):
        with self.assertRaises(ValueError):
            transform(SOURCE + SOURCE)

    def test_existing_override_rejected(self):
        with self.assertRaises(ValueError):
            transform(SOURCE.replace('virtual void CopyFromBase', 'virtual bool CompareWithBase'))

    def test_unhandled_shell_reference_rejected(self):
        with self.assertRaises(ValueError):
            transform(SOURCE + '\nFUN_00481d10_shell* another_view;\n')


if __name__ == '__main__':
    unittest.main()
