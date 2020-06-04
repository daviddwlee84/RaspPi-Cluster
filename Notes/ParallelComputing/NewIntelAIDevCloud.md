# Intel DevCloud oneAPI

> Registered in 2020/6/5, will be expired at 2020/10/3

## oneAPI

> Student can get a 90 days trial.
>
> * [Sign Up for Intel® DevCloud for oneAPI Projects | Intel® Software](https://intelsoftwaresites.secure.force.com/devcloud/oneapi)

* [Dashboard | Intel® DevCloud](https://devcloud.intel.com/oneapi/)
  1. Cononect: Use a Secure Shell (SSH) client terminal or a Jupyter* Notebook in your web browser to begin.
     * [Connection Options](https://devcloud.intel.com/oneapi/connect/)
  2. Get Started
     * [Try Your First Sample](https://devcloud.intel.com/oneapi/get-started/)
  3. Learn
     * [Browse Documentation](https://devcloud.intel.com/oneapi/learn/)
       * [Basic Shell Commands](https://devcloud.intel.com/oneapi/learn/shell-commands/)
       * [Basic VI Commands](https://devcloud.intel.com/oneapi/learn/vi-commands/)
       * [Queue Management and Job Submission](https://devcloud.intel.com/oneapi/learn/job-submission/)
       * [Advanced Queue Management](https://devcloud.intel.com/oneapi/learn/advanced-queue/)

## Queue Management

### qsub

```sh
echo "python <name>.py" | qsub -N <task_name> -d <log_dir> -l walltime 24:00:00
```

```sh
qsub job.sh
```

### qstat

```sh
qstat
```

```sh
qstat -f <job_num>
```

## Useful Command

```sh
qmgr -c "list queue batch"
```

---

```txt
###############################################################################
#
# Welcome to the Intel DevCloud for oneAPI Projects!
#
# 1) See https://devcloud.intel.com/oneapi/ for instructions and rules for
# the OneAPI Instance.
#
# 2) See https://github.com/intel/FPGA-Devcloud for instructions and rules for
# the FPGA Instance.
#
# Note: Your invitation email sent to you contains the authentication URL.
#
# If you have any questions regarding the cloud usage, post them at
# https://software.intel.com/en-us/forums/intel-devcloud
#
# Intel DevCloud Team
#
###############################################################################
#
# Note: Cryptocurrency mining on the Intel DevCloud is forbidden.
# Mining will lead to immediate termination of your account.
#
###############################################################################
```
