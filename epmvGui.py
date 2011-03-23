# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 08:38:56 2010

@author: Ludovic Autin - ludovic.autin@gmail.com
"""
import DejaVu
DejaVu.enableVertexArray = False
import os
import pyubic
from pyubic import uiadaptor
from ePMV import comput_util as C
import ePMV
from MolKit.molecule import AtomSet
from ePMV import comput_util as util
from APBSCommands import APBSgui

class ParameterModeller(uiadaptor):
    def setup(self,epmv,id=1005):
        self.subdialog = True
        self.block = True # special type for blender
        self.title = "Modeller"
        self.epmv = epmv
        witdh=350
        if id is not None :
            id=id
        else:
            id = self.bid
        self.LABEL_ID = {}

        self.NUMBERS = {
        "miniIterMax": self._addElemt(id=id,name="Max iteration",width=50,height=10,
                                            action=None,type="inputInt",
                                            icon=None,
                                            value = 1000,
                                            variable=self.addVariable("int",1000),
                                            mini=0,maxi=100000,step=1),
        "mdIterMax":self._addElemt(id=id+1,name="Max iteration",width=50,height=10,
                                            action=None,type="inputInt",
                                            icon=None,
                                            value = 1000,
                                            variable=self.addVariable("int",1000),
                                            mini=0,maxi=100000,step=1),
        "mdTemp":self._addElemt(id=id+2,name="Temperature",width=50,height=10,
                                            action=None,type="inputInt",
                                            icon=None,
                                            value = 300,
                                            variable=self.addVariable("int",300),
                                            mini=-100,maxi=1000,step=1),
        "rtstep":self._addElemt(id=id+3,name="number of steps",width=100,height=10,
                                            action=self.setRealTimeStep,
                                            type="inputInt",
                                            icon=None,
                                            value = 2,
                                            variable=self.addVariable("int",2),
                                            mini=0,maxi=100,step=1)
                        }
        id = id + len(self.NUMBERS) 
        
        self.LABEL_ID["miniIterMax"]=self._addElemt(id=id,
                    label=self.NUMBERS["miniIterMax"]["name"],
                    width=80)
        self.LABEL_ID["mdIterMax"]=self._addElemt(id=id+1,
                    label=self.NUMBERS["mdIterMax"]["name"],
                    width=80)
        self.LABEL_ID["mdTemp"]=self._addElemt(id=id+2,
                    label=self.NUMBERS["mdTemp"]["name"],
                    width=80)        
        self.LABEL_ID["rtstep"]=self._addElemt(id=id+3,
                    label=self.NUMBERS["rtstep"]["name"],
                    width=80)
        id = id + 4
        
        self.BTN = {
        "mini":self._addElemt(id=id,name="Minimize",width=50,height=10,
                              label = 'Minimize options',
                         action=self.epmv.gui.modellerOptimize,type="button"),
        "md":self._addElemt(id=id+1,name="run MD",width=50,height=10,
                            label = 'Molecular Dynamic options',
                         action=self.epmv.gui.modellerMD,type="button"),
        "cancel":self._addElemt(id=id+2,name="Close",width=50,height=10,
                         action=self.cancel,type="button"),
        "update coordinate":self._addElemt(id=id+3,name="Update coordinates",width=100,height=10,
                         action=self.updateCoord,type="button")
                         }
        id = id + len(self.BTN)
        
        self.LABEL_ID["mini"]=self._addElemt(id=id,
                    label=self.BTN["mini"]["label"],
                    width=80)        
        self.LABEL_ID["md"]=self._addElemt(id=id+1,
                    label=self.BTN["md"]["label"],
                    width=80)
        id = id + 2
        
        self.CHECKBOXS ={
        "store":self._addElemt(id=id,name="store",width=100,height=10,
                                              action=self.setStoring,type="checkbox",icon=None,
                                              variable=self.addVariable("int",0)),
        "real-time":self._addElemt(id=id+1,name="real-time",width=100,height=10,
                                              action=self.setRealTime,type="checkbox",icon=None,
                                              variable=self.addVariable("int",0))
                        }
        id = id + len(self.CHECKBOXS)
        
        self.rtType = ["mini","md"]
        self.sObject = ["cpk","lines","bones","spline"]
        self.COMB_BOX = {"sobject":self._addElemt(id=id,name="Object",
                                    value=self.sObject,
                                    width=60,height=10,action=self.setObjectSynchrone,
                                    variable=self.addVariable("int",0),
                                    type="pullMenu",),
                         "rtType":self._addElemt(id=id+1,name="rtType",
                                    value=self.rtType,
                                    width=60,height=10,action=self.setRToptimzeType,
                                    variable=self.addVariable("int",0),
                                    type="pullMenu",)}
        id = id + len(self.COMB_BOX)

        self.setupLayout()
        return True

    def setupLayout(self):
        self._layout=[]
        self._layout.append([self.CHECKBOXS["store"],])
        self._layout.append([self.CHECKBOXS["real-time"],self.COMB_BOX["rtType"]])
        self._layout.append([self.LABEL_ID["rtstep"],self.NUMBERS["rtstep"]])
        self._layout.append([self.BTN["update coordinate"],self.COMB_BOX["sobject"]])
        self._layout.append([self.LABEL_ID["mini"],])
        self._layout.append([self.LABEL_ID["miniIterMax"],self.NUMBERS["miniIterMax"]])
        self._layout.append([self.BTN["mini"],])
        self._layout.append([self.LABEL_ID["md"],])
        self._layout.append([self.LABEL_ID["mdIterMax"],self.NUMBERS["mdIterMax"]])
        self._layout.append([self.LABEL_ID["mdTemp"],self.NUMBERS["mdTemp"]])
        self._layout.append([self.BTN["md"],])
        self._layout.append([self.BTN["cancel"],])
#        return True
 
    def CreateLayout(self):
        self._createLayout()
#        self.restorePreferences()
        return True
        
    #overwrite RT checkbox action
    def setRealTime(self,*args):
        if hasattr(self.epmv.gui,'current_mol'):
            mol = self.epmv.gui.current_mol
            mol.pmvaction.temp = self.getLong(self.NUMBERS["mdTemp"])
            mol.pmvaction.realtime = self.getBool(self.CHECKBOXS['real-time'])
        
    def setRealTimeStep(self,*args):
        if hasattr(self.epmv.gui,'current_mol'):
            mol = self.epmv.gui.current_mol
            mol.pmvaction.mdstep = self.getLong(self.NUMBERS['rtstep'])

    def setStoring(self,*args):
        if hasattr(self.epmv.gui,'current_mol'):
            mol = self.epmv.gui.current_mol
            mol.pmvaction.store = self.getBool(self.CHECKBOXS['store'])

    def setObjectSynchrone(self,*args):
        if hasattr(self.epmv.gui,'current_mol'):
            mol = self.epmv.gui.current_mol
            mol.pmvaction.sObject = self.sObject[self.getLong(self.COMB_BOX["sobject"])]

    def setRToptimzeType(self,*args):
        if hasattr(self.epmv.gui,'current_mol'):
            mol = self.epmv.gui.current_mol
            rtype= self.rtType[self.getLong(self.COMB_BOX["rtType"])]
            if mol.pmvaction.rtType != rtype :
                mol.pmvaction.rtType = rtype
                #need to update the optimizer ie delete and create a new one
                mol.pmvaction.resetOptimizer()

    def updateCoord(self,*args):
        if hasattr(self.epmv,'gui'):
            mol = self.epmv.gui.current_mol
            if hasattr(mol,'pmvaction'):
                self.epmv.updateMolAtomCoord(mol,mol.pmvaction.idConf,types=mol.pmvaction.sObject)
                mol.pmvaction.updateModellerCoord(mol.pmvaction.idConf,mol.mdl)       

    def doIt(self,*args):
#        print args
        pass

    def cancel(self,*args):
        self.close()
        
    def Command(self,*args):
#        print args
        self._command(args)
        return True

class ParameterScoringGui(uiadaptor):
    _scorer = 'ad3Score'
    _display = False
    label = None
    
    def setup(self,epmv,id=1005):
        self.subdialog = True
        self.block = True # special type for blender
        self.title = "PyAutodock"
        self.epmv = epmv
        witdh=350
        if id is not None :
            id=id
        else:
            id = self.bid
        self.BTN = {"rec":self._addElemt(id=id,name="Browse",width=50,height=10,
                           action=None,type="button"),
                    "lig":self._addElemt(id=id+1,name="Browse",width=50,height=10,
                           action=None,type="button"),
                    "ok":self._addElemt(id=id+2,name="Add Scorer",width=100,height=10,
                           action=self.setupScoring,type="button"),
                    "gScore":self._addElemt(id=id+3,name="Get Score",width=100,height=10,
                           action=self.getScore,type="button"),
                    "cancel":self._addElemt(id=id+4,name="Close",width=100,height=10,
                           action=self.cancel,type="button") 
                    }
        id = id + len(self.BTN)
        self.LABEL_ID = {"rec":self._addElemt(id=id,label="Receptor",width=100,height=10),
                    "lig":self._addElemt(id=id+1,label="Ligand",width=100,height=10),
                    "score":self._addElemt(id=id+2,label="Type of score",width=100,height=10),
                    "scorer":self._addElemt(id=id+2,label="Available scorer",width=100,height=10),
                    }
        id = id + len(self.LABEL_ID)
        #txt input
        self.TXT = {"rec":self._addElemt(id=id,name="Receptor",action=None,width=100,
                          value="hsg1:::;",type="inputStr",
                          variable=self.addVariable("str","hsg1:::;")),
                    "lig":self._addElemt(id=id+1,name="Ligand",action=None,width=100,
                          value="ind:::;",type="inputStr",
                          variable=self.addVariable("str","ind:::;"))
                    }
        id = id + len(self.TXT)


        self.scorertype = ['PyPairWise','ad3Score','ad4Score']
        if C.cAD : #cAutodock is available
            self.scorertype.append('c_ad3Score')
            self.scorertype.append('PairWise')
        self.scoreravailable = self.getScorerAvailable()
        self.COMB_BOX = {"score":self._addElemt(id=id,name="Type of score",
                                    value=self.scorertype,
                                    width=60,height=10,action=self.setScorer,
                                    variable=self.addVariable("int",0),
                                    type="pullMenu",),
                         "scorer":self._addElemt(id=id+1,name="Available scorer",
                                    value=self.scoreravailable,
                                    width=60,height=10,action=self.setCurrentScorer,
                                    variable=self.addVariable("int",0),
                                    type="pullMenu",),
                         }
        id = id + len(self.COMB_BOX)


        self.CHECKBOXS ={"store":self._addElemt(id=id,name="Store",
                                        width=100,height=10,
                                        action=None,type="checkbox",icon=None,
                                        variable=self.addVariable("int",0)),
                        "displayLabel":self._addElemt(id=id+1,name="Display Label",
                                        width=100,height=10,
                                        action=self.toggleDisplay,type="checkbox",icon=None,
                                        variable=self.addVariable("int",0)),
                        "colorRec":self._addElemt(id=id+2,name="Color Rec",
                                        width=100,height=10,
                                        action=self.toggleColor,type="checkbox",icon=None,
                                        variable=self.addVariable("int",0)),
                        "colorLig":self._addElemt(id=id+3,name="Color Lig",
                                        width=100,height=10,
                                        action=self.toggleColor,type="checkbox",icon=None,
                                        variable=self.addVariable("int",0)),
                        "realtime":self._addElemt(id=id+4,name="Real time",width=100,height=10,
                                              action=self.setRealtime,type="checkbox",icon=None,
                                              variable=self.addVariable("int",0)),
                                    }
        id = id + len(self.CHECKBOXS)
        self.setupLayout()
        return True

    def setupLayout(self):
        self._layout=[]
        #setup
        self._layout.append([self.LABEL_ID["rec"],self.TXT["rec"]])
        self._layout.append([self.LABEL_ID["lig"],self.TXT["lig"]])
        self._layout.append([self.LABEL_ID["score"],self.COMB_BOX["score"]])
        self._layout.append([self.BTN["ok"],])
        #current scorer if any
        self._layout.append([self.LABEL_ID["scorer"],self.COMB_BOX["scorer"]])
        #option for the current score
        for butk in self.CHECKBOXS.keys():
            self._layout.append([self.CHECKBOXS[butk],])
        self._layout.append([self.BTN["gScore"],])        
        self._layout.append([self.BTN["cancel"],])

    def CreateLayout(self):
        self._createLayout()
        return True

    def setRealtime(self,*args):
        if hasattr(self.epmv.mv,'energy'):
            self.epmv.mv.energy.realTime = self.getBool(self.CHECKBOXS['realtime'])

    def toggleDisplay(self,*args):
        if hasattr(self.epmv.mv,'energy') :
            display = self.getBool(self.CHECKBOXS['displayLabel'])
            if display : 
                if self.label is None :
                    self.initDisplay()
                self.epmv._toggleDisplay(self.label,display)

            if not hasattr(self.epmv.mv.energy,'label'):
                setattr(self.epmv.mv.energy, 'label', display)
            else :
                self.epmv.mv.energy.label = display

    def toggleStore(self,*args):
        store = self.getBool(self.CHECKBOXS['store'])
        
    def toggleColor(self,*args):
        if hasattr(self.epmv.mv,'energy') :
            r=self.getBool(self.CHECKBOXS['colorRec'])
            l=self.getBool(self.CHECKBOXS['colorLig'])
            if hasattr(self.epmv.mv,'energy') :
                if not hasattr(self.epmv.mv.energy,'color'):
                    setattr(self.epmv.mv.energy, 'color', [r,l])
                else :
                    self.epmv.mv.energy.color = [r,l]
                
    def getScore(self,*args):
        if hasattr(self.epmv.mv,'energy'):
            self.epmv.get_nrg_score(self.epmv.mv.energy)

    def setRec(self):
        pass
    def setLig(self):
        pass

    def getScorerAvailable(self,*args):
        if hasattr(self.epmv.mv,'energy'):
            return self.epmv.mv.energy.data.keys()
        else :
            return []

    def setCurrentScorer(self,*args):
        self.scoreravailable = self.getScorerAvailable()
        if self.scoreravailable :
            name = self.scoreravailable[self.getLong(self.COMB_BOX["scorer"])]
            self.epmv.mv.energy.current_scorer = self.epmv.mv.energy.data[name]

    def setScorer(self,*args):
        self._scorer = self.scorertype[self.getLong(self.COMB_BOX["score"])]
        
    def setupScoring(self,*args):
        #get Rec
        rname = self.getString(self.TXT['rec'])
        #get Lig
        print rname
        lname = self.getString(self.TXT['lig'])
        print lname
        #is this can be selection ? yep
        #recSet=self.mv.select(rname,negate=False, only=True, xor=False, 
        #                           log=0, intersect=False)
        recSet=self.epmv.mv.expandNodes(rname)
        rec = recSet[0].top
        #=self.epmv.mv.getMolFromName(rname)
        ligSet=self.epmv.mv.expandNodes(lname)
        lig = ligSet[0].top
        #test lig and rec
        scorer_name =  rec.name+'-'+lig.name+'-'+self._scorer
        if rec is not None and lig is not None:
            if not hasattr(self.epmv.mv,'energy'):
                self.epmv.mv.energy = C.EnergyHandler(self.epmv.mv)
            self.getScorerAvailable()                
            self.epmv.mv.energy.add(recSet,ligSet,score_type=self._scorer)
            self.addItemToPMenu(self.COMB_BOX["scorer"],scorer_name)
            confNum = 1
            for mol in [rec,lig]:
                # check number of conformations available
                current_confNum = len(mol.allAtoms[0]._coords) -1
                mol.allAtoms.addConformation(mol.allAtoms.coords)
                mol.cconformationIndex = len(mol.allAtoms[0]._coords) -1
        self.toggleDisplay()
        self.toggleColor()
        self.setRealtime()   
            
    def initDisplay(self):
        scene =self.epmv.helper.getCurrentScene()
        #label
        self.label = label = self.epmv.helper.newEmpty("label")
        self.epmv.helper.addObjectToScene(scene,label)     
        self.epmv.helper.constraintLookAt(label)   
        listeName=["score","el","hb","vw","so"]
        y=0.0
        self.listeO=[]
        for i,name in enumerate(listeName):
            o=self.epmv.helper.Text(name,string=name+" : 0.00",pos=[0.,y,0.],
                                    parent=label)
            self.listeO.append(o)  
            y+=5.0
        self.epmv.mv.energy.labels = self.listeO
        #constraint the label to be oriented toward the persp camera
        self.epmv.mv.energy.display = True
        self.epmv.mv.energy.label = True

    def cancel(self,*args):
        self.close()
        
    def Command(self,*args):
#        print args
        self._command(args)
        return True
          
class Parameter_beadRibbons(uiadaptor):
    def setup(self,epmv,id=None):
        self.subdialog = True
        self.block = True
        self.title = "beadRibbons"
        self.epmv = epmv
        witdh=350
        if id is not None :
            id=id
        else:
            id = self.bid
        #default value and parameters type
        self.tapertypes=["sin","linear","cos"]
        self.paramstype = {'quality':{"type":"inputInt","value":12},
            'taperLength':{"type":"inputInt","value":6},
            'taperType':{"type":"pullMenu","value":self.tapertypes},
            'helixBeaded':{"type":"checkbox","value":1},
            'helixWidth':{"type":"inputFloat","value":1.6},
            'helixThick':{"type":"inputFloat","value":1},
            'helixThickness':{"type":"inputFloat","value":0.20},
            'helixBeadRadius':{"type":"inputFloat","value":0.32},
            'helixColor1':{"type":"color","value":(1,1,1)},
            'helixColor2':{"type":"color","value":(1,0,1)},
            'helixBeadColor1':{"type":"color","value":(1,1,1)},
            'helixBeadColor2':{"type":"color", "value":(1,1,1)}, 
            'helixSideColor':{"type":"color","value":(1,1,1)},            
            'coilRadius':{"type":"inputFloat","value":0.1},
            'coilColor':{"type":"color","value":(1,1,1)},
            'turnRadius':{"type":"inputFloat","value":0.1},
            'turnColor':{"type":"color","value":(0,0,1)},
            'sheetBeaded':{"type":"checkbox","value":1},
            'sheetWidth':{"type":"inputFloat","value":1.6},
            'sheetBodyStartScale':{"type":"inputFloat","value":0.4},
            'sheetThick':{"type":"checkbox","value":1},
            'sheetThickness':{"type":"inputFloat","value":0.20},
            'sheetBeadRadius':{"type":"inputFloat","value":0.32},
            'sheetColor1':{"type":"color","value":(1,1,0)},
            'sheetColor2':{"type":"color","value":(0,1,1)},
            'sheetBeadColor1':{"type":"color","value":(1,1,1)},
            'sheetBeadColor2':{"type":"color","value":(1,1,1)},
            'sheetSideColor':{"type":"color","value":(1,1,1)},            
            'sheetArrowhead':{"type":"checkbox","value":1},
            'sheetArrowheadWidth':{"type":"inputFloat","value":2.0},
            'sheetArrowHeadLength':{"type":"inputInt","value":8},
        }
        #create the widget
        #size order ???
        self.PARAMS = {}
        self.LABELS = {}
        for key in self.paramstype : 
            self.PARAMS[key] = self._addElemt(name=key,
                                            width=40,height=10,
                                            action=self.SetPreferences,type=self.paramstype[key]["type"],
                                            icon=None,
                                            value = self.paramstype[key]["value"],
                                            variable=self.addVar(self.paramstype[key]["type"],self.paramstype[key]["value"]))
            self.LABELS[key] = self._addElemt(label=key,width=100)
        self.BTN={}
        self.BTN["ok"] = self._addElemt(name="Update Bead",action=self.SetPreferences,width=50,
                          type="button")
        self.BTN["reset"] = self._addElemt(name="Reset to default",action=self.restorePreferences,width=50,
                          type="button")

        self.BTN["close"] = self._addElemt(name="Close",action=self.close,width=50,
                          type="button")
        
        self.setupLayout()
        return True

    def setupLayout(self):
        #form layout for each SS types ?
        self._layout = []
        ordered = self.PARAMS.keys()
        ordered.sort()
        #frame=[]
        i=0
        if self.host != "blender":
            label=["helix","sheet","coil","turn","general"]
            frame={}
            elemframe={}
            for l in label :
                elemframe[l] = []
            for key in ordered:
                found = False
                for l in label:
                    if key.find(l) != -1 :
                        elemframe[l].append([self.LABELS[key],self.PARAMS[key],])
                        found = True
                        break
                if not found:
                    elemframe["general"].append([self.LABELS[key],self.PARAMS[key],])
            for l in label :
                frame = self._addLayout(name=l,elems=elemframe[l],collapse=True)
                self._layout.append(frame)
        else:
            while i < len(ordered)-1:#in range(len(ordered)/2):
                self._layout.append([self.LABELS[ordered[i]],self.PARAMS[ordered[i]],
                                    self.LABELS[ordered[i+1]],self.PARAMS[ordered[i+1]],
                                    self.LABELS[ordered[i+2]],self.PARAMS[ordered[i+2]]])
                i = i + 3
            
#        for key in ordered:
#            self._layout.append([self.LABELS[key],self.PARAMS[key],])
#        elemFrame=[]
#        elemFrame.append([self.LOAD_BTN,self.LABEL_ID[0],self.LABEL_ID[1]])
#        elemFrame.append([self.EDIT_TEXT,self.FETCH_BTN,self.COMB_BOX["pdbtype"]])
##        elemFrame.append([self.LABEL_ID[2],self.COMB_BOX["mol"]])
#        
#        frame = self._addLayout(id=196,name="Get a Molecule",elems=elemFrame,collapse=False)
#        self._layout.append(frame)
#        
        self._layout.append([self.BTN["reset"],])
        self._layout.append([self.BTN["ok"],self.BTN["close"]])
 
    def CreateLayout(self):
        self._createLayout()
        self.restorePreferences()
        return True
        
    def SetPreferences(self,*args):
        #get the value
        #could use a general getCommand on the elem
        param={}
        for key in self.PARAMS:
           param[key] = self.getVal(self.PARAMS[key])
           print key,param[key]
        #should I do it ? or wait for OK
        #currentmol 
        if hasattr(self.epmv.gui,'current_mol'):
            mol = self.epmv.gui.current_mol
            self.epmv.mv.beadedRibbons(mol,redraw=0,createEvents=False,**param)

    def restorePreferences(self,*args):
        for key in self.paramstype :
            self.setVal(self.PARAMS[key],self.paramstype[key]["value"])
        
    def Command(self,*args):
#        print args
        self._command(args)
        return True  

from Pmv.pmvPalettes import AtomElements
from Pmv.pmvPalettes import DavidGoodsell, DavidGoodsellSortedKeys
from Pmv.pmvPalettes import RasmolAmino, RasmolAminoSortedKeys
from Pmv.pmvPalettes import Shapely
from Pmv.pmvPalettes import SecondaryStructureType
from Pmv.colorPalette import ColorPaletteNG,ColorPaletteFunctionNG

class Parameter_pmvPalette(uiadaptor):
    def setup(self,epmv,id=None):
        self.subdialog = True
        self.block = True
        self.title = "pmv Palette"
        self.epmv = epmv
        self.witdh=200
        if id is not None :
            id=id
        else:
            id = self.bid
        self.defaultColor = {
            "atoms": AtomElements.copy(),
            "atomsDG":DavidGoodsell.copy(),
            "amino":RasmolAmino.copy(),
            "aminoS":Shapely.copy(),
            "ss":SecondaryStructureType.copy()
            }
        self.listPalettes={
            "atoms": ["atoms type",AtomElements],
            "atomsDG":["atoms polarity type",DavidGoodsell],
            "amino":["residue type",RasmolAmino],
            "aminoS":["residue shape type",Shapely],
            "ss":["secondary structure",SecondaryStructureType]
            }
            
        self.group={}
        for key in self.listPalettes : 
            self.group[key] = {}
            palette = self.listPalettes[key][1]
            self.group[key]["title"] = self._addElemt(label=self.listPalettes[key][0],width=100)
            self.group[key]["widget"] = {}
            for name in palette:
                widget = self._addElemt(name=name,
                                            width=40,height=10,
                                            action=self.SetColors,type="color",
                                            icon=None,
                                            value = palette[name],
                                            variable=self.addVar("color",palette[name]))
                label = self._addElemt(label=name,width=100)
                self.group[key]["widget"][name] = [label,widget]
        self.BTN={}
        self.BTN["ok"] = self._addElemt(name="Set Color",action=self.SetColors,width=50,
                          type="button")
        self.BTN["reset"] = self._addElemt(name="Reset to default",action=self.restoreColors,width=50,
                          type="button")

        self.BTN["close"] = self._addElemt(name="Close",action=self.close,width=50,
                          type="button")
        
        self.setupLayout()
        return True

    def setupLayout(self):
        #form layout for each SS types ?
        self._layout = []
        ordered = ["atoms","atomsDG","amino","aminoS","ss"]
#        if self.host != "blender":
        frame={}
        elemframe={}
        for l in ordered :
            elemframe[l] = []
        for key in ordered:
            for name in self.group[key]["widget"]:
                wi = self.group[key]["widget"][name][1]
                la = self.group[key]["widget"][name][0]
                elemframe[key].append([wi,la,])
            frame = self._addLayout(name=self.listPalettes[key][0],
                                    elems=elemframe[key],collapse=True,)
#                                    type = "tab")
            self._layout.append(frame)
#        else:
#            for key in ordered:
#                title = self.group[key]["title"]
#                self._layout.append([title,])
#                for name in self.group[key]["widget"]:
#                    print key,name,name in self.group[key]["widget"]
#                    w = self.group[key]["widget"][name][1]
#                    l = self.group[key]["widget"][name][0]
#                    self._layout.append([l,w])
        self._layout.append([self.BTN["reset"],])
        self._layout.append([self.BTN["ok"],self.BTN["close"]])
 
    def CreateLayout(self):
        self._createLayout()
        #self.restorePreferences()
        return True
        
    def SetColors(self,*args):
        #get the value
        #could use a general getCommand on the elem
        ordered = ["atoms","atomsDG","amino","aminoS","ss"]
        fcolors = [self.epmv.mv.colorByAtomType,
                          self.epmv.mv.colorAtomsUsingDG,
                          self.epmv.mv.colorByResidueType,
                          self.epmv.mv.colorResiduesUsingShapely,
                          self.epmv.mv.colorBySecondaryStructure,
                          self.epmv.mv.colorByChains]#,
#                          self.epmv.mv.color,
#                          self.epmv.mv.colorByProperty]
        for i,key in enumerate(ordered) :
            palette = self.listPalettes[key][1]
            for name in palette:
                w=self.group[key]["widget"][name][1]
                color = self.getVal(w)
                self.listPalettes[key][1][name] = color
            lfction = None
            lmenber = fcolors[i].palette.lookupMember
            colorClass  = ColorPaletteNG
            if hasattr(fcolors[i].palette,"lookupFunction"):
                lfction = fcolors[i].palette.lookupFunction
                colorClass = ColorPaletteFunctionNG(
                self.listPalettes[key][0], self.listPalettes[key][1], readonly=0,
                lookupFunction=lfction)
            else :
                fcolors[i].palette = colorClass(
            self.listPalettes[key][0], self.listPalettes[key][1], readonly=0,
            lookupMember=lmenber)
        #need to update the palette attached to the MV commands
        
 
    def restoreColors(self,*args):
        for key in self.defaultColor :
            palette = self.defaultColor[key]
            for name in palette:
                w=self.group[key]["widget"][name][1]
                self.setVal(w,palette[name])
                self.listPalettes[key][1][name] = palette[name]
                
    def Command(self,*args):
#        print args
        self._command(args)
        return True  

class Parameter_epmvGUI(uiadaptor):
    def setup(self,epmv,id=None):
        self.subdialog = True
        self.title = "Preferences"
        self.epmv = epmv
        witdh=350
        if id is not None :
            id=id
        else:
            id = self.bid
        #need to split in epmv options and gui options - >guiClass?
        self.EPMVOPTIONS = {}
        for key in self.epmv.keywords : 
            if self.epmv.keywords[key] is not None and key != "synchro_ratio" \
                and key != "synchro_timeline":
                self.EPMVOPTIONS[key] = self._addElemt(id=id,
                                            name=self.epmv.keywords[key]["name"],
                                            width=witdh,height=10,
                                            action=None,type=self.epmv.keywords[key]["type"],
                                            icon=None,
#                                            value = self.epmv.keywords[key]["value"],
                                            variable=self.addVariable("int",0))
                id = id +1
        #special case of synchro_ratio
        self.SRATIO=[[self._addElemt(id=id,
                            name=self.epmv.keywords["synchro_timeline"]["name"],
                            width=witdh,height=10,
                            action=None,type=self.epmv.keywords["synchro_timeline"]["type"],
                            icon=None,
                            variable=self.addVariable("int",0)),],
                     [self._addElemt(id=id+1,
                                            name=self.epmv.keywords["synchro_ratio"][0]["name"],
                                            width=80,height=10,
                                            action=None,
                                            type=self.epmv.keywords["synchro_ratio"][0]["type"],
                                            icon=None,
                                            value=self.epmv.keywords["synchro_ratio"][0]["value"],
                                            mini=self.epmv.keywords["synchro_ratio"][0]["mini"],
                                            maxi=self.epmv.keywords["synchro_ratio"][0]["maxi"],
                                            variable=self.addVariable("int",0)),
                    self._addElemt(id=id+2,
                    label=self.epmv.keywords["synchro_ratio"][0]["name"],
                    width=120),],
                    [self._addElemt(id=id+3,
                                            name=self.epmv.keywords["synchro_ratio"][1]["name"],
                                            width=80,height=10,
                                            action=None,
                                            type=self.epmv.keywords["synchro_ratio"][1]["type"],
                                            icon=None,
                                            value=self.epmv.keywords["synchro_ratio"][1]["value"],
                                            mini=self.epmv.keywords["synchro_ratio"][1]["mini"],
                                            maxi=self.epmv.keywords["synchro_ratio"][1]["maxi"],                                            
                                            variable=self.addVariable("int",0)),
                    self._addElemt(id=id+4,
                    label=self.epmv.keywords["synchro_ratio"][1]["name"],
                    width=120)]]
        id = id +5
        self.BTN = self._addElemt(id=id,name="OK",action=self.SetPreferences,width=50,
                          type="button")
        
        self.setupLayout()
#        self.restorePreferences()
        return True

    def setupLayout(self):
        self._layout = []
        for key in self.EPMVOPTIONS:
            self._layout.append([self.EPMVOPTIONS[key],])
        self._layout.append(self.SRATIO[0])
        self._layout.append(self.SRATIO[1])
        self._layout.append(self.SRATIO[2])
        self._layout.append([self.BTN,])
 
    def CreateLayout(self):
        self._createLayout()
        self.restorePreferences()
        return True
        
    def SetPreferences(self,*args):
        print args
        for key in self.EPMVOPTIONS:
            print key
            setattr(self.epmv,key,self.getBool(self.EPMVOPTIONS[key]))
        self.epmv.synchro_timeline = self.getBool(self.SRATIO[0][0])
        self.epmv.synchro_ratio[0] = self.getLong(self.SRATIO[1][0])
        self.epmv.synchro_ratio[1] = self.getLong(self.SRATIO[2][0])
        if self.epmv.useModeller and self.epmv._modeller:
            self.epmv.center_mol = False
            self.epmv.center_grid = False
            if self.epmv.env is None:
                from ePMV.extension.Modeller.pmvAction import setupENV
                #setup Modeller
                self.epmv.env = setupENV()
        #if self.epmv.synchro_realtime:
        self.epmv.synchronize()
#        #self.AskClose()
#        if self.epmv.gui._depthQ :
#            self.epmv.helper.create_environment('depthQ',distance = 30.)
#        else :
#            obj=self.epmv.helper.getObject('depthQ')
#            if obj is not None :
#                self.epmv.helper.toggleDisplay(obj,False)
        self.close()
        
    def restorePreferences(self):
        for key in self.EPMVOPTIONS:
            self.setBool(self.EPMVOPTIONS[key],getattr(self.epmv,key))
        self.setBool(self.SRATIO[0][0],self.epmv.synchro_timeline)
        self.setLong(self.SRATIO[1][0],self.epmv.synchro_ratio[0])
        self.setLong(self.SRATIO[2][0],self.epmv.synchro_ratio[0])
#        if self.epmv.gui._modeller :
#            self.SetBool(self.OPTIONS['modeller']["id"],self.epmv.gui._useModeller)
        
    def Command(self,*args):
#        print args
        self._command(args)
        return True




#should be called uiDialog, and uiSubDialog ?
class epmvGui(uiadaptor):
    #TODO complete the command callback
    #
    restored=False
    status = 0
    link = 0
    nF=1000
    __version__="0.3.1b"
    __about__="ePMV v"+__version__+"\n"
    __about__+="""\:
ePMV by Ludovic Autin,Graham Jonhson,Michel Sanner.
Develloped in the Molecular Graphics Laboratory directed by Arthur Olson.
"""
    __url__ = ["http://epmv.scripps.edu",
           'http://mgldev.scripps.edu/projects/ePMV/update_notes.txt',
           'http://epmv.scripps.edu/documentation/citations-informations',]

    host=""
    
    def setup(self,epmv=None,rep="epmv",mglroot="",host=''):        
        if not host :
            if not self.host:
                self.host = epmv.host 
        elif not self.host:
            self.host = host
#        print "selfdict ",self.__dict__
#        print dir(self)
        self.restored = False   
        if epmv is None:
            #try to restore
            print "try to restore"
            epmv = self._restore('mv',rep)
            print epmv
            if epmv is None:
                epmv = ePMV.epmv_start(self.host,debug=0)
                if mglroot :
                    epmv.mglroot = mglroot
                else :
                    epmv.mglroot = ""
                epmv.gui = self
                epmv.initOption()
            else :
                self.restored = True
            self._store('mv',{epmv.rep:epmv})
        self.epmv = epmv
        self.mv = epmv.mv
        self.funcColor = [self.mv.colorByAtomType,
                          self.mv.colorAtomsUsingDG,
                          self.mv.colorByResidueType,
                          self.mv.colorResiduesUsingShapely,
                          self.mv.colorBySecondaryStructure,
                          self.mv.colorByChains,
                          self.mv.color,
                          self.mv.colorByProperty]
#        print self.funcColor
        self.colSchem=['Atoms using CPK',
               'AtomsDG (polarity/charge)',
               'Per residue',
               'Per residue shapely',
               'Secondary Structure',
               'Chains',
               'Custom color',
               'Rainbow from N to C',
               'Temperature Factor',
               'sas area']

        #before creating the menu check the extensiosn
        #self.checkExtension()
        #as the recent File
        self.title = "ePMV"
        self.y = 620
        self.w=160
        self.h=150
        self.epmv.setupMaterials()
        self.epmv.checkExtension()
        self.initWidget()
        self.setupLayout()
        self.pymolgui = None
        self.pym = None

    def CreateLayout(self):
        self._createLayout()
        if self.restored :
            for mol in self.mv.Mols:
                print "restore ",mol.name
                self.addItemToPMenu(self.COMB_BOX["mol"],mol.name)
                for dataname in self.mv.iMolData[mol.name] :
                    print "restore dataname ",dataname
                    self.addItemToPMenu(self.COMB_BOX["dat"],dataname)
                    self.current_traj = self.mv.iTraj[1]
#                self.buttonLoad(None,mname=mol.name)
#                self.firstmol = False
#                #need to restore the data
#                for dataname in self.mv.iMolData[mol.name] :
#                    print "dataname ",dataname               
#                    self.buttonLoadData(None,trajname=dataname,molname=mol.name)              
#                #need to restore the selection
#                if mol.name in self.mv.MolSelection.keys():
#                    self.add_Selection(n=mol.name)
#                #for selname in self.mv.MolSelection[mol.name].keys() :
                #    self.addChildToMolMenu(selname)
            self.restored = False                  
        return True

    def Command(self,*args):
#        print args
        self._command(args)
        return True

    def initWidget(self,id=None):
        if id is not None :
            id=id
        else:
            id = self.bid
        self.id = id
        self.iconsdir = self.epmv.mglroot+os.sep+"MGLToolsPckgs"+os.sep+"ePMV"+\
                        os.sep+"images"+os.sep+"icons"+os.sep
        self.menuorder = ["File","Edit","Extensions","Help"]
        #submenu recentFile.
        self.submenu= None
        if self.mv.recentFiles.categories.has_key("Documents"):
            self.submenu={}
            for i,r in enumerate(self.mv.recentFiles.categories["Documents"]):
                if r[1] == "readMolecule" :
                    self.submenu[str(self.id-1)]=self._addElemt(name=r[0],
                                                    action=self.loadRecentFile)
        #self.apbsub = {}
        #self.apbsub[str(self.id-1)]=self._addElemt(name="Compute Potential Using APBS",
        #                                            action=self.runAPBS)
        
        self._menu = self.MENU_ID = {"File":
                      [self._addElemt(name="Recent Files",action=None,sub=self.submenu),
                      self._addElemt(name="Open PDB",action=self.browsePDB),#self.buttonLoad},
                      self._addElemt(name="Open Data",action=self.browseDATA)],#self.buttonLoadData
                       "Edit" :
                      [self._addElemt(name="Options",action=self.drawPreferences),
                       self._addElemt(name="Colors palettes",action=self.drawPalette),
                      ],
                      #  "Compute" :
                      #[self._addElemt(name="Electrostatics",action=None,sub=self.apbsub),
                      #],
                      #self.drawPreferences}],
#                      [{"id": id+3, "name":"Camera&c&","action":self.optionCam},
#                       {"id": id+4, "name":"Light&c&","action":self.optionLight},
#                       {"id": id+5, "name":"CloudsPoints&c&","action":self.optionPC},
#                       {"id": id+6, "name":"BiCylinders&c&","action":self.optionCyl}],
                       "Extensions" : [
                       self._addElemt(name="APBS Electrostatics",action=self.drawAPBS),
                       self._addElemt(name="PyAutoDock",action=self.drawPyAutoDock),
                       ],
                       "Help" : 
                      [self._addElemt(name="About ePMV",action=self.drawAbout),#self.drawAbout},
                       self._addElemt(name="ePMV documentation",action=self.launchBrowser),#self.launchBrowser},
                       self._addElemt(name="Check for Update",action=self.check_update),#self.check_update},
                       self._addElemt(name="Citation Informations",action=self.citationInformation),#self.citationInformation},
                      ],
                       }

        if self.epmv._AF :
            self.MENU_ID["Extensions"].append(self._addElemt(name="AutoFill",
                                                action=None))#self.launchAFgui})
        if self.epmv._AR :
            self.MENU_ID["Extensions"].append(self._addElemt(name="ARViewer",
                                                action=None))#self.launchARgui})
        if self.epmv._modeller:            
            self.MENU_ID["Extensions"].append(self._addElemt(name="Modeller",
                                                action=self.drawModellerGUI))#self.modellerGUI})
        if self.epmv._modeller:            
            self.MENU_ID["Extensions"].append(self._addElemt(name="Pymol",
                                                action=self.drawPymolGUI))#self.modellerGUI})

        self.MENU_ID["Extensions"].append(self._addElemt(name="Add an Extension",
                                                action=self.addExtensionGUI))#self.addExtensionGUI})
        self.LABEL_ID = []
        self.LABEL_ID.append(self._addElemt(label="to a PDB file OR enter a 4 digit ID (e.g. 1crn):",
                                            width=120))
        self.LABEL_ID.append(self._addElemt(label="",width=1))
        self.LABEL_ID.append(self._addElemt(label="Current selection :",width=50))
        self.LABEL_ID.append(self._addElemt(label="Add selection set using string or",width=120))
        self.LABEL_ID.append(self._addElemt(label="Scheme:",width=50))
        self.LABEL_ID.append(self._addElemt(label="to load a Data file",width=50))
        self.LABEL_ID.append(self._addElemt(label="to Current Selection and play below:",width=120))
        self.LABEL_ID.append(self._addElemt(label="PMV-Python scripts/commands",width=50))
        self.LABEL_ID.append(self._addElemt(label="Molecular Representations",width=50))
        self.LABEL_ID.append(self._addElemt(label="Apply",width=30))
        self.LABEL_ID.append(self._addElemt(label="a Selection Set",width=50))
        self.LABEL_ID.append(self._addElemt(label="atoms in the Selection Set",width=120))
        self.LABEL_ID.append(self._addElemt(label="or",width=10))
        self.LABEL_ID.append(self._addElemt(label="or",width=10))
        self.LABEL_ID.append(self._addElemt(label=":",width=10))
        self.LABEL_ID.append(self._addElemt(label="Or choose a custom color",width=100))

        self.LABEL={}
        self.LABEL["uv1"]=self._addElemt(label="Create Texture Mapping for",width=100)
        self.LABEL["uv2"]=self._addElemt(label="Using",width=100)
        
        self.LABEL_VERSION = self._addElemt(label='welcome to ePMV '+self.__version__,width=100)
        
        self.pdbid = self.addVariable("str","1crn")
        self.EDIT_TEXT = self._addElemt(name="pdbId",action=None,width=100,
                          value="1crn",type="inputStr",variable=self.pdbid)
        self.LOAD_BTN = self._addElemt(name="Browse",width=40,height=10,
                         action=self.browsePDB,type="button")#self.buttonBrowse
        
        self.FETCH_BTN = self._addElemt(name="Fetch",width=40,height=10,
                         action=self.fetchPDB,type="button")#self.buttonLoad}
        
        self.DATA_BTN = self._addElemt(name="Browse",width=40,height=10,
                         action=self.browseDATA,type="button")#self.buttonLoadData}
        
        self.PMV_BTN = self._addElemt(name="Exec",width=80,height=10,
                         action=self.execPmvComds,type="button")#self.execPmvComds}
        
#        self.KEY_BTN= {"id":id,"name":"store key-frame",'width':80,"height":10,
#                         "action":None}
#        
#        self.DEL_BTN= self._addElemt(id=id,name="Delete",width=80,height=10,
#                         action=self.deleteMol,type="button")
#        
#        print "id del button", id-1
        self.BTN={}
        self.BTN["uv"] = self._addElemt(name="Create",width=80,height=10,
                         action=self.createTexture,type="button")
        self.BTN["bead"] = self._addElemt(name="Options",width=80,height=10,
                         action=self.drawBeadOption,type="button")
        #values and variable definition
        self.datatype=['e.g.','Trajectories:','  .trj','  .xtc','VolumeGrids:']
        DataSupported = '\.mrc$|\.MRC$|\.cns$|\.xplo*r*$|\.ccp4*$|\.grd$|\.fld$|\.map$|\.omap$|\.brix$|\.dsn6$|\.dn6$|\.rawiv$|\.d*e*l*phi$|\.uhbd$|\.dx$|\.spi$'
        DataSupported=DataSupported.replace("\\","  ").replace("$","").split("|")
        self.datatype.extend(DataSupported)
        
        self.presettype=['available presets:','  Lines','  Liccorice','  SpaceFilling',
                         '  Ball+Sticks','  RibbonProtein+StickLigand',
                         '  RibbonProtein+CPKligand','  Custom',
                         '  Save Custom As...']#'  xray',
        self._preset = self.addVariable("int",1)
        
        self.keyword = ['keywords:','  backbone','  sidechain','  chain','  picked']
        from MolKit.protein import ResidueSetSelector
        kw=map(lambda x:"  "+x,ResidueSetSelector.residueList.keys())
        self.keyword.extend(kw)
        self._keyword=self.addVariable("int",1)
        
        self.scriptliste = ['Open:',
                            'pymol_demo',
                            'interactive_docking',
                            'colorbyAPBS',
                            'demo1',
                            'user_script']
        self.scriptsave = ['Save','Save as']
        self._eOscript = self.addVariable("int",1)
        self._eSscript = self.addVariable("int",1)
        
        self.editselection = ['Save set','Rename set','Delete set']
        self._eSelection = self.addVariable("int",1)
        
        self.pdbtype=['PDB','TMPDB','OPM','CIF','PQS']
        self._pdbtype=self.addVariable("int",1)
        
        self._currentmol=self.addVariable("int",1)
        self._col=self.addVariable("int",1)
        self._dat=self.addVariable("int",1)
        
        self.boneslevel=["Trace","Backbone","Full Atoms","Domain","Chain","Mol","Selection"]
        self._bonesLevel=self.addVariable("int",1)
        
        self.uvselection=["unwrapped mesh UV","regular disposed triangle"]
        self._uvselection=self.addVariable("int",1)
        
        self.COMB_BOX = {"mol":self._addElemt(name="Current",value=[],
                                    width=60,height=10,action=self.setCurMol,
                                    variable=self._currentmol,
                                    type="pullMenu"),#self.setCurMol
                         "col":self._addElemt(name="Color",
                                    value=self.colSchem,
                                    width=80,height=10,action=self.color,
                                    variable=self._col,
                                    type="pullMenu",),#self.color},
                         "dat":self._addElemt(name="Data",value=["None"],
                                    width=60,height=10,action=self.updateTraj,
                                    variable=self._dat,
                                    type="pullMenu",),#self.updateTraj},
                         "pdbtype":self._addElemt(name="Fecth",
                                    value=self.pdbtype,
                                    width=50,height=10,action=None,
                                    variable=self._pdbtype,
                                    type="pullMenu",),
                         "datatype":self._addElemt(name="DataTypes",
                                    value=self.datatype,
                                    width=20,height=10,action=None,
                                    variable=self.addVariable("int",1),
                                    type="pullMenu",),
                         "preset":self._addElemt(name="Preset",
                                    value=self.presettype,
                                    width=100,height=10,action=self.drawPreset,
                                    variable=self._preset,
                                    type="pullMenu",),#self.drawPreset},
                         "keyword":self._addElemt(name="Keyword",
                                    value=self.keyword,
                                    width=80,height=10,action=self.setKeywordSel,
                                    variable=self._keyword,
                                    type="pullMenu",),#self.setKeywordSel},
                         "scriptO":self._addElemt(name="ScriptO",
                                    value=self.scriptliste,
                                    width=80,height=10,action=self.set_ePMVScript,
                                    variable=self._eOscript,
                                    type="pullMenu",),#self.set_ePMVScript},
                         "scriptS":self._addElemt(name="ScriptS",
                                    value=self.scriptsave,
                                    width=80,height=10,action=None,
                                    variable=self._eSscript,
                                    type="pullMenu",),#self.save_ePMVScript},
                         "selection":self._addElemt(name="Selection",
                                    value=self.editselection,
                                    width=80,height=10,action=self.edit_Selection,
                                    variable=self._eSelection,
                                    type="pullMenu",),#elf.edit_Selection},
                         "bones":self._addElemt(name="Bones Level",
                                    value=self.boneslevel,
                                    width=80,height=10,action=None,
                                    variable=self._bonesLevel,
                                    type="pullMenu",),
                         "uv":self._addElemt(name="Mapping:",
                                    value=self.uvselection,
                                    width=200,height=10,action=None,
                                    variable=self._uvselection,
                                    type="pullMenu",),#elf.edit_Selection},
                        }
        deflt = "/Users/Shared/uv.png"
        self.uvid = self.addVariable("str",deflt)
        self.INPUTSTR={}
        self.INPUTSTR["uv"] = self._addElemt(name="image filename",action=None,width=120,
                          value=deflt,type="inputStr",variable=self.uvid)
        self.INPUTSTR["uvg"] = self._addElemt(name="geom",action=None,width=120,
                          value="MSMSMOL",type="inputStr",variable=self.uvid)


        deflt='(Mol:Ch:Rletter:Atom), eg "1CRN:A:ALA:CA", \
                or keywords: BACKBONE, SIDECHAINS, etc...'
        self.selid = self.addVariable("str",deflt)
        self.SELEDIT_TEXT = self._addElemt(name="selection",action=None,width=120,
                          value=deflt,type="inputStr",variable=self.selid)

        self.SEL_BTN ={"add":self._addElemt(name="Save set",width=45,height=10,
                         action=None,type="button"),#self.add_Selection},
                        "rename":self._addElemt(name="Rename",width=45,height=10,
                         action=None,type="button"),#self.rename_Selection},
                        "deleteS":self._addElemt(name="Delete Set",width=45,height=10,
                         action=None,type="button"),#self.delete_Selection},
                        "deleteA":self._addElemt(name="Delete",width=45,height=10,
                         action=self.delete_Atom_Selection,type="button"),#self.delete_Atom_Selection}    
                        }
        #do we need check button for other representation? ie lineMesh,cloudMesh etc..
        self.CHECKBOXS ={"cpk":self._addElemt(name="Atoms",width=80,height=10,
                                              action=self.dsCPK,type="checkbox",icon=None,
                                              variable=self.addVariable("int",0)),#self.displayCPK},
                         "bs":self._addElemt(name="Sticks",width=80,height=10,
                                             action=self.dsBS,type="checkbox",icon=None,
                                             variable=self.addVariable("int",0)),#self.displayBS},
                         "ss":self._addElemt(name="Ribbons",width=80,height=10,
                                             action=self.dsSS,type="checkbox",icon=None,
                                             variable=self.addVariable("int",0)),#self.displaySS},
                         "bead":self._addElemt(name="BeadedRibbons",width=80,height=10,
                                             action=self.dsBR,type="checkbox",icon=None,
                                             variable=self.addVariable("int",0)),#self.displaySS},
                         "loft":self._addElemt(name="Loft",width=80,height=10,
                                               action=self.dsLoft,type="checkbox",icon=None,
                                               variable=self.addVariable("int",0)),#self.createLoft},
                         "arm":self._addElemt(name="Armature",width=80,height=10,
                                             action=self.dsBones,type="checkbox",icon=None,
                                             variable=self.addVariable("int",0)),#self.createArmature},
                         "spline":self._addElemt(name="Spline",width=80,height=10,
                                             action=self.dsSpline,type="checkbox",icon=None,
                                             variable=self.addVariable("int",0)),#self.createSpline},
                         "surf":self._addElemt(name="MSMSurf",width=80,height=10,
                                               action=self.dsMSMS,type="checkbox",icon=None,
                                               variable=self.addVariable("int",0)),#self.displaySurf},
                         "cms":self._addElemt(name="CoarseMolSurf",width=80,height=10,
                                             action=self.dsCMS,type="checkbox",icon=None,
                                             variable=self.addVariable("int",0)),#self.displayCoarseMS},
                         "meta":self._addElemt(name="Metaballs",width=80,height=10,
                                             action=self.dsMeta,type="checkbox",icon=None,
                                             variable=self.addVariable("int",0)),#self.displayMetaB}
                         }
       
        #need a variable for each one
        #no label for theses
        #do we need slider button for other representation? ie metaball?/loft etc..
        self.SLIDERS = {"cpk":self._addElemt(name="cpk_scale",width=80,height=10,
                                             action=self.dsCPK,type="sliders",label="scale",
                                             variable=self.addVariable("float",1.0),
                                             mini=0.01,maxi=5.,step=0.01),#self.displayCPK},
                        "bs_s":self._addElemt(name="bs_scale",width=80,height=10,
                                             action=self.dsBS,type="sliders",label="scale",
                                             variable=self.addVariable("float",1.0),
                                             mini=0.0,maxi=10.,step=0.01),#self.displayBS},
                        "bs_r":self._addElemt(name="bs_ratio",width=80,height=10,
                                             action=self.dsBS,type="sliders",label="ratio",
                                             variable=self.addVariable("float",1.5),
                                             mini=0.0,maxi=10.,step=0.01),#self.displayBS},
                        "surf":self._addElemt(name="probe",width=80,height=10,
                                              action=self.updateMSMS,type="sliders",label="probe radius",
                                              variable=self.addVariable("float",1.5),
                                             mini=0.01,maxi=10.,step=0.01),#self.updateSurf},
                        "surfdensity":self._addElemt(name="density",width=80,height=10,
                                              action=self.updateMSMS,type="sliders",label="triangle density",
                                              variable=self.addVariable("float",3.0),
                                             mini=0.01,maxi=10.,step=0.01),#self.updateSurf},
                        "cmsI":self._addElemt(name="isovalue",width=80,height=10,
                                              action=self.updateCMS,type="sliders",label="isovalue",
                                              variable=self.addVariable("float",7.1),
                                             mini=0.01,maxi=10.,step=0.01),#self.updateCMS},
                        "cmsR":self._addElemt(name="resolution",width=80,height=10,
                                              action=self.updateCMS,type="sliders",label="resolution",
                                              variable=self.addVariable("float",-0.3),
                                             mini=-5.,maxi=0.,step=0.01),#self.updateCoarseMS},
                        "cmsG":self._addElemt(name="grid size",width=80,height=10,
                                              action=self.updateCMS,type="sliders",label="grid size",
                                              variable=self.addVariable("int",32),
                                             mini=1,maxi=100,step=1),#self.updateCoarseMS},                                             
                        #"meta":{"id":id+8,"name":"MBalls",'width':15,"height":10,"action":self.displayMetaB}
                        "datS":self._addElemt(name="state",width=100,height=10,
                                              action=self.applyState,type="sliders",label="step/value",
                                              variable=self.addVariable("float",0.),
                                             mini=-10.,maxi=10.,step=0.01),#self.applyState},
                        #"datV":{"id":id+7,"name":"value",'width':15,"height":10,"action":self.applyValue},                        
                        }
        #slider labels
        self.SLIDERS_LABEL={}
        for key in self.SLIDERS:
            if self.SLIDERS[key]["label"]:
                self.SLIDERS_LABEL[key]=self._addElemt(
                                                label=self.SLIDERS[key]["label"],
                                                width=50)
        self.COLFIELD = self._addElemt(name="chooseCol",action=self.color,
                                       variable = self.addVariable("col",(0.,0.,0.)),
                                       type="color",width=30,height=15)#self.chooseCol}
        

        txt="\n\nprint 'put your own commands here'\nprint 'with self = PMV instance, and epmv as ePMV'\n"
        self._script = self.addVariable("str",txt)
        self.SCRIPT_TEXT = self._addElemt(name="epmvScript",action=None,width=200,
                          value=txt,type="inputStrArea",variable=self._script,height=200)
        
        bannerfile = self.epmv.mglroot+os.sep+"MGLToolsPckgs"+os.sep+"ePMV"+\
                        os.sep+"images"+os.sep+"banner.jpg"
        self.BANNER = self._addElemt(name="banner",value=bannerfile,type="image")
        
        self.pd = ParameterModeller()
        self.pd.setup(self.epmv)
        self.options = Parameter_epmvGUI()
        self.options.setup(self.epmv)
        self.ad=ParameterScoringGui()   
        self.ad.setup(self.epmv)
        self.beadUi= Parameter_beadRibbons()
        self.beadUi.setup(self.epmv)
        self.apbsgui = APBSgui()
        self.apbsgui.setup(epmv=self.epmv)
        self.pmvPalgui = Parameter_pmvPalette()
        self.pmvPalgui.setup(epmv=self.epmv)
        #TODO
#        self.argui = ParameterARViewer()
#        self.argui.setup(self.epmv)

    def setupLayout(self):
        #epmv layout:
        #first is the Menu / last as in blender self.MENU_ID did by the adaptor
        #then is the pdb browse/fetch buttons
        #Load Molecule
        #line1  
        #need to reset the layout for restore purpose
        #collapse=False
        self._layout = []
        
        elemFrame=[]
        elemFrame.append([self.LOAD_BTN,self.LABEL_ID[0],self.LABEL_ID[1]])
        elemFrame.append([self.EDIT_TEXT,self.FETCH_BTN,self.COMB_BOX["pdbtype"]])
#        elemFrame.append([self.LABEL_ID[2],self.COMB_BOX["mol"]])
        
        frame = self._addLayout(id=196,name="Get a Molecule",elems=elemFrame,collapse=False)
        self._layout.append(frame)
       
        #
#        self._layout.append([self.LOAD_BTN,self.LABEL_ID[0],self.LABEL_ID[1]])
        #line2
#        self._layout.append([self.EDIT_TEXT,self.COMB_BOX["pdbtype"],self.FETCH_BTN])        
        #line3
#        self._layout.append([self.LABEL_ID[2],self.COMB_BOX["mol"]])
        #DashBoard / Selection Display Options 
        elemFrame=[]
        elemFrame.append([self.LABEL_ID[2],self.COMB_BOX["mol"]])        
        elemFrame.append([self.LABEL_ID[3],self.COMB_BOX["keyword"],])
        elemFrame.append([self.SELEDIT_TEXT,self.COMB_BOX["selection"]])
        elemFrame.append([self.SEL_BTN["deleteA"],self.LABEL_ID[11]])
        frame = self._addLayout(id=197,name="Selections",elems=elemFrame,collapse=False)
        self._layout.append(frame)
        
#        #line4
#        self._layout.append([self.LABEL_ID[3],self.COMB_BOX["keyword"]])
#        #line5
#        self._layout.append([self.SELEDIT_TEXT,self.COMB_BOX["selection"]])
#        #line6
#        self._layout.append([self.SEL_BTN["deleteA"],self.LABEL_ID[11]])
        #line7
        #should add a separration here
        elemFrame=[]
        elemFrame.append([self.LABEL_ID[8],self.COMB_BOX["preset"]])
        frame = self._addLayout(id=198,name="Preset Representations",elems=elemFrame)
        self._layout.append(frame)
        
        #self._layout.append([self.LABEL_ID[8],self.COMB_BOX["preset"]])
        #line8 // Visual represnetation option CPK, MSMS etc...checkbox!
        #self._layout.append([self.LABEL_ID[8],self.COMB_BOX["preset"]])
        #form layout
        elemFrame=[]
        elemFrame.append([self.CHECKBOXS["cpk"],])
        elemFrame.append([self.SLIDERS_LABEL["cpk"],
                          self.SLIDERS["cpk"],])
        frame = self._addLayout(id=200,name="Atom Spacefill",elems=elemFrame,collapse=False)
        self._layout.append(frame)

        elemFrame=[]
        elemFrame.append([self.CHECKBOXS["bs"],])
        elemFrame.append([self.SLIDERS_LABEL["bs_s"],self.SLIDERS["bs_s"],])
        elemFrame.append([self.SLIDERS_LABEL["bs_r"],self.SLIDERS["bs_r"],])
        frame = self._addLayout(id=201,name="Atom Stick and Balls",elems=elemFrame)
        self._layout.append(frame)

        elemFrame=[]
        elemFrame.append([self.CHECKBOXS["ss"],])
        elemFrame.append([self.CHECKBOXS["bead"],self.BTN["bead"]])
        elemFrame.append([self.CHECKBOXS["arm"],self.COMB_BOX["bones"]])
        elemFrame.append([self.CHECKBOXS["loft"],])
        elemFrame.append([self.CHECKBOXS["spline"],])
        frame = self._addLayout(id=202,name="Backbone Representations",elems=elemFrame)
        self._layout.append(frame)

        
        
        
        elemFrame=[]
        elemFrame.append([self.CHECKBOXS["surf"],])
        elemFrame.append([self.SLIDERS_LABEL["surf"],self.SLIDERS["surf"],])
        elemFrame.append([self.SLIDERS_LABEL["surfdensity"],self.SLIDERS["surfdensity"],])
        elemFrame.append([self.CHECKBOXS["cms"],])
        elemFrame.append([self.SLIDERS_LABEL["cmsI"],self.SLIDERS["cmsI"],])
        elemFrame.append([self.SLIDERS_LABEL["cmsR"],self.SLIDERS["cmsR"],])
        elemFrame.append([self.SLIDERS_LABEL["cmsG"],self.SLIDERS["cmsG"],]) 
        elemFrame.append([self.CHECKBOXS["meta"],])
        frame = self._addLayout(id=203,name="Surface Representations",elems=elemFrame)
        self._layout.append(frame)

#        repLayout={ "0": [3,5],
#                    "1":[self.CHECKBOXS["cpk"],self.CHECKBOXS["ss"],self.CHECKBOXS["surf"]],
#                    "2":[self.SLIDERS["cpk"],self.CHECKBOXS["loft"],self.SLIDERS["surf"]],
#                    "3":[self.CHECKBOXS["bs"],self.CHECKBOXS["arm"],self.CHECKBOXS["cms"]],
#                    "4":[self.SLIDERS["bs_s"],self.CHECKBOXS["spline"],self.SLIDERS["cmsI"]],
#                    "5":[self.SLIDERS["bs_r"],self.CHECKBOXS["meta"],self.SLIDERS["cmsR"]],
#                    "6":[self.LABEL_ID[1],self.LABEL_ID[1],self.SLIDERS["cmsG"]]
#                    }
#        self._layout.append(repLayout)
        #line9#color what is check as display
        elemFrame=[]
        elemFrame.append([self.LABEL_ID[4],self.COMB_BOX["col"],])
        elemFrame.append([self.LABEL_ID[15],self.COLFIELD])
        frame = self._addLayout(id=204,name="Color By",elems=elemFrame)
        self._layout.append(frame)

        #lineUV -> will go in the options menu. as vertex colors to UV textur mapping (slow)
        elemFrame=[]
        elemFrame.append([self.LABEL["uv1"],self.INPUTSTR["uvg"]])#combo box OR Input
        elemFrame.append([self.LABEL["uv2"],self.COMB_BOX["uv"]])
        elemFrame.append([self.BTN["uv"],self.INPUTSTR["uv"] ])
        frame = self._addLayout(id=205,name="UV Texture mapping",elems=elemFrame)
        self._layout.append(frame)

#        self._layout.append([self.LABEL_ID[4],self.COMB_BOX["col"],self.COLFIELD])
        #line10#data player
        elemFrame=[]
        elemFrame.append([self.DATA_BTN,self.LABEL_ID[5],self.COMB_BOX["datatype"]])
        elemFrame.append([self.LABEL_ID[9],self.COMB_BOX["dat"],self.LABEL_ID[6]])
        elemFrame.append([self.SLIDERS_LABEL["datS"],self.SLIDERS["datS"]])
        frame = self._addLayout(id=206,name="Data Player",elems=elemFrame)    
        self._layout.append(frame)
#        self._layout.append([self.DATA_BTN,self.LABEL_ID[5],self.COMB_BOX["datatype"]])
#        self._layout.append([self.LABEL_ID[9],self.COMB_BOX["dat"],self.LABEL_ID[6]])
#        self._layout.append([self.SLIDERS["datS"],])
        #line10#script editor
        elemFrame=[]
        elemFrame.append([self.COMB_BOX["scriptO"],self.COMB_BOX["scriptS"]])
        elemFrame.append([self.SCRIPT_TEXT,])
        elemFrame.append([self.PMV_BTN,])
        frame = self._addLayout(id=207,name=self.LABEL_ID[7]["label"],elems=elemFrame)    
        self._layout.append(frame)
#        self._layout.append([self.LABEL_ID[7],self.COMB_BOX["scriptO"],self.COMB_BOX["scriptS"]])
#        self._layout.append([self.SCRIPT_TEXT,])        
#        self._layout.append([self.PMV_BTN,])
        #Version
        self._layout.append([self.LABEL_VERSION,])
        #Banner if we can
        self._layout.append([self.BANNER,])

    def setupLayoutOLD(self):
        #epmv layout:
        #first is the Menu / last as in blender self.MENU_ID did by the adaptor
        #then is the pdb browse/fetch buttons
        #Load Molecule
        #line1  
        #need to reset the layout for restore purpose
        self._layout = []
        self._layout.append([self.LOAD_BTN,self.LABEL_ID[0],self.LABEL_ID[1]])
        #line2
        self._layout.append([self.EDIT_TEXT,self.COMB_BOX["pdbtype"],self.FETCH_BTN])        
        #line3
        self._layout.append([self.LABEL_ID[2],self.COMB_BOX["mol"]])
        #DashBoard / Selection Display Options 
        #line4
        self._layout.append([self.LABEL_ID[3],self.COMB_BOX["keyword"]])
        #line5
        self._layout.append([self.SELEDIT_TEXT,self.COMB_BOX["selection"]])
        #line6
        self._layout.append([self.SEL_BTN["deleteA"],self.LABEL_ID[11]])
        #line7
        self._layout.append([self.LABEL_ID[8],self.COMB_BOX["preset"]])
        #line8 // Visual represnetation option CPK, MSMS etc...checkbox!
#        self._layout.append([self.LABEL_ID[8],self.COMB_BOX["preset"]])
        repLayout={ "0": [3,6],
                    "1":[self.CHECKBOXS["cpk"],self.CHECKBOXS["ss"],self.CHECKBOXS["surf"]],
                    "2":[self.SLIDERS["cpk"],self.CHECKBOXS["loft"],self.SLIDERS["surf"]],
                    "3":[self.CHECKBOXS["bs"],self.CHECKBOXS["arm"],self.CHECKBOXS["cms"]],
                    "4":[self.SLIDERS["bs_s"],self.CHECKBOXS["spline"],self.SLIDERS["cmsI"]],
                    "5":[self.SLIDERS["bs_r"],self.CHECKBOXS["meta"],self.SLIDERS["cmsR"]],
                    "6":[self.LABEL_ID[1],self.LABEL_ID[1],self.SLIDERS["cmsG"]]
                    }
        self._layout.append(repLayout)
        #line9#color what is check as display     
        self._layout.append([self.LABEL_ID[4],self.COMB_BOX["col"],self.COLFIELD])
        #line10#data player
        self._layout.append([self.DATA_BTN,self.LABEL_ID[5],self.COMB_BOX["datatype"]])
        self._layout.append([self.LABEL_ID[9],self.COMB_BOX["dat"],self.LABEL_ID[6]])
        self._layout.append([self.SLIDERS["datS"],])
        #line10#script editor
        self._layout.append([self.LABEL_ID[7],self.COMB_BOX["scriptO"],self.COMB_BOX["scriptS"]])
        self._layout.append([self.SCRIPT_TEXT,])        
        self._layout.append([self.PMV_BTN,])
        #Version
        self._layout.append([self.LABEL_VERSION,])
        #Banner if we can
        self._layout.append([self.BANNER,])

    
    def getGeomActive(self,name):
        lgeomName=[]
        mname,mol,sel,selection = self.getDsInfo()
        #lookup moldisp
        for key in self.CHECKBOXS:
            if self.getBool(self.CHECKBOXS[key]):
                if key == "bs" : 
                    lgeomName.append('balls')
                    lgeomName.append('sticks')
                elif key == "ss":
                    lgeomName.append('secondarystructure')
                elif key == "cms":
                    sname='CoarseMS_'+str(mname)
                    lgeomName.append(sname)   
                elif key == "surf":
                    sname='MSMS-MOL'+str(mname)
#                    if sel != mname :
#                        sname='MSMS-MOL'+str(sel) 
                    lgeomName.append(sname)
                elif key == "col":
                    continue
                else :
                    lgeomName.append(key)
        return lgeomName

    def getData(self,molname,adt=False):
#        if molname in self.mv.Mols.name : self.mv.hostApp.driver.duplicatemol=False
        self.mv.assignAtomsRadii(str(molname), united=0, log=0, overwrite=1)
        self.epmv._addMolecule(molname)
        #add a child to mol pop up menu which is the current selection puulDowmn menu
        
        self.addItemToPMenu(self.COMB_BOX["mol"],str(molname))
        mol = self.mv.getMolFromName(molname)
        if len(mol.allAtoms[0]._coords) > 1 or self.epmv.useModeller : 
            #need a test about trajectories...
            doit=True           
            if len(self.mv.iMolData[mol.name]) != 0 : #ok data
                for dataname in self.mv.iMolData[mol.name] : 
                    if dataname.find('xtc') != -1 : 
                        doit= False                             
            if doit : self.loadDATA(None,model=True,molname=molname,adt=adt)
        self.current_mol = mol

    def loadPDB(self,filename):
        if not filename : return
        molname=os.path.splitext(os.path.basename(filename))[0]
#        print molname
        #test the name lenght
        if len(molname) > self.epmv.MAX_LENGTH_NAME :
            self.drawError("Sorry, but the name of the given file is to long,\nand not suppported by Blender.\n Please rename it or load another file")
            return 0
#        if VERBOSE :print molname, self.Mols.name, (molname in self.Mols.name)
        name=filename
        adt=False
        ext = os.path.splitext(os.path.basename(name))[1]
#        print ext
        if ext == '.dlg' :#Autodock
            self.epmv.center_mol = False
            self.mv.readDLG(name,1,0) #addToPrevious,ask
            self.mv.showDLGstates(self.mv.Mols[-1])
            molname = self.mv.Mols[-1].name
            adt=True
#        if molname in self.mv.Mols.name : 
#            self.hostApp.driver.duplicatemol=True
#            if VERBOSE :print self.hostApp.driver.duplicatemol
        if self.epmv.useModeller and not adt :
            import modeller
            from modeller.scripts import complete_pdb
            mdl = complete_pdb(self.epmv.env, name)
            mdl.patch_ss()
            name = name.split(".pdb")[0]+"m.pdb"
            mdl.write(file=name)
        if not adt :
            self.mv.readMolecule(str(name))
            if self.epmv.useModeller :
                self.mv.Mols[-1].mdl=mdl
        molname = self.mv.Mols[-1].name
        molname=molname.replace(".","_")

        self.mv.Mols[-1].name=molname

#        if len(molname) > 7 : 
#            self.mv.Mols[-1].name=molname[0:6]
#            molname = self.mv.Mols[-1].name
#        self.epmv.testNumberOfAtoms(self.mv.Mols[-1])
        self.getData(self.mv.Mols[-1].name)
        self.updateViewer()

    def loadRecentFile(self,*args):
#        print "RF ",args, len(args)
        if len(args) == 1:
            if type(args[0]) is tuple :
                id = args[0][0] 
            else :
                id = args[0]
        elif len(args) == 2:
            if type(args[0]) is str :
                id = args[0]
            else :
                id = args[0][0]
        if self.submenu is not None :
            filename = self.submenu[str(id)]["name"]
            self.loadPDB(filename)

    def browsePDB(self,*args):
        #first need to call the ui fileDialog
        self.fileDialog(label="choose a file",callback=self.loadPDB)
        
    def fetchPDB(self,*args):
#        print args
        #get the text area    
        name = self.getString(self.EDIT_TEXT)
        #need to get the fetch Type
        type = self.pdbtype[self.getLong(self.COMB_BOX["pdbtype"])]
        if len(name) == 4 or len(name.split(".")[0]) == 4 :
#            print "PDB id, webdownload"
            molname=name.lower()
#                if molname in self.mv.Mols.name : self.mv.hostApp.driver.duplicatemol=True
            self.mv.fetch.db = type
            print self.epmv.forceFetch
            mol = self.mv.fetch(molname,f=self.epmv.forceFetch)           
            print "fetch ",mol
            if mol is None :
                return True
            self.epmv.testNumberOfAtoms(mol)
            self.getData(self.mv.Mols[-1].name)
            self.updateViewer()
        else :
            print "enter a Valid "+type+" id Code "
            
    def loadDATA(self,filename,model=False,trajname=None,molname=None,adt=False):
        if trajname == None :
            if model : 
                self.modelData(adt=adt)
                return True
            #filename=self.GetString(self.trajectoryfile)
            #if len(filename) == 0 :
            if filename is None :
                    return True
            dataname=os.path.splitext(os.path.basename(filename))[0]
            extension=os.path.splitext(os.path.basename(filename))[1] #.xtc,.trj,etc..
            if extension == '.xtc' or extension == '.dcd'  : self.gromacsTraj(file=filename)
            else : self.gridData(file=filename)
            #elif extension == '.map' : self.gridData_1(file=filename)
        else :
           print "restore ",trajname      
           if trajname.find(".model") != -1 or trajname.find(".dlg") != -1: #model conformation data
               self.modelData(dataname=trajname,molname=molname)          
           elif trajname.find("xtc") != -1 : #gromacs conformation data
               self.gromacsTraj(dataname=trajname,molname=molname)          
           else : #autodock map conformation data
               self.gridData(dataname=trajname,molname=molname)          
        #elif extension == '.trj' : self.amberTraj(filename)
        self.updateViewer()
        return True

    def browseDATA(self,*args):
        #first need to call the ui fileDialog
        self.fileDialog(label="choose a data file",callback=self.loadDATA)

    def modelData(self,dataname=None,molname=None,adt=False):
        if molname == None :
            val = self.getLong(self.COMB_BOX["mol"])
            vname = self.COMB_BOX["mol"]["value"][val]
            mname,mol=self.epmv.getMolName(vname)
            trajname = mname+'.model'
            if adt:
                trajname = mname+'.dlg'
            self.mv.iMolData[mname].append(trajname)
        else :
            mname = molname
            trajname = dataname                         
        self.addItemToPMenu(self.COMB_BOX["dat"],trajname)
        self.mv.iTraj[len(self.COMB_BOX["dat"]["value"])-1]=[trajname,"model"]
        self.current_traj=[trajname,"model"]

    def gromacsTraj(self,file=None,dataname=None,molname=None):
        if molname == None :
            self.mv.openTrajectory(file, log=0)
            trajname=os.path.basename(file)
            #print trajname
            val = self.getLong(self.COMB_BOX["mol"])
            vname = self.COMB_BOX["mol"]["value"][val]
            mname,mol=self.epmv.getMolName(vname) 
            self.mv.iMolData[mname].append(trajname)
            self.mv.playTrajectory(mname, trajname, log=0)
        else :
            mname = molname
            trajname = dataname
        self.addItemToPMenu(self.COMB_BOX["dat"],trajname)
        self.mv.iTraj[len(self.COMB_BOX["dat"]["value"])-1]=[self.mv.Trajectories[trajname],"traj"]
        self.current_traj=[self.mv.Trajectories[trajname],"traj"]
        self.nF=len(self.current_traj[0].coords)
            
    def gridData(self,file=None,dataname=None,molname=None):
        if molname == None :
            self.mv.readAny(file)
#            sys.stderr.write('DObe')
            name = self.mv.grids3D.keys()[-1] #the last read data
            val = self.getLong(self.COMB_BOX["mol"])
            vname = self.COMB_BOX["mol"]["value"][val]
            print val,vname,self.COMB_BOX["mol"]["value"]
            mname,mol=self.epmv.getMolName(vname) 
            self.mv.cmol = mol
#            sys.stderr.write('before Select and isoContour')            
            self.mv.isoC.select(grid_name=name)		   
            self.mv.isoC(self.mv.grids3D[name],name=mname+"IsoSurface",
                        isovalue=0.)#self.mv.grids3D[name].mean)  
            trajname=name#os.path.basename(filename)
            self.setReal(self.SLIDERS["datS"],0.)
            #print trajname
            if mname == "" and "IsoSurface" not in self.mv.iMolData.keys():
                self.mv.iMolData["IsoSurface"]=[]
                mname = "IsoSurface"
            self.mv.iMolData[mname].append(file)
        else :
            mname = molname
            trajname = dataname
        #self.mv.playTrajectory(mname, trajname, log=0)
        self.addItemToPMenu(self.COMB_BOX["dat"],os.path.basename(trajname))
        self.current_traj = self.mv.iTraj[len(self.COMB_BOX["dat"]["value"])-1]=[self.mv.grids3D[trajname],"grid"]
        self.nF=self.current_traj[0].maxi

    def updateTraj(self,*args):
        i = self.getLong(self.COMB_BOX["dat"])
        if i not in self.mv.iTraj.keys():
            return False
        self.current_traj = self.mv.iTraj[i]
        mini,maxi,default,step = self.epmv.updateTraj(self.current_traj)
        print mini,maxi,default,step
        self.updateSlider(self.SLIDERS["datS"],mini,maxi,default,step)
        return True
        
    def applyState(self,*args):
        #frame=self.GetLong(self.slider)
        mname,mol,sel,selection = self.getDsInfo()
        traj = self.current_traj
        disp = self.mv.molDispl[mname]
        if traj is not None : 
            if traj[1] in ["model" ,"traj"]:
                conf = self.getReal(self.SLIDERS["datS"])
                self.epmv.updateData(traj,int(conf))
                if disp.has_key("surf"):
                    if disp["surf"] : self.updateMSMS(None) #shoudl I redo the coloring?
                if disp.has_key("cms") :
                    if disp["cms"] : self.updateCMS(None)
                self.color(None)
            elif self.current_traj[1] == "grid":
                iso=self.getReal(self.SLIDERS["datS"])#isovalue
                self.mv.isoC(self.current_traj[0],isovalue=iso,name=mname+"IsoSurface")       
            elif hasattr(self.current_traj,'GRID_DATA_FILE'):
                #grid
                iso=self.getReal(self.SLIDERS["datS"])#isoself.GetReal(self.slider)
                self.mv.setIsovalue(self.current_traj[0].name,iso, log = 1)          
        self.updateViewer()
        #return True

    def getDsInfo(self,key=None):
        val = self.getLong(self.COMB_BOX["mol"])
        try :
            name = self.COMB_BOX["mol"]["value"][val]
        except :
            return None,None,None,None
        if name is None :
            return None,None,None,None
        if name not in self.mv.selections.keys(): 
            mol = self.getSelectionMol(name)
            mname = mol.name
            sel = self.mv.selections[mname][name]
            selection = self.mv.select(str(sel),
                                       negate=False, only=True, xor=False, 
                                       log=0, intersect=False)
            if key is not None :
#                print "ok key ",key
                if key != "col" :
                    display = self.getBool(self.CHECKBOXS[key])
                    self.updateMolDsDict(sel,name,display,key)
                else :
                    display = self.getColor(self.COLFIELD)
                return name,mol,sel,selection,display
            return name,mol,sel,selection
        mname,mol=self.epmv.getMolName(name) #just in case name is a selection..
        print mname,mol
        selString=self.getString(self.SELEDIT_TEXT)
        sel,selection=self.epmv.getSelectionLevel(mol,selString)
        if key is not None :
#            print "ok key ",key
            if key != "col" :
                display = self.getBool(self.CHECKBOXS[key])
#                print display,self.CHECKBOXS[key]["id"]
                self.updateMolDsDict(sel,mname,display,key)
            else :
                display = self.getColor(self.COLFIELD)
            return mname,mol,sel,selection,display
        return mname,mol,sel,selection

    def setCurMol(self,*args):  
        mname,mol,sel,selection = self.getDsInfo()
        if mol == None : 
            return  
        #restore display option
        doDisplay=False
        for k in self.CHECKBOXS:
#            print k,self.CHECKBOXS[k],self.CHECKBOXS[k]["id"]
            self.setBool(self.CHECKBOXS[k],self.mv.molDispl[mname][k])
            if self.mv.molDispl[mname][k] :
                doDisplay=True
#        #restore color option
        color = self.mv.molDispl[mname]["col"]
        if type(color) is int : #functId
            self.setLong(self.COMB_BOX["col"],color)
        elif color is None :
            pass
        else :
            self.setColor(self.COLFIELD,color)
        if mname not in self.mv.Mols.name:
           #selection
           self.setString(self.SELEDIT_TEXT,self.mv.MolSelection[mol.name][mname])
           
        else : 
           self.setString(self.SELEDIT_TEXT,"")
           #if True in self.molDispl[mname]: self.doDisplaySelection(self.molDispl[mname],private)"""
        #print "update"
        #should apply the ds...or not ? lets try
        self.current_mol = mol
        if doDisplay : 
            self.doDisplay(self.mv.molDispl[mname])
        self.updateViewer()
        return True

    def updateMolDsDict(self,sel,mname,display,key):
#        if sel == mname :
#            self.mv.molDispl[mname][key]= display
#        else :
#            self.mv.molDispl[mname][key] = False
        self.mv.molDispl[mname][key]= display
        
    def getSelectionMol(self,selname):
        for mol in self.mv.Mols:
            for molselname in self.mv.MolSelection[mol.name]:
                if molselname == selname :
                    return mol
        return None

    def edit_Selection(self,*args):
        edit = self.getLong(self.COMB_BOX['selection'])
        if edit == 0 : #add selection
            self.add_Selection()
        elif edit == 1 : #rename
            self.rename_Selection()
        elif edit == 2 : #delete
            self.delete_Selection()

    def delete_Selection(self):
        val = self.getLong(self.COMB_BOX["mol"])
        name = self.COMB_BOX["mol"]["value"][val]
        #name should be the current selection name if not return
        mol = self.getSelectionMol(name)
        if mol is None :
            return
        mname = mol.name
        selname = name
        question = "Are You sure you want to delete the current selection "+selname+" of molecule "+mname+"?"
        res = self.drawQuestion("delete Selection",question=question)
        if res :
            del self.mv.MolSelection[mname][selname]
            del self.mv.selections[mname][selname]
            del self.mv.molDispl[selname]
            self.resetPMenu(self.COMB_BOX["mol"])   
            self.restoreMolMenu()

    def rename_Selection(self):
        #whats the new name
        newname=self.drawInputQuestion(title="rename current selection",
                                       question="Give the new name",callback=None)
        val = self.getLong(self.COMB_BOX["mol"])
        name = self.COMB_BOX["mol"]["value"][val]
        #name should be the current selection name if not return
        mol = self.getSelectionMol(name)
        if mol is None :
            return
        mname = mol.name
        selname = name
        #change the name in dic of indice
        #change the name in the mol dictionary of selection
        sel = self.mv.MolSelection[mname][selname]
        dsDic = self.mv.molDispl[selname]
        del self.mv.MolSelection[mname][selname]
        del self.mv.selections[mname][selname]
        del self.mv.molDispl[selname]
        self.mv.MolSelection[mname][newname]=sel
        self.mv.selections[mname][newname]=sel
        self.mv.molDispl[newname]=dsDic
        self.resetPMenu(self.COMB_BOX["mol"])   
        self.restoreMolMenu()

    def add_Selection(self,n=None):
        newSelection = True
        print "add_selection"
        if n is not None:
            #restore mode
            for selname in self.mv.MolSelection[n].keys():
                self.addItemToPMenu(self.COMB_BOX["mol"],str(selname))
#                self.mv.selections[n][str(selname)]=self.mv.MolSelection[n]
            return True
        mname,mol,sel,selection = self.getDsInfo()        
        print "mname ",mname
        print "sel ",sel
        if mname not in self.mv.selections:
            selname = mname
            newSelection = False
        else :
            selname=mol.name+"_Selection"+str(len(self.mv.MolSelection[mol.name]))
        print "selname ", selname
        print self.mv.MolSelection[mol.name]
        self.mv.MolSelection[mol.name][selname]=sel
        self.mv.selections[mol.name][selname]=sel
        self.mv.molDispl[selname]={}
        for k in ["cpk","bs","ss","loft","arm","spline","surf","cms","meta"]:
            self.mv.molDispl[selname][k]=False
        self.mv.molDispl[selname]=self.mv.molDispl[mol.name].copy()
        for k in ["cpk","bs","ss","loft","arm","spline","surf","cms","meta"]:
            self.mv.molDispl[mol.name][k]=False
#        for k in self.CHECKBOXS:
#            self.mv.molDispl[selname][k]=self.getBool(self.CHECKBOXS[k])
        funcId = self.getLong(self.COMB_BOX["col"])
        self.mv.molDispl[selname]["col"]= funcId
        if funcId == 6 : 
            #custom color                
            color = self.getColor(self.COLFIELD)
            self.mv.molDispl[selname]["col"]=color
        if newSelection :
            self.addItemToPMenu(self.COMB_BOX["mol"],str(selname))
        print self.mv.molDispl[selname]
        #print str(self.indice_mol+self.indice)       
        return True

    def getSelectionName(self,sel,mol):
        for selname in self.mv.MolSelection[mol.name].keys() : 
            if sel == self.mv.MolSelection[mol.name][selname] : 
                return selname           
        return mol.name+"_Selection"+str(len(self.mv.MolSelection[mol.name]))

    def restoreMolMenu(self):
        #call this after flushing the combo box
        print self.mv.Mols
        for mol in self.mv.Mols:
            self.addItemToPMenu(self.COMB_BOX["mol"],str(mol.name))
            if self.mv.selections.has_key(mol.name) :
                for selname in self.mv.selections[mol.name].keys():
                    self.addItemToPMenu(self.COMB_BOX["mol"],str(selname))
                        
    def setKeywordSel(self):
        key=self.keyword[self.GetLong(self._keywordtype)]
        if key == 'keywords' : key = ""
        self.SetString(self.selection,key.replace(" ",""))

    def delete_Atom_Selection(self,*args):
        #self.mv.deleteAtomSet...
        mname,mol,sel,selection = self.getDsInfo()
        if sel is mol.name :
#            print sel,mname, mol , "del"
            res = self.drawQuestion("Delete?","Are You sure you want to delete "+mol.name)
            print res
            if res : 
                self.epmv._deleteMolecule(mol)
                #need to update the current_sel menu
                self.resetPMenu(self.COMB_BOX["mol"])   
                self.restoreMolMenu()
        else :
            res = self.drawQuestion("Delete?","Are You sure you want to delete the atoms of the current selection "+sel)
            if res : 
                self.mv.deleteAtomSet(selection)

    def doDisplay(self,disArray):
        if disArray["cpk"] : self.dsCPK()  
        if disArray["bs"] : self.dsBS()
        if disArray["ss"] : self.dsSS()
        if disArray["loft"] : self.dsLoft()
        if disArray["spline"] : self.dsSpline()        
        if disArray["surf"] : self.dsMSMS()
        if disArray["cms"] : self.dsCMS()
        if disArray["meta"] : self.dsMeta()        
        if disArray["arm"] : self.dsBones()
        if disArray["col"] != None : self.color()       

    def dsCPK(self,*args):
        print args
        mname,mol,sel,selection,display = self.getDsInfo("cpk")
        if mol is None:
            return
        scale = self.getReal(self.SLIDERS["cpk"])  
        #should do some dialog here
        #and what about the progress bar
        if not mol.doCPK:
            mol.doCPK = True#drawQuestion("Are You sure you want \nto display the CPK ("+str(len(mol.allAtoms))+" atoms) ","CPK")
        if mol.doCPK:
            self.mv.displayCPK(sel,log=0,negate=(not display),
                        scaleFactor=scale, redraw =0)#redraw?
        #funcColor[ColorPreset2.val-1](molname, [name], log=1)
#        self.updateViewer()
        return True        

    def dsBS(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("bs")
        if mol is None:
            return        
        ratio = self.getReal(self.SLIDERS["bs_r"])
        scale = self.getReal(self.SLIDERS["bs_s"])
        bRad = 0.3
        cradius = float(bRad/ratio)*scale
        if not mol.doCPK:
            print mol.doCPK
            mol.doCPK = self.drawQuestion("Are You sure you want \nto display the BallSticks for "+str(len(mol.allAtoms))+" atoms","Balls and Sticks")
        if mol.doCPK:
            self.mv.displaySticksAndBalls(sel, bRad=0.3*scale, 
                                   cradius =cradius, bScale=0., 
                                   negate=(not bool(display)),
                                   only=False, bquality=0, 
                                   cquality=0) 
        return True  
    
    def dsSS(self,*args):        
        mname,mol,sel,selection,display = self.getDsInfo("ss")
        if mol is None:
            return
        #this command rewrite the exElemt
        #self.mv.extrudeSecondaryStructure(sel, topCommand=0, log=0, display=0)
        self.mv.displayExtrudedSS(sel, negate=(not bool(display)), only=False)
        return True

    def drawBeadOption(self,*args):  
        self.drawSubDialog(self.beadUi,2555558)

    def dsBR(self,*args):        
        mname,mol,sel,selection,display = self.getDsInfo("bead")
        if mol is None:
            return        
        if display :
            #open the display option menu
            self.mv.beadedRibbons(sel,createEvents=False)
            self.drawBeadOption(None)
        #else :
        #    #selection?
        for ch in mol.chains :
            obj = self.epmv.helper.getObject(mol.name+ch.name+"_beadedRibbon")
            self.epmv.helper.toggleDisplay(obj,display)
        return True  

    def dsCMS(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("cms")
        if mol is None:
            return        
        name='CoarseMS_'+mname
        parent=mol.geomContainer.masterGeom.obj 
        iso = self.getReal(self.SLIDERS["cmsI"])
        res = self.getReal(self.SLIDERS["cmsR"])
        gridsize = self.getLong(self.SLIDERS["cmsG"])
        print iso,res,gridsize
        if name not in mol.geomContainer.geoms :
            geom=self.epmv.coarseMolSurface(mol,[gridsize,gridsize,gridsize],
                                        isovalue=iso,resolution=res,
                                        name=name)
            mol.geomContainer.geoms[name]=geom
            obj=self.epmv.helper.createsNmesh(name,geom.getVertices(),None,
                                          geom.getFaces(),smooth=True)
            self.epmv._addObjToGeom(obj,geom)
            self.epmv.helper.addObjectToScene(self.epmv.helper.getCurrentScene(),
                                          obj[0],parent=parent)
            self.mv.colorByAtomType(mname, [name], log=0)
            obj=obj[0]
        else :
            obj = mol.geomContainer.geoms[name].obj
        self.epmv.helper.toggleDisplay(obj,display)
        return True

    def updateCMS(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("cms")
        if mol is None : 
            return
        name='CoarseMS_'+mname
        if display and name in mol.geomContainer.geoms.keys():
            parent=mol.geomContainer.masterGeom.obj 
            iso = self.getReal(self.SLIDERS["cmsI"])
            res = self.getReal(self.SLIDERS["cmsR"]) 
            gridsize = self.getLong(self.SLIDERS["cmsG"])           
            #isovalue=7.1#float(cmsopt['iso'].val),
            #resolution=-0.3#float(cmsopt['res'].val)
            g = self.epmv.coarseMolSurface(selection,[gridsize,gridsize,gridsize],
                                      isovalue=iso,
                                      resolution=res,
                                      name=name,
                                      geom = mol.geomContainer.geoms[name])
            self.epmv.helper.updateMesh(g.mesh,vertices=g.getVertices(),
                                          faces=g.getFaces())
        return True
    
    def dsMSMS(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("surf")
        if mol is None : 
            return
        name='MSMS-MOL'+mname
        pradius=self.getReal(self.SLIDERS["surf"])
        density=self.getReal(self.SLIDERS["surfdensity"])
        if name in mol.geomContainer.geoms :
            try:
                self.mv.displayMSMS(sel, negate=(not bool(display)), 
                            only=False, surfName=name, nbVert=1)
            except :
                self.drawError("MSMS ERROR!")
        else :
            self.mv.computeMSMS(sel, display=(bool(display)), 
                             surfName=name,perMol=0,
                             pRadius=pradius,density = density)
        #funcColor[ColorPreset2.val-1](molname, [name], log=1)
        return True
        
    def updateMSMS(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("surf")
        if mol is None : 
            return        
        name='MSMS-MOL'+mname
        pradius=self.getReal(self.SLIDERS["surf"])
        density=self.getReal(self.SLIDERS["surfdensity"])
        if display and name in mol.geomContainer.geoms: 
            self.mv.computeMSMS(sel,#hdensity=msmsopt['hdensity'].val, 
                                     hdset=None, 
                                     density=density, 
                                     pRadius=pradius, 
                                     perMol=0, display=True, 
                                     surfName=name)
        return True

    def dsLoft(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("loft")
        i=self.getLong(self.COMB_BOX["bones"])
        if mol is None : 
            return        
        for c in mol.chains :
            name="loft"+mol.name+"_"+c.name
            loft = self.epmv.helper.getObject(name)
            if c.ribbonType()=='NA':
                laders = self.epmv.helper.getObject("loft"+mol.name+c.name+"_lader")
            if loft is None :
                #self.getAtomsSelection(self.boneslevel[i],sel,selection,mol,chain=c)
                if c.ribbonType()=='NA':
                    lsel = c.residues.atoms.get("O5'").coords
                else :
                    lsel = c.residues.atoms.get("CA").coords
                parent = mol.geomContainer.masterGeom.chains_obj[c.name]
                #parent = mol.geomContainer.masterGeom.obj
                loft = self.epmv._makeRibbon(name,lsel,parent=parent)               
                #waht about the lader
                if c.ribbonType()=='NA':
                    #make the ladder
                    laders=self.epmv.NAlader("loft",mol,c,parent = parent)[0]               
            self.epmv.helper.toggleDisplay(loft,display)
            if c.ribbonType()=='NA':
                #this doesnt work in blender
                if laders is not None :
                    self.epmv.helper.toggleDisplay(laders,display)
        return True
    
    def dsSpline(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("spline")
        i=self.getLong(self.COMB_BOX["bones"])
        if mol is None : 
            return        
        for c in mol.chains :
            name=mol.name+"_"+c.name+"spline"#'spline'+mol.name #
            obSpline=self.epmv.helper.getObject(name)
            if obSpline is None:
                #lsel = self.getAtomsSelection(self.boneslevel[i],sel,selection,mol,chain=c)
                if c.ribbonType()=='NA':
                    lsel = c.residues.atoms.get("O5'")
                else :
                    lsel = c.residues.atoms.get("CA")                
                parent = mol.geomContainer.masterGeom.chains_obj[c.name]
                if isinstance(lsel,AtomSet) :
                    obSpline,spline=self.epmv.helper.spline(name,lsel.coords,
                                                scene=self.epmv.helper.getCurrentScene(),
                                                parent=parent)
                else :
                    obSpline,spline=self.epmv.helper.spline(name,lsel,
                                                scene=self.epmv.helper.getCurrentScene(),
                                                parent=parent)
#                if c.ribbonType()=='NA':
#                    #make the ladder
#                    self.epmv.NAlader(mol,c)
            self.epmv.helper.toggleDisplay(obSpline,display)
        return True
        
    def dsMeta(self,*args):
        mname,mol,sel,selection,display = self.getDsInfo("meta")
        if mol is None : 
            return        
        #make the metaballs
        name='metaballs'+mol.name
        metaballs=self.epmv.helper.getObject(name)
        if metaballs is None :
#            atoms = selection.allAtoms #or a subselection of surface atoms according sas
            metaballsModifyer,metaballs = self.epmv._metaballs(name,
                                                selection.coords,
                                                selection.radius,
                                                scn=self.epmv.helper.getCurrentScene(),
                                                root=mol.geomContainer.masterGeom.obj)
        else :
            self.epmv.helper.toggleDisplay(metaballs,display)
        return True

    def getAtomsSelection(self,level,sel,selection,mol,chain = None):
        atlevel = {"Trace":["CA","O5'"],
                   "Backbone":["N,CA,C,N","P,O5',C5',C4',C3',O3'"],
                   "Full Atoms":["all","all"],
                   "Domain":["CA","P"], #how to define the domain
                   "Chain":["ccenter","ccenter"],
                   "Mol":["mcenter","mcenter"],
                   }
        lsel=AtomSet()        
        lchain = mol.chains
        if chain is not None :
            lchain = [chain]
        i=0
        #check selection,check if dna
        if level == 'Mol':
            lsel = [mol.getCenter(),]
        elif level == 'Chain' :
            lsel=[]
            for ch in lchain:
                #get the center of the chain
                lsel.append(util.getCenter(ch.residues.atoms.coords))
        elif level == 'Domain' :
            #how to get the domain and its center...
            lsel=[]
            for ch in lchain:
                #get the center of the chain
                lsel.append(util.getCenter(ch.residues.atoms.coords))           
        elif level =='Selection':
            lsel = selection
        else :
            if sel == mol.name :
                for ch in lchain:
                    if ch.ribbonType()=='NA':
                        i=1
                    selection = ch.residues.atoms.get(atlevel[level][i])
                    selection.sort()
                    lsel.extend(selection)
            else :
                ch=selection.findParentsOfType(Chain)[0]
                if ch.ribbonType()=='NA':
                    i=1
                selection = selection.get(atlevel[level][i])
                selection.sort()
                lsel.extend(selection)        
        print lsel
        return lsel

    def dsBones(self,*args):
        #boneslevel=["Trace","Backbone","Full Atoms","Domain","Chain","Mol","Selection"]
        mname,mol,sel,selection,display = self.getDsInfo("arm")
        if mol is None : 
            return        
        name=mname+"_Armature"
        armObj = self.epmv.helper.getObject(name)
        i=self.getLong(self.COMB_BOX["bones"])
        print self.boneslevel[i]
        atlevel="CA"
        if armObj is None :
            #level
            lsel = self.getAtomsSelection(self.boneslevel[i],sel,selection,mol)
            if isinstance(lsel,AtomSet) :
                object,bones=self.epmv._armature(name,lsel,
                                       scn=self.epmv.helper.getCurrentScene(),
                                       root=mol.geomContainer.masterGeom.obj)
#                                       mode=self.boneslevel[i])
            else :
                object,bones=self.epmv._armature(name,lsel,coords=lsel,
                                       scn=self.epmv.helper.getCurrentScene(),
                                       root=mol.geomContainer.masterGeom.obj)                
            mol.geomContainer.geoms["armature"]=[object,bones]
        else :
            #how to update > delete and recreate ?
            self.epmv.helper.toggleDisplay(armObj,display)
        return True

    def custom_color(self,*args):
        mname,mol,sel,selection,color = self.getDsInfo("col")
        if mol is None : 
            return       
        lGeom=self.getGeomActive(mname) 
        self.setLong(self.COMB_BOX["col"],6) #customcolor
        self.mv.molDispl[mname]["col"]=color
        self.funcColor[6](selection,[color], lGeom, log=1)

    def color(self,*args):
#        print self.funcColor
        mname,mol,sel,selection,color = self.getDsInfo("col")
        if mol is None : 
            return        
        lGeom=self.getGeomActive(mname)
        funcId = self.getLong(self.COMB_BOX["col"])
#        print "colorF ", funcId,self.funcColor[funcId], lGeom
        if funcId == 6 : 
            #custom color
            self.mv.molDispl[mname]["col"]=color
            self.funcColor[6](selection,[color], lGeom, log=1)
        elif funcId == 7 or funcId == 8 or funcId == 9  :
            #color by properties , ie NtoC, Bfactor, SAS
            self.mv.colorByProperty.level='Atom'
            if funcId == 7 :
                maxi = len(selection)
                mini = 1.0
                property = 'number'
            elif funcId == 8 :
                maxi = max(selection.temperatureFactor)
                mini = min(selection.temperatureFactor)
                property = 'temperatureFactor'
            elif funcId == 9 : 
                if not hasattr(selection,"sas_area"):
                    try :
                        self.mv.computeSESAndSASArea(mol)
                    except :
                        self.drawError("Problem with mslib")
                maxi = max(selection.sas_area)
                mini = min(selection.sas_area)
                property = 'sas_area'
            self.funcColor[7](selection, lGeom, property,mini=float(mini),
                                        maxi=float(maxi), propertyLevel='Atom', 
                                        colormap='rgb256')
            self.mv.molDispl[mname]["col"] = funcId
        else : 
            self.funcColor[funcId](selection, lGeom)
            self.mv.molDispl[mname]["col"] = funcId

    def drawPreset(self,*args):
        #To finish and define/...
        mname,mol,sel,selection = self.getDsInfo()
        if mol is None : 
            return        
#        self.presettype=['available presets:','  Lines','  Liccorice','  SpaceFilling',
#                         '  Ball+Sticks','  RibbonProtein+StickLigand',
#                         '  RibbonProtein+CPKligand','  xray','  Custom',
#                         '  Save Custom As...']
        #load,edit save representation preset
        preset=self.presettype[self.getLong(self.COMB_BOX["preset"])]
        print preset
        if preset.strip() == 'Liccorice':
            #displayBS as licorice which is simply ratio == 1.0
                #set the ratio and do the command
            self.setReal(self.SLIDERS["bs_r"],1.0)
            self.setBool(self.CHECKBOXS["bs"] ,True)
            self.dsBS()
        elif preset.strip() == 'xray':
            #??
            pass
        elif preset.strip() == 'Lines':
            self.mv.displayLines(selection)
        elif preset.strip() == 'Ball+Sticks':
            self.setReal(self.SLIDERS["bs_r"],1.5)
            self.setBool(self.CHECKBOXS["bs"],True)
            self.dsBS()
        elif preset.strip() == 'SpaceFilling':
            self.setReal(self.SLIDERS["cpk"],1.)
            self.setBool(self.CHECKBOXS["cpk"],True)
            self.dsCPK()
        elif preset.strip() == 'RibbonProtein+StickLigand':
            #need to check if ligand exist
            ligand = self.mv.select(mol.name+"::ligand:",
                                        negate=False, only=True, xor=False, 
                                        log=0, intersect=False)
            if not len(ligand) :
                return
            #1 select protein
            p = self.mv.select(mol.name+"::aminoacids:",
                                        negate=False, only=True, xor=False, 
                                        log=0, intersect=False)            
            #2 dsSS for protein
            self.mv.displayExtrudedSS(p, negate=False, molModes={mname:'From Pross'},
                                               only=False, log=1)
            self.mv.colorBySecondaryStructure(p,["secondarystructure"])           
            self.setBool(self.CHECKBOXS["ss"] ,True)
            #3ds ligand Liccroice
            ratio = self.getReal(self.SLIDERS["bs_r"])
            scale = self.getReal(self.SLIDERS["bs_s"])
            bRad = 0.3
            cradius = float(bRad/ratio)*scale            
            self.mv.displaySticksAndBalls(ligand, bRad=0.3*scale, 
                                   cradius =cradius, bScale=0., 
                                   negate=False,
                                   only=False, bquality=0, 
                                   cquality=0)
            self.setBool(self.CHECKBOXS["bs"] ,True)
        elif preset.strip() == 'RibbonProtein+CPKligand':
            #need to check if ligand exist
            ligand = self.mv.select(mol.name+"::ligand:",
                                        negate=False, only=True, xor=False, 
                                        log=0, intersect=False)
            if not len(ligand) :
                return            
            #1 select protein
            p = self.mv.select(mol.name+"::aminoacids:",
                                        negate=False, only=True, xor=False, 
                                        log=0, intersect=False)            
            #2 dsSS for protein
            self.mv.displayExtrudedSS(p, negate=False, molModes={mname:'From Pross'},
                                               only=False, log=1)
            self.mv.colorBySecondaryStructure(p,["secondarystructure"])   
            self.setBool(self.CHECKBOXS["ss"] ,True)        
            #3ds ligand CPK
            scale = self.getReal(self.SLIDERS["cpk"])  
            self.mv.displayCPK(ligand,log=0,negate=False,
                        scaleFactor=scale, redraw =0)#redraw? 
            self.setBool(self.CHECKBOXS["cpk"] ,True)
        #what are Custom and Save as?

    def createTexture(self,*args):
        mname,mol,sel,selection = self.getDsInfo()
        if mol is None:
            return
        lGeom=self.getGeomActive(mname)
        print lGeom
        i=self.getLong(self.COMB_BOX["uv"])
        print self.uvselection[i]
        filename = self.getString(self.INPUTSTR["uv"])
        surfName = self.getString(self.INPUTSTR["uvg"])
        import math
        #surfName="CoarseMS_ind"
        surf = mol.geomContainer.geoms[surfName]
        vertices=surf.getVertices()
        faces=surf.getFaces()
        colors=mol.geomContainer.getGeomColor(surf) #per vertex of per face...msms is per vertex
        if colors is None :
            if mol.geomContainer.atomPropToVertices.has_key(surfName):
                func = mol.geomContainer.atomPropToVertices[surfName]
                geom = mol.geomContainer.geoms[surfName]
                atms = mol.geomContainer.atoms[surfName]
                colors = func(geom, atms, 'colors', propIndex=surfName)
        surfobj = self.epmv.helper.getObject(surf.obj)

        print len(faces), math.sqrt(len(faces))
        s=20
        sizex= math.sqrt(len(faces))*(s+1)
        sizey = math.sqrt(len(faces))*(s+1)
        print  (sizex, sizey)
        
        #mat = epmv.helper.createTexturedMaterial(surfName+"UV","/Users/ludo/uv.png")
        #epmv.helper.assignMaterial(mat,surfobj,texture=True)
        if self.uvselection[i] == "regular disposed triangle" :
            if self.host != 'maya':
                mat = self.epmv.helper.getMaterial(surfName+"UV")
                if mat is None :
                    mat = self.epmv.helper.createTexturedMaterial(surfName+"UV",filename)
                    self.epmv.helper.assignMaterial(mat,surfobj,texture=True)           
            self.epmv.helper.makeTexture(surfobj,
                                filename=filename,colors=colors,
                                sizex=sizex,sizey=sizey,faces=faces,
                                s=s,draw=True) #maya need inversion.
                                
        #if uv already exist from automatic unwrapping :
        else :#"unwrapped mesh UV"
            self.epmv.helper.makeTextureFromUVs(surfobj,
                                filename=filename,colors=colors,
                                sizex=sizex,sizey=sizey,
                                s=s,draw=True)
        

    def setKeywordSel(self,*args):
        key=self.keyword[self.getLong(self.COMB_BOX["keyword"])]
        if key == 'keywords' : key = ""
        self.setString(self.SELEDIT_TEXT,key.replace(" ",""))

    def set_ePMVScript(self,*args):
        from ePMV import demo
        dir = demo.__path__[0]
        ids = self.getLong(self.COMB_BOX['scriptO'])
        filename = None
        if ids == 0 : #Open..ask for broser
            self.fileDialog(label="Open python file",callback=self.set_ePMVScript_cb)
        else :
            filename = dir+'/'+self.scriptliste[ids]+'.py'
            self.set_ePMVScript_cb(filename)

    def set_ePMVScript_cb(self,filename):
        if filename :
            try:
                f = open(filename,'r')
                script = f.read()
                f.close()
            except:
                script = "file :\n"+filename + " didnt exist !\n"
            self.setStringArea(self.SCRIPT_TEXT,script)
 
    def execPmvComds(self,*args):
        #first select the text
        #cmds=pmvcmds.val
        text = self.getStringArea(self.SCRIPT_TEXT)# getSelectTxt()
        if text is not None:
            cmds=text
#            for l in text:
#                cmds+=l+'\n'
#            print len(cmds),cmds
            exec(cmds,{'self':self.mv,'epmv':self.epmv})  
#            self.updateViewer()
            return True

    def drawPreferences(self,*args):
        #drawSubDialog
        self.drawSubDialog(self.options,2555554,callback = self.options.SetPreferences) #in c4d asynchr but blender syncrho

    def drawAbout(self,*args):
        self.drawMessage(title='About ePMV',message=self.__about__)
        
    def launchBrowser(self,*args):
        import webbrowser
        webbrowser.open(self.__url__[0])
        
    def citationInformation(self,*args):
        import webbrowser
        webbrowser.open(self.__url__[2])

    def check_update(self,*args):
        #get current version
        import Support
        self.epmv.inst.current_version = self.__version__
        self.epmv.inst.PMVv = Support.version.__version__
        self.epmv.inst.pyubicv = pyubic.__version__
        doit=self.epmv.inst.checkForUpdate()
        if True in doit :
            #need some display?
            msg = "An update is available.\nNotes:\n"
            msg+= self.epmv.inst.update_notes
            msg+= "Do you want to update?\n"
            res = self.drawQuestion(question=msg)
            if res :
                res = self.drawQuestion(question="Do you want to backup the current version?")
                self.epmv.inst.update(pmv=doit[0],epmv=doit[1],pyubic=doit[2],backup=res)
                self.drawMessage(title='update ePMV',message="You are now up to date! Please restart.")
        else :
            self.drawMessage(title='update ePMV',message="You are up to date! no update need.")
        
    def addExtensionGUI(self,*args):
        #should do a mini dialog asking to browse and propose the current 
        #supported extension excepting already set up extension
        #should have a subdialog instead
        question="Enter the extension name follow by the directory,\nie 'modeller:/Library/modeller/modlib'"
        self.drawInputQuestion(question=question,callback=self.epmv.inst.addExtension)

    def drawPyAutoDock(self,*args):
        #drawSubDialog
        self.drawSubDialog(self.ad,2555555)#in c4d asynchr but blender syncrho

    def drawModellerGUI(self,*args):
        #drawSubDialog
        self.drawSubDialog(self.pd,2555556,callback = self.pd.doIt) #in c4d asynchr but blender syncrho

    def drawPalette(self,*args):
        #drawSubDialog
        self.drawSubDialog(self.pmvPalgui,25555560) #in c4d asynchr but blender syncrho

    def drawPymolGUI(self,*args):
        #drawSubDialog
        print "drawSubPyMol"
        #if self.epmv._pymol :
        if self.pymolgui is None :
            print "create pymol gui as a subDialog"
            from ePMV.PyMol.pymolAdaptor import pymolGui
            #exec('self.pymolgui = pymolGui()\n',{"pymolGui":pymolGui,"self":self})
            self.pymolgui = pymolGui()
        if self.pym is None:
            from ePMV.PyMol.pymolAdaptor import pymolAdaptor
            print "createpymolAdaptor"
            self.pym = pymolAdaptor(debug =0)
            self.pymolgui.setup(sub=True,epmv=self.epmv,pym=self.pym)        
        self.drawSubDialog(self.pymolgui,25555570)
        

    def modellerOptimize(self,*args):
        import modeller
        mname,mol,sel,selection = self.getDsInfo()     
        mdl = mol.mdl
        mdl = mol.mdl
        print mname
        # Select all atoms:
        atmsel = modeller.selection(mdl)
        
        # Generate the restraints:
        mdl.restraints.make(atmsel, restraint_type='stereo', spline_on_site=False)
        #mdl.restraints.write(file=mpath+mname+'.rsr')
        mpdf = atmsel.energy()
        print "before optmimise"
        # Create optimizer objects and set defaults for all further optimizations
        cg = modeller.optimizers.conjugate_gradients(output='REPORT')
        mol.pmvaction.last = 10000
        print "optimise"
        maxit = self.pd.getLong(self.pd.NUMBERS['miniIterMax'])
        mol.pmvaction.store = self.pd.getBool(self.pd.CHECKBOXS['store'])
        mol.pmvaction.redraw = True
        cg.optimize(atmsel, max_iterations=maxit, actions=mol.pmvaction)#actions.trace(5, trcfil))
        del cg
        mol.pmvaction.redraw = False
        return True
        
    def modellerMD(self,*args):
        import modeller
        mname,mol,sel,selection = self.getDsInfo()     
        mdl = mol.mdl
        print mname
        # Select all atoms:
        atmsel = modeller.selection(mdl)
        
        # Generate the restraints:
        mdl.restraints.make(atmsel, restraint_type='stereo', spline_on_site=False)
        #mdl.restraints.write(file=mpath+mname+'.rsr')
        mpdf = atmsel.energy()
        print "before optmimise"
        md = modeller.optimizers.molecular_dynamics(output='REPORT')
        mol.pmvaction.last = 10000
        mol.pmvaction.store = True
        print "optimise"
        maxit = self.pd.getLong(self.pd.NUMBERS['mdIterMax'])
        temp = self.pd.getLong(self.pd.NUMBERS['mdTemp'])
        mol.pmvaction.store = self.pd.getBool(self.pd.CHECKBOXS['store'])
        print maxit,temp,mol.pmvaction.store
        mol.pmvaction.redraw = True
        md.optimize(atmsel, temperature=float(temp), 
                    max_iterations=int(maxit),actions=mol.pmvaction)
        del md
        mol.pmvaction.redraw = False
        return True

    def drawAPBS(self,*args):
        self.drawSubDialog(self.apbsgui,255555710)
