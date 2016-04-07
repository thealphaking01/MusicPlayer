

Update: 1

The requirements to run the project are : Django 1.9, Python3 

So, this is a Music sharing Website, where users can register, login, and share music. They can also upvote/downvote various songs. 

I have used 3 models - a member, a song, and a vote ( represented here as M2SVote ). Members are users, song is for songs ( each song is , and a vote links the member and a song together ( which the member voted for).

Note that I did not separate upvotes and downvotes - assuming that a person wouldn't upvote as well as downvote a song. So, what I show is the score - the number of upvotes - downvotes. Thus all of this is handled by a single model - M2SVote.

I have also used AJAX to enable upvoting/downvoting a song :)

Also, please create a folder labelled as media in the main project directory.

Loved the project :)

Pardon the frontend - I am not that good at it. I could have used a template, but I am busy with my final year project work and hence couldn't do much. Apologies for the inconvenience :(

Update 2:

I was given new features to add - creating/editing/cloning/sharing/rating playlists.

I have assumed that a user can make multiple playlists - kind of the same way how any media player app allows us to make. Also, we can set whether we want the playlist to be public or private ( public means all other users can view it as well ). Private playlists can only be viewed by us.

I have also implemented the rating system - for the public playlists, members can provide a rating and the net rating of the playlist is shown. I have used AJAX to fetch the rating after updation, thus giving it a better UX ( similar to how I did with the voting for songs ).

I have also implemented the cloning functionality - a member can clone any particular ( but public ) playlist he likes into his own account, and the new playlist assumes a default private scope.Other checks, such as not allowing the person to clone the same playlist multiple times are also there ( a person can only clone the playlist again only if it has been changed ). A person cannot clone his/her own playlist.

Editing Playlists ( where we can add , remove songs, change its name and private/public property etc ) is also complete.
