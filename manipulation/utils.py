import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

import pydrake.all


def FindResource(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def AddPackagePaths(parser):
    # Remove once https://github.com/RobotLocomotion/drake/issues/10531 lands.
    parser.package_map().PopulateFromFolder(FindResource(""))
    parser.package_map().Add(
        "manipulation_station",
        os.path.join(pydrake.common.GetDrakePath(),
                     "examples/manipulation_station/models"))
    parser.package_map().Add(
        "ycb",
        os.path.join(pydrake.common.GetDrakePath(), "manipulation/models/ycb"))
    parser.package_map().Add(
        "wsg_50_description",
        os.path.join(pydrake.common.GetDrakePath(),
                     "manipulation/models/wsg_50_description"))


reserved_labels = [
    pydrake.geometry.render.RenderLabel.kDoNotRender,
    pydrake.geometry.render.RenderLabel.kDontCare,
    pydrake.geometry.render.RenderLabel.kEmpty,
    pydrake.geometry.render.RenderLabel.kUnspecified,
]


def colorize_labels(image):
    """Colorizes labels."""
    # TODO(eric.cousineau): Revive and use Kuni's palette.
    cc = mpl.colors.ColorConverter()
    color_cycle = plt.rcParams["axes.prop_cycle"]
    colors = np.array([cc.to_rgb(c["color"]) for c in color_cycle])
    bg_color = [0, 0, 0]
    image = np.squeeze(image)
    background = np.zeros(image.shape[:2], dtype=bool)
    for label in reserved_labels:
        background |= image == int(label)
    foreground = image[np.logical_not(background)]
    color_image = colors[image % len(colors)]
    color_image[background] = bg_color
    return color_image
