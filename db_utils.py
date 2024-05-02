import logging
from typing import Tuple, List, Union
from app import db
from app.models import Package, PostOffice, PackageTrackingHistory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ROUTE_DELIMITER = "->"


def persist_package(recipient_name: str, destination_address: str, destination_zip_code: str, package_type: str) -> \
        Tuple[Package, str]:
    """ Add new package to the database """
    err_msg = ""
    logger.debug("Persisting Package object")
    package = Package(
        recipient_name=recipient_name,
        destination_address=destination_address,
        destination_zip_code=destination_zip_code,
        package_type=package_type
    )
    db.session.add(package)

    try:
        db.session.commit()

        # Create tracking history for successful package creation
        db.session.add(PackageTrackingHistory(package_id=package.tracking_number))
        db.session.commit()

    except Exception as e:
        logger.error(f"Failed to persist package: {e}")
        err_msg = repr(e)
        package = None
        db.session.rollback()

    return package, err_msg


def persist_post_office(name: str, address: str, zip_code: str) -> Tuple[PostOffice, str]:
    """ Add new post office to the database """
    err_msg = ""
    logger.debug("Persisting PostOffice object")
    post_office = PostOffice(
        name=name,
        address=address,
        zip_code=zip_code
    )
    db.session.add(post_office)
    try:
        db.session.commit()

    except Exception as e:
        logger.error(f"Failed to persist post office: {e}")
        err_msg = repr(e)
        post_office = None
        db.session.rollback()

    return post_office, err_msg


def get_package(tracking_number: str) -> Package:
    """ Fetch package from the database by its tracking number (PK) """
    package = Package.query.get(tracking_number)
    return package


def get_packages() -> List[Package]:
    """ Fetch all packages from the database """
    packages = Package.query.all()
    return packages


def get_post_office(name) -> PostOffice:
    """ Fetch post office from the database """
    post_office = PostOffice.query.get(name)
    return post_office


def get_post_offices() -> List[PostOffice]:
    """ Fetch all post office objects from the database """
    post_offices = PostOffice.query.all()
    return post_offices


def package_reached_final_destination(package: Package, post_office: PostOffice) -> bool:
    """ Checks if the package was intended to reach this post office as a final route """
    return package.destination_zip_code == post_office.zip_code and package.destination_address == post_office.address


def get_or_create_package_tracking(package: Package) -> PackageTrackingHistory:
    """ Fetch from database package tracking history object, create one in case it does not exist already """
    package_tracking = PackageTrackingHistory.query.get(package.tracking_number)
    if package_tracking is None:
        logger.debug(f"Creating new PackageTrackingHistory object")
        package_tracking = PackageTrackingHistory(package=package)
        db.session.add(package_tracking)
        db.session.commit()

    return package_tracking


def adjust_tracking_route(package_tracking: PackageTrackingHistory, post_office: PostOffice) -> PackageTrackingHistory:
    """ Adjusting the current route of the package tracking """
    post_offices = package_tracking.route.split(ROUTE_DELIMITER)
    post_offices.append(post_office.name)
    package_tracking.route = ROUTE_DELIMITER.join(post_offices)
    return package_tracking


def record_package_in_post_office(package: Package, post_office: PostOffice) -> Union[str, None]:
    """ Record package arrival on a specific post office """
    package_tracking = get_or_create_package_tracking(package)

    for office_name in package_tracking.route.split(ROUTE_DELIMITER):
        if post_office.name == office_name:
            logger.debug("Office already exists on route (due to double submission)")
            return f"Package already submitted in given post office"

    if not package_tracking.route:
        logger.debug(f"No route found for package {package.tracking_number} (first office on route)")
        package_tracking.route = post_office.name
        db.session.add(package_tracking)

    else:
        logger.debug(f"Office {post_office.name} yet to exist on package route")
        package_tracking = adjust_tracking_route(package_tracking, post_office)
        db.session.add(package_tracking)

    if package_reached_final_destination(package, post_office):
        logger.debug(f"Package {package.tracking_number} has reached its final post office, marked as 'delivered'")
        package.delivered = True
        db.session.add(package)

    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Failed to record package in post office: {e}")
        db.session.rollback()
        return repr(e)


def get_package_tracking(package: Package) -> PackageTrackingHistory:
    """ Fetch package tracking history from the database """
    package_tracking = PackageTrackingHistory.query.get(package.tracking_number)
    return package_tracking
