# -*- coding: utf-8 -*-


def migrate(cr, version):
    # delete oldies
    old_models = tuple([
        'ir.qweb.widget', 'ir.qweb.widget.monetary', 'base.module.import',
        'res.currency.rate.type', 'website.converter.test.sub',
        'website.converter.test', 'runbot.config.settings',
        'report.abstract_report',  'base.action.rule.lead.test',
        'base.action.rule.line.test'
    ])
    cr.execute("DELETE FROM ir_model WHERE model IN %s", [old_models])

    # pre-create the log_list column
    cr.execute("ALTER TABLE runbot_build ADD COLUMN log_list character varying")
    cr.execute("UPDATE runbot_build SET log_list='base,all,run' WHERE job_type = 'all' or job_type is null")
    cr.execute("UPDATE runbot_build SET log_list='base,all' WHERE job_type = 'testing'")
    cr.execute("UPDATE runbot_build SET log_list='all,run' WHERE job_type = 'running'")

    # pre-create run_config_id column
    cr.execute('ALTER TABLE runbot_build ADD COLUMN run_config_id integer')

    # pre-fill global result column for old builds
    cr.execute("ALTER TABLE runbot_build ADD COLUMN global_result character varying")
    cr.execute("UPDATE runbot_build SET global_result=result")

    # pre-fill global state column for old builds
    cr.execute("ALTER TABLE runbot_build ADD COLUMN global_state character varying")
    cr.execute("UPDATE runbot_build SET global_state=state")

    # pre-fill nb_ fields to avoid a huge recompute
    cr.execute("ALTER TABLE runbot_build ADD COLUMN nb_pending INTEGER")
    cr.execute("ALTER TABLE runbot_build ADD COLUMN nb_testing INTEGER")
    cr.execute("ALTER TABLE runbot_build ADD COLUMN nb_running INTEGER")

    cr.execute("UPDATE runbot_build SET nb_pending=0")
    cr.execute("UPDATE runbot_build SET nb_testing=0")
    cr.execute("UPDATE runbot_build SET nb_running=0")
