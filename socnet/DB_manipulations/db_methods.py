import datetime

from socnet.DB_manipulations.db import Post, Reaction, User


class BaseRepository():
    __model__ = None

    def __init__(self, session):
        self.session = session

    def get(self, id):
        """
        Returns a content with a certain id
        """
        return self.query.get(id)

    def get_list(self):
        """
        Returns a list of all non-removed items
        """
        return self.query.filter_by(removed_at=None).all()

    def save(self, model):
        """
        Creates the context
        """
        self.session.add(model)
        self.session.commit()
        return model

    def delete(self, id):
        model = self.get(id)
        if not model:
            raise Exception('Model not found')
        self.session.query(self.__model__).filter_by(id=id).update(
            {'removed_at': datetime.datetime.now()},
        )
        self.session.commit()
        return model

    @property
    def query(self):
        """
        The decorator sets the query funciton as a class attribute. 
        The fuction returns it so I don't have to pass the __model__ 
        every time I need to query. 
        """
        return self.session.query(self.__model__)


class UserRepository(BaseRepository):
    __model__ = User


class PostRepository(BaseRepository):
    __model__ = Post

    def update_post(self, model):
        model_to_update = self.get(model.id)
        model_to_update.text = model.text

        self.session.commit()
        return model


class ReactionRepository(BaseRepository):
    __model__ = Reaction

    # def get_post_reactions(self, post_id):
    #     """Returns a list of specified post reactions"""
    #     return self.query.get(post_id)

    def get_post_reactions(self, postid):
        """
        Returns a list of all non-removed items
        """
        return self.query.filter_by(post_id=postid).all()

    def update_reaction(self, model):
        model_to_update = self.get(model.id)
        model_to_update.reaction = model.reaction

        self.session.commit()
        return model
