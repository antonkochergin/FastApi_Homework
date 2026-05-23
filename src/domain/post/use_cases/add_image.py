import os
import shutil
from uuid import uuid4

from fastapi import UploadFile

from core.exceptions.database_exceptions import NotFoundException
from core.exceptions.domain_exceptions import (
    NotEnoughRightsException,
    PostNotFoundException,
    UploadFileIsNotImageException,
)
from infrastructure.postgres.database import database
from infrastructure.postgres.repositories import PostRepository
from schemas.post import PostImageResponse
from schemas.user import UserResponse

ALLOWED_EXT = ["jpeg", "jpg", "png"]


class AddImageUseCase:
    def __init__(self):
        self._database = database
        self.image_folder = "../static/images"

        os.makedirs(self.image_folder, exist_ok=True)

    async def execute(
        self, post_id: int, image: UploadFile, current_user: UserResponse
    ) -> PostImageResponse:
        file_extension = image.filename.split(".")[-1].lower()
        if file_extension not in ALLOWED_EXT:
            raise UploadFileIsNotImageException()

        async with self._database.session() as session:
            repo = PostRepository(session)

            try:
                post = await repo.get(post_id)
            except NotFoundException:
                raise PostNotFoundException(id=post_id)

            if post.user_id != current_user.id:
                raise NotEnoughRightsException(username=current_user.username)

            image_name = f"post_{post_id}_{uuid4()}.{file_extension}"
            image_path = os.path.join(self.image_folder, image_name)

            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            post.image = image_name
            await session.commit()

            return PostImageResponse(image_path=image_name)
