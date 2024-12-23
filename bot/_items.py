"""Specification of the work item passed to Robocorp Control Room."""

import pydantic
import datetime

import aconio.db as db
import aconio.dao as dao


class Item(pydantic.BaseModel):
    """A work item created by the Producer and processed by the Consumer."""

    client: dao.Client


def create_work_items_from_db(bmd_db: db.MSSQLConnection) -> list[Item]:
    """Create a work item for each client whose birthday is today."""

    rows = bmd_db.execute_query_from_file("queries/birthdays.sql")

    items = []
    for row in rows:
        if _dob_is_today(row):
            items.append(_create_item_from_row(bmd_db, row))

    return items


def _dob_is_today(row: dict) -> bool:
    """Check if the client's birthday is today."""
    today = datetime.date.today()
    return row["dob"].day == today.day and row["dob"].month == today.month


def _create_item_from_row(bmd_db: db.MSSQLConnection, row: dict) -> dao.Client:
    """Create a work item from a `queries/birthdays.sql` query row."""

    client_dao = dao.ClientDAO(conn=bmd_db)

    client = client_dao.with_ids(
        client_bmd_company_id=row["bmd_company_id"],
        client_bmd_id=row["bmd_id"],
    )

    client_dao.set_emails_to_display(client)

    client_dao.set_employees(
        client=client,
        bmd_frist_id=None,
        bmd_sachbearbeiter=dao.BMDSachbearbeiter.HAUPT,
        append_mode=dao.EmployeeSelectionMode.SB_ONLY,
    )

    return Item(client=client)
