from tkinter.ttk import *

# Colors
tb = "#505050"
tb_fg = "#C0C0C0"
bg = "#303030"
fg = "#E3E3E3"
fg_dark = "#B3B3B3"
accent = "#34515E"
accent_h = "#607D8B"
accent_s = "#006594"
accent_s_h = "#009ceb"
second = "#AB793C"
green = "#40d040"
red = "#ff5050"

# Fonts
font_family = "Segoe UI"
f_xl = (font_family, 16, "roman")
f_xl_bold = (font_family, 16, "bold")
f_large = (font_family, 14, "roman")
f_large_bold = (font_family, 14, "bold")
f_normal = (font_family, 12, "roman")
f_normal_bold = (font_family, 12, "bold")
f_small = (font_family, 10, "roman")
f_small_bold = (font_family, 10, "bold")


def add_style():
    style = Style()
    style.theme_create("VANN_Dark")
    style.theme_settings("VANN_Dark", settings={
        "TButton": {
            "configure": {
                "padding": (10, 1),
                "background": accent_s,
                "foreground": fg,
                "borderwidth": 0,
                "activebackground": accent_s_h,
                "activeforeground": fg,
                "font": f_normal
            },
            "map": {
                "background": [("active", accent_s_h)]
            }
        },
        "TFrame": {
            "configure": {
                "background": bg
            }
        },
        "TLabel": {
            "configure": {
                "background": bg,
                "foreground": fg,
                "font": f_normal
            }
        },
        "TEntry": {
            "configure": {
                "background": accent_s,
                "foreground": fg,
                "borderwidth": 0,
                "insertbackground": fg,
                "disabledbackground": bg,
                "disabledforeground": fg_dark,
                "font": f_large_bold
            }
        },
    })

    style.theme_use("VANN_Dark")
