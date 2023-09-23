import pytest
from sqlalchemy import func

from src.ips.models import FloatingIP, Instance


@pytest.mark.fixtures({"db": "db_with_instances_and_ips"})
def test_query(f):
    session = f.db

    RankedInstance = (
        # we can omit models in query statemement since output will be defined in .with_entities() statement
        session.query()

        # define WITH statement for our query
        .with_entities(
            # define outputs we want to get from our WITH statement: Instance model and role_rank column
            Instance,
            func.row_number().over(order_by=[Instance.role]).label('role_rank'),
        )

        # turn our query into a subquery
        .subquery()
    )

    RankedFloatingIP = (
        session.query()
        .with_entities(
            FloatingIP,
            func.row_number().over(order_by=[FloatingIP.role]).label('role_rank'),
        )
        .subquery()
    )

    query = (
        # define what we outputs we want to get from query result
        session.query(Instance, FloatingIP)

        # join our ranked tables to get correct mapping between ip and id according to roles
        .select_from(RankedFloatingIP)
        .join(RankedInstance, RankedInstance.role_rank == RankedFloatingIP.role_rank)

        # join our models to have them in query result
        .join(FloatingIP, FloatingIP.ip == RankedFloatingIP.c.ip)
        .join(Instance, Instance.id == RankedInstance.c.id)
    )

    result = query.all()


    print("\n")
    print(" instance id | instance role | floating_ip ip | floating_ip role ")
    print(" ----------- + ------------- + -------------- + ---------------- ")
    for row in result:
        print(
            f" {str(row[0].id).center(11)} |"
            f" {str(row[0].role).center(13)} |"
            f" {str(row[1].ip).center(14)} |"
            f" {str(row[1].role).center(16)} "
        )

    pass

    # cte_floating_ips = session.query(
    #     models.FloatingIP.id,
    #     func.row_number().over(order_by=[models.FloatingIP.instance_role, models.FloatingIP.ip_address]).label('rank_floatings')
    # ).filter(
    #     models.FloatingIP.datastore_id == datastore_id
    # ).cte('RankedFloatingIPs')

    # cte_instances = session.query(
    #     models.Instance.id,
    #     func.row_number().over(order_by=[models.Instance.role, models.Instance.id]).label('rank_instances')
    # ).filter(
    #     models.Instance.datastore_id == datastore_id
    # ).cte('RankedInstances')

    # # Build the final query to join the CTEs and retrieve both models.Instance and models.FloatingIP objects
    # query = (
    #     session.query(models.Instance, models.FloatingIP)
    #     .join(cte_instances, cte_instances.c.id == models.Instance.id)
    #     .join(cte_floating_ips, cte_floating_ips.c.id == models.FloatingIP.id)
    #     .filter(cte_instances.c.rank_instances == cte_floating_ips.c.rank_floatings)
    # )
