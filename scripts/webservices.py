#!/usr/bin/python

import web
import itertools

import config.webapiconfig as config

import socorro.lib.ConfigurationManager as configurationManager
import socorro.lib.productVersionCache as pvc
import socorro.webapi.classPartial as cpart
import socorro.storage.crashstorage as cs
import socorro.database.database as db

import socorro.services.topCrashBySignatureTrends as tcbst
import socorro.services.signatureHistory as sighist
import socorro.services.aduByDay as adubd
#import socorro.services.aduByDayDetails as adudetails
import socorro.services.getCrash as getcr
import socorro.services.emailCampaign as emailcampaign
import socorro.services.emailCampaignCreate as emailcreate
import socorro.services.emailCampaigns as emaillist
import socorro.services.emailCampaignVolume as emailvolume
import socorro.services.emailSubscription as emailsub
import socorro.services.hello as hello
import socorro.services.status as status 

#-------------------------------------------------------------------------------
configurationContext = \
    configurationManager.newConfiguration(configurationModule=config,
                                          applicationName="Socorro Webapi 2.0")

#-------------------------------------------------------------------------------
import logging
import logging.handlers

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

syslog = logging.handlers.SysLogHandler(facility=configurationContext.syslogFacilityString)
syslog.setLevel(configurationContext.syslogErrorLoggingLevel)
syslogFormatter = logging.Formatter(configurationContext.syslogLineFormatString)
syslog.setFormatter(syslogFormatter)
logger.addHandler(syslog)

logger.info("current configuration:")
for value in str(configurationContext).split('\n'):
  logger.info('%s', value)

configurationContext.logger = logger
configurationContext.productVersionCache = pvc.ProductVersionCache(configurationContext)
configurationContext.databasePool = db.DatabaseConnectionPool(configurationContext,
                                                       logger=logger)
configurationContext.crashStoragePool = cs.CrashStoragePool(configurationContext)
configurationContext.counters = {}

#-------------------------------------------------------------------------------
web.webapi.internalerror = web.debugerror
web.config.debug = False

servicesList = (tcbst.TopCrashBySignatureTrends,
                sighist.SignatureHistory,
                adubd.AduByDay,
                adubd.AduByDay200912,
                #adudetails.AduByDayDetails,
                getcr.GetCrash,
                getcr.GetCrash201005,
                emailcampaign.EmailCampaign,
                emaillist.EmailCampaigns,
                emailcreate.EmailCampaignCreate,
                emailvolume.EmailCampaignVolume,
                emailsub.EmailSubscription,
                hello.Hello,
                status.Status,
               )
configurationContext.servicesList = servicesList
servicesUriTuples = ((x.uri,
                      cpart.classWithPartialInit(x, configurationContext))
                     for x in servicesList)
urls = tuple(itertools.chain(*servicesUriTuples))

logger.info(str(urls))

if configurationContext.modwsgiInstallation:
  logger.info('This is a mod_wsgi installation')
  application = web.application(urls, globals()).wsgifunc()
else:
  logger.info('This is stand alone installation without mod_wsgi')
  app = web.application(urls, globals())

if __name__ == "__main__":
  app.run()
