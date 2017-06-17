import re


def group_by(stream, field, success=None):
    '''
    Function counting rochet launches in months or years
    :param stream stream: file stream in reading mode
    :param string field: either "month" or "year"
    :param bool success: filters for succesful or not launches
    None doesn't filter
    :rtype: dict
    :return: dictionary of years or months as keys
    and number of launches as values
    '''
    # checking parameters
    if not hasattr(stream, 'readline'):
        print("First argument is not file stream")
        return
    if not (field == 'month' or field == 'year'):
        print("Second argument is not 'year' or 'month'")
        return
    if not (success is None or isinstance(success, bool)):
        print("Third argument is not bool or None")
        return
    headers = stream.readline()

    # looking for needed fields in header
    date = re.search(r"Launch Date \(UTC\)( )*", headers)
    if date:
        date_start = date.start()
        date_end = date.end()
    else:
        print("Couldn't find launch date in header")
        return
    suc = re.search(r"Suc", headers)
    if suc:
        succes_place = suc.start()
    else:
        print("Couldn't find success data in header")
        return

    # creating regex that can find required data
    if field == 'year':
        regex = re.compile(r"\d{4}")
    elif field == 'month':
        regex = re.compile(r"[A-Z][a-z]{2}")
    # getting read of the line with hashes
    stream.readline()

    result_dict = {}
    previous_found = None
    previous_success = None

    # searching for data and saving it in dict
    for line in stream.readlines():
        match = re.search(regex, line[date_start:date_end])
        if match:
            found = match.group()
        else:
            found = previous_found
        if len(line) > succes_place:
            if line[succes_place] == 'F':
                current_success = False
            elif line[succes_place] == 'S':
                current_success = True
        else:
            current_success = previous_success

        if success is None or success == current_success:
            if found in result_dict.keys():
                result_dict[found] += 1
            else:
                result_dict[found] = 1
        previous_found = found
        previous_success = current_success
    stream.close()
    return result_dict
