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

# a ready-to-fire pill: glow halo, hot gradient body, sheen, sweeping glint
func _pill(rect: Rect2, base: Color, hot: Color, label: String, pulse: float, phase: float) -> void:
	var rad := rect.size.y * 0.5
	for g in 3:                                          # halo rings breathe outward
		var grow := (g + 1) * 4.0 + pulse * 4.0
		draw_style_box(_sb(Color(hot.r, hot.g, hot.b, 0.085 * (3 - g) * (0.4 + 0.6 * pulse)),
			rad + grow), rect.grow(grow))
	draw_style_box(_sb(base.lerp(hot, 0.3 + 0.4 * pulse), rad, 2,
		Color(1, 1, 1, 0.75 + 0.25 * pulse)), rect)
	draw_style_box(_sb(Color(1, 1, 1, 0.20), rad * 0.7),  # top sheen
		Rect2(rect.position + Vector2(5, 3), Vector2(rect.size.x - 10, rect.size.y * 0.34)))
	# a glint sweeps along the pill every second or so
	var sx: float = fposmod(t * 150.0 + phase, rect.size.x + 90.0) - 45.0
	if sx > 6.0 and sx < rect.size.x - 20.0:
		draw_rect(Rect2(rect.position.x + sx, rect.position.y + 4, 13, rect.size.y - 8),
			Color(1, 1, 1, 0.25))
	draw_string(font, rect.position + Vector2(1.5, rect.size.y * 0.5 + 9.5), label,
		HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 23, Color(0, 0, 0, 0.45))
	draw_string(font, rect.position + Vector2(0, rect.size.y * 0.5 + 8), label,
		HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 23, Color.WHITE)

func _draw() -> void:
	var w := size.x
	var h := size.y
	var rad := h * 0.5

	if is_ready:
		# two armed pill buttons: MEGA HOP (cool blue) | LASER (hot red)
		var pulse := 0.5 + 0.5 * sin(t * 6.0)
		var gap := 8.0
		var bw := (w - gap) * 0.5
		_pill(Rect2(0, 0, bw, h), Color(0.13, 0.45, 0.80), Color(0.45, 0.85, 1.0),
			"↟ MEGA HOP", pulse, 0.0)
		_pill(Rect2(bw + gap, 0, bw, h), Color(0.78, 0.22, 0.18), Color(1.0, 0.55, 0.35),
			"LASER ✸", pulse, 130.0)
		return

	# track
	draw_style_box(_sb(Color(0.05, 0.09, 0.13, 0.85), rad, 2, Color(1, 1, 1, 0.18)), Rect2(0, 0, w, h))
	# quarter ticks so progress reads at a glance
	for q in [0.25, 0.5, 0.75]:
		draw_rect(Rect2(w * q - 1.0, h * 0.28, 2.0, h * 0.44), Color(1, 1, 1, 0.13))
	# fill: blue -> gold, rounded, min width keeps the pill shape
	if value > 0.001:
		var col := Color(0.20, 0.62, 0.92).lerp(Color(1.0, 0.86, 0.32), value)
		var fw := maxf(value * w, h)
		draw_style_box(_sb(col, rad), Rect2(0, 0, fw, h))
		draw_style_box(_sb(Color(1, 1, 1, 0.16), rad), Rect2(3, 3, maxf(fw - 6, 1), h * 0.34))
		# shimmer crawls along the fill as it charges
		var sx: float = fposmod(t * 90.0, fw + 50.0) - 25.0
		if sx > 4.0 and sx < fw - 16.0:
			draw_rect(Rect2(sx, 4, 9, h - 8), Color(1, 1, 1, 0.18))
	# label w/ soft shadow
	draw_string(font, Vector2(1.5, h * 0.5 + 8.5), "LOFT  %d%%" % int(value * 100.0),
		HORIZONTAL_ALIGNMENT_CENTER, w, 22, Color(0, 0, 0, 0.4))
	draw_string(font, Vector2(0, h * 0.5 + 7), "LOFT  %d%%" % int(value * 100.0),
		HORIZONTAL_ALIGNMENT_CENTER, w, 22, Color(1, 1, 1, 0.92))
