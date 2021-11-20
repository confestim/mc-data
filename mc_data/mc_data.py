import Stats
import numpy as np
import matplotlib.pyplot as plt


def top(
    chart_type:str="bar",
    data=Stats.Stats().get_data(data_type="minecraft:used"),
    limit:int=10,
    chart_only:bool=True,
    filename:str="chart",
    blitem:str=None):
    """Saves a graph of given data, regarding top n number of data type given.
    
    `e.g. top 12 of data type 'minecraft:broken'`
    
    Parameters
    ----------

    chart_type : Chart type. Right now you can only choose between 'pie' and 'bar'.

    data : defaults to `Stats().get_data(data_type="minecraft:used")`, but you can use it with your own instance of Stats() with your own data_type
    
    limit : defaults to `10`, you can put any integer there, but the bigger it is, the more data it will collect (the worse the chart will look).

    chart_only : is `True` by default. If set to `False`, you'll get the top n number of the data type given in a dict.

    filename : is `chart.png` by default. It's the filename/name of the chart.

    blitem :  Makes a leaderboard of a category --> block/item of choice (in category set within Stats instance)

    Returns
    -------

    dict_new : if the `chart_only` flag is set to False

    otherwise returns `True` if everything happens without error. 
    """
    
    all_data = {}


    if not blitem:
        for i in data:
                for l in i:
                    for le in i[l]:
                        # print(le)
                        # all_data.update(le=i[l][e])
                        try:
                            all_data[le] += i[l][le]
                        except KeyError:
                            all_data[le] = i[l][le]
   
    else:
        all_data = {}
        for i in data:
            for l in i:
                for le in i[l]:
                    if le == blitem:
                        all_data[l] = i[l][le]
        if not all_data:
            raise KeyError("No such block/item in this category/dataset")
    
    dict_new = dict(sorted(all_data.items(), key=lambda x:x[1], reverse=True)[:limit])
    for i in list(dict_new):
        dict_new[i.replace("minecraft:", "")] = dict_new[i]


    if not chart_only:
        return dict_new

    if chart_type == "bar":
        plt.figure(figsize=(20, 10))
        plt.bar(range(len(dict_new)), list(dict_new.values()), align='center', width=0.3)
        plt.xticks(range(len(dict_new)), list(dict_new.keys()))

    elif chart_type == "pie":
        y = np.array(list(dict_new.values()))
        mylabels = list(dict_new.keys())

        plt.pie(y, labels = mylabels, autopct='%1.1f%%')
        
    else:
        raise TypeError("This only supports either 'bar' or 'pie' charts as of now.")
    
    plt.title(filename)
    if " " in filename:
        filename = filename.replace(" ", "_")

    plt.savefig(f"{filename}.png", bbox_inches='tight', dpi=200)
    print(f"Saved graph as {filename}.png!")
    
    return True
    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="python3 mc_data", description="CLI interface of mc_data")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bar", "-b", dest="ch_type", action="store_const", const="bar", help="Generate a bar chart from top n results")
    group.add_argument("--pie", "-pie", dest="ch_type", action="store_const", const="pie", help="Generate a pie chart from top n results")
    parser.add_argument("--limit", "-l", default=10, type=int, help="Set a limit to the data put in the chart")
    parser.add_argument("--name", "-n", required=True, type=str, help="Set (file)name of the chart")
    parser.add_argument("--user", "-u", default=None, type=str, help="Get chart for a specific user")   
    parser.add_argument("--category", "-c", required=True, type=str, help="Choose what category of data to use for the chart")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,  help="Enable verbose mode")
    parser.add_argument("--blitem", "-bi", default=None, type=str, help="Choose what block/item to use for the chart")
    parser.set_defaults(ch_type="bar")

    args = parser.parse_args()
    
    data_user = Stats.Stats(verbose=args.verbose, user=args.user).get_data(data_type=f"{args.category}")
   
    top(chart_type=args.ch_type, limit=args.limit, data=data_user, filename=args.name, blitem=args.blitem)

