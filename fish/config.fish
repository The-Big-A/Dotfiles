if status is-interactive
    # Commands to run in interactive sessions can go here
    alias cl='clear'
    alias files='nautilus'
    alias brightness='xrandr --output eDP-1 --brightness'
    alias ..='cd ..'
    alias ...='cd ../..'
    alias .3='cd ../../..'
    alias .4='cd ../../../..'
    alias .5='cd ../../../../..'
    set fish_greeting
end
# THEME PURE #
set fish_function_path /home/ash/.config/fish/functions/theme-pure/functions/ $fish_function_path
source /home/ash/.config/fish/functions/theme-pure/conf.d/pure.fish
