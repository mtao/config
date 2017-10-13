import XMonad
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig(additionalKeys)
import System.IO
import XMonad.Hooks.SetWMName
import XMonad.Actions.GridSelect
import XMonad.Layout.NoBorders
import Graphics.X11.ExtraTypes.XF86

--xmain = xmonad $ defaultConfig
--
main = xmonad =<< dzen (additionalKeys defaultConfig
    { borderWidth = 1
    , terminal = "urxvtc"
    , normalBorderColor = "#cccccc"
    , focusedBorderColor = "#cd8b00"
    , layoutHook = smartBorders (avoidStruts $ layoutHook defaultConfig)
    , manageHook = manageHook defaultConfig <+> manageDocks
    , startupHook = setWMName "LG3D"
    }  myKeys)

myKeys :: [((KeyMask, KeySym), X ())]
myKeys = [ 
            ((mod1Mask, xK_g), goToSelected defaultGSConfig)
                    , ((controlMask .|. mod1Mask, xK_l), spawn "slock")
                    , ((0, xF86XK_AudioRaiseVolume), spawn "pactl set-sink-volume 0 +5%")
                    , ((0, xF86XK_AudioLowerVolume), spawn "pactl set-sink-volume 0 -5%")
                    , ((controlMask, xF86XK_AudioRaiseVolume), spawn "pactl set-sink-volume 0 +1%")
                    , ((controlMask, xF86XK_AudioLowerVolume), spawn "pactl set-sink-volume 0 -1%")
                    , ((0, xF86XK_AudioMute), spawn "muted=$(pactl list sinks | grep 'Mute' | tail -1 | awk '{print $2}'); if [ $muted == yes ]; then pactl set-sink-mute 0 0; else pactl set-sink-mute 0 1; fi")
                    , ((0, xF86XK_MonBrightnessUp), spawn "xbacklight +20")
                    , ((0, xF86XK_MonBrightnessDown), spawn "xbacklight -20")
                    , ((controlMask, xF86XK_MonBrightnessUp), spawn "xbacklight +5")
                    , ((controlMask, xF86XK_MonBrightnessDown), spawn "xbacklight -5")
            ]

