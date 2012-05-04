#!/usr/bin/python
# -*- coding: utf-8 -*-

# MKMySql.py
# jwu April 2, 2012

import base64, os
import MKconfig, MKMySql, MKController, MKUtils


def ListUsers(condition):
# @parm condition:		List-Sets		[(Fiels, operator, value),...] (ex. ('Name', '==', 'Ali'))
# @ return json
	RQfields = ['ID','EMAIL','USER_HANDLE', 'FULL_NAME', 'JOINED']
	rows = MKController.GetUsers(RQfields, condition)
	# yield the JSON
	users= []
	for row in rows:
		hash = {}
		for i in xrange(len(RQfields)):
			hash[RQfields[i]] = str(row[i])
		users.append(hash)
	return users

def ListKloudlets(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return json
	# get the required fields
	RQfields = ['ID', 'NAME', 'CREATED_BY', 'DESCRIPTION','ACCESS', 'PIN', 'CREATED_ON']
	rows = MKController.GetKloudlets(RQfields, condition)
	
	# yield the JSON
	kloudlets= []
	for row in rows:
		tmp_hash = {}
		for i in xrange(len(RQfields)):
			tmp_hash[RQfields[i]] = str(row[i])
		kloudlets.append(tmp_hash)
	return kloudlets
	

def ListKloudletsWithCover(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return json
	# get the required fields
	RQfields = ['ID', 'BLOBDATA', 'NAME', 'CREATED_BY', 'DESCRIPTION','ACCESS', 'PIN', 'CREATED_ON', ]
	rows = MKController.GetKloudletsWithCover(RQfields, condition)

	# yield the JSON
	kloudlets= []
	for row in rows:
		hash = {}
		for i in xrange(len(RQfields)):
			if (i == 1) and (row[i]!=None) :
				hash[RQfields[i]] = base64.b64encode(row[i])
			else:
				hash[RQfields[i]] = str(row[i])
		kloudlets.append(hash)
	return kloudlets

def ListMoments(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return json
	# get the required fields
	RQfields = ['ID', 'TYPE', 'TEXT', 'MEDIA_ID', 'BLOBDATA', 'URL', 'GEOLOCATION', 'PARENTID', 'CREATED_BY', 'CREATED_ON']
	rows = MKController.GetMoments(RQfields, condition)
	
	# yield the JSON
	moments= []
	for row in rows:
		hash = {}
		for i in xrange(len(RQfields)):
			if (i == 4) and (row[i]!=None) :
				hash[RQfields[i]] = base64.b64encode(row[i])
			else:
				hash[RQfields[i]] = str(row[i])
		moments.append(hash)
	return moments

def ListMomentsByKloudletId(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return json
	# get the required fields
	RQfields = ['ID', 'TYPE', 'TEXT', 'MEDIA_ID', 'BLOBDATA', 'URL', 'GEOLOCATION', 'PARENTID', 'CREATED_BY', 'CREATED_ON']
	rows = MKController.GetMomentsByKloudletId(RQfields, condition)
	
	# yield the JSON
	moments= []
	for row in rows:
		hash = {}
		for i in xrange(len(RQfields)):
			if (i == 4) and (row[i]!=None) :
				hash[RQfields[i]] = base64.b64encode(row[i])
			else:
				hash[RQfields[i]] = str(row[i])
		moments.append(hash)
	return moments


def ListMoments2(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return json
	# get the required fields
	RQfields = ['ID', 'TYPE', 'TEXT', 'MEDIA_ID', 'BLOBDATA', 'URL', 'GEOLOCATION', 'PARENTID', 'CREATED_BY', 'CREATED_ON']
	rows = MKController.GetMoments(RQfields, condition)
	
	# yield the JSON
	moments= []
	for row in rows:
		hash = {}
		for i in xrange(len(RQfields)):
			if (i == 4) and (row[i]!=None) :
				filePath = MKUtils.GetSubFolder() + "momentId_" + str(row[0]) + ".jpg"
				if (not os.path.exists(filePath)):
					with open(filePath, "wb") as output_file:
						output_file.write(row[i])
				hash[RQfields[i]] = filePath
			else:
				hash[RQfields[i]] = str(row[i])
		moments.append(hash)
	return moments

def ListMomentsByKloudletId2(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return json
	# get the required fields
	RQfields = ['ID', 'TYPE', 'TEXT', 'MEDIA_ID', 'BLOBDATA', 'URL', 'GEOLOCATION', 'PARENTID', 'CREATED_BY', 'CREATED_ON']
	rows = MKController.GetMomentsByKloudletId(RQfields, condition)
	
	# yield the JSON
	moments= []
	for row in rows:
		hash = {}
		for i in xrange(len(RQfields)):
			if (i == 4) and (row[i]!=None) :
				filePath = MKUtils.GetSubFolder() + "momentId_" + str(row[0]) + ".jpg"
				if (not os.path.exists(filePath)):
					with open(filePath, "wb") as output_file:
						output_file.write(row[i])
				hash[RQfields[i]] = filePath
			else:
				hash[RQfields[i]] = str(row[i])
		moments.append(hash)
	return moments