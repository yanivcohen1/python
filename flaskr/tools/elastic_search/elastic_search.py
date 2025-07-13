from datetime import datetime, date
from math import ceil
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

# Initialize Elasticsearch client
es = Elasticsearch() # host='localhost', port=9200
try:
    info = es.info()
    print("Elasticsearch Cluster Info:")
    # print(info)
except Exception as e:
    print("Failed to connect to Elasticsearch.")
    print(f"Error: {e}")

# Check if the index exists
index_name="analitics"
if not es.indices.exists(index=index_name):
    print(f"Index '{index_name}' does not exist.")

def find_query(string_query, page_request, from_date, to_date, group_name, index_name="analitics"):

    # Build the date range filter
    date_range_filter = Q('range', **{
        '@timestamp': {
            'gte': from_date.isoformat(),
            'lte': to_date.isoformat()
        }
    })

    # Build the string query
    combined_query = Q('query_string', query=f'groupName:{group_name} AND {string_query}')

    # Combine filter and query
    s = Search(using=es, index=index_name).query(combined_query).filter(date_range_filter)

    # Apply pagination
    page_number = page_request["page"]
    page_size = page_request["size"]
    s = s[page_number * page_size : (page_number + 1) * page_size]

    # Execute the search
    response = s.execute()

    # Calculate total pages
    total_hits = response.hits.total
    total_pages = ceil(float(total_hits) / page_size)
    print(f"Find total Pages: {total_pages}")

    # Return the results
    return response


if __name__ == '__main__':
    # Example usage
    from_date = date(2025, 1, 1)
    to_date = date(2025, 1, 31)
    page_request = {'page': 0, 'size': 10}
    group_name = 'group1_agrs2f5sa2'
    string_query = "productName:(*) AND stepUpdateStatus:('failed')" # test the query in Kibana before using it here
    results = find_query(string_query, page_request, from_date, to_date, group_name, index_name=index_name)
    for hit in results:
        print(hit)  # Do something with the hit
        print(hit.stepName)  # Do something with the hit
