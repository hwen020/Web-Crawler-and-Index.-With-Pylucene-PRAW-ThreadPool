import os
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating the directory' + directory)
        os.makedirs(directory)

create_project_dir("RedditData")
create_project_dir("IndexFolder")