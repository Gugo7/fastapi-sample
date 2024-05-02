from typing import List
from app import schemas
import pytest



# def test_get_all_posts(authorized_client, test_post):
#     res = authorized_client.get('/posts/')

#     def validate(post):
#         return schemas.PostOut(**post)
    
#     posts_map = map(validate, res.json())
#     posts_list = list(posts_map)

#     # assert posts_list[0].Post.id == test_post[0].id
#     # assert len(res.json()) == len(test_post)
#     assert res.status_code == 200


# def test_unauthorized_user_get_all_posts(client, test_post):
#     res = client.get('/posts/')
#     assert res.status_code == 401


# def test_unauthorized_user_get_post(client, test_post):
#     res = client.get(f'/posts/{test_post[0].id}')
#     assert res.status_code == 401


# def test_post_not_exist(authorized_client,test_post):
#     res = authorized_client.get('/posts/7987979879879')
#     assert res.status_code == 404


# def test_authorized_get_post(authorized_client, test_post):
#     res = authorized_client.get(f'/posts/{test_post[0].id}')
#     post = schemas.PostOut(**res.json())
#     assert post.Post.id == test_post[0].id
#     assert post.Post.title == test_post[0].title
#     assert post.Post.content == test_post[0].content


# @pytest.mark.parametrize('title, content, published',[
#     ('title one', 'test content 1', True),
#     ('title two', 'test content 2', False),
#     ('title three', 'test content 3', False),
#     ('title four', 'test content 4', True),])
# def test_create_post(authorized_client, test_user, test_post, title, content, published):
#     res = authorized_client.post('/posts/',
#                                  json={'title':title,
#                                        'content':content,
#                                        'published':published})
#     created_post = schemas.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.title == title
#     assert created_post.content == content
#     assert created_post.published == published
#     assert created_post.owner_id == test_user['id']


# def test_create_post_published_default(authorized_client, test_user, test_post):
#     res = authorized_client.post('/posts/',
#                                  json={'title':'title one', 'content':'some content'})
#     created_post = schemas.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.title == 'title one'
#     assert created_post.content == 'some content'
#     assert created_post.published == False
#     assert created_post.owner_id == test_user['id']


# def test_unauthorized_user_create_posts(client, test_user, test_post):
#     res = client.post('/posts/', json={'title':'title one', 'content':'some content'})
#     assert res.status_code == 401


# def test_unauthorized_user_delete_posts(client, test_user, test_post):
#     res = client.delete(f'/posts/{test_post[0].id}')
#     assert res.status_code == 401


# def test_user_delete_posts(authorized_client, test_user, test_post):
#     res = authorized_client.delete(f'/posts/{test_post[0].id}')
#     assert res.status_code == 204


# def test_non_exist_delete_posts(authorized_client, test_user, test_post):
#     res = authorized_client.delete('/posts/87989874916')
#     assert res.status_code == 404


# def test_delete_other_user_post(authorized_client, test_user, test_post):
#     res = authorized_client.delete(f'/posts/{test_post[3].id}')
#     assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_post):
    data = {
        'title':'updated title',
        'content':'updated content',
        'id':test_post[0].id
    }

    res = authorized_client.put(f'/posts/{test_post[0].id}', json=data)
    print(res.json())
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 202
    assert updated_post.title == data['title']
    assert updated_post.content == data ['content']
    

def test_update_post_non_exist(authorized_client, test_user, test_post):
    data = {
        'title':'updated title',
        'content':'updated content',
        'id':test_post[0].id
    }

    res = authorized_client.put(f'/posts/3213213132132', json=data)
    assert res.status_code == 404
