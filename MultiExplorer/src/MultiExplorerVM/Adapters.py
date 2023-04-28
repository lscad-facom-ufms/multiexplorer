import json
import os
import sys
import re
from typing import Dict, Union, Any, Optional
from xml.dom import minidom
from xml.etree import ElementTree
from MultiExplorer.src.MultiExplorerVM.AllowedValues import PredictedModels, \
    PredictedApplications
from MultiExplorer.src.MultiExplorerVM.DS_DSE.Nsga2MainVM import Nsga2Main
from MultiExplorer.src.Infrastructure.ExecutionFlow import Adapter
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup, InputType
from MultiExplorer.src.config import PATH_PRED_VM

class CloudsimAdapter(Adapter):
    def __init__(self):
        Adapter.__init__(self)

        self.presenter = None

        self.set_inputs([
            
        ]
        )