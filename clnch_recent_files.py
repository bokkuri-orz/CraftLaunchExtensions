# coding: utf-8

# config.py に登録
# import clnch_recent_files
# clnch_recent_files.regist_recent_files(window)


import os
import ctypes
import glob
from ctypes.wintypes import MAX_PATH
from clnch import *
from stat import *

# 登録時にメインウィンドウを保存する
g_window = None

# コマンド本体
def command_recent_files():
	global g_window
	window = g_window
	
	# 「最近使った項目」のパスを取得
	path = getRecentFilesPath()
	
	# ファイル一覧を取得
	items = None
	if path != None:
		items = glob.glob(path + "\\*.*")

	# ソート
	if items != None and len(items) > 0:

		# 辞書作成
		fileDict = {}

		fileArray = []

		for item in items:
			fullPath = item
			stat = os.stat(fullPath)

			# ディレクトリ以外を辞書に登録
			if os.path.isfile(fullPath):
				last_modified = stat.st_mtime
				# タイムスタンプが同じファイルも存在するので、ファイル名の配列を辞書に登録する
				if not last_modified in fileDict:
					fileDict[last_modified] = []
				fileDict[last_modified].append(os.path.basename(item))

		# キー(更新日時)でソートする
		for key, value in sorted(fileDict.items(), reverse=True):
			# valueは配列なので
			for item in value:
				fileArray.append(item)

		# ファイル一覧置き換え
		items = fileArray

	if items != None and len(items) > 0:
		# ファイルリスト表示
		select = 0
		select = clnch_listwindow.popMenu(window, 60, 20, u"Recent files", items, select)
	
		# ファイルが選択されたら、それを開く
		if select >= 0:
			os.startfile(path + "\\" + items[select])

# 「最近使った項目」のパスを取得
def getRecentFilesPath():
	CSIDL_RECENT = 0x0008
	
	path = None
	
	buf = ctypes.create_unicode_buffer(MAX_PATH)
	if ctypes.windll.shell32.SHGetSpecialFolderPathW( None, buf, CSIDL_RECENT, 0 ):
		path = buf.value
	
	return path

# CraftLaunchに登録する関数
def regist_recent_files(window):
	global g_window
	g_window = window
	
	window.launcher.command_list += [(u"Recent", command_recent_files)]

