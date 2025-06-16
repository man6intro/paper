-- Pull in the wezterm API
local wezterm = require 'wezterm'
-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices.
local mux = wezterm.mux

---{{{ Maximize wezterm on startup
wezterm.on("gui-startup", function()
  local tab, pane, window = mux.spawn_window{}
  window:gui_window():maximize()
end)
---}}}

--- {{{ shell
-- Spawn a zsh shell in login mode
config.default_prog = { '/usr/bin/zsh' }
--- }}}

--- {{{ font
config.font = wezterm.font_with_fallback {
	{ family = 'Fira Code' },
	{ family = 'Terminus' },
	'Noto Color Emoji'
}
config.font_size = 18
--- }}}

--- {{{ bar
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = true
config.window_frame = {
	font = wezterm.font { family = 'Fira Code', weight = 'Bold' },
	font_size = 9.0,
	active_titlebar_bg = '#000000',
	inactive_titlebar_bg = '#000000',
}
config.colors = {
	tab_bar = {
		background = '#000000',
		active_tab = {
			bg_color = '#000000',
			fg_color = '#ffffff',
			intensity = 'Bold',
		},
		inactive_tab = {
			bg_color = '#000000',
			fg_color = '#ffffff',
		},
		inactive_tab_hover = {
			bg_color = '#000000',
			fg_color = '#ffffff',
			intensity = 'Bold',
		},
		new_tab = {
			bg_color = '#000000',
			fg_color = '#ffffff',
		},
		new_tab_hover = {
			bg_color = '#000000',
			fg_color = '#ffffff',
			intensity = 'Bold',
		},
	},
}
--- }}}

--- {{{ bg
config.window_background_opacity = 0.7
config.inactive_pane_hsb = {
	saturation = 0.9,
	brightness = 0.6,
}
--- }}}

-- Finally, return the configuration to wezterm:
return config
