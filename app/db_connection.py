cursor = conn.cursor()

#Methods

@router.get('/')
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts


@router.get('/{id}')
async def get_post_by_id(id: str):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    return post


@router.post('/', status_code=status.HTTP_201_CREATED)
async def new_post(post: schemas.CreatePost):
    cursor.execute("INSERT INTO posts (title, author, content) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.author, post.content))
    post = cursor.fetchone()
    conn.commit()

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str):

    cursor.execute('DELETE FROM posts WHERE id = %s RETURNING *', (id))
    del_post = cursor.fetchone()
    conn.commit()

    if not del_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    
    return del_post


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: str, post: schemas.UpdatedPost):
    
    cursor.execute('UPDATE posts SET title = %s, author = %s, content = %s WHERE id = %s RETURNING *',
                   (post.title, post.author, post.content, id))
    update_post = cursor.fetchone()
    conn.commit()

    if not update_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    
    return update_post
