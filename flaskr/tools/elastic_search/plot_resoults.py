from datetime import datetime, date
import matplotlib.pyplot as plt
from flaskr.tools.elastic_search.elastic_search import find_query


def plot_build_name_counts(build_name_counts):
    # Sort the dictionary by count in descending order
    # sorted_counts = dict(sorted(build_name_counts.items(), key=lambda item: item[1], reverse=True))

    # Prepare data for plotting
    build_names = list(build_name_counts.keys())
    counts = list(build_name_counts.values())

    # Create the bar chart
    plt.figure(figsize=(12, 6))
    bars = plt.bar(build_names, counts, color="skyblue")

    # Add value labels on top of each bar
    for bar, count in zip(bars, counts):
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 0.1,
            count,
            ha="center",
            va="bottom",
        )

    # Customize the plot
    plt.xlabel("Build Name")
    plt.ylabel("Steps Count")
    plt.title("Build Name vs. Steps Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    from_date = date(2025, 1, 1)
    to_date = date(2025, 1, 31)
    page_request = {"page": 0, "size": 10}
    group_name = "group1_agrs2f5sa2"
    string_query = "productName:(*) AND stepUpdateStatus:('failed')"  # test the query in Kibana before using it here
    results = find_query(
        string_query,
        page_request,
        from_date,
        to_date,
        group_name,
        index_name="analitics",
    )

    # Extract aggregation results
    build_name_counts = {}
    for result in results:
        build_name = result.buildName
        build_name_counts[build_name] = build_name_counts.get(build_name, 0) + 1

    plot_build_name_counts(build_name_counts)
