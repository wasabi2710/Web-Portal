def get_files(directory, search_term, os):
    """_summary_

    Args:
        directory (_type_): _description_
        search_term (_type_): _description_
        os (_type_): _description_

    Returns:
        _type_: _description_
    """    
    files = []
    for filename in os.listdir(directory):
        # append the searched term
        if search_term and search_term.lower() in filename.lower():
            files.append(filename)
        # else... append none searched term
        elif not search_term:
            files.append(filename)
    
    return files