import manim as mn

colour_grid_pre = ["BLUE", "TEAL", "GREEN", "YELLOW", "GOLD", "RED", "MAROON", "PURPLE", "GREY"]
colour_grid_post = ["A", "B", "C", "D", "E"]
colour_others = ["PINK", "LIGHT_PINK", "ORANGE", "LIGHT_BROWN", "DARK_BROWN", "GREY_BROWN"]

if __name__ == "__main__":
    all_colours = {}
    for c1 in colour_grid_pre:
        for c2 in colour_grid_post:
            cc = f"{c1}_{c2}"
            colour_code = str(getattr(mn.color, cc))
            all_colours[f"--{cc.lower()}"] = colour_code.lower()

    for cc in colour_others:
        colour_code = str(getattr(mn.color, cc))
        all_colours[f"--{cc.lower()}"] = colour_code.lower()

    colour_lines = []
    for name, val in all_colours.items():
        colour_lines.append(f"{name}: {val};")
    css_block = "\n".join(colour_lines)
    print(css_block)





