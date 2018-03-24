#!/usr/bin/env python3

from win32api import (
		GetModuleHandle, GetSystemMetrics, RGB
	)
from win32gui import (
		WNDCLASS, LoadCursor, GetStockObject, RegisterClass, DrawText,
		CreateWindowEx, PostQuitMessage, DefWindowProc, EndPaint, GetClientRect,
		SetTextColor, BeginPaint, RedrawWindow, PumpMessages, ShowWindow, 
		UpdateWindow, MoveWindow, SetLayeredWindowAttributes
	)
from win32con import (
		CS_HREDRAW, CS_VREDRAW, DT_SINGLELINE, DT_CENTER, DT_VCENTER, WM_DESTROY,
		WM_PAINT, RDW_INVALIDATE, RDW_ERASE, SM_CXSCREEN, SW_SHOWNORMAL, LWA_COLORKEY,
		LWA_ALPHA, SM_CXSCREEN, SM_CYSCREEN, WS_EX_COMPOSITED, WS_EX_LAYERED, WS_EX_NOACTIVATE,
		WS_EX_TOPMOST, WS_DISABLED, WS_POPUP, WS_VISIBLE, WS_EX_TRANSPARENT, IDC_ARROW, WHITE_BRUSH
	)
from time import sleep, gmtime, strftime
from threading import Thread
from datetime import datetime

def main():
	hInstance = GetModuleHandle()

	className = 'hXD'

	wndClass                = WNDCLASS()
	wndClass.style          = CS_HREDRAW | CS_VREDRAW
	wndClass.lpfnWndProc    = wndProc
	wndClass.hInstance      = hInstance
	wndClass.hCursor        = LoadCursor(None, IDC_ARROW)
	wndClass.hbrBackground  = GetStockObject(WHITE_BRUSH)
	wndClass.lpszClassName  = className

	wndClassAtom = RegisterClass(wndClass)
	exStyle = WS_EX_COMPOSITED | WS_EX_LAYERED | WS_EX_NOACTIVATE | WS_EX_TOPMOST | WS_EX_TRANSPARENT
	style = WS_DISABLED | WS_POPUP | WS_VISIBLE

	hWindow = CreateWindowEx(
		exStyle,
		wndClassAtom,
		None,
		style,
		0,
		0,
		GetSystemMetrics(SM_CXSCREEN),
		GetSystemMetrics(SM_CYSCREEN),
		None,
		None,
		hInstance,
		None
	)

	SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, LWA_COLORKEY | LWA_ALPHA)

	ShowWindow(hWindow, SW_SHOWNORMAL)
	UpdateWindow(hWindow)
	MoveWindow(
		hWindow, 
		int(
			(GetSystemMetrics(SM_CXSCREEN) / 2) - 130
		), 
		0, 
		260, 
		30, 
		True
	)

	thr = Thread(target=customDraw, args=(hWindow,))
	thr.setDaemon(False)
	thr.start()

	PumpMessages()

def customDraw(hWindow):
	global windowText
	while True:
		sleep(1)
		windowText = getText()
		RedrawWindow(hWindow, None, None, RDW_INVALIDATE | RDW_ERASE)

def getText():
	return strftime('%X - %A, %B %d %Y', gmtime())

def wndProc(hWnd, message, wParam, lParam):

	if message == WM_PAINT:
		hDC, paintStruct = BeginPaint(hWnd)

		SetTextColor(hDC, wRGB(245, 215, 110))

		rect = GetClientRect(hWnd)
		DrawText(
			hDC,
			getText(),
			-1,
			rect,
			DT_SINGLELINE | DT_CENTER | DT_VCENTER
		)

		EndPaint(hWnd, paintStruct)
		return 0

	elif message == WM_DESTROY:
		PostQuitMessage(0)
		return 0

	else:
		return DefWindowProc(hWnd, message, wParam, lParam)

if __name__ == '__main__':
	print('[+] Screen detected [x:{0},y:{1}]'.format(
		GetSystemMetrics(SM_CXSCREEN),
		GetSystemMetrics(SM_CYSCREEN)
	))
	main()
