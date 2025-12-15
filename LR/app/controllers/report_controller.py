from datetime import date
from typing import List

from litestar import Controller, get
from litestar.params import Parameter
from LR.orm.db import Report
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ReportController(Controller):
    path = "/report"

    @get("/")
    async def get_report(
        self,
        db_session: AsyncSession,
        report_date: date = Parameter(query="date", required=True),
    ) -> List[dict]:
        """Получить отчёт по заказам за указанную дату."""
        result = await db_session.execute(
            select(Report).where(Report.report_at == report_date)
        )
        reports = result.scalars().all()

        # Преобразуем ORM-объекты в JSON-совместимые словари
        return [
            {
                "id": r.id,
                "report_at": r.report_at.isoformat(),
                "order_id": r.order_id,
                "count_product": r.count_product,
            }
            for r in reports
        ]
