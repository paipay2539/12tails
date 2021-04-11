#Persistent
CoordMode, ToolTip, screen
AnyKeyPress = 0
CountDownTime = 0
Return
;~Space::
~q::
    If Active:=!Active
	{
        Sleep, 100
		SetTimer PreCheck, 100
        ;SetTimer NoMainTask, Off
	}
    Else
	{
        SetTimer PreCheck, Off
        ;SetTimer NoMainTask, 1000

	}
Return


PreCheck:
    gosub CheckAnyKeyPress
    If( AnyKeyPress = 0 )
    {
        gosub rightHold
    }
Return

rightHold:
    PixelGetColor, color, 1773, 73

    If ( color = 0x00DDFF )
    {
        SendInput, {right down}
        Sleep, 10
        SendInput, {right up}
        Sleep, 10
    }
    Else
    {
        SendInput, {space down}
        Sleep, 10
        SendInput, {space up}
        Sleep, 10
    }


    ;MouseGetPos, MouseX, MouseY
    ;PixelGetColor, color, %MouseX%, %MouseY%
    ;ToolTip, Screen :`t`tx %color% %MouseX% %MouseY%

Return

Esc::
    ExitApp
Return


CheckAnyKeyPress:

    GetKeyState, KeyPressUp,      w
    GetKeyState, KeyPressDown,    a
    GetKeyState, KeyPressRight,   s
    GetKeyState, KeyPressLeft,    d
    GetKeyState, KeyPress1,       1
    GetKeyState, KeyPress2,       2
    GetKeyState, KeyPress3,       3
    GetKeyState, KeyPress4,       4
    GetKeyState, KeyPress5,       5
    GetKeyState, KeyPress6,       6
    GetKeyState, KeyPress7,       7
    GetKeyState, KeyPress8,       8
    GetKeyState, KeyPress9,       9
    GetKeyState, KeyPress0,       0
    If (   KeyPressUp      = "D"
        Or KeyPressDown    = "D"
        Or KeyPressRight   = "D"
        Or KeyPressLeft    = "D"
        Or KeyPress1       = "D"
        Or KeyPress2       = "D"
        Or KeyPress3       = "D"
        Or KeyPress4       = "D"
        Or KeyPress5       = "D"
        Or KeyPress6       = "D"
        Or KeyPress7       = "D"
        Or KeyPress8       = "D"
        Or KeyPress9       = "D"
        Or KeyPress0       = "D" )
    {
        AnyKeyPress := 1
        CountDownTime := 0
    }
    Else
    {
        If ( CountDownTime > 0 )
        {
            AnyKeyPress := 0
        }
        Else
        {
            AnyKeyPress := 1
            CountDownTime++
        }
    }
Return
