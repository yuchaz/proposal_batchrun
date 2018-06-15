import lsst.sims.ocs.configuration.science.wide_fast_deep
assert type(config)==lsst.sims.ocs.configuration.science.wide_fast_deep.WideFastDeep, 'config is of type %s.%s instead of lsst.sims.ocs.configuration.science.wide_fast_deep.WideFastDeep' % (type(config).__module__, type(config).__name__)
config.sky_region.selections[0].minimum_limit=3
config.sky_region.selections[0].maximum_limit=-10
