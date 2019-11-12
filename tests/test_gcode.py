import unittest2
import p2pp.variables as v
from p2pp.gcode import GCodeCommand

class TestGCodeCommand(unittest2.TestCase):
    def test_gcode_is_parsed(self):
        g = GCodeCommand("G1 X2 Y3 Z4 E5 ; [comment]")

        self.subTest("Command is valid")
        self.assertEqual(g.Command, 'G')
        self.assertEqual(g.Command_value, '1')

        self.subTest("X Parameters are valid")
        self.assertTrue(g.has_parameter("X"))
        self.assertEqual(g.get_parameter("X", 0), 2)
        self.assertEqual(g.X, 2)

        self.subTest("Y Parameters are valid")
        self.assertTrue(g.has_parameter("Y"))
        self.assertEqual(g.get_parameter("Y", 0), 3)
        self.assertEqual(g.Y, 3)

        self.subTest("Z Parameters are valid")
        self.assertTrue(g.has_parameter("Z"))
        self.assertEqual(g.get_parameter("Z", 0), 4)
        self.assertEqual(g.Z, 4)

        self.subTest("Comment is valid")
        self.assertEqual(g.Comment, " [comment]")

    def test_missing_parameters_are_not_present(self):
        g = GCodeCommand("G28")
        self.assertFalse(g.has_parameter("X"))
        self.assertFalse(g.has_parameter("Y"))
        self.assertFalse(g.has_parameter("Z"))

    def test_g1_output_format_is_correct(self):
        g = GCodeCommand("G1 F10 E10 Z10 Y10 X10")
        o = str(g)
        self.assertEqual(o, "G1 X10.000 Y10.000 Z10.000 E10.0000 F10")

    def test_parameter_is_updated(self):
        g = GCodeCommand("G1 X1")
        g.update_parameter("X", 10)
        self.assertEqual(g.X, 10)

    def test_parameter_is_removed(self):
        g = GCodeCommand("G1 X1")
        g.remove_parameter("X")
        self.assertFalse(g.has_parameter("X"))

    def test_move_to_comment(self):
        g = GCodeCommand("G1 X1")
        g.move_to_comment("[test]")
        self.assertEqual(g.Command, None)
        self.assertEqual(g.Command_value, None)
        self.assertIn("[test]", g.Comment)
        self.assertTrue(g.is_comment())

    def test_movement_gcodes_match(self):
        gcodes = [
            "G1 X1 Y1"
            "G1 E2"
        ]

        for gcode in gcodes:
            with self.subTest(gcode):
                g = GCodeCommand(gcode)
                self.assertTrue(g.is_movement_command())

    def test_retract_gcodes_match(self):
        gcodes = [
            "G1 E-" + str(v.retract_length[v.current_tool]),
            "G1 E-" + str(v.retract_length[v.current_tool]) + " ; [retract]",
            "G10"
        ]

        for gcode in gcodes:
            with self.subTest(gcode):
                g = GCodeCommand(gcode)
                self.assertTrue(g.is_retract_command())

    def test_unretract_gcodes_match(self):
        gcodes = [
            "G1 E" + str(v.retract_length[v.current_tool]),
            "G1 E" + str(v.retract_length[v.current_tool]) + " ; [retract]",
            "G11"
        ]

        for gcode in gcodes:
            with self.subTest(gcode):
                g = GCodeCommand(gcode)
                self.assertTrue(g.is_unretract_command())

if __name__ == '__main__':
    unittest2.main()