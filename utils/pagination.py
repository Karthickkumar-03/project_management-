from pydantic import BaseModel

class PaginationFilter(BaseModel):
    page: int = 1
    page_size: int = 10

class BaseRepository:
    def __init__(self, model):
        self.model = model

    async def get_with_filters(self, db, pagination: PaginationFilter):
        skip = (pagination.page - 1) * pagination.page_size
        limit = pagination.page_size
        query = db.query(self.model).offset(skip).limit(limit)
        total = await db.query(self.model).count()
        data = await query.all()
        return {
            "total": total,
            "page": pagination.page,
            "pageSize": pagination.page_size,
            "data": data
        }
