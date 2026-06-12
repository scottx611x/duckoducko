extends Control
# Slim LOFT meter pinned top-center, Tony Hawk "SPECIAL" style. Display-only:
# it just charges quietly; a full bar GLOWS and the special auto-deploys from Main.

var value := 0.0
var is_ready := false
var t := 0.0
var font: Font

func _ready() -> void:
	font = ThemeDB.fallback_font
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _process(delta: float) -> void:
	t += delta
	queue_redraw()

func _sb(color: Color, radius: float, border := 0.0, border_col := Color(0, 0, 0, 0)) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = color
	s.set_corner_radius_all(int(radius))
	if border > 0.0:
		s.set_border_width_all(int(border))
		s.border_color = border_col
	return s

func _draw() -> void:
	var w := size.x
	var h := size.y
	var rad := h * 0.5

	if is_ready:
		# SPECIAL: the whole bar burns through slow hue cycles under a breathing halo
		var pulse := 0.5 + 0.5 * sin(t * 5.0)
		var hue := fposmod(t * 0.25, 1.0)
		var hot := Color.from_hsv(hue, 0.75, 1.0)
		for g in 2:
			var grow := (g + 1) * 3.0 + pulse * 3.0
			draw_style_box(_sb(Color(hot.r, hot.g, hot.b, 0.10 * (2 - g)), rad + grow),
				Rect2(0, 0, w, h).grow(grow))
		draw_style_box(_sb(hot.darkened(0.25), rad, 1, Color(1, 1, 1, 0.5 + 0.4 * pulse)),
			Rect2(0, 0, w, h))
		draw_style_box(_sb(Color(1, 1, 1, 0.22), rad * 0.7),
			Rect2(3, 2, w - 6, h * 0.38))
		var sx: float = fposmod(t * 120.0, w + 70.0) - 35.0   # sweeping glint
		if sx > 4.0 and sx < w - 14.0:
			draw_rect(Rect2(sx, 2, 10, h - 4), Color(1, 1, 1, 0.3))
		draw_string(font, Vector2(0, h * 0.5 + 5.5), "S P E C I A L",
			HORIZONTAL_ALIGNMENT_CENTER, w, 13, Color(1, 1, 1, 0.85 + 0.15 * pulse))
		return

	# charging: quiet slim track, blue -> gold fill, faint ticks. no text, no noise.
	draw_style_box(_sb(Color(0.04, 0.08, 0.12, 0.6), rad, 1, Color(1, 1, 1, 0.12)),
		Rect2(0, 0, w, h))
	for q in [0.25, 0.5, 0.75]:
		draw_rect(Rect2(w * q - 1.0, h * 0.3, 1.5, h * 0.4), Color(1, 1, 1, 0.10))
	if value > 0.001:
		var col := Color(0.20, 0.62, 0.92, 0.85).lerp(Color(1.0, 0.86, 0.32, 0.95), value)
		var fw := maxf(value * w, h)
		draw_style_box(_sb(col, rad), Rect2(0, 0, fw, h))
		draw_style_box(_sb(Color(1, 1, 1, 0.14), rad * 0.7), Rect2(2, 2, maxf(fw - 4, 2), h * 0.36))
