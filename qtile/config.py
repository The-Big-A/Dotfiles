# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

mod = "mod4"
terminal = "alacritty"
browser = "firefox"
file_browser = "nautilus"

keys = [

    ### applications
    
    Key([mod], 
        "Return", 
        lazy.spawn(terminal), 
        desc="Launch terminal"
        ),
        
    Key([mod], 
        "b", 
        lazy.spawn(browser), 
        desc="Launch browser"
        ),

    Key([mod], 
        "p", 
        lazy.spawn("rofi -show run"), 
        desc="Launch rofi"
        ),
        
    Key([mod], 
        "f", 
        lazy.spawn(file_browser), 
        desc="Launch file browser"
        ),
        
        
    ### Essentials


    Key([mod],
        "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
        ),
    Key([mod],
        "k",
        lazy.restart(),
        desc="Toggle ur mom"
        ),

    Key([mod, "shift"],
        "c",
        lazy.window.kill(),
        desc="Kill focused window"
        ),

    Key([mod, "control"],
        "r",
        lazy.reload_config(),
        desc="Reload the config"
        ),

    Key([mod, "control"],
        "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"
        ),

    Key([mod],
        "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"
        ),


    ### Switch between windows


    Key([mod],
        "h",
        lazy.layout.left(),
        desc="Move focus to left"
        ),

    Key([mod],
        "l",
        lazy.layout.right(),
        desc="Move focus to right"
        ),

    Key([mod],
        "j",
        lazy.layout.down(),
        desc="Move focus down"
        ),

    Key([mod],
        "k",
        lazy.layout.up(),
        desc="Move focus up"
        ),

    Key([mod],
        "space",
        lazy.layout.next(),
        desc="Move window focus to other window"
        ),


    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.


    Key([mod, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
        ),

    Key([mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
        ),

    Key([mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"
        ),

    Key([mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"
        ),


    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.


    Key([mod, "control"],
        "h",
        lazy.layout.grow_left(),
        desc="Grow window to the left"
        ),

    Key([mod, "control"],
        "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
        ),

    Key([mod, "control"],
        "j",
        lazy.layout.grow_down(),
        desc="Grow window down"
        ),

    Key([mod, "control"],
        "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
        ),

    Key([mod],
        "n",lazy.layout.normalize(),
        desc="Reset all window sizes"
        ),


    Key([mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
        ),

]

groups = [Group("", layout="monadtall"),
        Group("", layout="monadtall"),
        Group("", layout="monadtall"),
        Group("", layout="monadtall"),
        Group("", layout="max"),
        Group("", layout="max")
        ]

for i, group in enumerate(groups[:], 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[group.name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(group.name)))

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(margin=5,border_width=2,border_focus="#ffffff"),
    layout.MonadTall(margin=5,border_width=2,border_focus="#ffffff"),
    # layout.Floating()
    # layout.Tile()
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 12,
    padding = 2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [   
                widget.GroupBox(fontsize = 15,inactive="#5d5d61",disable_drag=True,highlight_method='line',this_current_screen_border="ffffff"),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.TextBox(text="+",mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("pulseaudio-ctl up")},fontsize=20),
                widget.Volume(),
                widget.TextBox(text="-",mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("pulseaudio-ctl down")},fontsize=20),
                #widget.BatteryIcon(),
                widget.Sep(foreground="#ffffff"),
                widget.Battery(format="{char} {percent:2.0%}"),
                widget.Sep(foreground="#ffffff"),
                widget.CurrentLayout(),
                widget.Sep(foreground="#ffffff"),
                widget.Clock(format="%a %d %b"),
                widget.Sep(foreground="#ffffff"),
                # widget.TextBox(
                #        text='◢',
                #        font = "Ubuntu Mono",
                #        padding=0,
                #        fontsize = 55),
                widget.Clock(format="%H:%M %p")
                
            ],
            24,
            border_width=[0, 2, 0, 2],  # Draw top and bottom borders
            background="#2a313e",
            opacity=0.8,
            # margin=1,
        ),
    )
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='firefox'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])

##qtilerc sorta..
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We"re lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn"t work correctly. We may as well just lie
# and say that we"re a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java"s whitelist.
wmname = "LG3D"
