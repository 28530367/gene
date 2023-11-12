# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WtCrisprWago1FlagIpSrnaSeqBedgraph(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    init_pos = models.BigIntegerField(blank=True, null=True)
    end_pos = models.BigIntegerField(blank=True, null=True)
    evenly_rc = models.FloatField(blank=True, null=True)
    ref_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WT_CRISPR_WAGO_1_FLAG_IP_sRNA_seq_bedgraph'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Clashfilter(models.Model):
    clashread = models.TextField(db_column='CLASHRead', primary_key=True, blank=True)  # Field name made lowercase.
    readcount = models.IntegerField(blank=True, null=True)
    smallrnaname = models.TextField(db_column='SmallRNAName', blank=True, null=True)  # Field name made lowercase.
    regiononclashreadidentifiedassmallrna = models.TextField(db_column='RegiononCLASHReadidentifiedasSmallRNA', blank=True, null=True)  # Field name made lowercase.
    smallrnaregionfoundinclashread = models.TextField(db_column='SmallRNARegionFoundinCLASHRead', blank=True, null=True)  # Field name made lowercase.
    targetrnaname = models.TextField(db_column='TargetRNAName', blank=True, null=True)  # Field name made lowercase.
    regiononclashreadidentifiedastargetrna = models.TextField(db_column='RegiononCLASHReadidentifiedasTargetRNA', blank=True, null=True)  # Field name made lowercase.
    targetrnaregionfoundinclashread = models.TextField(db_column='TargetRNARegionFoundinCLASHRead', blank=True, null=True)  # Field name made lowercase.
    rnaupmaxregulatorsequence = models.TextField(db_column='RNAupMaxRegulatorsequence', blank=True, null=True)  # Field name made lowercase.
    rnaupmaxtargetsequence = models.TextField(db_column='RNAupMaxTargetsequence', blank=True, null=True)  # Field name made lowercase.
    rnaupmaxbindingsite = models.TextField(db_column='RNAupMaxbindingsite', blank=True, null=True)  # Field name made lowercase.
    rnaupmaxscore = models.FloatField(db_column='RNAupMaxscore', blank=True, null=True)  # Field name made lowercase.
    rnaupregulatorsequence = models.TextField(db_column='RNAupRegulatorsequence', blank=True, null=True)  # Field name made lowercase.
    rnauptargetsequence = models.TextField(db_column='RNAupTargetsequence', blank=True, null=True)  # Field name made lowercase.
    rnaupbindingsite = models.TextField(db_column='RNAupbindingsite', blank=True, null=True)  # Field name made lowercase.
    rnaupscore = models.FloatField(db_column='RNAupscore', blank=True, null=True)  # Field name made lowercase.
    mirandaenergy = models.FloatField(db_column='Mirandaenergy', blank=True, null=True)  # Field name made lowercase.
    mirandascore = models.FloatField(db_column='Mirandascore', blank=True, null=True)  # Field name made lowercase.
    mirandabindingsite = models.TextField(db_column='Mirandabindingsite', blank=True, null=True)  # Field name made lowercase.
    mirandatargetsequence = models.TextField(db_column='MirandaTargetsequence', blank=True, null=True)  # Field name made lowercase.
    mirandaregulatorsequence = models.TextField(db_column='MirandaRegulatorsequence', blank=True, null=True)  # Field name made lowercase.
    mirandamaxenergy = models.FloatField(db_column='MirandaMaxenergy', blank=True, null=True)  # Field name made lowercase.
    mirandamaxscore = models.FloatField(db_column='MirandaMaxscore', blank=True, null=True)  # Field name made lowercase.
    mirandamaxbindingsite = models.TextField(db_column='MirandaMaxbindingsite', blank=True, null=True)  # Field name made lowercase.
    mirandamaxtargetsequence = models.TextField(db_column='MirandaMaxTargetsequence', blank=True, null=True)  # Field name made lowercase.
    mirandamaxregulatorsequence = models.TextField(db_column='MirandaMaxRegulatorsequence', blank=True, null=True)  # Field name made lowercase.
    d = models.TextField(db_column='D', blank=True, null=True)  # Field name made lowercase.
    m = models.TextField(db_column='M', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clashfilter'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GeneCodingTranscript(models.Model):
    wormbase_id = models.TextField(blank=True, null=True)
    gene_name = models.TextField(blank=True, null=True)
    coding_transcript = models.TextField(blank=True, null=True)
    transcript_id = models.TextField(primary_key=True, blank=True)

    class Meta:
        managed = False
        db_table = 'gene_coding_transcript'


class Geneid(models.Model):
    wormbase_id = models.TextField(primary_key=True, blank=True)
    gene_sequqnce_name = models.TextField(blank=True, null=True)
    gene_name = models.TextField(blank=True, null=True)
    other_name = models.TextField(blank=True, null=True)
    transcript_id = models.TextField(blank=True, null=True)
    numbers = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geneid'


class WtclashHybFinalWeb(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    clash_read = models.TextField(db_column='CLASH Read', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    region_on_clash_read_identified_as_regulator_rna = models.TextField(db_column='Region on CLASH Read identified as Regulator RNA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    region_on_clash_read_identified_as_target_rna = models.TextField(db_column='Region on CLASH Read identified as Target RNA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    read_count = models.TextField(db_column='Read Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    regulator_rna_name = models.TextField(db_column='Regulator RNA Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    regulator_rna_sequence = models.TextField(db_column='Regulator RNA Sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    regulator_rna_region_found_in_clash_read = models.TextField(db_column='Regulator RNA Region Found in CLASH Read', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    target_rna_name = models.TextField(db_column='Target RNA Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    target_rna_region_found_in_clash_read = models.TextField(db_column='Target RNA Region Found in CLASH Read', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_min_ex_binding_site = models.TextField(db_column='pirscan min_ex binding site', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pirscan_min_ex_target_sequence = models.TextField(db_column='pirscan min_ex Target sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_min_ex_score = models.TextField(db_column='pirscan min_ex score', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pirscan_max_ex_binding_site = models.TextField(db_column='pirscan max_ex binding site', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pirscan_max_ex_target_sequence = models.TextField(db_column='pirscan max_ex Target sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_max_ex_score = models.TextField(db_column='pirscan max_ex score', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rnaup_min_ex_regulator_rna_sequence = models.TextField(db_column='RNAup min_ex Regulator RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_target_rna_sequence = models.TextField(db_column='RNAup min_ex Target RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_binding_site = models.TextField(db_column='RNAup min_ex binding site', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_score = models.TextField(db_column='RNAup min_ex score', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_regulator_rna_sequence = models.TextField(db_column='RNAup max_ex Regulator RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_target_rna_sequence = models.TextField(db_column='RNAup max_ex Target RNA sequence', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_binding_site = models.TextField(db_column='RNAup max_ex binding site', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_score = models.TextField(db_column='RNAup max_ex score', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d = models.TextField(db_column='D', blank=True, null=True)  # Field name made lowercase.
    m = models.TextField(db_column='M', blank=True, null=True)  # Field name made lowercase.
    wt_wago_pirscan_min_ex25_22g = models.TextField(db_column='WT_WAGO_pirscan min_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wt_wago_pirscan_max_ex25_22g = models.TextField(db_column='WT_WAGO_pirscan max_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wt_wago_rnaup_min_ex25_22g = models.TextField(db_column='WT_WAGO_RNAup min_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wt_wago_rnaup_max_ex25_22g = models.TextField(db_column='WT_WAGO_RNAup max_ex25_22G', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mutation_count = models.BigIntegerField(blank=True, null=True)
    mutation_pos = models.TextField(blank=True, null=True)
    algorithm = models.TextField(blank=True, null=True)
    pirscan_min_ex_22g_pvalue_corrected = models.TextField(db_column='pirscan min_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pirscan_max_ex_22g_pvalue_corrected = models.TextField(db_column='pirscan max_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_min_ex_22g_pvalue_corrected = models.TextField(db_column='RNAup min_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rnaup_max_ex_22g_pvalue_corrected = models.TextField(db_column='RNAup max_ex 22G pvalue-corrected', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mutation_string = models.TextField(blank=True, null=True)
    prg1mut_wago1_22g_rnaup_min_ex25 = models.TextField(db_column='PRG1MUT_WAGO1_22G_RNAup min_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prg1mut_wago1_22g_pirscan_min_ex25 = models.TextField(db_column='PRG1MUT_WAGO1_22G_pirscan min_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prg1mut_wago1_22g_rnaup_max_ex25 = models.TextField(db_column='PRG1MUT_WAGO1_22G_RNAup max_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prg1mut_wago1_22g_pirscan_max_ex25 = models.TextField(db_column='PRG1MUT_WAGO1_22G_pirscan max_ex25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_rnaup_min_ex25_foldchange = models.TextField(db_column='WAGO1_22G_RNAup min_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_pirscan_max_ex25_foldchange = models.TextField(db_column='WAGO1_22G_pirscan max_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_rnaup_max_ex25_foldchange = models.TextField(db_column='WAGO1_22G_RNAup max_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wago1_22g_pirscan_min_ex25_foldchange = models.TextField(db_column='WAGO1_22G_pirscan min_ex25 foldchange', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'wtCLASH_hyb_final_web'
