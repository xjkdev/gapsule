from unittest import TestCase
from gapsule.settings import settings
from gapsule.models import user, connection, repo, post, notification
from gapsule.utils import async_test
from gapsule.models.git import delete_repo


class Test_TestModelsInterface(TestCase):

    def setUp(self):
        settings['dbname'] = 'gapsule_test'
        connection._connection = connection._create_instance()

        async def _task():
            tables = ['users_info', 'profiles', 'repos']
            for table in tables:
                await connection.execute('delete from {};'.format(table))
        async_test(_task)()

    def test_add_user_pending_verifying(self):
        err_name_data = [['123', 'example@qq.cn', 'Qp123455'],
                         ['a123456', 'example@@qq.cn', 'Qp123455'],
                         ['123', 'test', 'Qp123455']]
        for err_name in err_name_data:
            with self.assertRaises(NameError):
                user.add_user_pending_verifying(err_name[0], err_name[1],
                                                err_name[2])

    @async_test
    async def test_many(self):
        err_data = [['123', 'example@qq.cn', 'Qp123455'],
                    ['a123456', 'example@@qq.cn', 'Qp123455'],
                    ['123', 'test', 'Qp123455']]
        for err in err_data:
            self.assertFalse(await
                             user.create_new_user(err[0], err[1], err[2]))

        self.assertTrue(await user.create_new_user('Player', 'ppp@dd.aa',
                                                   'Poi12334'))
        with self.assertRaises(NameError):
            await user.create_new_user('Player', 'player@gmail.cn',
                                       'Player123')

        self.assertTrue(await user.verify_user('Player', 'Poi12334'))
        self.assertFalse(await user.verify_user('Player', 'Poi123345'))

        self.assertTrue(await user.set_profile('Player',
                                               'Ian',
                                               'Tom',
                                               introduction='I am',
                                               public_email='ppp@ee.qq',
                                               company='NEU'))
        with self.assertRaises(NameError):
            await user.set_profile('Notexisting',
                                   'Ian',
                                   'Tom',
                                   introduction='I am',
                                   public_email='ppp@ee.qq',
                                   company='NEU')

        self.assertTrue(await user.check_session_status(
            'Player', await user.user_login('Player', 'Poi12334')))

        delete_repo('Player', 'examplerepo')
        self.assertTrue(await repo.create_new_repo('Player',
                                                   'examplerepo',
                                                   default_branch='ppobranch'))
        delete_repo('Player', 'examplerepo')
        with self.assertRaises(NameError):
            await repo.create_new_repo('Player',
                                       'examplerepo',
                                       default_branch='ppobranch')

        self.assertTrue((await repo.get_repo_info(await repo.get_repo_id(
            'Player', 'examplerepo')))['default_branch'] == 'ppobranch')

        with self.assertRaises(NameError):
            await repo.create_new_repo('Player',
                                       'exa',
                                       default_branch='ppobranch')

        self.assertTrue(await repo.check_repo_existing('Player',
                                                       'examplerepo'))

        await post.create_new_attached_post(
            await repo.get_repo_id('Player', 'examplerepo'), 'Player', 'title',
            'status', True)

        self.assertTrue(await post.check_post_existing(
            await repo.get_repo_id('Player', 'examplerepo'), 1))

        self.assertTrue(await post.get_postername(
            await repo.get_repo_id('Player', 'examplerepo'), 1) == 'Player')

        self.assertTrue(await post.get_title(
            await repo.get_repo_id('Player', 'examplerepo'), 1) == 'title')

        with self.assertRaises(post.PostNotFoundException):
            await post.create_new_comment(
                (await repo.get_repo_id('Player', 'examplerepo')) * 100, 1,
                'type', 'content', 'Player')

        await post.create_new_comment(
            (await repo.get_repo_id('Player', 'examplerepo')), 1, 'type',
            'content', 'Player')

        self.assertTrue(await post.check_comment_existing(
            await repo.get_repo_id('Player', 'examplerepo'), 1, 1))
