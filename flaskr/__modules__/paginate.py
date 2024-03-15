def paginator(current_url, logs, request, PER_PAGE, url_for):
    """_summary_

    Args:
        current_url (_type_): _description_
        logs (_type_): _description_
        request (_type_): _description_
        PER_PAGE (_type_): _description_
        url_for (_type_): _description_

    Returns:
        _type_: _description_
    """    
    # get current page number, 1 is default
    page = int(request.args.get('page', 1))
    # total numbers of pages
    total_pages = len(logs) // PER_PAGE + (len(logs) % PER_PAGE > 0)
    if page > total_pages:
        page = 1
    # start and end index for current page
    start_index = (page - 1) * PER_PAGE
    end_index = start_index + PER_PAGE
    # get paginated colors
    paginated_log = logs[start_index:end_index]
    # generate pagination links
    prev_url = None
    next_url = None
    # start previous and next paginations
    if page > 1:
        prev_url = url_for(f'{current_url}', page=page - 1)
    if page < total_pages:
        next_url = url_for(f'{current_url}', page=page + 1)
    # start numbered pagination
    links = {}
    total_numbered_links = min(total_pages, 5)
    # generate links for all pages if total_pages <= 5
    if total_pages <= 5:
        for i in range(1, total_numbered_links + 1):
            link = url_for(f'{current_url}', page=i)
            print(link)
            links[f"{link}"] = i
    # generate links based on current page for total_pages > 5
    else:
        # first or second page: show first 5 pages
        if page <= 2:
            for i in range(1, total_numbered_links + 1):
                link = url_for(f'{current_url}', page=i)
                links[f"{link}"] = i 
        # middle pages: show 2 pages before and after current page
        elif 2 < page < total_pages - 1:
            start_page = page - 2
            end_page = page + 2
            for i in range(start_page, end_page + 1):
                link = url_for(f'{current_url}', page=i)
                links[link] = i
        # last two pages: show last 5 pages
        else:
            start_page = total_pages - 4
            for i in range(start_page, total_pages + 1):
                link = url_for(f'{current_url}', page=i)
                links[link] = i
        
    return paginated_log, page, prev_url, next_url, total_pages, links
    
    