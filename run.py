import logging
from cpdlog import import_ea_cpd_activities, create_db
from cpdlog import get_cpd_activities
from cpdlog import combine_report_data, build_report


if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level='INFO', format=LOG_FORMAT)

    db_url = 'sqlite:///data/cpdlog.db'
    create_db(db_url)
    import_ea_cpd_activities(db_url, 'data/record_20190507.xlsx')

    activities = get_cpd_activities(db_url)
    report_data = combine_report_data(activities)
    build_report(activities, report_data, "build/cpd_report.html")

    logging.info('Done!')
