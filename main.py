#!/usr/bin/pyhthon
import wx
import wx.lib.dialogs
import wx.stc as stc
import os
import sys

#Create font faces for different systems
if wx.Platform == '__WXMSW__':
	faces = {
		'times': 'Times New Roman',
		'mono' : 'Courier New',
		'helv' : 'Arial',
		'other': 'Comic Sans MS',
		'size' : 10,
		'size2': 8,
}
elif wx.Platform == '__WXMAC__':
    faces = {
        'times': 'Times New Roman',
        'mono' : 'Monaco',
        'helv' : 'Arial',
        'other': 'Comic Sans MS',
        'size' : 10,
        'size2': 8,
}
else:
    faces = {
        'times': 'Times',
        'mono' : 'Courier New',
        'helv' : 'Helvetica',
        'other': 'new century schoolbook',
        'size' : 10,
        'size2': 8,
}

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		self.leftMarginWidth = 30
		self.dirName = ''
		self.fileName = ''
		self.extension = ''
		self.fold_symbols = 2;

		self.htmlKeywords = ["a", "abbr", "acronym", "address", "applet", "area", "b", "base", "basefont", "bdo", "big",
		 "blockquote","body", "br", "button", "caption", "center","cite", "code", "col", "colgroup", "dd", "del", "dfn", "dir",
		 "div", "dl", "dt", "em", "fieldset", "font", "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head",
		 "hr", "html", "i", "iframe", "img", "input", "ins", "isindex", "kbd", "label", "legend", "li", "link", "map", "menu",
		 "meta", "noframes", "noscript", "object", "ol", "optgroup", "option", "p", "param", "pre", "q", "s", "samp", "script",
		 "select", "small", "span", "strike", "strong", "style", "sub", "sup", "table", "tbody", "td", "textarea", "tfoot", "th",
		 "thead", "title", "tr" ,"tt", "u", "ul", "var", "xml", "xmlns", "abbr", "accept-charset", "accept", "accesskey", 
		 "action" ,"align", "alink", "alt", "archive", "axis", "background", "bgcolor", "border", "cellpadding", "cellspacing",
		 "char", "charoff", "charset", "checked", "cite", "class", "classid", "clear", "codebase", "codetype", "color", "cols",
		 "colspan", "compact", "content", "coords","data", "datafld", "dataformatas", "datapagesize", "datasrc", "datetime", 
		 "declare", "defer","dir", "disabled", "enctype", "event", "face", "for", "frame", "frameborder", "headers", "height",
		 "href", "hreflang", "hspace", "http-equiv", "id", "ismap", "label", "lang", "language", "leftmargin", "link", "longdesc",
		 "marginwidth", "marginheight", "maxlength", "media", "method", "multiple", "name", "nohref", "noresize", "noshade", 
		 "nowrap", "object", "onblur", "onchange", "onclick", "ondblclick", "onfocus", "onkeydown", "onkeypress", "onkeyup", 
		 "onload", "onmousedown", "onmousemove", "onmouseover", "onmouseout", "onmouseup", "onreset","onselect", "onsubmit", 
		 "onunload", "profile", "prompt", "readonly", "rel", "rev", "rows", "rowspan", "rules", "scheme", "scope", "selected", 
		 "shape", "size", "span", "src", "standby", "start", "style", "summary", "tabindex", "target","text", "title", 
		 "topmargin","type", "usemap", "valign", "value", "valuetype", "version", "vlink", "vspace", "width", "text", "password",
		 "checkbox", "radio", "submit", "reset" ,"file" ,"hidden", "image", "public", "!DOCTYPE"]

		#Create frame with a with of 1280 x 720
		wx.Frame.__init__(self,parent,title=title,size=(1280,720))

		#Create the styledTextController
		self.control = stc.StyledTextCtrl(self,wx.TE_MULTILINE|wx.TE_WORDWRAP)

		self.control.SetLexer(stc.STC_LEX_HTML)
		self.control.SetKeyWords(4," ".join(self.htmlKeywords))

		#Set the fold property
		self.control.SetProperty("fold", "1")
		self.control.SetProperty("tab.timmy.whinge.level", "1")
		self.control.SetMargins(0,0)

		#Create bar for RowNumbers
		self.control.SetViewWhiteSpace(False)
		self.control.SetMargins(5,0)
		self.control.SetMarginType(1,stc.STC_MARGIN_NUMBER)
		self.control.SetMarginWidth(1,self.leftMarginWidth)

		#Create bar for the folding lines
		self.control.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
		self.control.SetMarginMask(2, stc.STC_MASK_FOLDERS)
		self.control.SetMarginSensitive(2, True)
		self.control.SetMarginWidth(2, 12)

		#create the status bar on the bottom
		self.CreateStatusBar()

		#Create the file submenu
		fileMenu = wx.Menu()

		#Create the options for the FileMenu
		fileMenuNew = fileMenu.Append(wx.ID_NEW, "&New", "Create a new file")
		fileMenuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "Open an existing file")
		fileMenuSave = fileMenu.Append(wx.ID_SAVE, "&Save", "Save the current file")
		fileMenuSaveAs = fileMenu.Append(wx.ID_SAVEAS, "Save &As", "Save file as new")

		#Create a line to represent a saperator
		fileMenu.AppendSeparator()

		#Option to close the application
		fileMenuClose = fileMenu.Append(wx.ID_EXIT,"&Close", "Close the FreeTimeDev Editor")

		#Create the submenu called Editor
		editMenu = wx.Menu()
		#Create the options for the editMenu
		editMenuUndo = editMenu.Append(wx.ID_UNDO, "&Undo", "Undo the last action")
		editMenuRedo = editMenu.Append(wx.ID_REDO, "&Redo", "Redo the undone action")
		editMenuSelectAll = editMenu.Append(wx.ID_SELECTALL, "&Select All", "Select everything in the document")
		editMenuCopy = editMenu.Append(wx.ID_COPY, "&Copy", "Copy the selected text")
		editMenuCut = editMenu.Append(wx.ID_CUT, "&Cut", "Cut the selected text")
		editMenuPaste = editMenu.Append(wx.ID_PASTE, "&Paste", "Paste text from the clipboard")

		#Create the submenu called Extras
		extraMenu = wx.Menu()
		#Create the options for the extraMenu
		extraHtml = extraMenu.Append(wx.ID_ANY, "&Basic HTML5 template", "Load a basic HTML5 template to edit")
		extraCpp = extraMenu.Append(wx.ID_ANY, "&Basic C++ template", "Load in a basic C++ template")
		extraPython = extraMenu.Append(wx.ID_ANY, "&Basic Python template", "Load in a basic Python template")

		#Create the submenu called Help
		helpMenu = wx.Menu()
		#Create the options for the helpMenu
		helpMenuHelp = helpMenu.Append(wx.ID_ANY, "&Help", "Are you okay?")
		helpMenuAbout = helpMenu.Append(wx.ID_ABOUT, "&About", "About the FreeTimeDev Editor")

		#Create the MenuBar and add it to the window
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")
		menuBar.Append(editMenu, "&Edit")
		menuBar.Append(extraMenu, "&Extra")
		menuBar.Append(helpMenu, "&Help")
		self.SetMenuBar(menuBar)
		self.createFolding()

		#Zoom in and zoom out
		self.control.CmdKeyAssign(ord('='),stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
		self.control.CmdKeyAssign(ord('-'),stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
		#Eventhandlers for the fileTab
		self.Bind(wx.EVT_MENU, self.newFile,fileMenuNew)
		self.Bind(wx.EVT_MENU, self.openFile,fileMenuOpen)
		self.Bind(wx.EVT_MENU, self.saveFile,fileMenuSave)
		self.Bind(wx.EVT_MENU, self.saveAs,fileMenuSaveAs)
		self.Bind(wx.EVT_MENU, self.closeApp,fileMenuClose)

		#EventHandlers for the EditTab
		self.Bind(wx.EVT_MENU, self.controlUndo,editMenuUndo)
		self.Bind(wx.EVT_MENU, self.controlRedo,editMenuRedo)
		self.Bind(wx.EVT_MENU, self.controlSelectAll,editMenuSelectAll)
		self.Bind(wx.EVT_MENU, self.controlCopy,editMenuCopy)
		self.Bind(wx.EVT_MENU, self.controlCut,editMenuCut)
		self.Bind(wx.EVT_MENU, self.controlPaste,editMenuPaste)

		#EventHandlers for the HelpTab
		self.Bind(wx.EVT_MENU, self.helpMe,helpMenuHelp)
		self.Bind(wx.EVT_MENU, self.aboutUs,helpMenuAbout)

		#EventHandlers for the Extras tab
		self.Bind(wx.EVT_MENU, self.basicHTML5,extraHtml)
		self.Bind(wx.EVT_MENU, self.basicCpp,extraCpp)
		self.Bind(wx.EVT_MENU, self.basicPython,extraPython)

		#Update the line and column
		self.control.Bind(wx.EVT_KEY_UP,self.lineAndCol)
		self.control.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
		self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
		self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)

		#show the window
		self.Show()

		#Create the variables to hold the styling values
		self.backgroundColour=None
		self.selBackColour=None
		self.lineIndexBackColour=None
		self.lineIndexForeColour=None
		self.braceLightForeColour=None
		self.braceLightBackColour=None
		self.braceBadForeColour=None
		self.braceBadBackColour=None
		self.defaultForeColour=None
		self.defaultBackColour=None
		self.commentForeColour=None
		self.commentBackColour=None
		self.numbersForeColour=None
		self.numbersBackColour=None
		self.stringForeColour=None
		self.stringBackColour=None
		self.singleQuoteStringForeColour=None
		self.singleQuoteStringBackColour=None
		self.keywordForeColour=None
		self.keywordBackColour=None
		self.tripleQuoteForeColour=None
		self.tripleQuoteBackColour=None
		self.tripleDoubleForeColour=None
		self.tripleDoubleBackColour=None
		self.classNameForeColour=None
		self.classNameBackColour=None
		self.functionNameForeColour=None
		self.functionNameBackColour=None
		self.operatorForeColour=None
		self.operatorBackColour=None
		self.identifierForeColour=None
		self.identifierBackColour=None
		self.commentBlockForeColour=None
		self.commentBlockBackColour=None
		self.stringEOLForeColour=None
		self.stringEOLBackColour=None
		self.caretForegroundColour=None
		self.caretBackgroundColour=None

		#Load in the theme from the dat file
		self.setTheme()

		#Set the defaultfonts and colours
		self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(mono)s" %faces)
		self.control.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:"+self.braceLightForeColour+",back:"+self.braceLightBackColour+",bold")
		self.control.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:"+self.braceBadForeColour+",back:"+self.braceBadBackColour+",bold")
		self.control.StyleClearAll()
		
		self.setHtmlStyle()

		self.control.SetCaretForeground(self.caretForegroundColour)
		self.control.SetCaretLineBackground(self.caretBackgroundColour)
		self.control.SetCaretLineVisible(True)

		#Set the line and column in the statusBar
		self.lineAndCol(self)

		#Set image for the Keywords
		self.control.RegisterImage(2,wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16,16)))

	#Set the colours for the folding markers
	def createFolding(self):
		if self.fold_symbols == 0:
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_ARROWDOWN, "black", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_ARROW, "black", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "black", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "black", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")
		elif self.fold_symbols == 1:
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_MINUS, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_PLUS, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")
		elif self.fold_symbols == 2:
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_CIRCLEMINUS, "white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_CIRCLEPLUS, "white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNERCURVE, "white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_CIRCLEPLUSCONNECTED, "white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE, "white", "#404040")
		elif self.fold_symbols == 3:
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "#808080")

	def OnKeyPressed(self, event):
			#save the keycode in a variable
			key = event.GetKeyCode()
			#Check if the tipWindow is open
			if self.control.CallTipActive():
				#Close the window if you start typing
				self.control.CallTipCancel()

			#Check if ctrl+space is pressed
			if key == 32 and event.ControlDown():
				#Save the current position in a variable
				pos = self.control.GetCurrentPos()

				#First check if the shift is pressed as well
				if event.ShiftDown():
					#If so, open the tip window
					self.control.CallTipSetBackground("#444")
					self.control.CallTipShow(pos, 'im dying')
				#if not
				else:
					#Create an array for the keywords
					kw = self.htmlKeywords
					#Sort the
					kw.sort()
					#Make autocomplete case insensitive
					self.control.AutoCompSetIgnoreCase(False)
					#Show the autocomplete window
					self.control.AutoCompShow(0, " ".join(kw))
			else:
				#skip the event
				event.Skip()

	#Higligh the braces when the caret is next to them
	def OnUpdateUI(self, evt):
			braceAtCaret = -1
			braceOpposite = -1
			charBefore = None
			caretPos = self.control.GetCurrentPos()

			if caretPos > 0:
				charBefore = self.control.GetCharAt(caretPos - 1)
				styleBefore = self.control.GetStyleAt(caretPos - 1)

				# check before
				if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
					braceAtCaret = caretPos - 1

			# check after
			if braceAtCaret < 0:
				charAfter = self.control.GetCharAt(caretPos)
				styleAfter = self.control.GetStyleAt(caretPos)

			if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
				braceAtCaret = caretPos

			if braceAtCaret >= 0:
				braceOpposite = self.control.BraceMatch(braceAtCaret)

			if braceAtCaret != -1  and braceOpposite == -1:
				self.control.BraceBadLight(braceAtCaret)
			else:
				self.control.BraceHighlight(braceAtCaret, braceOpposite)

	#cheek
	def OnMarginClick(self, evt):
			if evt.GetMargin() == 2:
				if evt.GetShift() and evt.GetControl():
					self.control.FoldAll()
				else:
					lineClicked = self.control.LineFromPosition(evt.GetPosition())

				if self.control.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
					if evt.GetShift():
						self.control.SetFoldExpanded(lineClicked, True)
						self.control.Expand(lineClicked, True, True, 1)
					elif evt.GetControl():
						if self.control.GetFoldExpanded(lineClicked):
							self.control.SetFoldExpanded(lineClicked, False)
							self.control.Expand(lineClicked, False, True, 0)
						else:
							self.control.SetFoldExpanded(lineClicked, True)
							self.control.Expand(lineClicked, True, True, 100)
					else:
						self.control.ToggleFold(lineClicked)

	def FoldAll(self):
			lineCount = self.control.GetLineCount()
			expanding = True

			#find out if we are folding or unfolding
			for lineNum in range(lineCount):
				if self.control.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
					expanding = not self.control.GetFoldExpanded(lineNum)
					break

				lineNum = 0
				while lineNum < lineCount:
					level = self.control.GetFoldLevel(lineNum)
					if level & stc.STC_FOLDLEVELHEADERFLAG and \
						(level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

						if expanding:
							self.control.SetFoldExpanded(lineNum, True)
							lineNum = self.control.Expand(lineNum, True)
							lineNum = lineNum - 1
					else:
						lastChild = self.control.GetLastChild(lineNum, -1)
						self.control.SetFoldExpanded(lineNum, False)

					if lastChild > lineNum:
						self.control.HideLines(lineNum+1, lastChild)

					lineNum = lineNum + 1

	def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
			lastChild = self.control.GetLastChild(line, level)
			line = line + 1

			while line <= lastChild:
				if force:
					if visLevels > 0:
						self.control.ShowLines(line, line)
					else:
						self.control.HideLines(line, line)
				else:
					if doExpand:
						self.control.ShowLines(line, line)

			if level == -1:
				level = self.control.GetFoldLevel(line)

			if level & stc.STC_FOLDLEVELHEADERFLAG:
				if force:
					if visLevels > 1:
						self.control.SetFoldExpanded(line, True)
					else:
						self.control.SetFoldExpanded(line, False)

						line = self.control.Expand(line, doExpand, force, visLevels-1)

				else:
					if doExpand and self.control.GetFoldExpanded(line):
						line = self.control.Expand(line, True, force, visLevels-1)
					else:
						line = self.control.Expand(line, False, force, visLevels-1)
			else:
				line = line + 1
				return line

	def newFile(self, e):
			self.fileName = ''
			self.control.SetValue('Check out www.freetimedev.com for some HTML lessons')

	def openFile(self,e):
			try:
				dlg = wx.FileDialog(self, "Choose your file", self.dirName, "", "*.*",wx.FD_OPEN)
				if (dlg.ShowModal()==wx.ID_OK):
					self.fileName = dlg.GetFilename()
					self.dirName = dlg.GetDirectory()
					f = open(os.path.join(self.dirName,self.fileName), 'r')
					self.control.SetValue(f.read())
					f.close()
				dlg.Destroy()
			except:
				dlg = wx.MessageDialog(self,"Failed to open the file...", "Error",wx.ICON_ERROR)
				dlg.ShowModal()
				dlg.Destroy()

	def saveFile(self,e):
			try:
				f=open(os.path.join(self.dirName,self.fileName),'w')
				f.write(self.control.GetValue())
				f.close()
			except:
				try:
					dlg = wx.FileDialog(self,"Save file as...",self.dirName, "Untitled", "*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
					if(dlg.ShowModal()==wx.ID_OK):
						self.fileName = dlg.GetFilename()
						self.dirName = dlg.GetDirectory()
						f = open(os.path.join(self.dirName, self.fileName),"w")
						f.write(self.control.GetValue())
						f.close()
						self.setTheme()
						self.setHtmlStyling()
					dlg.Destroy()
				except:
					pass

	def saveAs(self,e):
			try:
				dlg = wx.FileDialog(self,"Save file as...",self.dirName, "Untitled", "*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
				if(dlg.ShowModal()==wx.ID_OK):
					self.fileName = dlg.GetFilename()
					self.dirName = dlg.GetDirectory()
					f = open(os.path.join(self.dirName, self.fileName),"w")
					f.write(self.control.GetValue())
					f.close()
				dlg.Destroy()
			except:
				pass

	def closeApp(self,e):
			self.Close(True)

	def controlUndo(self,e):
			self.control.Undo()

	def controlRedo(self,e):
			self.control.Redo()

	def controlSelectAll(self,e):
			self.control.SelectAll()

	def controlCopy(self,e):
			self.control.Copy()

	def controlCut(self,e):
			self.control.Cut()

	def controlPaste(self,e):
			self.control.Paste()

	def helpMe(self,e):
			dlg = wx.lib.dialogs.ScrolledMessageDialog(self,"This is a just a texteditor, do you actually need any help?\n\nIf you want to alter the styling, open config/*.dat depending on which language of highlighting you want to alter\n\nNOTICE: YOU ARE RESPONSIBLE FOR ANY DAMAGE THAT MAY OCCUR AFTER CHANGING THE CODE, DO NOT EDIT THE FILES WITHOUT ANY KNOWLEDGE ON PYTHON AND WX!!!", "How to...",size=(700,500))
			dlg.ShowModal()
			dlg.Destroy()

	def aboutUs(self,e):
			dlg = wx.MessageDialog(self, "This texteditor is part of www.freetimedev.com.\n For free HTML/PHP/UNITYC# code, visit www.freetimedev.com", "About",wx.OK)
			dlg.ShowModal()
			dlg.Destroy()

	def lineAndCol(self,e):
			line = self.control.GetCurrentLine()+1
			col = self.control.GetColumn(self.control.GetCurrentPos())
			stat = "Line %s, Column %s" % (line,col)
			self.StatusBar.SetStatusText(stat,0)

	def basicHTML5(self,e):
			self.control.SetValue('<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset="utf-8">\n\t<meta name="author" content="YOURNAME">\n\t<meta name="description" content="YOUR DESCRIPTION">\n\t<meta name="keywords" content="YOURKEYWORDS">\n\t<title>HTML5</title>\n</head>\n<body>\n\t<h1>HTML5</h1>\n</body>\n</html>')

	def basicCpp(self,e):
			self.control.SetValue('#include <iostream>\nusing namespace std;\n\nint main(int argc, char* argv[])\n{\n\tcout<<"Hello World"<<endl;\n}')

	def basicPython(self,e):
			self.control.SetValue('class MyClass():\n\tdef __init__(self):\n\tprint "Python is awesome"')

	def setTheme(self):
		'''
		try:
			theExtension = os.path.splitext(self.fileName)[1][1:]
			theme = open("config/"+theExtension+".dat","r")

		except:
			theme = open("config/default.dat","r")
		'''
		theme = open("config/default.dat","r")
		self.backgroundColour=theme.readline().split("=")[1]
		self.selBackColour=theme.readline().split("=")[1]
		self.lineIndexBackColour=theme.readline().split("=")[1]
		self.lineIndexForeColour=theme.readline().split("=")[1]
		self.braceLightForeColour=theme.readline().split("=")[1]
		self.braceLightBackColour=theme.readline().split("=")[1]
		self.braceBadForeColour=theme.readline().split("=")[1]
		self.braceBadBackColour=theme.readline().split("=")[1]
		self.defaultForeColour=theme.readline().split("=")[1]
		self.defaultBackColour=theme.readline().split("=")[1]
		self.commentForeColour=theme.readline().split("=")[1]
		self.commentBackColour=theme.readline().split("=")[1]
		self.numbersForeColour=theme.readline().split("=")[1]
		self.numbersBackColour=theme.readline().split("=")[1]
		self.stringForeColour=theme.readline().split("=")[1]
		self.stringBackColour=theme.readline().split("=")[1]
		self.singleQuoteStringForeColour=theme.readline().split("=")[1]
		self.singleQuoteStringBackColour=theme.readline().split("=")[1]
		self.keywordForeColour=theme.readline().split("=")[1]
		self.keywordBackColour=theme.readline().split("=")[1]
		self.tripleQuoteForeColour=theme.readline().split("=")[1]
		self.tripleQuoteBackColour=theme.readline().split("=")[1]
		self.tripleDoubleForeColour=theme.readline().split("=")[1]
		self.tripleDoubleBackColour=theme.readline().split("=")[1]
		self.classNameForeColour=theme.readline().split("=")[1]
		self.classNameBackColour=theme.readline().split("=")[1]
		self.functionNameForeColour=theme.readline().split("=")[1]
		self.functionNameBackColour=theme.readline().split("=")[1]
		self.operatorForeColour=theme.readline().split("=")[1]
		self.operatorBackColour=theme.readline().split("=")[1]
		self.identifierForeColour=theme.readline().split("=")[1]
		self.identifierBackColour=theme.readline().split("=")[1]
		self.commentBlockForeColour=theme.readline().split("=")[1]
		self.commentBlockBackColour=theme.readline().split("=")[1]
		self.stringEOLForeColour=theme.readline().split("=")[1]
		self.stringEOLBackColour=theme.readline().split("=")[1]
		self.caretForegroundColour=theme.readline().split("=")[1]
		self.caretBackgroundColour=theme.readline().split("=")[1]
		theme.close()

	def setHtmlStyle(self):
		'''Set all the colours and faces'''
		self.control.StyleSetSpec(stc.STC_HBA_COMMENTLINE, "fore:"+self.commentForeColour+",back:"+self.commentBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJA_COMMENT, "fore:"+self.commentForeColour+",back:"+self.commentBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_COMMENT, "fore:"+self.commentForeColour+",back:"+self.commentBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_H_SGML_COMMENT, "fore:"+self.commentForeColour+",back:"+self.commentBackColour+",face:%(mono)s,size:%(size)d"%faces)		
		self.control.StyleSetSpec(stc.STC_H_COMMENT, "fore:"+self.commentForeColour+",back:"+self.commentBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_HBA_DEFAULT, "fore:"+self.defaultForeColour+",back:"+self.defaultBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_HJA_DEFAULT, "fore:"+self.defaultForeColour+",back:"+self.defaultBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_HJ_DEFAULT, "fore:"+self.defaultForeColour+",back:"+self.defaultBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_H_DEFAULT, "fore:"+self.defaultForeColour+",back:"+self.defaultBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_H_OTHER, "fore:"+self.defaultForeColour+",back:"+self.defaultBackColour+",face:%(mono)s,size:%(size)d" %faces)

		self.control.StyleSetSpec(stc.STC_HJA_DOUBLESTRING, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_DOUBLESTRING, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_H_SGML_DOUBLESTRING, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_H_DOUBLESTRING, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_HJA_SINGLESTRING, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_SINGLESTRING, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_H_SINGLESTRING, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_H_ATTRIBUTE, "fore:"+self.stringForeColour+",back:"+self.stringBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_H_ATTRIBUTEUNKNOWN, "fore:"+self.stringForeColour+",back:"+self.stringBackColour+",face:%(mono)s,size:%(size)d, underline" %faces)

		self.control.StyleSetSpec(stc.STC_HBA_NUMBER, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_HJA_NUMBER, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_HJ_NUMBER, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_H_NUMBER, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)


		self.control.StyleSetSpec(stc.STC_H_TAG, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_H_TAGEND, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_H_TAGUNKNOWN, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d, line-through" %faces)

		self.control.StyleSetBackground(stc.STC_STYLE_DEFAULT,self.backgroundColour)
		self.control.StyleSetBackground(stc.STC_H_SGML_DEFAULT,self.backgroundColour)

		self.control.StyleSetSpec(stc.STC_H_VALUE, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)

		self.control.StyleSetSpec(stc.STC_H_ASP, "fore:"+self.numbersForeColour+",back:"+self.numbersBackColour+",face:%(mono)s,size:%(size)d" %faces)

		self.control.StyleSetSpec(stc.STC_HBA_STRINGEOL, "fore:"+self.stringEOLForeColour+",back:"+self.stringEOLBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_HJA_STRINGEOL, "fore:"+self.stringEOLForeColour+",back:"+self.stringEOLBackColour+",face:%(mono)s,size:%(size)d" %faces)
		self.control.StyleSetSpec(stc.STC_HJ_STRINGEOL, "fore:"+self.stringEOLForeColour+",back:"+self.stringEOLBackColour+",face:%(mono)s,size:%(size)d" %faces)

		self.control.StyleSetSpec(stc.STC_H_CDATA, "fore:"+self.classNameForeColour+",back:"+self.classNameBackColour+",face:%(mono)s,size:%(size)d" %faces)


		self.control.StyleSetSpec(stc.STC_H_ENTITY, "fore:"+self.identifierForeColour+",back:"+self.identifierBackColour+",face:%(mono)s,size:%(size)d, italic" %faces)
		self.control.StyleSetSpec(stc.STC_H_SGML_ENTITY, "fore:"+self.identifierForeColour+",back:"+self.identifierBackColour+",face:%(mono)s,size:%(size)d, italic" %faces)

		self.control.StyleSetSpec(stc.STC_H_XMLSTART, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_H_XMLEND, "fore:"+self.singleQuoteStringForeColour+",back:"+self.singleQuoteStringBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_HBA_WORD, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJA_WORD, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_WORD, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJA_KEYWORD, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_KEYWORD, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_H_ASPAT, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		
		self.control.StyleSetSpec(stc.STC_H_QUESTION, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		
		self.control.StyleSetSpec(stc.STC_H_SCRIPT, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		
		self.control.StyleSetSpec(stc.STC_H_XCCOMMENT, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		
		self.control.StyleSetSpec(stc.STC_HBA_IDENTIFIER, "fore:"+self.classNameForeColour+",back:"+self.classNameBackColour+",face:%(mono)s,size:%(size)d"%faces)
		
		self.control.StyleSetSpec(stc.STC_HBA_START, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJA_START, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_START, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_HBA_STRING, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		
		self.control.StyleSetSpec(stc.STC_HJA_COMMENTDOC, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_COMMENTDOC, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_HJA_COMMENTLINE, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_COMMENTLINE, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_HJA_REGEX, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_REGEX, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_HJA_SYMBOLS, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_HJ_SYMBOLS, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_H_SGML_ERROR, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_H_SGML_SIMPLESTRING, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_H_SGML_SPECIAL, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)

		self.control.StyleSetSpec(stc.STC_H_SGML_1ST_PARAM, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_H_SGML_1ST_PARAM_COMMENT, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)		

		self.control.StyleSetSpec(stc.STC_H_SGML_BLOCK_DEFAULT, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)
		self.control.StyleSetSpec(stc.STC_H_SGML_COMMAND, "fore:"+self.keywordForeColour+",back:"+self.keywordBackColour+",face:%(mono)s,size:%(size)d"%faces)


app = wx.App()
frame = MainWindow(None, "FTD Editor")
app.MainLoop()
