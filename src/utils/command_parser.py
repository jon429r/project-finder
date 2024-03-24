
def input_parser(user_input):

    parsed_input = user_input.split(' ')
    project_name, project_link, working_directory = None, None, None
    
    valid_args = ['-name', '-link', '-dir']

    
    for idx, input in enumerate(parsed_input):
        if input in valid_args:
            match = valid_args.index(input)
            if match == 0:
                project_name = input[idx+1]
            elif match == 1:
                project_link = input[idx+1]
            elif match == 2:
                working_directory = input[idx+1]
            else:
                return 400

    return project_name, project_link, working_directory
