from Stats import Stats
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def top(
    chart_type:str="bar",
    data=Stats().get_data(data_type="minecraft:used"),
    limit:int=10,
    chart_only:bool=True,
    filename:str="chart.png"):
    """Saves a graph of given data, regarding top n number of data type given.
    
    `e.g. top 12 of data type 'minecraft:broken'`
    
    Parameters
    ----------

    chart_type : Chart type. Right now you can only choose between 'pie' and 'bar'.

    data : defaults to `Stats().get_data(data_type="minecraft:used")`, but you can use it with your own instance of Stats() with your own data_type
    
    limit : defaults to `10`, you can put any integer there, but the bigger it is, the worse the chart will look.

    chart_only : is `True` by default. If set to `False`, you'll get the top n number of the data type given in a dict.

    filename : is `chart.png` by default. It's the filename of the chart.

    Returns
    -------

    dict_new : if the `chart_only` flag is set to False

    otherwise returns `True` if everything happens without error. 
    """
    
    all_data = {}

    for i in data:
        for l in i:
            for le in i[l]:
                # print(le)
                # all_data.update(le=i[l][e])
                try:
                    all_data[le] += i[l][le]
                except KeyError:
                    all_data[le] = i[l][le]
        
    
    dict_new = dict(sorted(all_data.items(), key=lambda x:x[1], reverse=True)[:limit])
    for i in list(dict_new):
        dict_new[i.replace("minecraft:", "")] = dict_new[i]
        del dict_new[i]
    
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
    plt.savefig(filename, bbox_inches='tight', dpi=200)
    print(f"Saved graph as {filename}!")
    
    return True
    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True




