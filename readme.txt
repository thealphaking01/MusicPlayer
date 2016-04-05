The requirements to run the project are : Django 1.9, Python3 

So, this is a Music sharing Website, where users can register, login, and share music. They can also upvote/downvote various songs. 

I have used 3 models - a member, a song, and a vote ( represented here as M2SVote ). Members are users, song is for songs ( each song is , and a vote links the member and a song together ( which the member voted for).

Note that I did not separate upvotes and downvotes - assuming that a person wouldn't upvote as well as downvote a song. So, what I show is the score - the number of upvotes - downvotes. Thus all of this is handled by a single model - M2SVote.

I have also used AJAX to enable upvoting/downvoting a song :)

Also, please create a folder labelled as media in the main project directory.

Loved the project :)

Pardon the frontend - I am not that good at it. I could have used a template, but I am busy with my final year project work and hence couldn't do much. Apologies for the inconvenience :(
