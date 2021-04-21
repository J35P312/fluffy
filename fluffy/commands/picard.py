"""Commands to run picard tools"""


def get_collect_gc_bias_cmd(
    singularity: str, out_prefix: str, reference: str, javasettings: str, tmp_dir: str
) -> str:
    """Get a string with command for running picard GC bias"""
    picard_gc_cmd = (
        f"{singularity} picard CollectGcBiasMetrics I={out_prefix}.bam "
        f"O={out_prefix}.gc_bias_metrics.txt CHART={out_prefix}.gc_bias_metrics.pdf "
        f"S={out_prefix}.gc.summary.tab R={reference} VALIDATION_STRINGENCY=LENIENT {javasettings} TMP_DIR={tmp_dir}"
    )

    return picard_gc_cmd


def get_collect_insert_size_cmd(
    singularity: str, out_prefix: str, javasettings: str, tmp_dir: str
) -> str:
    """Get a string with command to run picard collect insert size metrics"""
    picard_insert_cmd = (
        f"{singularity} picard CollectInsertSizeMetrics I={out_prefix}.bam "
        f"O={out_prefix}.insert_size_metrics.txt H={out_prefix}.insert_size_histogram.pdf "
        f"VALIDATION_STRINGENCY=LENIENT M=0.5 {javasettings} TMP_DIR={tmp_dir}"
    )

    return picard_insert_cmd


def get_estimate_complexity_cmd(
    singularity: str, out_prefix: str, javasettings: str, tmp_dir: str
) -> str:
    """Get a string with command to estimate library complexity with picard tools"""
    picard_complexity_cmd = (
        f"{singularity} picard EstimateLibraryComplexity I={out_prefix}.bam "
        f"O={out_prefix}.complex_metrics.txt VALIDATION_STRINGENCY=LENIENT {javasettings} TMP_DIR={tmp_dir}"
    )

    return picard_complexity_cmd
