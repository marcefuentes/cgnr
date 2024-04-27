""" Module to process the plot """

from matplotlib.animation import FuncAnimation


def save_movie(fig, update_args):
    """Function to create a movie"""

    movie = {
        "fig": fig,
        "frames": update_args["frames"],
        "func": update_args["update_function"],
        "fargs": (update_args,),
        "blit": True,
    }
    ani = FuncAnimation(**movie)
    ani.save(f"{update_args['file_name']}.mp4", writer="ffmpeg", fps=10)
