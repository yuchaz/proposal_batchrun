import lsst.sims.ocs.configuration.survey
assert type(config)==lsst.sims.ocs.configuration.survey.Survey, 'config is of type %s.%s instead of lsst.sims.ocs.configuration.survey.Survey' % (type(config).__module__, type(config).__name__)
config.duration=0.003
config.start_date='2022-10-01'
config.general_proposals=['WideFastDeep']
