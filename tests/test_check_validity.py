from gapsule.utils.check_validity import check_mail_validity, check_password_validity, check_reponame_validity, check_username_validity
import unittest


class Test_TestCheckValidity(unittest.TestCase):
    def test_check_mail(self):
        self.assertEqual(check_mail_validity('abcddd'), False)
        self.assertEqual(check_mail_validity('abceee@cn'), False)
        self.assertEqual(check_mail_validity('abc@ddd.com'), True)


if __name__ == '__main__':
    unittest.main()
