#Author-
#Description-


import adsk.core, adsk.fusion, traceback
from . import mainfunc

# global set of event handlers to keep them referenced for the duration of the command
handlers = []
ui = None
app = adsk.core.Application.get()
if app:
    ui  = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
rootComp = design.rootComponent
planes = rootComp.constructionPlanes

class PointMakingExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            command = args.firingEvent.sender
            inputs = command.commandInputs
            sel = []
            selctionCounts =ui.activeSelections.count
            for ii in range (selctionCounts ):#line:215
                sel.append (ui.activeSelections.item (ii) )

            planebuilder = mainfunc.main()
            planebuilder.Excecute(sel)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class AirfoilCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class AirfoilValidateInputHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
       
    def notify(self, args):
        try:
            sels = ui.activeSelections
            if len(sels) == 0:
                args.areInputsValid = False
            else:
                args.areInputsValid = True
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class PlaneBuildCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.command
            onExecute = PointMakingExecuteHandler()
            cmd.execute.add(onExecute)
            onDestroy = AirfoilCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            onValidateInput = AirfoilValidateInputHandler()
            cmd.validateInputs.add(onValidateInput)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onDestroy)
            handlers.append(onValidateInput)
            #define the inputs
            inputs = cmd.commandInputs
            i0 = inputs.addSelectionInput('ConstPlane', 'Construction Plane', 'Please select a construction plane')
            i0.addSelectionFilter(adsk.core.SelectionCommandInput.ConstructionPlanes)
            i0.addSelectionFilter(adsk.core.SelectionCommandInput.RootComponents)
            i0.setSelectionLimits(0,0)


            i1 = inputs.addSelectionInput('Line', 'Line', 'Please select some lines')
            i1.addSelectionFilter(adsk.core.SelectionCommandInput.SketchCurves)     
            i1.addSelectionFilter(adsk.core.SelectionCommandInput.SketchLines)     
            i1.setSelectionLimits(0,0)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Main function
def run(context):
    try:
        title = 'Select Construction Plane'

        if not design:
            ui.messageBox('No active Fusion design', title)
            return

        commandDefinitions = ui.commandDefinitions

        # check the command exists or not
        cmdDef = commandDefinitions.itemById('AirfoilCMDDef')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('AirfoilCMDDef',
                                                            'Create Prism',
                                                            'Create a prism.')

        onCommandCreated = PlaneBuildCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

