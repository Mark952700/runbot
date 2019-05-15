# -*- coding: utf-8 -*-


def migrate(cr, version):

    def ref(xmlid):
        cr.execute("SELECT res_id FROM ir_model_data WHERE module=%s AND name=%s", xmlid.split('.'))
        return cr.fetchone()

    # fill run_config_id Many2one  with the default config
    cr.execute('UPDATE runbot_build SET run_config_id = %s', ref('runbot.runbot_build_config_default'))
    cr.execute('ALTER TABLE runbot_build ALTER COLUMN run_config_id SET NOT NULL')
    cr.execute("UPDATE runbot_repo SET repo_run_config_id = %s", ref('runbot.runbot_build_config_default'))
    cr.execute("UPDATE runbot_branch SET branch_run_config_id = %s WHERE job_type = 'testing'", ref('runbot.runbot_build_config_default_no_run'))

    # set no_build on tmp branches
    cr.execute("UPDATE runbot_branch SET no_build = 't' WHERE job_type = 'none'")

    # set config to Default_no_ run when branch is testing
    cr.execute("UPDATE runbot_branch SET branch_run_config_id = %s WHERE job_type = 'testing'" % ref('runbot.runbot_build_config_default_no_run'))

    # set build_start/_end
    cr.execute("UPDATE runbot_build SET build_start = job_start")
    cr.execute("UPDATE runbot_build SET build_end = job_end")
