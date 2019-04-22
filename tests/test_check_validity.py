from gapsule.utils.check_validity import check_mail_validity, check_password_validity, check_reponame_validity, check_username_validity
import unittest


class Test_TestCheckValidity(unittest.TestCase):
    def test_check_mail(self):
        false_data = ['', 'test', 'teste@cn', '-- test@dd.com', 'test@@qq.com']
        true_data = ['test@ddd.com', 'test@qq.com.cn']
        for false in false_data:
            self.assertFalse(check_mail_validity(false))
        for true in true_data:
            self.assertTrue(check_mail_validity(true))

    def test_check_password(self):
        false_data = [
            'Ex1', '12345678', 'a1234567', 'Aaaaaaaa', '-- Aa123456',
            'Aa012345678901234567890123456789012345678'
        ]
        true_data = ['Aa123456', 'A1234567']
        for false in false_data:
            self.assertFalse(check_password_validity(false))
        for true in true_data:
            self.assertTrue(check_password_validity(true))

    def test_check_reponame(self):
        false_data = ['tes', "test'--", 'abcdefghijabcdefghij123', '12345']
        true_data = ['anexample', 'ANEXAMPLE', 'a12345']
        for false in false_data:
            self.assertFalse(check_reponame_validity(false))
        for true in true_data:
            self.assertTrue(check_reponame_validity(true))

    def test_check_username(self):
        false_data = [
            ';drop database gapsule;', 'a12', 'a01234567890123456789', '*test'
        ]
        true_data = ['anexample', 'ANEXAMPLE', 'a12345']
        true_data = ['anexample', 'ANEXAMPLE', 'a12345']
        for false in false_data:
            self.assertFalse(check_reponame_validity(false))
        for true in true_data:
            self.assertTrue(check_reponame_validity(true))


if __name__ == '__main__':
    unittest.main()
