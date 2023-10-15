import adsk.core, adsk.fusion, traceback

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

class main:
    def Excecute(self, inputlist ):
        try:
            objlist = []
            planelist = []
            linelist = []
            for ii in range(len(inputlist)):  #"or" didn't work...
                objlist.append(inputlist[ii].entity)
                if objlist[ii].objectType == adsk.fusion.ConstructionPlane.classType() :
                    planelist.append(objlist[ii])

                else:
                    linelist.append(objlist[ii])

            for ii in range(len(planelist) ):  
                sketches = rootComp.sketches    
                plane1 = planelist[ii]
                sketch = sketches.add(plane1)
                entities = []
                entities.append(plane1)
                for jj in range(len(linelist) ):
                    entities.append(linelist[jj])
                sketch.intersectWithSketchPlane(entities)

                plane1.isLightBulbOn = True

        except:
            if ui:
               ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))