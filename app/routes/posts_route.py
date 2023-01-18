from fastapi import APIRouter
from fastapi import Depends, HTTPException,  status
from ..depend.authdepen import get_current_user
from ..DB_manipulations.db_methods import PostRepository, ReactionRepository
from ..DB_manipulations.db_session import session_init
from ..DB_manipulations.db import User, Post, Reaction
from ..models import req_models


def build_post_repository(session=Depends(session_init)):
    return PostRepository(session)


def build_react_repository(session=Depends(session_init)):
    return ReactionRepository(session)


router = APIRouter(
    prefix='/posts',
    tags=['posts'],
    # dependencies=[Depends(get_current_user)]
)


@router.post('/')
async def create_post(
    post_to_create: req_models.text_post,
    repo: PostRepository = Depends(build_post_repository),
    current_user: User = Depends(get_current_user),
):
    """Creates a post"""

    post_to_add = Post()
    post_to_add.user_id = current_user.id
    post_to_add.text = post_to_create.text
    model = repo.save(post_to_add)
    return model


@router.get('/')
async def get_posts(
        repo: PostRepository = Depends(build_post_repository),
        rearepo: ReactionRepository = Depends(build_react_repository),
        current_user: User = Depends(get_current_user),
):
    """Returns  a list of PostObjects"""

    list_of_posts = []
    for post in repo.get_list():
        spec_post = {}
        spec_post['id'] = str(post.id)
        spec_post['created_at'] = str(post.created_at)
        # spec_post['updated_ad'] = str(post.updated_ad)
        spec_post['user_id'] = str(post.user_id)
        spec_post['text'] = str(post.text)
        spec_post['likes'] = 0
        spec_post['dlikes'] = 0

        for react in rearepo.get_list():
            if spec_post['id'] == str(react.post_id):
                if str(react.reaction) == 'like':
                    spec_post['likes'] = spec_post['likes'] + 1

                if str(react.reaction) == 'dlike':
                    spec_post['dlikes'] = spec_post['dlikes'] + 1

        list_of_posts.append(spec_post)

    return list_of_posts


@router.get('/{post_id}')
async def get_post(
    post_id,
    repo: PostRepository = Depends(build_post_repository),
    rearepo: ReactionRepository = Depends(build_react_repository),
    current_user: User = Depends(get_current_user),
):
    """Returns a dict of a specified post, with like and dis count"""
    spec_post = {}

    for post in repo.get_list():
        if str(post.id) == str(post_id):
            spec_post = {}
            spec_post['id'] = str(post.id)
            spec_post['created_at'] = str(post.created_at)
            # spec_post['updated_ad'] = str(post.updated_ad)
            spec_post['user_id'] = str(post.user_id)
            spec_post['text'] = str(post.text)
            spec_post['likes'] = 0
            spec_post['dlikes'] = 0

            for reaction in rearepo.get_list():

                if spec_post['id'] == str(reaction.post_id):
                    if str(reaction.reaction) == 'like':
                        spec_post['likes'] = spec_post['likes'] + 1

                    if str(reaction.reaction) == 'dlike':
                        spec_post['dlikes'] = spec_post['dlikes'] + 1

    return spec_post


@router.put('/{post_id}')
async def update_post(
    post_id,
    post_to_update: req_models.text_post,
    repo: PostRepository = Depends(build_post_repository),
    current_user: User = Depends(get_current_user),
):
    """Updates the context of post"""
    post_to_add = Post()
    post_to_add.id = post_id
    post_to_add.text = post_to_update.text
    model = repo.update_post(post_to_add)
    return model


@router.delete('/{post_id}')
async def delete_post(
    post_id,
    repo: PostRepository = Depends(build_post_repository),
    current_user: User = Depends(get_current_user),
):
    """Deletes a post with a specified id"""
    for post in repo.get_list():
        if str(post.id) == str(post_id):
            if str(post.user_id) == current_user.id:
                repo.delete(post_id)
                return {'message': 'Done'}

    return {'message': 'Not Found/You are not the Author'}


@router.post('/{post_id}/react')
async def add_reaction(
    post_id,
    passed_reaction: req_models.which_reaction,
    repo: PostRepository = Depends(build_post_repository),
    rearepo: ReactionRepository = Depends(build_react_repository),
    current_user: User = Depends(get_current_user),
):
    """Adds reaction to a post, currently supports only 'like' and 'dlike' """
    reaction_to_give = Reaction()

    if passed_reaction.reaction == 'like':
        reaction_to_give.reaction = 'like'
    elif passed_reaction.reaction == 'dlike':
        reaction_to_give.reaction = 'dlike'
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect reaction',
        )

    the_post = repo.get(post_id)
    if str(the_post.user_id) == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Cannot react your own posts',
        )

    posts = rearepo.get_post_reactions(post_id)

    post_to_update = None
    if posts:
        for post in posts:
            if str(post.user_id) == str(current_user.id):
                post_to_update = post
                post_to_update.reaction = passed_reaction.reaction
                rearepo.update_reaction(post_to_update)
                return {'message': 'Reaction Updated'}

    reaction_to_give.post_id = post_id
    reaction_to_give.reaction = passed_reaction.reaction
    reaction_to_give.user_id = current_user.id
    print(reaction_to_give.post_id)
    rearepo.save(reaction_to_give)
    return {'message': '2Done'}
