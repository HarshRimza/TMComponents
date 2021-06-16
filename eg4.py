import tkinter
import tkinter.font
class User:
 def __init__(self,name,invite=None):
  self.name=name
  self.invite=invite

class DataModel():
 def __init__(self):
  self.data=[]
  self.data.append(User("Amit"))
  self.data.append(User("Bobby"))
  self.data.append(User("Sumit"))
  self.data.append(User("Rakesh"))
  self.inviteIcon=tkinter.PhotoImage(file="invite.png")
  self.editCommand=None
 def getRowCount(self):
  return len(self.data)
 def getColumnCount(self):
  return 2
 def getColumnTitle(self,columnIndex):
  if columnIndex==0: return "Available Users"
  return "I"
 def getColumnWidth(self,columnIndex):
  if columnIndex==0: return 150
  if columnIndex==1: return 30
 def getValueAt(self,rowIndex,columnIndex,master=None):
  u=self.data[rowIndex]
  if columnIndex==0: return u.name
  if u.invite is None: u.invite=tkinter.Button(master,image=self.inviteIcon,width=18,height=18)
  return u.invite
 def getCellType(self,rowIndex,columnIndex):
  if columnIndex==0: return "str"
  return "Button"
 def getContentAlignment(self,rowIndex,columnIndex):
  if columnIndex==0: return "left"
  return "center"
 def getCellCommand(self,rowIndex,columnIndex):
  if columnIndex==1: return self.editCommand
  return None


class TMGrid(tkinter.Canvas):
 def __init__(self,master,model,width,height,rowHeight,titleFont=None,dataFont=None):
  tkinter.Canvas.__init__(self,master)
  self.customEvents={}
  self.customEvents["<RowSelectionChanged>"]=None
  self.width=width
  self.height=height
  self.model=model
  self.images={}
  self.rowSelectionChanged=None
  self.rectanglesToClear=None
  self.bind("<Button-1>",self.gridClicked)
  self.bind("<Key>",self.gridKeyHandler)
  self.selectedRowIndex=-1
  self.rowHeight=rowHeight
  if titleFont: self.titleFont=titleFont
  else: self.titleFont=tkinter.font.Font(family="verdana",size=14,weight="bold")
  if dataFont: self.dataFont=dataFont
  else: self.dataFont=tkinter.font.Font(family="verdana",size=12)
  self.update()
 def canvasWidgetClickHandler(self,r,c):
  self.changeRowSelection(r)
  if self.model.editCommand: self.model.editCommand(r,c)
 def gridKeyHandler(self,event):
  if event.keysym=="Up":
   if self.selectedRowIndex==-1 or self.selectedRowIndex==0: rowIndex=self.model.getRowCount()-1
   else: rowIndex=self.selectedRowIndex-1
  elif event.keysym=="Down":
   if self.selectedRowIndex==-1 or self.selectedRowIndex==self.model.getRowCount()-1: rowIndex=0
   else: rowIndex=self.selectedRowIndex+1    
  else: 
   return
  oldRowIndex=self.selectedRowIndex
  newRowIndex=rowIndex
  # print(rowIndex)
  # if a row was selected earlier, unhighlight it (back to normal)
  if self.selectedRowIndex!=-1:
   rectX1=self.x1+1
   rectX2=self.x2-1
   rectY1=self.y1+((self.selectedRowIndex+1)*self.rowHeight)+5
   rectY2=rectY1+self.rowHeight-5
   self.create_rectangle(rectX1,rectY1,rectX2,rectY2,fill="#E0E0E0",width=0)
   columns=self.model.getColumnCount()
   x=self.x1+1
   for i in range(columns-1):
    x+=self.model.getColumnWidth(i)  
    self.create_line(x+1,rectY1,x+1,rectY2,fill="white")
    self.create_line(x,rectY1,x,rectY2,fill="#ADADAD")
   dataFont=self.dataFont
   x=self.x1+1
   y=self.y1+((self.selectedRowIndex+1)*self.rowHeight)+1
   for c in range(columns):
    cellContent=self.model.getValueAt(self.selectedRowIndex,c)
    cellType=self.model.getCellType(self.selectedRowIndex,c)
    contentAlignment=self.model.getContentAlignment(self.selectedRowIndex,c)
    if cellType=="PhotoImage":
     if cellContent not in self.images: self.images[cellContent]=tkinter.PhotoImage(file=cellContent)
     img=self.images[cellContent]
     imageWidth=img.width()
     imageHeight=img.height()
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     imageX=int(cellWidth/2)-int(imageWidth/2)
     imageY=int(cellHeight/2)-int(imageHeight/2)
     self.create_image(x+imageX,y+imageY,anchor='nw',image=img)
    elif cellType=="Button": 
     pass
    else:
     contentWidth=dataFont.measure(cellContent)
     contentHeight=dataFont.metrics("linespace")
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     contentX,contentY=eval(f"self.{contentAlignment}")(contentWidth,contentHeight,cellWidth-10,cellHeight)
     self.create_text(x+contentX+5,y+contentY,font=dataFont,text=cellContent,anchor='nw')
    x+=self.model.getColumnWidth(c) 

  #highlight the newly selected row
  self.selectedRowIndex=rowIndex
  rectX1=self.x1+1
  rectX2=self.x2-1
  rectY1=self.y1+((rowIndex+1)*self.rowHeight)+5
  rectY2=rectY1+self.rowHeight-5
  self.create_rectangle(rectX1,rectY1,rectX2,rectY2,fill="#AAAAAA",width=0)
  columns=self.model.getColumnCount()
  x=self.x1+1
  for i in range(columns-1):
   x+=self.model.getColumnWidth(i)  
   self.create_line(x+1,rectY1,x+1,rectY2,fill="white")
   self.create_line(x,rectY1,x,rectY2,fill="#ADADAD")
  dataFont=self.dataFont
  x=self.x1+1
  y=self.y1+((rowIndex+1)*self.rowHeight)+1
  for c in range(columns):
   cellContent=self.model.getValueAt(rowIndex,c)
   cellType=self.model.getCellType(rowIndex,c)
   contentAlignment=self.model.getContentAlignment(self.selectedRowIndex,c)
   if cellType=="PhotoImage":
    if cellContent not in self.images: self.images[cellContent]=tkinter.PhotoImage(file=cellContent)
    img=self.images[cellContent]
    imageWidth=img.width()
    imageHeight=img.height()
    cellHeight=self.rowHeight
    cellWidth=self.model.getColumnWidth(c)
    imageX=int(cellWidth/2)-int(imageWidth/2)
    imageY=int(cellHeight/2)-int(imageHeight/2)
    self.create_image(x+imageX,y+imageY,anchor='nw',image=img)
   elif cellType=="Button":
    pass
   else:
     contentWidth=dataFont.measure(cellContent)
     contentHeight=dataFont.metrics("linespace")
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     contentX,contentY=eval(f"self.{contentAlignment}")(contentWidth,contentHeight,cellWidth-10,cellHeight)
     self.create_text(x+contentX+5,y+contentY,font=dataFont,text=cellContent,anchor='nw')
   x+=self.model.getColumnWidth(c) 
  callBack=self.customEvents["<RowSelectionChanged>"]
  if callBack: callBack(oldRowIndex,newRowIndex)


 def gridClicked(self,event):
  self.focus_set()
  x=event.x
  y=event.y
  if not self.inGrid(x,y): return
  rowIndex=self.getRowClickedOn(x,y)
  if rowIndex==-1: return
  if self.selectedRowIndex==rowIndex: return
  oldRowIndex=self.selectedRowIndex
  newRowIndex=rowIndex
  #print(rowIndex)
  # if a row was selected earlier, unhighlight it (back to normal)
  if self.selectedRowIndex!=-1:
   rectX1=self.x1+1
   rectX2=self.x2-1
   rectY1=self.y1+((self.selectedRowIndex+1)*self.rowHeight)+5
   rectY2=rectY1+self.rowHeight-5
   self.create_rectangle(rectX1,rectY1,rectX2,rectY2,fill="#E0E0E0",width=0)
   columns=self.model.getColumnCount()
   x=self.x1+1
   for i in range(columns-1):
    x+=self.model.getColumnWidth(i)  
    self.create_line(x+1,rectY1,x+1,rectY2,fill="white")
    self.create_line(x,rectY1,x,rectY2,fill="#ADADAD")
   dataFont=self.dataFont
   x=self.x1+1
   y=self.y1+((self.selectedRowIndex+1)*self.rowHeight)+1
   for c in range(columns):
    cellContent=self.model.getValueAt(self.selectedRowIndex,c)
    cellType=self.model.getCellType(self.selectedRowIndex,c)
    contentAlignment=self.model.getContentAlignment(self.selectedRowIndex,c)
    if cellType=="PhotoImage":
     if cellContent not in self.images: self.images[cellContent]=tkinter.PhotoImage(file=cellContent)
     img=self.images[cellContent]
     imageWidth=img.width()
     imageHeight=img.height()
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     imageX=int(cellWidth/2)-int(imageWidth/2)
     imageY=int(cellHeight/2)-int(imageHeight/2)
     self.create_image(x+imageX,y+imageY,anchor='nw',image=img)
    elif cellType=="Button":
     pass
    else:
     contentWidth=dataFont.measure(cellContent)
     contentHeight=dataFont.metrics("linespace")
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     contentX,contentY=eval(f"self.{contentAlignment}")(contentWidth,contentHeight,cellWidth-10,cellHeight)
     self.create_text(x+contentX+5,y+contentY,font=dataFont,text=cellContent,anchor='nw')
    x+=self.model.getColumnWidth(c) 

  #highlight the newly selected row
  self.selectedRowIndex=rowIndex
  rectX1=self.x1+1
  rectX2=self.x2-1
  rectY1=self.y1+((rowIndex+1)*self.rowHeight)+5
  rectY2=rectY1+self.rowHeight-5
  self.create_rectangle(rectX1,rectY1,rectX2,rectY2,fill="#AAAAAA",width=0)
  columns=self.model.getColumnCount()
  x=self.x1+1
  for i in range(columns-1):
   x+=self.model.getColumnWidth(i)  
   self.create_line(x+1,rectY1,x+1,rectY2,fill="white")
   self.create_line(x,rectY1,x,rectY2,fill="#ADADAD")
  dataFont=self.dataFont
  x=self.x1+1
  y=self.y1+((rowIndex+1)*self.rowHeight)+1
  for c in range(columns):
   cellContent=self.model.getValueAt(rowIndex,c)
   cellType=self.model.getCellType(rowIndex,c)
   contentAlignment=self.model.getContentAlignment(self.selectedRowIndex,c)
   if cellType=="PhotoImage":
    if cellContent not in self.images: self.images[cellContent]=tkinter.PhotoImage(file=cellContent)
    img=self.images[cellContent]
    imageWidth=img.width()
    imageHeight=img.height()
    cellHeight=self.rowHeight
    cellWidth=self.model.getColumnWidth(c)
    imageX=int(cellWidth/2)-int(imageWidth/2)
    imageY=int(cellHeight/2)-int(imageHeight/2)
    self.create_image(x+imageX,y+imageY,anchor='nw',image=img)
   elif cellType=="Button":
    pass
   else:
     contentWidth=dataFont.measure(cellContent)
     contentHeight=dataFont.metrics("linespace")
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     contentX,contentY=eval(f"self.{contentAlignment}")(contentWidth,contentHeight,cellWidth-10,cellHeight)
     self.create_text(x+contentX+5,y+contentY,font=dataFont,text=cellContent,anchor='nw')
   x+=self.model.getColumnWidth(c) 
  callBack=self.customEvents["<RowSelectionChanged>"]
  if callBack!=None: callBack(oldRowIndex,newRowIndex)
  
 def getRowClickedOn(self,x,y):
  row=int((y-self.y1)/self.rowHeight)-1
  if row>=self.model.getRowCount(): return -1
  else: return row  
  
 def inGrid(self,x,y):
  return x>=self.x1 and x<=self.x2 and y>=self.y1 and y<=self.y2

 def changeRowSelection(self,rowIndex):
  if self.selectedRowIndex==rowIndex: return
  oldRowIndex=self.selectedRowIndex
  newRowIndex=rowIndex
  #print(rowIndex)
  # if a row was selected earlier, unhighlight it (back to normal)
  if self.selectedRowIndex!=-1:
   rectX1=self.x1+1
   rectX2=self.x2-1
   rectY1=self.y1+((self.selectedRowIndex+1)*self.rowHeight)+5
   rectY2=rectY1+self.rowHeight-5
   self.create_rectangle(rectX1,rectY1,rectX2,rectY2,fill="#E0E0E0",width=0)
   columns=self.model.getColumnCount()
   x=self.x1+1
   for i in range(columns-1):
    x+=self.model.getColumnWidth(i)  
    self.create_line(x+1,rectY1,x+1,rectY2,fill="white")
    self.create_line(x,rectY1,x,rectY2,fill="#ADADAD")
   dataFont=self.dataFont
   x=self.x1+1
   y=self.y1+((self.selectedRowIndex+1)*self.rowHeight)+1
   for c in range(columns):
    cellContent=self.model.getValueAt(self.selectedRowIndex,c)
    cellType=self.model.getCellType(self.selectedRowIndex,c)
    contentAlignment=self.model.getContentAlignment(self.selectedRowIndex,c)
    if cellType=="PhotoImage":
     if cellContent not in self.images: self.images[cellContent]=tkinter.PhotoImage(file=cellContent)
     img=self.images[cellContent]
     imageWidth=img.width()
     imageHeight=img.height()
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     imageX=int(cellWidth/2)-int(imageWidth/2)
     imageY=int(cellHeight/2)-int(imageHeight/2)
     self.create_image(x+imageX,y+imageY,anchor='nw',image=img)
    elif cellType=="Button":
     pass
    else:
     contentWidth=dataFont.measure(cellContent)
     contentHeight=dataFont.metrics("linespace")
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     contentX,contentY=eval(f"self.{contentAlignment}")(contentWidth,contentHeight,cellWidth-10,cellHeight)
     self.create_text(x+contentX+5,y+contentY,font=dataFont,text=cellContent,anchor='nw')
    x+=self.model.getColumnWidth(c) 

  #highlight the newly selected row
  self.selectedRowIndex=rowIndex
  rectX1=self.x1+1
  rectX2=self.x2-1
  rectY1=self.y1+((rowIndex+1)*self.rowHeight)+5
  rectY2=rectY1+self.rowHeight-5
  self.create_rectangle(rectX1,rectY1,rectX2,rectY2,fill="#AAAAAA",width=0)
  columns=self.model.getColumnCount()
  x=self.x1+1
  for i in range(columns-1):
   x+=self.model.getColumnWidth(i)  
   self.create_line(x+1,rectY1,x+1,rectY2,fill="white")
   self.create_line(x,rectY1,x,rectY2,fill="#ADADAD")
  dataFont=self.dataFont
  x=self.x1+1
  y=self.y1+((rowIndex+1)*self.rowHeight)+1
  for c in range(columns):
   cellContent=self.model.getValueAt(rowIndex,c)
   cellType=self.model.getCellType(rowIndex,c)
   contentAlignment=self.model.getContentAlignment(self.selectedRowIndex,c)
   if cellType=="PhotoImage":
    if cellContent not in self.images: self.images[cellContent]=tkinter.PhotoImage(file=cellContent)
    img=self.images[cellContent]
    imageWidth=img.width()
    imageHeight=img.height()
    cellHeight=self.rowHeight
    cellWidth=self.model.getColumnWidth(c)
    imageX=int(cellWidth/2)-int(imageWidth/2)
    imageY=int(cellHeight/2)-int(imageHeight/2)
    self.create_image(x+imageX,y+imageY,anchor='nw',image=img)
   elif cellType=="Button":
    pass
   else:
     contentWidth=dataFont.measure(cellContent)
     contentHeight=dataFont.metrics("linespace")
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     contentX,contentY=eval(f"self.{contentAlignment}")(contentWidth,contentHeight,cellWidth-10,cellHeight)
     self.create_text(x+contentX+5,y+contentY,font=dataFont,text=cellContent,anchor='nw')
   x+=self.model.getColumnWidth(c) 
  callBack=self.customEvents["<RowSelectionChanged>"]
  if callBack!=None: callBack(oldRowIndex,newRowIndex)
  
 def update(self): 
  x1=10
  y1=10
  x2=x1+self.width-10
  y2=y1+self.height-10
  self.x1=x1
  self.y1=y1
  self.x2=x2
  self.y2=y2
  self.create_rectangle(x1,y1,x2,y2,fill="#E0E0E0",width=1)  
  left=x1+1
  right=x2-1
  top=y1+1
  rowHeight=self.rowHeight
  self.create_rectangle(left,top,right,top+rowHeight,fill="black")
  top+=rowHeight
  rows=self.model.getRowCount()
  for i in range(rows+1):
   y=top+i*rowHeight
   self.create_line(left,y,right,y,fill="#ADADAD")     
   self.create_line(left,y+1,right,y+1,fill="white")     
  columns=self.model.getColumnCount()
  top=y1+1
  bottom=y2-1
  x=left
  for i in range(columns-1):
   x+=self.model.getColumnWidth(i)  
   self.create_line(x+1,top,x+1,bottom,fill="white")
   self.create_line(x,top,x,bottom,fill="#ADADAD")
  titleFont=self.titleFont
  columnTitleHeight=titleFont.metrics("linespace")
  x=left
  for i in range(columns):
   columnTitle=self.model.getColumnTitle(i)
   if columnTitle is None : continue
   columnTitleWidth=titleFont.measure(columnTitle)
   cellHeight=rowHeight
   cellWidth=self.model.getColumnWidth(i)
   titleX=int(cellWidth/2)-int(columnTitleWidth/2)
   titleY=int(cellHeight/2)-int(columnTitleHeight/2)
   self.create_text(x+titleX,top+titleY,font=titleFont,text=columnTitle,fill="white",anchor='nw')
   x=x+cellWidth  
  dataFont=self.dataFont
  dataFontHeight=dataFont.metrics("linespace")
  y=y1+1+rowHeight
  for r in range(rows):
   x=left
   for c in range(columns):
    cellType=self.model.getCellType(r,c)
    contentAlignment=self.model.getContentAlignment(r,c)
    if cellType=="PhotoImage":
     cellContent=self.model.getValueAt(r,c)
     if cellContent not in self.images: self.images[cellContent]=tkinter.PhotoImage(file=cellContent)
     img=self.images[cellContent]
     imageWidth=img.width()
     imageHeight=img.height()
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     imageX=int(cellWidth/2)-int(imageWidth/2)
     imageY=int(cellHeight/2)-int(imageHeight/2)
     self.create_image(x+imageX,y+imageY,anchor='nw',image=img)
    elif cellType=="Button":
     button=self.model.getValueAt(r,c,self)
     buttonWidth=button['width']
     buttonHeight=button['height']
     cellHeight=self.rowHeight
     cellWidth=self.model.getColumnWidth(c)
     buttonX=int(cellWidth/2)-int(buttonWidth/2)
     buttonY=int(cellHeight/2)-int(buttonHeight/2)
     button.config(command=lambda x=r,y=c: self.canvasWidgetClickHandler(x,y))
     self.create_window(x+buttonX-3,y+buttonY-1,anchor='nw',window=button)
    else:
     cellContent=self.model.getValueAt(r,c)
     contentWidth=dataFont.measure(cellContent)
     contentHeight=dataFont.metrics("linespace")
     cellHeight=rowHeight
     cellWidth=self.model.getColumnWidth(c)
     contentX,contentY=eval(f"self.{contentAlignment}")(contentWidth,contentHeight,cellWidth-10,cellHeight)
     self.create_text(x+contentX+5,y+contentY,font=dataFont,text=cellContent,anchor='nw')
    x+=self.model.getColumnWidth(c) 
   y+=rowHeight 
 
 def center(self,contentWidth,contentHeight,cellWidth,cellHeight):
  contentX=int(cellWidth/2)-int(contentWidth/2)
  contentY=int(cellHeight/2)-int(contentHeight/2)
  return (contentX,contentY)
 def left(self,contentWidth,contentHeight,cellWidth,cellHeight):
  contentY=int(cellHeight/2)-int(contentHeight/2)
  return (0,contentY)
 def right(self,contentWidth,contentHeight,cellWidth,cellHeight):
  contentX=cellWidth-contentWidth
  contentY=int(cellHeight/2)-int(contentHeight/2)
  return (contentX,contentY)
 def bind(self,event,callBack):
  if event in self.customEvents: self.customEvents[event]=callBack
  else: super().bind(event,callBack)

def dosomething(oldRowIndex,newRowIndex):
 print(f"Old row index : {oldRowIndex}, New row index : {newRowIndex}")

def editClicked(rowIndex,columnIndex):
 u=model.data[rowIndex]
 print(u.name)
 if columnIndex==2: print("Accept Clicked") 
 elif columnIndex==3: print("Decline Clicked")

window=tkinter.Tk()
model=DataModel()
model.editCommand=editClicked
window.geometry("650x650")

titleFont=tkinter.font.Font(family="Comic Sans MS",size=11,weight="bold")
dataFont=tkinter.font.Font(family="Comic Sans MS",size=11)
tmGrid=TMGrid(window,model,190,600,30,titleFont,dataFont)
tmGrid.grid(row=0,column=0)
tmGrid.bind("<RowSelectionChanged>",dosomething)
tmGrid.pack(fill=tkinter.BOTH,expand=1)
window.mainloop()