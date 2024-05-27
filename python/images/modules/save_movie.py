""" Module to process the plot """

from matplotlib.animation import FuncAnimation


def save_movie(fig, data_dict, file_name):
    """Function to create a movie"""

    movie = {
        "fig": fig,
        "frames": data_dict["frames"],
        "func": data_dict["update_function"],
        "fargs": (data_dict,),
        "blit": True,
    }
    ani = FuncAnimation(**movie)
    ani.save(f"{file_name}.mp4", writer="ffmpeg", fps=10)
