import os
import subprocess
import unittest2

class RegressionTests(unittest2.TestCase):
    dir_path = None
    script_path = None
    gcodes_path = None
    output_path = None

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.script_path = os.path.join(self.dir_path, "..")
        self.gcodes_path = os.path.join(self.dir_path, "gcodes")
        self.output_path = os.path.join(self.dir_path, "output")

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def __run_test__(self, inputFile, outputFile):
        p2 = os.path.join(self.script_path, "p2pp.py")
        gcode = os.path.join(self.gcodes_path, inputFile)
        mcf = os.path.join(self.output_path, outputFile)
        res = subprocess.call(["python", p2, "-n", "-g", "-i", gcode, "-d", mcf])
        return res

    def test_simple_case(self):
        res = self.__run_test__("TestSimple.gcode", "TestSimple.mcf.gcode")
        self.assertEqual(res, 0)

    def test_absolute_extrusions(self):
        res = self.__run_test__("TestAbsolute.gcode", "TestAbsolute.mcf.gcode")
        self.assertEqual(res, 0)

    def test_maf_file(self):
        res = self.__run_test__("TestMSF.gcode", "TestMAF.maf")
        self.assertEqual(res, 0)
    
    def test_msf_file(self):
        res = self.__run_test__("TestMSF.gcode", "TestMSF.msf")
        self.assertEqual(res, 0)

    def test_palette_plus(self):
        res = self.__run_test__("TestPalettePlus.gcode", "TestPalettePlus.mcf.gcode")
        self.assertEqual(res, 0)

    def test_purge_tower_delta(self):
        res = self.__run_test__("TestPurgeTowerDelta.gcode", "TestPurgeTowerDelta.mcf.gcode")
        self.assertEqual(res, 0)

    def test_purge_tower_full_optimization(self):
        res = self.__run_test__("TestPurgeTowerFullOptim.gcode", "TestPurgeTowerFullOptim.mcf.gcode")
        self.assertEqual(res, 0)

    def test_short_splices(self):
        res = self.__run_test__("TestShortSplices.gcode", "TestShortSplices.mcf.gcode")
        self.assertEqual(res, 0)

    def test_side_wipe(self):
        res = self.__run_test__("TestSideWipe.gcode", "TestSideWipe.mcf.gcode")
        self.assertEqual(res, 0)

    def test_wipe_modes(self):
        res = self.__run_test__("TestWipeIntoObject.gcode", "TestWipeIntoObject.mcf.gcode")
        self.assertEqual(res, 0)

    def test_firmware_retractions(self):
        res = self.__run_test__("TestFirmware.gcode", "TestFirmware.mcf.gcode")
        self.assertEqual(res, 0)

if __name__ == '__main__':
    unittest2.main()