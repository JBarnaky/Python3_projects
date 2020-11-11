import unittest

# def setUpModule():
#     print("SetUp Module")
#
# def tearDownModule():
#     print("Tear Down Module")

class AppTesting(unittest.TestCase):

    # @classmethod
    # def setUp(self):
    #     print("Login test")
    #
    # @classmethod
    # def tearDown(self):
    #     print("Logout test")
    #
    # @classmethod
    # def setUpClass(cls):
    #     print("Open App")
    #
    # @classmethod
    # def tearDownClass(cls):
    #     print("Close App")

    def test_search(self):
        print("Search test")

    @unittest.SkipTest
    def test_advancedSearch(self):
        print("Advanced search test")

    # @unittest.skip("Not ready")
    def test_prePaidRecharge(self):
        print("Pre Paid Recharge test")

    # @unittest.skipIf(1 == 1, "1 = 1")
    def test_postPaidRecharge(self):
        print("Post Paid Recharge test")

    def test_loginByEmail(self):
        print("Login By Email test")

if __name__ == "__main__":
    unittest.main()