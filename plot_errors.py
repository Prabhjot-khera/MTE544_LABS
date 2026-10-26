import matplotlib.pyplot as plt
from utilities import FileReader




def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    if not values:
        print(f"No samples in {filename}")
        return
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append((val[-1] - first_stamp) / 1e9)

    if headers == ["v", "omega", "stamp"]:
        fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
        fig.suptitle(f"Measured robot velocity: {filename}")
        for axis, column, label in zip(
            axes, (0, 1), ("Forward velocity (m/s)", "Yaw rate (rad/s)")
        ):
            axis.plot(time_list, [row[column] for row in values], label=headers[column])
            axis.set_ylabel(label)
            axis.legend()
            axis.grid()
        axes[-1].set_xlabel("Elapsed time (s)")
        fig.tight_layout()
        plt.show()
        return

    
    
    fig, axes = plt.subplots(1,2, figsize=(14,6))


    axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])
    axes[0].set_title("state space")
    axes[0].grid()

    
    axes[1].set_title("each individual state")
    axes[1].set_xlabel("Elapsed time (s)")
    for i in range(0, len(headers) - 1):
        axes[1].plot(time_list, [lin[i] for lin in values], label= headers[i]+ " linear")

    axes[1].legend()
    axes[1].grid()

    plt.show()
    
    





import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)



