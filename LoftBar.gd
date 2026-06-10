extends Control
# Rounded capsule LOFT meter for the HUD. Display-only: Main triggers MEGA HOP / LASER
# when the player taps the (ready) bar's left / right half.

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
		# two glowing pill buttons: MEGA HOP (cool blue) | LASER (hot red)
		var pulse := 0.5 + 0.5 * sin(t * 7.0)
		var gap := 8.0
		var bw := (w - gap) * 0.5
		var mega_col := Color(0.16, 0.52, 0.86).lerp(Color(0.45, 0.8, 1.0), pulse)
		var laser_col := Color(0.86, 0.26, 0.22).lerp(Color(1.0, 0.55, 0.4), pulse)
		draw_style_box(_sb(mega_col, rad, 2, Color(1, 1, 1, 0.8)), Rect2(0, 0, bw, h))
		draw_style_box(_sb(laser_col, rad, 2, Color(1, 1, 1, 0.8)), Rect2(bw + gap, 0, bw, h))
		draw_string(font, Vector2(0, h * 0.5 + 7), "↟ MEGA HOP", HORIZONTAL_ALIGNMENT_CENTER, bw, 22, Color.WHITE)
		draw_string(font, Vector2(bw + gap, h * 0.5 + 7), "LASER ✸", HORIZONTAL_ALIGNMENT_CENTER, bw, 22, Color.WHITE)
		return

	# track
	draw_style_box(_sb(Color(0.05, 0.09, 0.13, 0.85), rad, 2, Color(1, 1, 1, 0.18)), Rect2(0, 0, w, h))
	# fill: blue -> gold, rounded, min width keeps the pill shape
	if value > 0.001:
		var col := Color(0.20, 0.62, 0.92).lerp(Color(1.0, 0.86, 0.32), value)
		var fw := maxf(value * w, h)
		draw_style_box(_sb(col, rad), Rect2(0, 0, fw, h))
		# sheen along the top
		draw_style_box(_sb(Color(1, 1, 1, 0.16), rad), Rect2(3, 3, maxf(fw - 6, 1), h * 0.34))
	# label
	draw_string(font, Vector2(0, h * 0.5 + 7), "LOFT  %d%%" % int(value * 100.0),
		HORIZONTAL_ALIGNMENT_CENTER, w, 22, Color(1, 1, 1, 0.9))
