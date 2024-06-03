""" Module to create an animation """

from matplotlib.animation import FuncAnimation


def save_movie(fig, update_args, config_data, dynamic_data):
    """Function to create a movie"""

    movie = {
        "fig": fig,
        "frames": dynamic_data["frames"],
        "func": update_args["function"],
        "fargs": (update_args, config_data, dynamic_data,),
        "blit": True,
    }
    ani = FuncAnimation(**movie)
    ani.save(f"{update_args['file_name']}.mp4", writer="ffmpeg", fps=10)
