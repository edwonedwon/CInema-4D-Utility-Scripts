import c4d
import os

from c4d import gui, storage

origDoc = c4d.documents.GetActiveDocument()
tempDoc = c4d.documents.BaseDocument()
selected = origDoc.GetActiveObjects(0)
tempDoc_filepath = "string"

def CloseDocument():
    c4d.CallCommand(12664) #close document
    pass
            
def SaveSelectedObjectsAs():
    #bring up the file save dialog
    global tempDoc
    global tempDoc_filepath
    tempDoc_filepath = storage.LoadDialog(title="Save File for Export", 
    flags=c4d.FILESELECT_SAVE, force_suffix="c4d")
    print(tempDoc_filepath)
    #save the file
    tempDoc = c4d.documents.IsolateObjects(origDoc,selected)
    c4d.documents.SaveDocument(tempDoc,tempDoc_filepath,
    c4d.SAVEDOCUMENTFLAGS_0, 
    c4d.FORMAT_C4DEXPORT)

def OpenTempScene():
    c4d.documents.LoadFile(tempDoc_filepath)

def DeleteTempScene():
    pass

def ExportFBX():
    global tempDoc
    #get the FBX plugin in
    fbx_plugin_id = 1026370
    
    fbx_filepath = tempDoc_filepath
    fbx_filepath = fbx_filepath.replace('.c4d', '')
    
    #bring up the file save dialog
    #fbx_filepath = storage.LoadDialog(title="Save File for Alembic Export", 
    #flags=c4d.FILESELECT_SAVE, force_suffix="fbx")
    #if fbx_filepath is None:
    #    return
    
    #the FBX export settings
    container = c4d.plugins.GetWorldPluginData(fbx_plugin_id)
    for id, value in container:
        if id == c4d.FBXEXPORT_ASCII:  container[id] = 0
        elif id == c4d.FBXEXPORT_BAKE_ALL_FRAMES: container[id] = 0
        elif id == c4d.FBXEXPORT_SAVE_NORMALS: container[id] = 1
        elif id == c4d.FBXEXPORT_GRP_ANIMATION: container[id] = 1
        elif id == c4d.FBXEXPORT_TEXTURES: container[id] = 1
        elif id == c4d.FBXEXPORT_EMBED_TEXTURES: container[id] = 1
    c4d.plugins.SetWorldPluginData(fbx_plugin_id, container)
    c4d.documents.SaveDocument(tempDoc,fbx_filepath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, fbx_plugin_id)

def main():
    global tempDoc_filepath
    global tempDoc
    SaveSelectedObjectsAs()
    OpenTempScene()
    ExportFBX()
    CloseDocument()
    DeleteTempScene()

if __name__=='__main__':
    main()
