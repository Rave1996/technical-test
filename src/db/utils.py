from db.models.base import Base
from db.models.models import *  # noqa: F403
from db.session import engine

from db.models import CustomerORM, LoanORM
from sqlalchemy.orm import sessionmaker


def init_db():
    Base.metadata.create_all(engine)
    populate_db(engine)


def drop_db():
    Base.metadata.drop_all(engine)


def populate_db(conn):
    Session = sessionmaker(bind=conn)
    session = Session()

    if session.query(CustomerORM).count() == 0:
        ''''
            Customer records
        '''

        customers = [
            {'full_name': 'Juan Perez', 'email': 'juan@email.com', "status": True},
            {'full_name': 'Maria Rodriguez', 'email': 'maria@email.com', "status": True},
            {'full_name': 'Luis Martinez', 'email': 'luis@email.com', "status": True},
            {'full_name': 'Ana Garcia', 'email': 'ana@email.com', "status": True},
            {'full_name': 'Pedro Lopez', 'email': 'pedro@email.com', "status": True},
            {'full_name': 'Laura Sanchez', 'email': 'laura@email.com', "status": True},
            {'full_name': 'Carlos Gomez', 'email': 'carlos@email.com', "status": True},
            {'full_name': 'Sofia Diaz', 'email': 'sofia@email.com', "status": True},
            {'full_name': 'Daniel Martin', 'email': 'daniel@email.com', "status": True},
            {'full_name': 'Elena Fernandez', 'email': 'elena@email.com', "status": False},
        ]

        for customer in customers:
            new_customer = CustomerORM(full_name=customer['full_name'], email=customer['email'])
            session.add(new_customer)

        # Insert customers in DB
        session.commit()

        '''
            Loan records
        '''

        loans = [
            {"customer_id": 1, "amount": 2987, "status": False},
            {"customer_id": 1, "amount": 8683, "status": True},
            {"customer_id": 1, "amount": 4532, "status": True},
            {"customer_id": 2, "amount": 7543, "status": True},
            {"customer_id": 2, "amount": 1852, "status": False},
            {"customer_id": 2, "amount": 7543, "status": True},
            {"customer_id": 3, "amount": 6752, "status": True},
            {"customer_id": 3, "amount": 9125, "status": True},
            {"customer_id": 3, "amount": 5122, "status": False},
            {"customer_id": 4, "amount": 1321, "status": True},
            {"customer_id": 4, "amount": 6910, "status": True},
            {"customer_id": 4, "amount": 5679, "status": False},
            {"customer_id": 5, "amount": 8765, "status": True},
            {"customer_id": 5, "amount": 4875, "status": True},
            {"customer_id": 5, "amount": 8765, "status": True},
            {"customer_id": 6, "amount": 2435, "status": True},
            {"customer_id": 6, "amount": 3456, "status": False},
            {"customer_id": 6, "amount": 4298, "status": True},
            {"customer_id": 7, "amount": 5690, "status": True},
            {"customer_id": 7, "amount": 6342, "status": False},
            {"customer_id": 7, "amount": 3467, "status": True},
            {"customer_id": 8, "amount": 2783, "status": True},
            {"customer_id": 8, "amount": 7234, "status": True},
            {"customer_id": 8, "amount": 2764, "status": False},
            {"customer_id": 9, "amount": 7198, "status": True},
            {"customer_id": 9, "amount": 5971, "status": True},
            {"customer_id": 9, "amount": 1346, "status": True},
            {"customer_id": 10, "amount": 1233, "status": False},
            {"customer_id": 10, "amount": 8543, "status": False},
            {"customer_id": 10, "amount": 3744, "status": False},
        ]

        for loan in loans:
            new_loan = LoanORM(customer_id=loan['customer_id'], amount=loan['amount'], status=loan['status'])
            session.add(new_loan)

        # Insert loans linked to customers in DB
        session.commit()

    session.close()
