"""Testing fmu-ensemble."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

import pandas as pd

from fmu.tools.sensitivities import summarize_design, fmudesignrunner

from test_designmatrix import valid_designmatrix


def test_designsummary():
    """Test import and summary of design matrix"""

    if "__file__" in globals():
        # Easen up copying test code into interactive sessions
        testdir = os.path.dirname(os.path.abspath(__file__))
    else:
        testdir = os.path.abspath(".")

    snorrebergdesign = summarize_design(
        testdir + "/data/sensitivities/distributions/" + "design.xlsx", "DesignSheet01"
    )
    # checking dimensions and some values in summary of design matrix
    assert snorrebergdesign.shape == (7, 9)
    assert snorrebergdesign["sensname"][0] == "rms_seed"
    assert snorrebergdesign["startreal2"][6] == 100
    assert snorrebergdesign["endreal2"][6] == 109
    assert snorrebergdesign["endreal1"].sum() == 333

    # Test same also when design matrix is in .csv format
    designcsv = summarize_design(
        testdir + "/data/sensitivities/distributions/" + "design.csv"
    )

    # checking dimensions and some values in summary of design matrix
    assert designcsv.shape == (7, 9)
    assert designcsv["sensname"][0] == "rms_seed"
    assert designcsv["startreal2"][6] == 100
    assert designcsv["endreal2"][6] == 109
    assert designcsv["endreal1"].sum() == 333


def test_endpoint():
    """Test the installed endpoint"""
    testdatadir = os.path.dirname(os.path.abspath(__file__))

    examplefile = testdatadir + "/data/sensitivities/config/design_input_onebyone.xlsx"
    # The xlsx file contains a relative path, so chdir so that we fit:
    os.chdir(testdatadir + "/..")
    sys.argv = ["fmudesign", examplefile]
    fmudesignrunner.main()

    result = "generateddesignmatrix.xlsx"
    another = "anotheroutput.xlsx"

    assert os.path.exists(result)  # Default output file
    valid_designmatrix(pd.read_excel(result))

    sys.argv = ["fmudesign", examplefile, another]
    fmudesignrunner.main()
    assert os.path.exists(another)

    # clean up
    os.unlink(result)
    os.unlink(another)
