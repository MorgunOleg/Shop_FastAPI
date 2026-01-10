from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel


async def update_product_rating(db: AsyncSession, product_id: int):
    """
    Считает средний рейтинг всех активных отзывов для товара по его ID.
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0

    # Обновляем поле rating у товара
    product = await db.get(ProductModel, product_id)
    if product:
        # Округляем до одного знака после запятой
        product.rating = float(round(avg_rating, 1))
