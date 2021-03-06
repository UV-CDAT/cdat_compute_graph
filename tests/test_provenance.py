import basetest
import compute_graph
import cdat_compute_graph as prov


class TestProvenanceIntegration(basetest.CDMSBaseTest):
    def testFullProvenance(self):
        u_uri = compute_graph.RawValueNode("file://" + self.getDataFilePath("u_2000.nc"))
        v_uri = compute_graph.RawValueNode("file://" + self.getDataFilePath("v_2000.nc"))

        u_var = prov.DatasetFunction(u_uri, "variable", "u")
        u_sub = prov.GeospatialFunction("subset", u_var, latitude=(-90, 0))
        v_var = prov.DatasetFunction(v_uri, "variable", "v")
        v_sub = prov.GeospatialFunction("subset", v_var, latitude=(-90, 0))

        u_square = compute_graph.ArithmeticOperation("**", u_sub, 2)
        v_square = prov.NDArrayBinaryFunction("power", v_sub, 2)

        wind_magnitude_square = prov.NDArrayBinaryFunction("add", u_square, v_square)
        wind_magnitude = compute_graph.ArithmeticOperation("**", wind_magnitude_square, .5)

        wind_mag = wind_magnitude.derive()

        ufile = self.getDataFile("u_2000.nc")
        vfile = self.getDataFile("v_2000.nc")
        u = ufile("u", latitude=(-90, 0))
        v = vfile("v", latitude=(-90, 0))
        w = (u**2 + v ** 2) ** .5
        self.assertArraysEqual(w, wind_mag)
