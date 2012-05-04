# MKController.py
# April 9th, 2012 JWU
# Utilities 

import os, time
import MKconfig

def GetSubFolder():
	SubFolder = time.strftime("%Y%m%d")
	FolderPath = MKconfig.FSFile + SubFolder + "/" 
	if not os.path.exists(FolderPath):
		os.makedirs(FolderPath)
	return FolderPath


def GetFile(File_Path):
	ResponseCode = 404
	ContentBody = None
	ContentType = File_Path[-4:]
	try:
		if ContentType == '.jpg':
			ContentType ='image/jpeg'
			f = open (File_Path, 'rb')
			ContentBody = f.read()
			f.close()
			ResponseCode = 200
	finally:
		return ResponseCode, ContentType, ContentBody
		