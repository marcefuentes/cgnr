""" Format lines. """


def format_lines(lines, image):
    """ Format lines. """

    for i in range(lines.shape[0]):
        for j in range(lines.shape[1]):
            for k in range(lines.shape[2]):
                for m in range(lines.shape[3]):
                    line = lines[i, j, k, m]
                    line.set_color(image["line_color"])
                    line.set_linewidth(image["line_width"] * image["plot_size"])

