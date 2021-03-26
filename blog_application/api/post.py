import datetime

from flask import abort
from flask_restful import Resource, fields, marshal_with

from ..models import db, User, Post, Tag
from .fields import HTMLField
from .parsers import post_get_parser
from .parsers import post_post_parser
from .parsers import post_put_parser
from .parsers import post_delete_parser


nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}


post_fields = {
    'author': fields.String(attribute=lambda x: x.user.username),
    'title': fields.String(),
    'text': HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_dt': fields.DateTime(dt_format='iso8601')
}


class PostApi(Resource):
    @marshal_with(post_fields)
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)

            return post
        else:
            args = post_get_parser.parse_args()
            page = args['page'] or 1
            posts = Post.query.order_by(
                Post.publish_dt.desc()
            ).paginate(page, 30).items

            return posts

    def post(self, post_id=None):
        if post_id:
            abort(405)
        else:
            args = post_post_parser.parse_args(strict=True)

        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)

        new_post = Post(args['title'])
        new_post.user = user
        new_post.publish_dt = datetime.datetime.now()
        new_post.text = args['text']

        if args['tags']:
            for item in args['tags']:
                tag = Tag.query.filter_by(title=item).first()
                if tag:
                    new_post.tags.append(tag)
                else:
                    new_tag = Tag(item)
                    new_post.tags.append(new_tag)

            db.session.add(new_post)
            db.session.commit()

        return new_post.id, 201

    def put(self, post_id=None):
        if not post_id:
            abort(401)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_put_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)
        if user != post.user:
            abort(403)

        if args['title']:
            post.title = args['title']
        if args['text']:
            post.text = args['text']
        if args['tags']:
            for item in args['tags']:
                tag = Tag.query.filter_by(title=item).first()
                if tag:
                    if tag not in post.tags:
                        post.tags.append(tag)
                else:
                    new_tag = Tag(item)
                    post.tags.append(new_tag)

        db.session.add(post)
        db.session.commit()
        return post.id, 201

    def delete(self, post_id=None):
        if not post_id:
            abort(400)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if user != post.user:
            abort(403)

        db.session.delete(post)
        db.session.commit()
        return '', 204
