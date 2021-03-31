import base64
import io
import os
import urllib

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


def get_base64_string(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png',  bbox_inches="tight")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def generate_plots_with_data(alldata):
    cols = ['DATE', 'AMOUNT', 'WHERE', 'TAGS']
    data = [[p.date, p.amount, p.where, p.tags] for p in alldata]
    df = pd.DataFrame(data=data, columns=cols)
    df.set_index("DATE", inplace=True)
    return df


def generate_plot(tdata):

    plt.style.use("ggplot")
    matplotlib.use('Agg')

    tdata.index = pd.to_datetime(tdata.index)
    # path = os.path.dirname(os.path.abspath(__file__))
    # static_path = os.path.join(path, "static", "exp")
    year = tdata.index.year.unique().max()
    data = tdata[tdata.index.year == year]

    this_month = data.index.month.unique().max()

    monthgroup = data.groupby(data.index.month)
    mmean = monthgroup.mean().mean()

    datadict = {}

    with plt.xkcd():
        ax = monthgroup.sum().plot.bar(color="orange", alpha=0.8, rot=0)
        ax.hlines(mmean, -100, 100, linestyles="dashed")
        ax.set_xlabel("Months")
        ax.set_title("Months Spends")
        fig = plt.gcf()
        # plt.savefig(os.path.join(static_path,"month.png"))
        monthly_spend = get_base64_string(fig)
        datadict["monthly_spend"] = monthly_spend
        plt.close()

    weekgroup = data.groupby([data.index.week])
    wmean = weekgroup.mean().mean()

    with plt.xkcd():
        ax = weekgroup.sum()[-5:].plot.bar(rot=0, color="green", alpha=0.8)
        ax.hlines(wmean, -10, 100, linestyles="dashed")
        ax.set_xlabel("Weeks")
        ax.set_title("Last 5 weeks")
        # plt.savefig(os.path.join(static_path,"week.png"))
        fig = plt.gcf()
        weekly_spend = get_base64_string(fig)
        datadict["weekly_spend"] = weekly_spend
        plt.close()

    thismonth = data[data.index.month == this_month]
    thismonth = thismonth.sort_index()

    with plt.xkcd():
        thismonth.AMOUNT.cumsum().plot(alpha=0.9, rot=0)
        ax.set_title("Trend for this month")
        # plt.savefig(os.path.join(static_path,"days.png"))
        fig = plt.gcf()
        month_trend = get_base64_string(fig)
        datadict["month_trend"] = month_trend
        plt.close()

    lastday = data.index.dayofyear.max()
    tenthday = lastday-30

    last10days = data[data.index.dayofyear >= tenthday]
    last10group = last10days.groupby(last10days.index.dayofyear)
    lmean = last10group.mean().mean()

    with plt.xkcd():
        ax = last10group.sum().plot.bar(rot=0, color="yellow", alpha=0.8)
        ax.hlines(lmean, -10, 500, linestyles="dashed")
        ax.set_title("Last 30 days")
        # plt.savefig(os.path.join(static_path,"last10days.png"))
        fig = plt.gcf()
        last10days_in = get_base64_string(fig)
        datadict["last10days_in"] = last10days_in
        plt.close()

    total_this_year = round(data.AMOUNT.sum(), 2)
    total_this_month = round(thismonth.AMOUNT.sum(), 2)
    no_purchases_this_month = thismonth.AMOUNT.count()
    no_purchases_this_year = data.AMOUNT.count()

    with plt.xkcd():
        ax = thismonth.groupby(thismonth.WHERE).sum().sort_values(
            by="AMOUNT")[-5:].plot.bar(color="pink", alpha=0.9, rot=0)
        ax.set_title("Top 5 this month")
        # plt.savefig(os.path.join(static_path,"top5thismonth.png"))
        fig = plt.gcf()
        top5thismonth = get_base64_string(fig)
        datadict["top5thismonth"] = top5thismonth
        plt.close()

    with plt.xkcd():
        ax = data.groupby(data.WHERE).sum().sort_values(
            by="AMOUNT")[-10:].plot.bar(color="purple", alpha=0.8, rot=0)
        ax.set_title("Top of the year")
        plt.xticks(fontsize=10)
        # plt.savefig(os.path.join(static_path,"top10thisyear.png"))
        fig = plt.gcf()
        top10year = get_base64_string(fig)
        datadict["top10year"] = top10year
        plt.close()

    with plt.xkcd():
        plt.text(0.1, 0.9, "Total this year:")
        plt.text(0.1, 0.5, str(total_this_year), fontsize=100)
        plt.axis("off")
        # plt.savefig(os.path.join(static_path,"total_this_year.png"))
        fig = plt.gcf()
        total_year = get_base64_string(fig)
        datadict["total_year"] = total_year
        plt.close()

    with plt.xkcd():
        plt.text(0.1, 0.9, "This Month:")
        plt.text(0.1, 0.5, str(total_this_month), fontsize=100)
        plt.axis("off")
        # plt.savefig(os.path.join(static_path,"total_this_month.png"))
        fig = plt.gcf()
        total_month = get_base64_string(fig)
        datadict["total_month"] = total_month
        plt.close()

    with plt.xkcd():
        plt.text(0.1, 0.9, "Total spends:")
        plt.text(0.1, 0.5, str(no_purchases_this_year), fontsize=100)
        plt.axis("off")
        # plt.savefig(os.path.join(static_path,"no_purchases_this_year.png"))
        fig = plt.gcf()
        no_of_purchase = get_base64_string(fig)
        datadict["no_of_purchase"] = no_of_purchase
        plt.close()

    with plt.xkcd():
        plt.text(0.1, 0.9, "This month no of spends:")
        plt.text(0.1, 0.5, str(no_purchases_this_month), fontsize=100)
        plt.axis("off")
        # plt.savefig(os.path.join(static_path,"no_purchases_this_month.png"))
        fig = plt.gcf()
        no_of_purchase_this_month = get_base64_string(fig)
        datadict["no_of_purchase_this_month"] = no_of_purchase_this_month
        plt.close()

    return datadict

    # with plt.xkcd():
    #     plt.text(0.1, 0.9, "Total this year:")
    #     plt.text(0.1, 0.5, str(total_this_year), fontsize=100)
    #     plt.axis("off");
    #     fig = plt.gcf()
    #     buff = io.BytesIO()
    #     fig.savefig(buff, format="png")
    #     buff.seek(0)
    #     string=base64.b64encode(buff.read())
    #     total_this_year_s = urllib.parse.quote(string)
    #     plt.close()
