import logging
from typing import List

from litestar import Controller, Request, delete, get, post, put
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Parameter
from LR.app.models.model import ProductCreate, ProductResponse, ProductUpdate
from LR.app.services.product_service import ProductService


class ProductController(Controller):
    path = "/products"
    signature_namespace = {
        "ProductService": ProductService,
        "ProductCreate": ProductCreate,
        "ProductResponse": ProductResponse,
    }

    @get("/{product_id:int}")
    async def get_product_by_id(
        self,
        product_service: ProductService,
        product_id: int = Parameter(gt=0),
    ) -> ProductResponse:
        """Получить продукт по ID"""
        product = await product_service.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f"Product with ID {product_id} not found")
        return ProductResponse.model_validate(product, from_attributes=True)

    @get()
    async def get_all_products(
        self,
        product_service: ProductService,
        count: int = 10,
        page: int = 1,
    ) -> List[ProductResponse]:
        """Получить все продукты"""
        try:
            products = await product_service.get_by_filter(count=count, page=page)
            return [
                ProductResponse.model_validate(product, from_attributes=True)
                for product in products
            ]
        except Exception as e:
            logging.exception("Error in get_all_products")
            raise HTTPException(status_code=500, detail=str(e)) from e

    @post()
    async def create_product(
        self, product_service: ProductService, request: Request
    ) -> ProductResponse:
        """Создать продукт"""
        data = await request.json()
        logging.info("Received product_data: %s", data)
        product_data = ProductCreate(**data)
        try:
            product = await product_service.create(product_data)
            logging.info("product.__dict__: %s", product.__dict__)
            return ProductResponse.model_validate(product, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            logging.exception("Unhandled error in create_product")
            raise HTTPException(
                status_code=500, detail=f"Error creating product: {str(e)}"
            ) from e

    @put("/{product_id:int}")
    async def update_product(
        self,
        product_service: ProductService,
        product_id: int,
        request: Request,
    ) -> ProductResponse:
        """Обновить продукт"""
        try:
            data = await request.json()
            logging.info("Received update data: %s", data)
            product_data = ProductUpdate(**data)
            product = await product_service.update(product_id, product_data)
            if not product:
                raise NotFoundException(
                    detail=f"Product with ID {product_id} not found"
                )
            return ProductResponse.model_validate(product, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error updating product: {str(e)}"
            ) from e

    @delete("/{product_id:int}")
    async def delete_product(
        self, product_service: ProductService, product_id: int
    ) -> None:
        """Удалить продукт"""
        return await product_service.delete(product_id)
