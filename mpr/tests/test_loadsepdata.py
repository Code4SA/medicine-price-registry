from django.test import TestCase
from mpr.management.commands import loadsepdata

class TestLoadSepData(TestCase):
    @staticmethod
    def gen_foo(arr):
        def foo(idx, col):
            return arr[col]
        return foo

    def test_process_row_conversions(self):
        foo = TestLoadSepData.gen_foo([
            None, "My applicant", "REGNO", "22222", None, "My schedule", "NAME NAME2", None, None,
            None, "My dosage form", "3.5", "2", None, None, None, "9.34", None, None, None,
            "originator"
        ])

        res = loadsepdata.Command.process_row(1, foo)
        self.assertTrue(res is not None)

        self.assertTrue("applicant" in res)
        self.assertEquals(res["applicant"], "My Applicant")

        self.assertTrue("regno" in res and res["regno"] == "regno")

        self.assertTrue("nappi_code" in res)
        self.assertEquals(res["nappi_code"], 22222)

        self.assertTrue("schedule" in res)
        self.assertEquals(res["schedule"], "My schedule")

        self.assertTrue("name" in res and res["name"] == "Name Name2")

        self.assertTrue("dosage_form" in res)
        self.assertEquals(res["dosage_form"], "My Dosage Form")

        self.assertTrue("pack_size" in res and res["pack_size"] == 3.5)
        self.assertTrue("num_packs" in res and res["num_packs"] == 2)
        self.assertTrue("sep" in res and res["sep"] == 9.34)
        self.assertTrue("is_generic" in res)
        self.assertEquals(res["is_generic"], "Originator")

        foo = TestLoadSepData.gen_foo([
            None, None, "REGNO", "23232", None, None, "NAME NAME2", None, None,
            None, None, "3.5", "2", None, None, None, "9.34", None, None, None,
            ""
        ])

        res = loadsepdata.Command.process_row(1, foo)
        self.assertTrue("is_generic" in res)
        self.assertEquals(res["is_generic"], "Generic")

    def test_process_value_errors(self):

        foo = TestLoadSepData.gen_foo([
            None, None, "REGNO", "NAPPI", None, None, "NAME NAME2", None, None,
            None, None, "a3.5", "2", None, None, None, "9.34", None, None, None,
            "originator"
        ])

        foo = TestLoadSepData.gen_foo([
            None, None, "REGNO", "1111", None, None, "NAME NAME2", None, None,
            None, None, "a3.5", "2", None, None, None, "9.34", None, None, None,
            "originator"
        ])

        # self.assertraises(valueerror, loadsepdata.command.process_row, 1, foo)

        foo = TestLoadSepData.gen_foo([
            None, None, "REGNO", "1111", None, None, "NAME NAME2", None, None,
            None, None, "3.5", "a2", None, None, None, "9.34", None, None, None,
            "originator"
        ])

        # self.assertRaises(ValueError, loadsepdata.Command.process_row, 1, foo)

        foo = TestLoadSepData.gen_foo([
            None, None, "REGNO", "1111", None, None, "NAME NAME2", None, None,
            None, None, "3.5", "2", None, None, None, "9.34a", None, None, None,
            "originator"
        ])

        # self.assertRaises(ValueError, loadsepdata.Command.process_row, 1, foo)
