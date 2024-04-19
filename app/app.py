# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:21:10 2019

@author: Marcos

https://docs.python.org/3/faq/windows.html#is-a-pyd-file-the-same-as-a-dll
https://github.com/ContinuumIO/anaconda-issues/issues/10949

"""

#  This file is part of DeepSpineTool
#  Copyright (C) 2021 VG-Lab (Visualization & Graphics Lab), Universidad Rey Juan Carlos
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import Qt
from app.core.ui.mainWindow import MainWindow

from app.core.utils import StdoutManager, OutFileStream  # , OutNullStream

from app.plugins.ui import sceneManagerUi as smui

from app.plugins.ui import nodeViewer as nvui

from app.plugins.ui.image.viewer import img3Viewer as i3vui
from app.plugins.ui.image.viewer import img3MultiProjViewer as i3mpvui
from app.plugins.ui.image.editor import roiSelector as rs
from app.plugins.ui.image.editor import marchingCubes as mc
from app.plugins.ui.image.editor import img3MultiProjEditor as i3mpeui
from app.plugins.ui.image.segmentation import segmentationConnector as sc
from app.plugins.ui.saverManager import saverManager as SM
from app.plugins.ui.image import segmentation as sgui
from app.plugins.utils.image import segmentation as sg
from app.plugins.ui.vtkViewer import vtkViewer as vtk
from app.plugins.ui.image.segmentation import segmentationComparator as segComp
from app.plugins.ui.image.segmentation import noiseFilter as nFilt

def run():
    import sys

    # =============================================================================
    #  Inicialización del sistema de log
    # =============================================================================
    logFile = open("qttool.log", "w")
    ofsout = OutFileStream(logFile, out=StdoutManager().consolestdout)
    ofserr = OutFileStream(logFile, out=StdoutManager().consolestderr)
    StdoutManager().defaultstdout = ofsout
    StdoutManager().defaultstderr = ofserr
    StdoutManager().pushStdout(ofsout)
    StdoutManager().pushStderr(ofserr)
    #    StdoutManager().verbose = False
    #    StdoutManager().allowForcePrint = True
    StdoutManager().tfverbose = False
    #    StdoutManager().pushStderr(OutNullStream())
    #    StdoutManager().pushStdout(OutNullStream())

    # =============================================================================
    #  Inicialización de la ventana principal
    # =============================================================================
    app = Qt.QApplication(sys.argv)
    mw = MainWindow(title="Spine Segmentation Tool")

    # =============================================================================
    # Inicialización de las extensiones
    # =============================================================================
    smui.init()
    nvui.init()
    i3vui.init()
    i3mpvui.init()
    i3mpeui.init()
    rs.init()
    sc.init()
    SM.init()
    vtk.init()
    mc.init()
    segComp.init()
    nFilt.init()

    hasSupportedGPU, hasGPU = sg.initUnet()
    sgui.initCNDL(None, hasSupportedGPU, hasGPU)

    # =============================================================================
    #  Ventana principal
    # =============================================================================
    mw.createWindowMenu()
    mw.show()
    try:
        sys.exit(app.exec())
    except Exception as err:
        raise err
    finally:
        StdoutManager().popStdout()
        StdoutManager().popStderr()
        logFile.close()


if __name__ == '__main__':
    run()
